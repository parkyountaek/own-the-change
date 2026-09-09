# 범용 에이전트 안내

이 파일은 다른 에이전트를 위한 얇은 연결층이다. 공통 규칙을 여기에서 복사하거나 바꾸지 않는다.

1. 먼저 저장소 루트의 `docs/protocol/understanding-protocol.md`를 읽는다.
2. 사용자가 요청한 경우에만 Plan Check, Change Debrief, Understanding Check를 진행한다.
3. Change Debrief에는 현재 저장소의 실제 `git diff`와 실제 테스트 결과만 쓴다.
4. 기록은 `templates/understanding-record.md`를 바탕으로 `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`에 쓴다.
5. `python3 scripts/validate_record.py <record>`를 실행해 형식을 검사한다.
6. 사용자의 답변이 없으면 `confirmed`를 절대 쓰지 않는다. 실행 메타데이터가 없으면 `unknown`을 유지한다.

이 도구는 코드 수정, 코드 품질 점수, PR 승인, 외부 전송 도구가 아니다.
