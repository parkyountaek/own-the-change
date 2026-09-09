# 작은 구조

## 결론

Own The Change는 서버 없이 저장소 안에서만 동작하는 학습 보조 도구다. 에이전트가 코드를 고친 뒤 사용자가 변경 이유와 위험을 자기 말로 설명할 기회를 만들고, 그 결과를 Markdown으로 남긴다.

## 구성

- `docs/protocol/understanding-protocol.md`: 모든 에이전트가 따라야 하는 유일한 공통 학습 규칙 정본이다.
- `skills/own-the-change/`: Claude Code, Codex, Cursor, Copilot 등에서 공유하는 단일 skill 연결층이다. 공통 규칙은 복사하지 않는다.
- `.claude-plugin/`, `commands/`, `hooks/`: Claude Code plugin manifest와 명시 command, 선택형 알림 hook이다.
- `.codex-plugin/`, `.agents/skills/`: Codex plugin metadata와 프로젝트 범위 skill 발견 경로다.
- `.cursor/skills/`: Cursor가 같은 공통 skill을 찾는 경로다.
- `adapters/`: 도구별 연결 방식을 설명하는 얇은 안내 파일이다.
- `adapters/generic/`: 다른 도구가 정본을 읽도록 하는 안내 파일이다.
- `templates/understanding-record.md`: 사람과 도구가 함께 쓰는 기록 양식이다.
- `scripts/validate_record.py`: 기록의 형식만 결정론적으로 검사한다. 이해도를 판단하지 않는다.
- `docs/ai-understanding/YYYY-MM-DD/`: 실제 작업의 로컬 기록 위치다.

## 데이터 흐름

1. 사용자는 작업 전 `Plan Check` 질문에 답하거나 건너뛴다.
2. 에이전트는 작업 후 실제 `git diff`와 실행한 테스트 결과만 사용해 `Change Debrief`를 쓴다.
3. 사용자는 위험도에 맞는 최대 3개 질문에 자기 말로 답한다.
4. 에이전트는 답변이 없으면 `not_confirmed`로 남긴다. 답변에 중요한 빈틈이 있으면 `needs_follow_up`로 남긴다.
5. 기록 검증기는 파일 형식만 확인한다. `confirmed` 판정은 사용자의 실제 답변과 근거를 사람이 검토한 결과여야 한다.

## 확장 경계

공통 규칙은 `docs/protocol/understanding-protocol.md` 한 곳에만 둔다. 어댑터는 그 파일을 가리키고 각 도구가 제공하는 호출 방식만 적는다. 새 에이전트는 `adapters/generic/AGENT-INSTRUCTIONS.md`를 출발점으로 같은 정본을 참조한다.

## 하지 않는 일

- 서버, 계정, 데이터베이스, 결제, 분석 대시보드
- API Key 요구나 원본 코드·환경 변수·비밀값·전체 터미널 로그 전송
- 코드 자동 수정, 자동 배포, 자동 병합, PR 승인
- 테스트 성공 또는 AI 자기평가로 이해 상태를 `confirmed`로 바꾸는 일
- 알림 발송. 첫 버전은 중요한 변경의 `follow_up_at`만 기록한다.
