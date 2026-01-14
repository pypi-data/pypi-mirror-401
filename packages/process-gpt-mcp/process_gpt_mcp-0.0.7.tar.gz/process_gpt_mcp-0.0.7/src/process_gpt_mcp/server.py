"""
Work Assistant MCP Server

프로세스 조회, 회사 정보 질의, 프로세스 실행을 위한 MCP 도구 모음.
Agent가 사용자 요청을 분석하고 필요한 도구를 선택해서 호출합니다. 

보안 모델:
- service_role_key를 사용하지 않음
- 사용자의 JWT를 그대로 사용하여 Supabase에 접근
- RLS 정책이 사용자의 tenant_id를 검증하여 데이터 접근 제어

사용자 요청 유형별 처리 흐름:
1. 프로세스 생성 요청 → generate_process 도구 호출 후 즉시 종료 (프론트엔드에서 실제 처리)
2. 프로세스 실행 요청 → get_process_list → get_process_detail → get_form_fields → execute_process
3. 질문/조회 요청 → get_process_list → get_instance_list → get_todolist 또는 get_organization
"""

import os
import json
import uuid
import logging
import httpx
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP

# 파일 로깅 설정 (즉시 flush)
log_file = os.path.join(os.path.dirname(__file__), 'mcp_debug.log')

# 핸들러에 즉시 flush 설정
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# Supabase 설정 (환경변수는 mcp_config.json의 env에서 전달됨)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
# 변경: service_role_key 대신 anon_key 사용 (RLS가 적용됨)
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# 기본 인증 정보 (환경변수에서 읽어옴 - mcp.json의 env에서 설정 가능)
# 환경변수에 설정되어 있으면 파라미터보다 우선 사용됨
ENV_USER_JWT = os.getenv("user_jwt", "")
ENV_TENANT_ID = os.getenv("tenant_id", "")
ENV_USER_EMAIL = os.getenv("user_email", "")  # 현재 사용자 이메일 (Cursor 등 외부 MCP 클라이언트용)


def get_effective_credentials(user_jwt: str, tenant_id: str) -> tuple:
    """환경변수 우선, 없으면 파라미터 사용"""
    effective_jwt = ENV_USER_JWT if ENV_USER_JWT else user_jwt
    effective_tenant = ENV_TENANT_ID if ENV_TENANT_ID else tenant_id
    return effective_jwt, effective_tenant

# 백엔드 API 설정 (프로세스 실행용)
# API_BASE_URL은 tenant_id를 기반으로 동적 생성: https://{tenant_id}.process-gpt.io
def get_api_base_url(tenant_id: str) -> str:
    """테넌트 ID를 기반으로 API Base URL을 동적으로 생성"""
    return f"https://{tenant_id}.process-gpt.io"

# FastMCP 서버 생성
mcp = FastMCP(
    "work-assistant",
    instructions=f"""업무 지원 도구 서버입니다.

[현재 사용자 정보]
- 환경변수에 설정된 사용자 이메일: {ENV_USER_EMAIL if ENV_USER_EMAIL else '(설정되지 않음)'}
- 프로세스 실행 시 사용자 정보가 필요하면 get_current_user를 먼저 호출하세요.

[프로세스 생성 vs 실행 구분 - 최우선 규칙]
★ 프로세스 "생성/만들기" 요청 판단 기준 (generate_process 호출):
  - "프로세스 생성해줘", "프로세스 만들어줘", "워크플로우 만들어줘"
  - "새로운 프로세스", "프로세스를 새로 만들고 싶어"
  - 명확하게 "생성", "만들기", "만들어" 키워드가 포함된 경우만!

★ 프로세스 "실행" 요청 판단 기준 (execute_process 호출):
  - "휴가 신청해줘", "출장 신청", "결재 요청"
  - "~~ 프로세스 실행해줘", "~~ 해줘" (기존 프로세스 사용)
  - 생성/만들기 키워드가 없는 일반 업무 요청

★ 헷갈리면 ask_user로 "새 프로세스를 만드시겠습니까, 아니면 기존 프로세스를 실행하시겠습니까?" 질문!

[관련 컨텍스트 활용]
"[관련 컨텍스트]" 섹션에 이전 조회 결과가 있으면 도구를 다시 호출하지 마세요.

[프로세스 실행 전 필수 검증 - 매우 중요]
execute_process 전 반드시 아래 순서로 확인:

1. ★ 담당자 배정 확인 (최우선, 실행 전 반드시 체크!) ★
   - get_process_detail 결과의 definition.roles 배열 확인
   - 각 role의 endpoint와 default 값 검사
   - endpoint가 ""(빈문자열)이고 default도 ""(빈문자열)인 role이 하나라도 있으면:
     → execute_process 호출 금지!
     → 사용자에게 안내 (프로세스 수정 링크 포함):
       "{{role.name}} 역할의 담당자가 배정되지 않았습니다.
        아래 링크에서 담당자를 배정한 후 다시 요청해주세요.
        👉 https://{{tenant_id}}.process-gpt.io/definitions/{{process_id}}?edit=true"
   - 예시: {{"name": "운영팀", "endpoint": "", "default": ""}} → 담당자 미배정!

2. 폼 필드 확인: 사용자가 제공하지 않은 필수 정보는 ask_user로 질문

[ask_user 규칙 - 매우 중요]
★ ask_user는 적극적으로 사용하세요! 남발해도 됩니다!
★ ask_user를 제외한 다른 도구들은 실제 결과를 생성하므로, 사용자 의도가 100% 명확할 때만 호출!
★ 조금이라도 모호하면 → 먼저 ask_user로 확인!

ask_user를 사용해야 하는 경우:
- 어떤 프로세스를 실행할지 불명확할 때
- 생성인지 실행인지 헷갈릴 때
- 폼에 입력할 값이 불분명할 때
- 날짜/시간/기간이 모호할 때
- 사용자 요청에 여러 해석이 가능할 때

두 번째 질문 시에는 "빈 값으로 진행할까요?" 옵션 제공.

[도구 흐름] - 관련 컨텍스트에 정보가 없을 때만 호출
- 프로세스 실행: get_current_user → get_process_list → get_process_detail(담당자 검증!) → get_form_fields → execute_process
- 프로세스 생성: generate_process (생성/만들기 명시된 경우만!)
- PDF to BPMN: [InputData]에 PDF 파일 정보가 있으면 create_pdf2bpmn_workitem 호출
- 결과 조회: get_instance_list → get_todolist
- 조직도: get_organization

[이미지 처리]
사용자가 이미지를 첨부하면 자동으로 분석되어 [이미지 분석 결과] 섹션에 포함됩니다.
분석 결과를 바탕으로 사용자 요청을 처리하세요 (프로세스 생성 등).

모든 도구는 user_jwt, tenant_id 생략 가능 (환경변수에서 자동 로드)."""
)


