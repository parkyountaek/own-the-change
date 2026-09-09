---
task_id: add-index-migration
date: 2026-09-09
understanding_status: confirmed
risk_level: high
follow_up_at: 2026-09-10, 2026-09-16 — database migration 되돌리기와 영향 다시 설명
execution_metadata:
  provider: unknown
  model: unknown
  turn: unknown
  token: unknown
  cost: unknown
---

# 이해 기록: add-index-migration

## 작업 목표
- 자주 찾는 주문 번호 조회를 빠르게 하기 위한 인덱스를 추가한다.

## 변경 파일
- `migrations/20260909_add_order_index.sql`
- `tests/test_migration.sql`

## 테스트 근거
- `./scripts/test-migration.sh`를 실행했고 종료 코드가 0이었다.

## 핵심 설명
- 주문 번호를 찾을 때 데이터베이스가 모든 줄을 훑지 않도록 찾아보기 목록인 인덱스를 추가했다. 대신 주문을 새로 쓰거나 바꿀 때 인덱스도 함께 갱신해야 한다.

## 사용자 답변
- “조회는 빨라질 수 있지만, 주문을 추가하거나 수정할 때는 인덱스 유지 비용이 생긴다. 문제가 나면 인덱스를 제거하는 이전 파일을 준비해야 한다”고 설명했다.

## 이해 상태
- `confirmed`: 사용자가 선택 이유, 쓰기 비용, 되돌리기 위험을 자기 말로 설명했고 변경 내용과 큰 모순이 없었다.

## 남은 위험
- 운영 데이터 크기에서 실제 성능이 좋아지는지는 아직 측정하지 않았다.

## 다음 확인 항목
- 다음 날과 일주일 뒤에 인덱스를 되돌려야 하는 상황과 배포 순서를 설명한다.
