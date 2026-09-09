# Own The Change

AI 코딩 에이전트가 만든 변경을 사용자가 나중에도 직접 설명하고 고칠 수 있게 돕는 로컬 우선 학습 플러그인입니다. Claude Code와 Codex를 둘 다 지원합니다.

이 프로젝트는 코드 자동 수정 도구, 코드 품질 점수 도구, PR 승인 자동화 도구, SaaS가 아닙니다.

## 하는 일

작업 전에는 `Plan Check`로 예상 파일·위험·테스트를 짧게 생각하게 합니다. 작업 후에는 실제 Git diff와 실제 테스트 결과를 바탕으로 `Change Debrief`를 만듭니다. 이어서 위험도별로 최대 3개 질문을 던져 사용자의 설명을 듣고, 결과를 저장소의 Markdown 기록으로 남깁니다.

공통 규칙의 정본은 [이해 프로토콜](docs/protocol/understanding-protocol.md) 한 곳입니다. 도구별 어댑터는 그 규칙을 참조만 합니다.

## 빠른 시작

```sh
cd /path/to/own-the-change
python3 -m unittest discover -s tests -v
python3 scripts/validate_record.py docs/ai-understanding/*/*.md
```

새 기록은 `templates/understanding-record.md`를 복사해 `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`에 저장한 뒤 검사합니다.

```sh
python3 scripts/validate_record.py docs/ai-understanding/2026-09-09/rename-label.md
```

## Claude Code 지원

이 저장소의 `adapters/claude-code/`는 공식 plugin 구조인 `.claude-plugin/plugin.json`, `commands/`, `skills/`, `hooks/`를 사용합니다.

프로젝트에서 임시로 불러오려면 저장소 루트에서 실행합니다.

```sh
claude --plugin-dir adapters/claude-code
```

그 뒤 다음 명령을 명시적으로 사용할 수 있습니다.

```text
/own-plan-check
/own-change-debrief
/own-understanding-check
```

`Stop` hook은 작업 후 점검을 **제안만** 합니다. 기록을 만들거나 이해 상태를 바꾸지 않습니다. 플러그인을 설치하지 않고 세션에서만 썼다면 세션 종료로 제거됩니다. 로컬 plugin 설치 방법은 Claude Code 버전에 따라 달라질 수 있으므로, 배포 설치 전에는 [공식 plugin 문서](https://code.claude.com/docs/en/plugins)를 확인하세요.

## Codex 지원

Codex는 저장소 또는 사용자 범위의 `.agents/skills/`에서 skill을 찾습니다. 이 프로젝트는 정본 skill을 `adapters/codex/.agents/skills/own-the-change/`에 두고 설치 스크립트가 심볼릭 링크를 만듭니다.

프로젝트 범위 설치는 이 저장소에서만 보입니다.

```sh
scripts/install-local.sh codex-project
```

사용자 범위 설치는 이 컴퓨터의 모든 저장소에서 보입니다.

```sh
scripts/install-local.sh codex-user
```

Codex에서 `$own-the-change`을 명시적으로 호출하거나 Plan Check, Change Debrief, Understanding Check를 요청하면 됩니다. Codex가 새 skill을 못 찾으면 다시 시작합니다. 제거는 아래처럼 합니다.

```sh
scripts/install-local.sh remove-codex-project
scripts/install-local.sh remove-codex-user
```

Codex skill 위치와 명시 호출 방식은 [공식 Codex Skills 문서](https://developers.openai.com/codex/skills/)를 따릅니다.

## 다른 에이전트 지원

`adapters/generic/AGENT-INSTRUCTIONS.md`를 다른 도구에 제공하세요. 이 파일은 공통 프로토콜을 복사하지 않고 정본 문서를 읽도록 안내합니다.

## 기록과 상태

기록 위치는 `docs/ai-understanding/YYYY-MM-DD/<task-id>.md`입니다. 지원 상태값은 `confirmed`, `needs_follow_up`, `not_confirmed`, `unknown`입니다.

- 사용자가 답하지 않았으면 `not_confirmed` 또는 `unknown`입니다.
- 테스트 통과나 AI 자기평가만으로 `confirmed`가 되지 않습니다.
- 실행 도구가 신뢰할 수 있는 값을 제공하지 않으면 `provider`, `model`, `turn`, `token`, `cost`는 `unknown`으로 남깁니다.
- 인증, 권한, 결제, 데이터베이스 이전, 동시성, 배포, 외부 연동처럼 중요한 변경은 `follow_up_at`에 다음 날과 일주일 뒤 복습 날짜를 적습니다. 이 버전은 알림을 보내지 않습니다.

예시는 [낮은 위험](docs/examples/low-risk-change.md), [권한](docs/examples/authentication-change.md), [데이터베이스](docs/examples/database-change.md)를 보세요.

## 개인정보 보호와 범위

서버, 계정, 데이터베이스, 결제, 외부 SaaS가 없습니다. 별도 API Key를 요구하지 않습니다. 사용자가 이미 로그인한 Claude Code 또는 Codex 환경을 그대로 사용합니다. 이 프로젝트는 원본 코드, 환경 변수, 비밀값, 전체 터미널 로그를 외부로 보내는 기능을 포함하지 않습니다.

자동 배포, 자동 병합, 자동 코드 수정, PR 승인, 이해도 점수는 지원하지 않습니다.

## 출력 형태 참고

긴 변경 설명을 실제 행동으로 이어지게 하려고 [i-have-adhd](https://github.com/ayghri/i-have-adhd)의 행동 우선, 작은 단계, 가시적 진행 원칙을 참고했습니다. Own The Change는 ADHD 진단이나 치료 기능이 아니며, 그 프로젝트의 코드를 복사하지 않습니다. 적용한 제품 규칙은 [공통 이해 프로토콜](docs/protocol/understanding-protocol.md)의 `읽기 쉬운 출력 형태`에만 둡니다.

## 연구 근거

학습 설계와 논문 정보, 그리고 연구 사실과 제품 적용 가설의 구분은 [학습 원리](docs/research/learning-principles.md)에 있습니다. 논문은 AI 코딩 환경에서의 효과를 보장하지 않습니다.

## 라이선스

[MIT](LICENSE)
