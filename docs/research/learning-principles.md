# 학습 원리와 적용 가설

## 읽는 방법

아래 연구는 주로 사람의 학습 과제를 다룬다. AI 코딩 환경의 제품 효과를 직접 보장하지 않는다. 각 `이 도구에서의 적용`은 Own The Change의 적용 가설이다.

## 1. 능동 회상

- 연구 근거: Roediger, H. L., & Karpicke, J. D. (2006). *Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*. Psychological Science, 17(3), 249–255. DOI: [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x). Karpicke, J. D., & Blunt, J. R. (2011). *Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping*. Science, 331(6018), 772–775. DOI: [10.1126/science.1199327](https://doi.org/10.1126/science.1199327).
- 이 도구에서의 적용: 설명을 읽는 것만으로 끝내지 않고 사용자가 변경 이유와 영향을 자기 말로 답한다.
- 한계: 짧은 답변이 장기 유지보수를 보장하지 않는다. 답변을 강요하지 않으며, 답변이 없으면 `not_confirmed`다.

## 2. 자기 설명

- 연구 근거: Chi, M. T. H., Bassok, M., Lewis, M. W., Reimann, P., & Glaser, R. (1989). *Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems*. Cognitive Science, 13(2), 145–182. DOI: [10.1207/s15516709cog1302_1](https://doi.org/10.1207/s15516709cog1302_1).
- 이 도구에서의 적용: “무엇”뿐 아니라 “왜 이 방식을 골랐는가”와 영향 범위를 묻는다.
- 한계: 연구 과제와 실제 저장소의 복잡도는 다르다. 자연스러운 설명이 항상 정확한 것은 아니다.

## 3. 완성 예제와 점진적 도움 축소

- 연구 근거: Sweller, J., & Cooper, G. A. (1985). *The Use of Worked Examples as a Substitute for Problem Solving in Learning Algebra*. Cognition and Instruction, 2(1), 59–89. DOI: [10.1207/s1532690xci0201_3](https://doi.org/10.1207/s1532690xci0201_3).
- 이 도구에서의 적용: 처음에는 쉬운 Change Debrief 예시를 보이고, 익숙해지면 힌트와 질문 위주로 줄인다.
- 한계: 개인별 숙련도를 자동으로 정확히 재지 않는다. 도움 축소는 사용자가 요청하거나 기록을 보고 조심스럽게 적용한다.

## 4. 인지 부담 관리

- 연구 근거: Sweller, J. (1988). *Cognitive Load During Problem Solving: Effects on Learning*. Cognitive Science, 12(2), 257–285. DOI: [10.1207/s15516709cog1202_4](https://doi.org/10.1207/s15516709cog1202_4).
- 이 도구에서의 적용: 전체 diff를 한꺼번에 설명하지 않고 핵심 동작, 테스트, 부수 변경으로 나눈다. 체크포인트 질문은 최대 3개다.
- 한계: 작은 diff도 어려울 수 있고 큰 diff도 단순할 수 있다. 위험도 분류는 보조 판단이다.

## 5. 간격 복습

- 연구 근거: Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). *Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis*. Psychological Bulletin, 132(3), 354–380. DOI: [10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354).
- 이 도구에서의 적용: 인증, 권한, 결제, 데이터베이스 이전, 동시성, 배포, 외부 연동처럼 중요한 변경에만 다음 날과 일주일 뒤 날짜를 기록한다.
- 한계: 첫 버전은 알림을 보내지 않으며, 날짜 기록만으로 복습이 실제로 일어난다는 뜻은 아니다.

## 6. 구체적 피드백

- 연구 근거: Hattie, J., & Timperley, H. (2007). *The Power of Feedback*. Review of Educational Research, 77(1), 81–112. DOI: [10.3102/003465430298487](https://doi.org/10.3102/003465430298487).
- 이 도구에서의 적용: “현재 이해한 것”, “빠진 것”, “다음 확인 행동”을 나눠 적고 점수나 막연한 칭찬을 피한다.
- 한계: 피드백의 질은 변경 근거와 질문 품질에 좌우된다. 자동 점수는 제공하지 않는다.

## 7. 이해 착각 방지

- 연구 근거: Rozenblit, L., & Keil, F. (2002). *The Misunderstood Limits of Folk Science: An Illusion of Explanatory Depth*. Cognitive Science, 26(5), 521–562. DOI: [10.1207/s15516709cog2605_1](https://doi.org/10.1207/s15516709cog2605_1).
- 이 도구에서의 적용: 자신감 질문과 별개로 “코드를 보지 않고 설명할 수 있는가”를 묻는다.
- 한계: 말로 설명하기 어려운 실무 능력도 있다. 답변은 평가 점수가 아니라 다음 학습 대화를 위한 근거다.
