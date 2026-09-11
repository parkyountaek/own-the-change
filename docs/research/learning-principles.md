# Learning principles and product hypotheses

## How to read this document

The studies below examine human learning tasks. They do not directly prove that an AI coding product improves learning. Each application is an Own The Change product hypothesis.

## 1. Retrieval practice

- Evidence: Roediger, H. L., & Karpicke, J. D. (2006). *Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*. Psychological Science, 17(3), 249-255. DOI: [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x). Karpicke, J. D., & Blunt, J. R. (2011). *Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping*. Science, 331(6018), 772-775. DOI: [10.1126/science.1199327](https://doi.org/10.1126/science.1199327).
- Application: offer independent explanation as an opt-in deeper check. The default multiple-choice interaction lowers the requested writing effort but is not treated as unaided recall.
- Limit: a short answer does not prove long-term maintainability. Do not require an answer; use `not_confirmed` when none is given.

## 2. Self-explanation

- Evidence: Chi, M. T. H., Bassok, M., Lewis, M. W., Reimann, P., & Glaser, R. (1989). *Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems*. Cognitive Science, 13(2), 145-182. DOI: [10.1207/s15516709cog1302_1](https://doi.org/10.1207/s15516709cog1302_1).
- Application: in requested free-text checks, ask not only what changed but why this approach was chosen and what it affects. A selected explanation supplied by the agent is not the user's self-explanation.
- Limit: classroom tasks and real repositories differ. A fluent explanation can still be wrong.

## 3. Worked examples and fading support

- Evidence: Sweller, J., & Cooper, G. A. (1985). *The Use of Worked Examples as a Substitute for Problem Solving in Learning Algebra*. Cognition and Instruction, 2(1), 59-89. DOI: [10.1207/s1532690xci0201_3](https://doi.org/10.1207/s1532690xci0201_3).
- Application: begin with a simple Change Debrief example, then rely more on prompts and questions as the user gains familiarity.
- Limit: the tool does not automatically measure skill. Reduce support only by user request or careful review of records.

## 4. Cognitive load

- Evidence: Sweller, J. (1988). *Cognitive Load During Problem Solving: Effects on Learning*. Cognitive Science, 12(2), 257-285. DOI: [10.1207/s15516709cog1202_4](https://doi.org/10.1207/s15516709cog1202_4).
- Application: split a debrief into core behavior, tests, and incidental changes. Present a short Understanding Check one multiple-choice question at a time, with visible progress and an early-stop option. The risk-based question budgets are a product choice, not a research-established optimum; their effect on participation and experienced burden has not been measured.
- Limit: a small diff can be difficult and a large diff can be simple. Risk level is only a guide.

## 5. Spaced practice

- Evidence: Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). *Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis*. Psychological Bulletin, 132(3), 354-380. DOI: [10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354).
- Application: record next-day and one-week dates only for important changes such as authentication, authorization, payments, migrations, concurrency, deployment, and external integrations.
- Limit: this version sends no reminder. Recording a date does not mean a review occurred.

## 6. Specific feedback

- Evidence: Hattie, J., & Timperley, H. (2007). *The Power of Feedback*. Review of Educational Research, 77(1), 81-112. DOI: [10.3102/003465430298487](https://doi.org/10.3102/003465430298487).
- Application: separate what is understood, what is missing, and the next check. Avoid scores and vague praise.
- Limit: feedback quality depends on the evidence and question quality. The tool provides no automatic score.

## 7. Avoiding the illusion of understanding

- Evidence: Rozenblit, L., & Keil, F. (2002). *The Misunderstood Limits of Folk Science: An Illusion of Explanatory Depth*. Cognitive Science, 26(5), 521-562. DOI: [10.1207/s15516709cog2605_1](https://doi.org/10.1207/s15516709cog2605_1).
- Application: distinguish recognizing an option from independently explaining the reason and impact. Offer unaided explanation only when requested; a confidence statement is not evidence of understanding.
- Limit: some practical skill is hard to explain verbally. An answer is evidence for the next learning conversation, not a grade.

## 8. Correcting distractors and applying ideas

- Evidence: Butler, A. C., & Roediger, H. L. (2008). *Feedback enhances the positive effects and reduces the negative effects of multiple-choice testing*. Memory & Cognition, 36(3), 604-616. [Study abstract](https://pubmed.ncbi.nlm.nih.gov/18491500/). Multiple-choice distractors can introduce false information; their experiments investigated corrective feedback, not just answer selection.
- Evidence: Butler, A. C., Black-Maier, A. C., Raley, N. D., & Marsh, E. J. (2017). *Retrieving and applying knowledge to different examples promotes transfer of learning*. Journal of Experimental Psychology: Applied, 23(4), 433-446. [Author's institutional study abstract](https://scholars.duke.edu/publication/1292911), DOI [10.1037/xap0000142](https://doi.org/10.1037/xap0000142). The experiments found benefits from varied application examples in a geology-learning setting.
- Application: correct the specific misconception selected, and include a concrete prediction or related-fix scenario within the existing question budget. Do not merely repeat an answer that was just explained.
- Limit: these studies do not validate AI-authored questions, this plugin, a four-content-choice optimum, its answer-position rule, or long-term coding ability.

## Implementation review: 0.3.0

This is a design review, not a measured learning result. Common behavior remains defined only in the [protocol](../protocol/understanding-protocol.md).

| Mechanism | Implemented support | Still unproven or limited |
| --- | --- | --- |
| A usable mental model | Actual diff/test evidence and a small before/after example when useful | Agent explanations can still be wrong or incomplete |
| Active thinking | Concrete behavior prediction or a related-fix scenario within the existing budget | A correct choice alone is recognition, not unaided understanding |
| Corrective feedback | Explain the selected misconception's boundary without forcing retries | Ordering tests cannot judge factual truth or ambiguity |
| Independent explanation | Optional keywords or free text, evaluated separately from selections | Not forced by risk level or a desire to get a better status |
| Transfer | Distinct inputs, exceptions, or related repairs grounded in the change | No real-user maintenance study has been completed |
| Delayed review | User-initiated review and suggested dates for important saved work | No reminders; a date is not evidence that review occurred |
| Manageable effort | One question at a time, brief natural wording, unsure/skip/stop, no-save choice | Four content choices can increase reading effort; monitor voluntary feedback |

The [two-task invitation](https://github.com/parkyountaek/own-the-change/blob/main/docs/launch/early-access.md) separates ease of use, perceived usefulness, actual reuse, and missing follow-up. Validate retention or transfer only through real voluntary participation; do not replace those observations with stars, synthetic replies, immediate correctness, or token savings.
