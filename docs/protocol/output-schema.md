# 기록 형식

기록 파일은 `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`에 둔다. 날짜는 실제 작업 날짜를 `YYYY-MM-DD`로 쓴다.

맨 앞 YAML에는 아래 키가 모두 있어야 한다.

```yaml
task_id: short-kebab-case-id
date: YYYY-MM-DD
understanding_status: not_confirmed
risk_level: low
follow_up_at: none
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
```

실행 도구가 신뢰할 수 있는 값을 직접 제공한 경우에만 `provider`, `model`, `turn`, `token`, `cost`를 바꾼다. 하나라도 알 수 없으면 그 항목은 `unknown`으로 남긴다. 현재 설정값이나 계정 전체 사용량으로 과거 실행 값을 추정하지 않는다.

본문에는 다음 제목이 모두 있어야 한다.

- `## 작업 목표`
- `## 변경 파일`
- `## 테스트 근거`
- `## 핵심 설명`
- `## 사용자 답변`
- `## 이해 상태`
- `## 남은 위험`
- `## 다음 확인 항목`

`follow_up_at`은 중요한 작업에서만 사람이 읽을 수 있는 날짜와 이유를 쓴다. 예: `2026-09-10, 2026-09-16 — authorization 경계 다시 설명`. 중요하지 않으면 `none`이다.
