# Own The Change 작업 규칙

- 공통 학습 규칙은 `docs/protocol/understanding-protocol.md`만 정본으로 사용한다.
- 에이전트별 파일에는 공통 규칙을 복사하지 말고 정본 링크만 둔다.
- 실제 `git diff`와 실제 실행 결과가 없는 설명을 사실처럼 쓰지 않는다.
- 사용자 답변이 없으면 이해 상태는 `not_confirmed` 또는 `unknown`이다.
- 테스트 성공이나 AI 자기평가만으로 `confirmed`를 쓰지 않는다.
- 원본 코드, 비밀값, 환경 변수, 전체 터미널 로그를 외부로 전송하지 않는다.
- 자동 코드 수정, 배포, 병합, PR 승인은 이 프로젝트 범위가 아니다.
- 기록을 만들거나 바꾼 뒤 `python3 scripts/validate_record.py <record>`로 형식을 확인한다.
