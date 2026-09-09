# 설치 구조

## 바로 쓸 수 있는 범위

- Claude Code: 저장소 루트에서 `claude --plugin-dir .`
- Codex: 저장소 루트의 `.agents/skills/own-the-change`을 자동 발견
- Cursor: 저장소 루트의 `.cursor/skills/own-the-change`을 자동 발견
- GitHub Copilot 등 Agent Skills 호환 도구: `.agents/skills/own-the-change`을 사용

이 저장소는 `skills/own-the-change/` 하나를 공통 skill으로 유지하고, 각 도구의 발견 경로에는 심볼릭 링크만 둔다. 학습 규칙 자체는 `docs/protocol/understanding-protocol.md` 한 곳에만 있다.

## 아직 배포하지 않는 범위

`.claude-plugin/marketplace.json`과 `.codex-plugin/plugin.json`은 나중에 공개 marketplace 배포를 준비하는 metadata다. 이 저장소는 현재 외부 게시나 push를 하지 않으며, 개발 중에는 위의 로컬 경로를 사용한다.
