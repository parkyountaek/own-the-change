# Claude Code 어댑터

Claude Code의 실제 진입점은 저장소 루트의 `.claude-plugin/`, `commands/`, `hooks/`, `skills/`다. 이 폴더는 Claude Code가 공통 프로토콜을 어떤 방식으로 연결하는지 설명하는 얇은 어댑터다.

- manifest: `../../.claude-plugin/plugin.json`
- 명시 command: `../../commands/own-*.md`
- 선택형 Stop hook: `../../hooks/hooks.json`
- 공통 skill: `../../skills/own-the-change/SKILL.md`
- 학습 규칙 정본: `../../docs/protocol/understanding-protocol.md`

공통 학습 규칙을 이 파일에 복사하지 않는다.