def get_supabase_headers(user_jwt: str) -> dict:
    """
    Supabase API 호출용 헤더 생성
    
    변경: service_role_key 대신 user_jwt 사용
    - apikey: anon_key (Supabase 프로젝트 식별용)
    - Authorization: user_jwt (사용자 인증, RLS 적용)
    """
    # 디버깅: user_jwt 전달 여부 및 내용 확인
    if user_jwt:
        logger.info(f"[RLS] user_jwt 전달됨: {user_jwt[:50]}... (길이: {len(user_jwt)})")
        # JWT 페이로드 디코딩 (디버깅용)
        try:
            import base64
            parts = user_jwt.split('.')
            if len(parts) >= 2:
                # 패딩 추가
                payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
                decoded = base64.urlsafe_b64decode(payload).decode('utf-8')
                logger.info(f"[RLS] JWT 페이로드: {decoded}")
        except Exception as e:
            logger.warning(f"[RLS] JWT 디코딩 실패: {e}")
    else:
        logger.warning("[RLS] ⚠️ user_jwt가 비어있음! RLS가 제대로 작동하지 않을 수 있습니다.")
    
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {user_jwt}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }


def generate_uuid() -> str:
    """UUID 생성"""
    return str(uuid.uuid4())


# =============================================================================
# 도구 0: 사용자에게 질문 (Human in the Loop)
# =============================================================================
@mcp.tool()
async def ask_user(
    question: str,
    context: Optional[str] = None,
    missing_fields: Optional[List[str]] = None,
    suggestions: Optional[List[str]] = None,
    allow_skip: bool = False
) -> str:
    """
    사용자에게 추가 정보를 요청합니다.
    
    호출 후 사용자 답변을 기다립니다. 답변 후 관련 컨텍스트의 정보를 활용하여 진행하세요.
    
    Args:
        question: 질문 내용
        context: 질문 맥락 (선택)
        missing_fields: 누락된 필드명 목록 (선택)
        suggestions: 제안 답변 목록 (선택)
        allow_skip: 건너뛰기 가능 여부 (기본: False)
    """
    response = {
        "user_request_type": "ask_user",
        "question": question,
        "waiting_for_user_input": True
    }
    
    if context:
        response["context"] = context
    if missing_fields:
        response["missing_fields"] = missing_fields
    if suggestions:
        response["suggestions"] = suggestions
    if allow_skip:
        response["allow_skip"] = allow_skip
        
    logger.info(f"[ask_user] 사용자에게 질문: {question}")
    if missing_fields:
        logger.info(f"[ask_user] 누락된 필드: {missing_fields}")
    
    return json.dumps(response, ensure_ascii=False)


