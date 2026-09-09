---
task_id: authorization-guard
date: 2026-09-09
understanding_status: needs_follow_up
risk_level: high
follow_up_at: 2026-09-10, 2026-09-16 — authorization 경계를 다시 설명
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# 이해 기록: authorization-guard

## 작업 목표
- 관리자만 설정을 바꿀 수 있게 한다.

## 변경 파일
- `src/authz.py`
- `tests/test_authz.py`

## 테스트 근거
- `python3 -m unittest tests/test_authz.py -v`를 실행했고 통과했다.

## 핵심 설명
- 설정 변경 전에 사용자의 역할을 확인하는 보호 코드를 추가했다. 관리자가 아니면 변경 요청을 거절한다.

## 사용자 답변
- “관리자가 아닌 사용자가 설정을 바꾸지 못하게 막는다”고 설명했다.

## 이해 상태
- `needs_follow_up`: 왜 화면 버튼을 숨기는 것만으로 충분하지 않은지, 서버 쪽 확인이 필요한 이유는 설명하지 못했다.

## 남은 위험
- 실제 로그인 토큰이 잘못된 역할 정보를 담는 경우는 이 단위 테스트가 확인하지 못한다.

## 다음 확인 항목
- 다음 날과 일주일 뒤에 화면 보호와 서버 보호의 차이를 코드 없이 설명한다.