# =============================================================================
# 도구 0.5: 현재 사용자 정보 조회
# =============================================================================
@mcp.tool()
async def get_current_user(user_jwt: str = "", tenant_id: str = "", email: str = "") -> str:
    """
    현재 사용자 정보를 조회합니다.
    
    환경변수에 user_email이 설정되어 있으면 해당 이메일로 사용자 정보를 조회합니다.
    Cursor 등 외부 MCP 클라이언트에서 로그인 없이 사용자를 특정할 때 유용합니다.
    
    호출 시점:
    - execute_process 등 사용자 정보(user_uid, user_email)가 필요한 도구 호출 전
    - 프로세스 실행 시 "누가 신청하는지" 알아야 할 때
    
    사용 예시:
    - "휴가 신청해줘" → get_current_user로 사용자 정보 확인 후 execute_process
    - "내 정보 알려줘" → get_current_user 호출
    
    Args:
        user_jwt: 사용자 JWT 토큰 (선택, 환경변수에서 자동 로드)
        tenant_id: 테넌트 ID (선택, 환경변수에서 자동 로드)
        email: 조회할 사용자 이메일 (선택, 환경변수 user_email에서 자동 로드)
    
    Returns:
        사용자 정보 JSON. user_uid, user_email, username, team_id, team_name, role 등 포함.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    # 이메일: 파라미터 > 환경변수
    target_email = email if email else ENV_USER_EMAIL
    
    if not target_email:
        return json.dumps({
            "error": "사용자 이메일이 필요합니다. 환경변수 user_email을 설정하거나 email 파라미터를 전달해주세요.",
            "hint": "mcp.json의 env에 user_email을 추가하세요."
        }, ensure_ascii=False)
    
    if not user_jwt or not tenant_id:
        return json.dumps({"error": "user_jwt와 tenant_id가 필요합니다."}, ensure_ascii=False)
    
    try:
        # users 테이블에서 이메일로 사용자 정보 조회
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=get_supabase_headers(user_jwt),
                params={
                    "tenant_id": f"eq.{tenant_id}",
                    "email": f"eq.{target_email}",
                    "select": "id,email,username,role,profile,is_admin,is_agent"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                user_data = data[0]
                user_info = {
                    "user_uid": user_data.get("id"),
                    "user_email": user_data.get("email"),
                    "username": user_data.get("username"),
                    "role": user_data.get("role", "user"),
                    "profile": user_data.get("profile"),
                    "is_admin": user_data.get("is_admin", False),
                    "is_agent": user_data.get("is_agent", False)
                }
                logger.info(f"[get_current_user] 사용자 정보 조회 성공: {target_email} -> {user_info.get('username')}")
                return json.dumps(user_info, ensure_ascii=False, indent=2)
            else:
                return json.dumps({
                    "error": f"이메일 '{target_email}'에 해당하는 사용자를 찾을 수 없습니다.",
                    "hint": "users 테이블에 해당 이메일의 사용자가 등록되어 있는지 확인하세요."
                }, ensure_ascii=False)
                
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[get_current_user] 오류: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 1: 프로세스 생성 (프론트엔드 위임)
# =============================================================================
@mcp.tool()
async def generate_process(user_message: str, image_analysis_result: str = "") -> str:
    """
    프로세스 생성 요청을 처리합니다.
    
    매우 중요 
    - 사용자가 프로세스 생성/만들기를 요청한 경우 이 도구만 호출하고 즉시 종료하세요.
    - 이 도구 호출 후 다른 도구를 호출하지 마세요!
    - 실제 프로세스 생성은 프론트엔드에서 처리됩니다.
    
    사용 예시 (이런 요청이 오면 이 도구를 호출):
    - "휴가신청 프로세스 만들어줘"
    - "새로운 업무 프로세스 생성해줘"
    - "출장신청 워크플로우 만들어줘"
    - "프로세스 하나 만들고 싶어"
    - "업무 자동화 프로세스 생성"
    - [이미지 첨부] "이대로 프로세스 만들어줘"
    
    동작 방식:
    1. 이 도구 호출 (사용자의 원본 메시지와 이미지 분석 결과를 파라미터로 전달)
    2. 고정된 JSON 응답 반환 (user_message에 이미지 분석 결과 포함)
    3. 에이전트 동작 종료 (추가 도구 호출 금지)
    4. 프론트엔드가 응답을 받아 프로세스 생성 UI로 전환
    
    Args:
        user_message: 사용자가 입력한 원본 메시지 (프론트엔드에서 프로세스 생성 시 활용)
        image_analysis_result: 이미지 분석 결과 (선택)
                               - 이미지에서 추출한 프로세스 단계, 역할, 조건 등
                               - 이 정보가 있으면 user_message에 합쳐서 전달됨
    
    Returns:
        항상 {"user_request_type": "generate_process", "user_message": "...", "image_analysis_result": "..."} 반환
        프론트엔드에서 두 필드를 합쳐서 사용
    """
    return json.dumps({
        "user_request_type": "generate_process",
        "user_message": user_message,
        "image_analysis_result": image_analysis_result or ""
    }, ensure_ascii=False)


# =============================================================================
# 도구 2: 프로세스 목록 조회
# =============================================================================
@mcp.tool()
async def get_process_list(user_jwt: str, tenant_id: str) -> str:
    """
    프로세스 정의 목록을 조회합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    - 사용자가 tenant_id를 변조해도 RLS가 차단합니다.
    
    호출 시점 (매우 중요):
    - 프로세스 관련 모든 요청의 첫 번째 단계
    - 사용자가 어떤 프로세스를 실행/조회하려는지 파악하기 위해 반드시 먼저 호출
    
    사용 예시:
    - "휴가신청 해줘" → 먼저 이 도구로 "휴가신청" 프로세스 ID 확인
    - "나라장터 검색 결과" → 먼저 이 도구로 "나라장터" 프로세스 ID 확인
    - "어떤 프로세스가 있어?" → 이 도구로 전체 목록 조회
    
    Args:
        user_jwt: 사용자 JWT 토큰 (Supabase Auth에서 발급받은 토큰)
        tenant_id: 테넌트 ID (서브도메인, 예: "uengine")
    
    Returns:
        프로세스 목록 JSON. 각 프로세스는 id, name을 포함합니다.
        예: [{"id": "vacation_request", "name": "휴가신청"}, ...]
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/proc_def",
                headers=get_supabase_headers(user_jwt),
                params={
                    "tenant_id": f"eq.{tenant_id}",
                    "select": "id,name"
                }
            )
            response.raise_for_status()
            data = response.json()
            return json.dumps(data, ensure_ascii=False, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 3: 프로세스 상세 조회
# =============================================================================
@mcp.tool()
async def get_process_detail(user_jwt: str, tenant_id: str, process_id: str) -> str:
    """
    특정 프로세스의 상세 정보를 조회합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - get_process_list 이후, 프로세스 실행 전 반드시 호출
    - 첫 번째 액티비티 ID와 폼 키(tool 필드)를 확인하기 위해 필수
    
    반환값에서 확인할 것:
    1. definition.sequences: source가 "start_event"인 시퀀스의 target이 첫 번째 액티비티 ID
    2. definition.activities: 첫 번째 액티비티의 tool 필드에서 "formHandler:" 뒤의 값이 폼 키
    3. definition.roles: 역할 목록 (프로세스 실행 시 role_mappings에 사용)
    
    ★ 담당자 배정 검증 (execute_process 전 필수) ★
    각 액티비티에는 role 속성이 있고, 해당 role이 definition.roles에 정의되어 있습니다.
    검증 방법:
    1. definition.activities에서 각 액티비티의 role 확인
    2. definition.roles에서 해당 role 찾기
    3. role의 endpoint 또는 default 값 확인
       - endpoint: 실제 담당자 ID 배열 (예: ["user-uuid-1", "user-uuid-2"])
       - default: 기본 담당자 ID 배열
    4. endpoint와 default가 모두 비어있으면([], "", null) 담당자 미배정!
    
    담당자 미배정 시 처리:
    - execute_process 호출하지 말 것!
    - 사용자에게 안내: "{{액티비티명}} 단계의 담당자가 배정되지 않았습니다. 
      프로세스 정의 화면에서 담당자를 배정한 후 다시 요청해주세요."
    
    사용 예시:
    - "휴가신청" 실행 시 → 이 도구로 첫 번째 액티비티와 폼 키 확인 + 담당자 검증
    - "이 프로세스 어떻게 진행돼?" → 이 도구로 단계별 흐름 확인
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
        process_id: 프로세스 정의 ID (get_process_list에서 얻은 id 값)
    
    Returns:
        프로세스 상세 정보 JSON. definition 필드에 activities(단계), roles(역할), 
        events(시작/종료 이벤트), sequences(흐름) 등이 포함됩니다.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/proc_def",
                headers=get_supabase_headers(user_jwt),
                params={
                    "tenant_id": f"eq.{tenant_id}",
                    "id": f"eq.{process_id}",
                    "select": "id,name,definition"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                return json.dumps(data[0], ensure_ascii=False, indent=2)
            else:
                return json.dumps({"error": "프로세스를 찾을 수 없습니다."}, ensure_ascii=False)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 4: 폼 필드 조회
# =============================================================================
@mcp.tool()
async def get_form_fields(user_jwt: str, tenant_id: str, form_key: str) -> str:
    """
    폼의 입력 필드 정보를 조회합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - get_process_detail 이후, execute_process 전에 호출
    - 프로세스 실행에 필요한 입력 필드 정보를 얻기 위해 필수
    
    form_key 찾는 방법:
    get_process_detail 결과에서:
    1. sequences에서 source가 "start_event"인 항목 찾기 → target이 첫 번째 액티비티 ID
    2. activities에서 해당 ID의 액티비티 찾기
    3. 해당 액티비티의 tool 필드에서 "formHandler:" 뒤의 값이 form_key
       예: tool이 "formHandler:vacation_request_activity_001_form"이면
           form_key는 "vacation_request_activity_001_form"
    
    반환값 활용:
    - fields_json: 각 필드의 이름, 타입, 필수 여부 등 확인
    - 사용자 메시지에서 이 필드들에 맞는 값을 추출하여 execute_process에 전달
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
        form_key: 폼 키 (예: "vacation_request_activity_001_form")
    
    Returns:
        폼 필드 정보 JSON. fields_json에 각 필드의 상세 정보가 포함됩니다.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/form_def",
                headers=get_supabase_headers(user_jwt),
                params={
                    "tenant_id": f"eq.{tenant_id}",
                    "id": f"eq.{form_key}"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                return json.dumps(data[0], ensure_ascii=False, indent=2)
            else:
                return json.dumps({"error": "폼을 찾을 수 없습니다."}, ensure_ascii=False)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 5: 프로세스 실행
# =============================================================================
@mcp.tool()
async def execute_process(
    user_jwt: str,
    tenant_id: str,
    user_uid: str,
    user_email: str,
    process_definition_id: str,
    activity_id: str,
    form_key: str,
    form_values: Dict[str, Any],
    username: Optional[str] = None
) -> str:
    """
    프로세스를 실행합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - 반드시 get_process_list → get_process_detail → get_form_fields 순서로 호출한 후 마지막에 호출
    - 이전 단계에서 얻은 정보로 파라미터를 채워서 호출
    
    파라미터 설정 방법:
    1. process_definition_id: get_process_list에서 얻은 프로세스 id
    2. activity_id: get_process_detail에서 찾은 첫 번째 액티비티 id
       - sequences에서 source가 "start_event"인 항목의 target 값
    3. form_key: get_process_detail에서 찾은 폼 키
       - 첫 번째 액티비티의 tool 필드에서 "formHandler:" 뒤의 값
    4. form_values: get_form_fields에서 얻은 필드 정보를 기반으로 사용자 요청에서 추출한 값
       - 예: {"start_date": "2024-12-26", "days": 1, "reason": "개인 사유"}
    
    역할 매핑 (role_mappings)은 서버에서 자동 생성되므로 전달하지 않아도 됩니다.
    
    사용 예시:
    사용자: "12월 26일 휴가 1일 신청"
    → form_values: {"start_date": "2024-12-26", "days": 1}
    
    사용자: "날씨 검색 - 서울"
    → form_values: {"location": "서울"}
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
        user_uid: 실행하는 사용자의 UID (UUID 형식, 예: "550e8400-e29b-41d4-a716-446655440000")
        user_email: 실행하는 사용자의 이메일 (예: "user@example.com")
        process_definition_id: 프로세스 정의 ID
        activity_id: 첫 번째 액티비티 ID
        form_key: 폼 키
        form_values: 폼에 입력할 값들 (dict)
        username: 사용자 이름 (선택, 미제공 시 user_email 사용)
    
    Returns:
        프로세스 실행 결과 JSON. 성공 시 process_instance_id 포함.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        # process_instance_id 생성
        process_instance_id = f"{process_definition_id}.{generate_uuid()}"
        
        # username 기본값 처리 (없으면 email 사용)
        effective_username = username if username else user_email
        
        # role_mappings 초기화 (항상 서버에서 자동 생성)
        role_mappings = None
        
        # role_mappings가 비어있으면 프로세스 정의에서 자동 생성
        if not role_mappings:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    # 프로세스 정의 조회 (user_jwt 사용)
                    response = await client.get(
                        f"{SUPABASE_URL}/rest/v1/proc_def",
                        headers=get_supabase_headers(user_jwt),
                        params={
                            "tenant_id": f"eq.{tenant_id}",
                            "id": f"eq.{process_definition_id}",
                            "select": "definition"
                        }
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    if data and len(data) > 0:
                        definition = data[0].get("definition", {})
                        roles = definition.get("roles", [])
                        activities = definition.get("activities", [])
                        logger.info(f"roles: {roles}")
                        logger.info(f"activities 개수: {len(activities)}")
                        
                        # 첫 번째 액티비티의 role 찾기
                        first_activity = None
                        for act in activities:
                            if act.get("id") == activity_id:
                                first_activity = act
                                break
                        
                        first_activity_role = first_activity.get("role") if first_activity else None
                        
                        # 역할 매핑 생성 (ProcessGPTExecute.vue 참고)
                        role_mappings = []
                        for role in roles:
                            role_name = role.get("name")
                            role_default = role.get("default", [])
                            role_endpoint = role.get("endpoint", [])
                            
                            # endpoint 값 결정
                            if role_name == first_activity_role:
                                # 첫 번째 액티비티의 role에 현재 사용자 매핑
                                endpoint_value = user_uid
                            elif role_default:
                                # default 값이 있으면 사용
                                endpoint_value = role_default if isinstance(role_default, list) else [role_default]
                            elif role_endpoint:
                                # endpoint 값이 있으면 사용
                                endpoint_value = role_endpoint if isinstance(role_endpoint, list) else [role_endpoint]
                            else:
                                endpoint_value = ""
                            
                            role_mapping = {
                                "name": role_name,
                                "endpoint": endpoint_value,
                                "resolutionRule": role.get("resolutionRule"),
                                "default": role_default if role_default else ""
                            }
                            role_mappings.append(role_mapping)                        
                    else:
                        logger.warning("프로세스 정의를 찾을 수 없음")
            except Exception as e:
                # 역할 매핑 조회 실패 시 빈 배열로 진행
                logger.error(f"역할 매핑 생성 오류: {e}")
                role_mappings = []
        
        logger.info(f"최종 role_mappings: {role_mappings}")
        
        # 입력 데이터 구성
        input_data = {
            "process_definition_id": process_definition_id.lower(),
            "process_instance_id": process_instance_id,
            "activity_id": activity_id,
            "form_values": {
                form_key: form_values
            },
            "role_mappings": role_mappings,
            "answer": "",
            "user_id": user_uid,
            "username": effective_username,
            "email": user_email,
            "tenant_id": tenant_id,
            "version_tag": "major",
            "version": None,
            "source_list": []
        }
        
        api_base_url = get_api_base_url(tenant_id)
        logger.info(f"API 호출 URL: {api_base_url}/completion/complete")
        logger.info(f"API 호출 input_data: {json.dumps(input_data, ensure_ascii=False, default=str)}")
        
        # API 호출 (백엔드 API는 별도 인증 사용)
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{api_base_url}/completion/complete",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {user_jwt}"  # 백엔드에도 JWT 전달
                },
                json={"input": input_data}
            )
            logger.info(f"API 응답 status_code: {response.status_code}")
            logger.info(f"API 응답 body: {response.text[:500] if response.text else 'empty'}")
            
            response.raise_for_status()
            result = response.json()
            
            # 성공 응답에 process_instance_id 추가
            if isinstance(result, dict):
                result["process_instance_id"] = process_instance_id
                result["message"] = f"프로세스 '{process_definition_id}'가 성공적으로 실행되었습니다."
            
            logger.info(f"========== execute_process 성공 ==========")
            return json.dumps(result, ensure_ascii=False, indent=2)
            
    except httpx.HTTPStatusError as e:
        logger.error(f"API 호출 실패: {e.response.status_code}")
        logger.error(f"API 에러 응답: {e.response.text}")
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({
            "error": f"API 호출 실패: {e.response.status_code}",
            "detail": e.response.text
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"execute_process 예외 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 6: 인스턴스 목록 조회
# =============================================================================
@mcp.tool()
async def get_instance_list(user_jwt: str, tenant_id: str, user_uid: str, process_id: Optional[str] = None) -> str:
    """
    진행 중인 프로세스 인스턴스(업무) 목록을 조회합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - 프로세스 실행 결과를 조회할 때 사용
    - get_process_list 이후에 호출하여 특정 프로세스의 인스턴스 확인
    
    사용 예시:
    - "내 진행 중인 업무" → process_id 없이 호출
    - "휴가신청 현황" → get_process_list로 휴가신청 ID 확인 후 process_id로 필터링
    - "나라장터 실행 결과" → get_process_list로 나라장터 ID 확인 후 process_id로 필터링
    
    다음 단계:
    - 이 도구로 얻은 proc_inst_id를 get_todolist에 전달하여 실행 결과 확인
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
        user_uid: 사용자 UID (참여자로 필터링)
        process_id: (선택) 특정 프로세스로 필터링할 경우 프로세스 ID
    
    Returns:
        인스턴스 목록 JSON. 각 인스턴스는 proc_inst_id, proc_def_id, status, 
        start_date, participants, current_activity_ids 등을 포함합니다.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        params = {
            "tenant_id": f"eq.{tenant_id}",
            "participants": f"cs.{{{user_uid}}}"  # contains user_uid
        }
        
        if process_id:
            params["proc_def_id"] = f"eq.{process_id}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/bpm_proc_inst",
                headers=get_supabase_headers(user_jwt),
                params=params
            )
            response.raise_for_status()
            data = response.json()
            return json.dumps(data, ensure_ascii=False, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 7: 할 일 목록 조회 (실행 결과 포함)
# =============================================================================
@mcp.tool()
async def get_todolist(user_jwt: str, tenant_id: str, instance_ids: List[str]) -> str:
    """
    특정 인스턴스들의 할 일(activity) 목록과 실행 결과를 조회합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - 프로세스 실행 결과를 확인할 때 마지막 단계로 호출
    - get_process_list → get_instance_list → get_todolist 순서로 호출
    
    중요: 실행 결과는 각 activity의 output 필드에 저장됩니다.
    - 에이전트가 실행한 작업의 결과물이 output에 포함
    - 예: 검색 결과, API 호출 결과 등
    
    사용 예시:
    - "나라장터 검색 결과 알려줘" → output 필드에서 검색 결과 확인
    - "휴가신청 진행 상황" → status와 output으로 진행 상황 확인
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
        instance_ids: 조회할 인스턴스 ID 목록 (get_instance_list에서 얻은 proc_inst_id 값들)
    
    Returns:
        할 일 목록 JSON. 프로세스별, 인스턴스별로 그룹화된 activity 정보.
        각 activity에는 activityId, activityName, status, output(실행 결과) 등이 포함됩니다.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        if not instance_ids:
            return json.dumps({"error": "instance_ids가 비어있습니다."}, ensure_ascii=False)
        
        # instance_ids를 쉼표로 구분된 문자열로 변환
        ids_filter = ",".join([f'"{id}"' for id in instance_ids])
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/todolist",
                headers=get_supabase_headers(user_jwt),
                params={
                    "tenant_id": f"eq.{tenant_id}",
                    "proc_inst_id": f"in.({ids_filter})",
                    "order": "start_date.asc"
                }
            )
            response.raise_for_status()
            todos = response.json()
            
            # 프로세스별, 인스턴스별로 그룹화
            result = {}
            for todo in todos:
                def_id = todo.get("proc_def_id", "unknown")
                inst_id = todo.get("proc_inst_id", "unknown")
                
                if def_id not in result:
                    result[def_id] = {"processDefinitionId": def_id, "instances": {}}
                
                if inst_id not in result[def_id]["instances"]:
                    result[def_id]["instances"][inst_id] = {"instanceId": inst_id, "activities": []}
                
                result[def_id]["instances"][inst_id]["activities"].append({
                    "activityId": todo.get("activity_id"),
                    "activityName": todo.get("activity_name"),
                    "status": todo.get("status"),
                    "startDate": todo.get("start_date"),
                    "endDate": todo.get("end_date"),
                    "userId": todo.get("user_id"),
                    "output": todo.get("output")  # 실행 결과
                })
            
            return json.dumps(result, ensure_ascii=False, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 8: PDF to BPMN 워크아이템 생성
# =============================================================================
@mcp.tool()
async def create_pdf2bpmn_workitem(
    user_jwt: str,
    tenant_id: str,
    user_uid: str,
    user_email: str,
    pdf_file_url: str,
    pdf_file_name: str,
    pdf_file_path: Optional[str] = None,
    pdf_file_id: Optional[str] = None,
    description: Optional[str] = None,
    username: Optional[str] = None
) -> str:
    """
    PDF 파일을 BPMN 프로세스로 변환하는 워크아이템을 생성합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - 사용자가 PDF 파일을 업로드하고 BPMN 프로세스 생성을 요청할 때
    - PDF 파일이 이미 Supabase Storage에 업로드되어 있어야 함
    
    사용 예시:
    - "이 PDF 문서를 분석해서 프로세스 만들어줘"
    - "PDF 파일로 BPMN 생성해줘"
    - "[InputData]가 포함된 메시지에서 PDF 파일 URL 확인 후 호출"
    
    동작 방식:
    1. todolist 테이블에 새 워크아이템 생성
    2. agent_orch를 'pdf2bpmn'으로 설정
    3. 에이전트가 해당 워크아이템을 처리하여 PDF 분석 및 BPMN 생성
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
        user_uid: 실행하는 사용자의 UID (UUID 형식)
        user_email: 실행하는 사용자의 이메일
        pdf_file_url: Supabase Storage에 업로드된 PDF 파일의 공개 URL (publicUrl)
        pdf_file_name: 원본 PDF 파일명 (originalFileName)
        pdf_file_path: (선택) Storage 내 파일 경로 (예: "uploads/1767848673372_content.pdf")
        pdf_file_id: (선택) 파일 고유 ID (UUID 형식)
        description: (선택) 추가 설명 또는 요청사항
        username: (선택) 사용자 이름 (미제공 시 user_email 사용)
    
    Returns:
        생성된 워크아이템 정보 JSON. 성공 시 workitem_id와 상태 포함.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        # 워크아이템 ID 생성
        workitem_id = generate_uuid()
        
        # username 기본값 처리
        effective_username = username if username else user_email
        
        # path 추출: pdf_file_path가 없으면 URL에서 추출 (예: /files/uploads/xxx.pdf -> uploads/xxx.pdf)
        effective_path = pdf_file_path
        if not effective_path and pdf_file_url:
            # URL에서 '/files/' 이후 부분을 path로 추출
            if '/files/' in pdf_file_url:
                effective_path = pdf_file_url.split('/files/')[-1]
            else:
                effective_path = pdf_file_url.split('/')[-1]  # 파일명만 추출
        
        # id 생성: pdf_file_id가 없으면 새로 생성
        effective_file_id = pdf_file_id if pdf_file_id else generate_uuid()
        
        # 쿼리 구성 (PDF 파일 정보 포함)
        query = f"""[Description]
PDF 파일을 분석하여 BPMN 프로세스를 생성합니다.

[Instruction]
1. 첨부된 PDF 파일을 분석하세요.
2. 문서 내용에서 업무 프로세스를 추출하세요.
3. BPMN 형식의 프로세스 정의를 생성하세요.

[InputData]
{{"path": "{effective_path}", "id": "{effective_file_id}", "fullPath": "{pdf_file_url}", "originalFileName": "{pdf_file_name}", "publicUrl": "{pdf_file_url}"}}"""

        if description:
            query = f"{query}\n\n[추가 요청사항]\n{description}"
        
        # 워크아이템 데이터 구성
        workitem_data = {
            "id": workitem_id,
            "user_id": user_uid,
            "username": effective_username,
            "tenant_id": tenant_id,
            "proc_inst_id": uuid.uuid4().hex,
            "root_proc_inst_id": None,
            "proc_def_id": None,
            "activity_id": None,
            "activity_name": None,
            "status": "IN_PROGRESS",
            "tool": "formHandler:defaultform",
            "description": query,
            "query": query,
            "duration": 0,
            "start_date": None,  # 서버에서 자동 설정
            "due_date": None,
            "agent_mode": "DRAFT",
            "agent_orch": "pdf2bpmn",
            "adhoc": False,
            "output": None,
        }
        
        logger.info(f"[create_pdf2bpmn_workitem] 워크아이템 생성 시작: {workitem_id}")
        logger.info(f"[create_pdf2bpmn_workitem] PDF 파일: {pdf_file_name} -> {pdf_file_url}")
        
        # Supabase에 워크아이템 저장
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/todolist",
                headers=get_supabase_headers(user_jwt),
                json=workitem_data
            )
            response.raise_for_status()
            
            logger.info(f"[create_pdf2bpmn_workitem] 워크아이템 생성 성공: {workitem_id}")
            
            return json.dumps({
                "success": True,
                "workitem_id": workitem_id,
                "message": f"PDF to BPMN 워크아이템이 생성되었습니다. 파일: {pdf_file_name}",
                "status": "IN_PROGRESS",
                "agent_orch": "pdf2bpmn",
                "pdf_file_url": pdf_file_url
            }, ensure_ascii=False, indent=2)
            
    except httpx.HTTPStatusError as e:
        logger.error(f"[create_pdf2bpmn_workitem] HTTP 오류: {e.response.status_code}")
        logger.error(f"[create_pdf2bpmn_workitem] 응답: {e.response.text}")
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({
            "error": f"워크아이템 생성 실패: {e.response.status_code}",
            "detail": e.response.text
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[create_pdf2bpmn_workitem] 예외 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 도구 9: 이미지 분석 (Vision API)
# =============================================================================


# =============================================================================
# 도구 10: 조직도 조회
# =============================================================================
@mcp.tool()
async def get_organization(user_jwt: str, tenant_id: str) -> str:
    """
    회사 조직도를 조회합니다.
    
    보안:
    - user_jwt로 인증하며, RLS가 해당 사용자의 테넌트 데이터만 반환합니다.
    
    호출 시점:
    - 조직도에 대한 질문에만 사용
    - 다른 도구 호출 없이 바로 사용 가능
    
    사용 예시:
    - "조직도 보여줘"
    - "우리 회사 구조가 어떻게 돼?"
    - "개발팀에 누가 있어?"
    - "팀원 누구야?"
    
    Args:
        user_jwt: 사용자 JWT 토큰
        tenant_id: 테넌트 ID (서브도메인)
    
    Returns:
        조직도 정보 JSON. 부서, 팀, 직원 계층 구조를 포함합니다.
    """
    # 환경변수 우선 사용
    user_jwt, tenant_id = get_effective_credentials(user_jwt, tenant_id)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/configuration",
                headers=get_supabase_headers(user_jwt),
                params={
                    "tenant_id": f"eq.{tenant_id}",
                    "key": "eq.organization"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                value = data[0].get("value", {})
                chart = value.get("chart", value) if isinstance(value, dict) else value
                return json.dumps(chart, ensure_ascii=False, indent=2)
            else:
                return json.dumps({"error": "조직도 정보를 찾을 수 없습니다."}, ensure_ascii=False)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "인증 실패: JWT가 유효하지 않거나 만료되었습니다."}, ensure_ascii=False)
        elif e.response.status_code == 403:
            return json.dumps({"error": "접근 거부: 해당 테넌트에 대한 권한이 없습니다."}, ensure_ascii=False)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# =============================================================================
# 메인 진입점
# =============================================================================
def main():
    """MCP 서버 실행"""
    mcp.run()


if __name__ == "__main__":
    main()
