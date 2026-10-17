---
title: "포맷은 100% 맞추는데 결과는 매번 다르다…LLM의 '틀 문제'는 2024년 문법 제약으로 닫혔고, 남은 것은 온도 0에서도 1,000번 중 80가지가 나오는 재현성"
slug: 2026-10-17-llm-format-solved-reproducibility-unsolved
topic: ai-data-engineering
published_at: 2026-10-17T13:21:00+09:00
tags:
  - LLM
  - 구조화출력
  - 비결정성
  - 에이전트
  - OpenAI
  - Anthropic
  - 벤치마크
summary: "'확률 모델이라 정보시스템이 요구하는 정규 포맷을 못 지킨다'는 통념은 두 문제를 섞고 있다. JSON 스키마 준수는 2024년 8월 OpenAI, 2025년 11월 Anthropic이 디코더 단계에서 문법으로 묶어 100%를 보장하는 영역이 됐고, 운영 중인 에이전트의 80%는 정해진 워크플로 안에서 도구 호출로 돈다. 반면 같은 입력에 같은 결과가 나오는 재현성은 미해결이다. Thinking Machines는 온도 0에서도 1,000번 요청에 80가지 답이 나오는 원인이 서버 부하에 따른 배치 크기 변화임을 밝혔고, τ-bench는 한 번 성공률 60% 안팎의 에이전트가 8번 연속 성공은 25% 미만임을 보였다. 틀은 보장되고 값은 흔들리는 상태에서 현장은 자율성을 줄이고 사람 검토를 늘리는 쪽으로 움직이고 있다."
generated_by: claude
model: claude-fable-5-1
---

# 포맷은 100% 맞추는데 결과는 매번 다르다…LLM의 '틀 문제'는 2024년 문법 제약으로 닫혔고, 남은 것은 온도 0에서도 1,000번 중 80가지가 나오는 재현성

## 한눈에 보기

- "확률 모델이라 매번 같은 포맷에 같은 결과를 못 낸다"는 말은 서로 다른 두 문제를 하나로 묶은 것이다. 포맷은 해결됐고, 결과의 동일성은 해결되지 않았다.
- OpenAI는 2024년 8월 구조화 출력(Structured Outputs)을 내며 JSON 스키마를 문법으로 변환해 유효하지 않은 토큰을 아예 뽑지 못하게 했고 자체 평가에서 스키마 일치 100%를 보고했다. Anthropic도 같은 방식을 2025년 11월 베타로 내고 지금은 정식 제공한다. 보장되는 것은 구조와 타입이며, 잘리거나 거부된 응답과 값의 정확성은 보장 밖이다.
- "채팅식으로만 말한다"는 2026년 운영 현장과 맞지 않는다. ICML 2026에 실린 운영 에이전트 조사에서 20개 사례 중 80%가 정해진 워크플로 안에서 돌고 68%는 10단계 안에 사람이 개입한다. 에이전트를 못 만드는 것이 아니라, 못 믿어서 짧게 끊는 것이다.
- 재현성은 모델이 아니라 추론 인프라의 문제다. Thinking Machines는 2025년 9월 온도 0으로 1,000번 요청해 80가지 다른 답을 얻었고, 원인이 흔히 말하는 부동소수점 오차가 아니라 서버 부하에 따라 달라지는 배치 크기라고 밝혔다. 배치 불변 커널로 고치면 1,000번이 모두 같아지지만 속도가 떨어지고, 상용 API는 이를 보장하지 않는다.
- 스키마가 맞아도 값은 흔들린다. τ-bench에서 GPT-4o는 소매 과제 한 번 성공률 60% 안팎이 8번 연속 성공률 25% 미만으로 떨어졌고, 형식을 강하게 묶을수록 추론 정확도가 떨어진다는 연구도 있다. 기업 조사에서는 사전 평가를 통과한 에이전트가 고객 대면 장애를 낸 경험이 61%, 자동 검사만으로 배포를 허용하는 비율은 한 달 사이 75%에서 56%로 줄었다.

## 2024년 8월에 닫힌 문제: 틀

언어 모델이 JSON을 깨뜨리거나 필드를 빠뜨리는 문제는 오랫동안 "확률 모델의 한계"로 설명됐다. OpenAI가 2024년 8월 6일 구조화 출력을 발표하면서 이 설명은 효력을 잃었다. 스키마를 문법으로 바꾸고 디코딩 단계에서 문법에 맞는 토큰만 고르게 하는 제약 디코딩(constrained decoding)을 적용해, 자체 평가에서 gpt-4o-2024-08-06이 복잡한 스키마를 100% 맞췄다고 밝혔다. 같은 평가에서 이전 모델 gpt-4-0613은 40%에 못 미쳤다([OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/)). 모델이 더 똑똑해져서가 아니라, 틀을 벗어나는 선택지를 샘플링 전에 지워 버리는 방식이다.

Anthropic도 같은 방식을 택했다. 2025년 11월 베타로 시작한 구조화 출력은 현재 Claude API에서 정식 기능이며, 응답 본문을 스키마에 묶는 JSON 출력(`output_config.format`)과 도구 호출 인자를 스키마에 묶는 엄격 도구 사용(`strict: true`) 두 가지로 제공된다. 공식 문서는 응답이 "컴파일된 문법으로 제약"되므로 파싱 오류나 스키마 위반 재시도가 사라진다고 적고, 동시에 보장되지 않는 경우를 명시한다. 안전 거부가 발생하면 거부가 스키마보다 우선하고, `max_tokens`에 잘리면 불완전한 출력이 나오며, enum 값의 대소문자가 바뀔 수 있다. 지원하는 스키마도 JSON Schema 전체가 아니라 부분집합이어서 재귀 구조, 숫자 범위, 문자열 길이 제약은 쓸 수 없고, 첫 사용 시 문법 컴파일 지연이 있으며 스키마를 바꾸면 프롬프트 캐시가 무효화된다([Anthropic](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)).

정리하면 "항상 같은 틀에 맞춰 답한다"는 요구는 2026년 기준으로 모델의 성격이 아니라 API 옵션의 문제다. 보장되는 것은 구조와 타입이고, 그 안에 들어가는 값이 맞는지는 다른 문제다. 문서가 값의 정확성을 보장한다고 쓰지 않는 이유가 여기에 있다.

## 채팅만 한다는 오해: 도구 호출과 운영 에이전트

"채팅식으로만 말하고 정보시스템이 요구하는 정규적인 결과를 못 만든다"는 인식도 현장과 어긋난다. 2026년의 에이전트는 자연어로 답하는 대신 스키마가 정해진 도구 호출(tool use)을 내보내고, 호출 결과를 받아 다음 호출을 결정하는 구조로 돈다. 코드 편집, 명령 실행, 데이터베이스 조회, 풀 리퀘스트 생성은 모두 이름과 인자 타입이 고정된 함수 호출이며, 엄격 도구 사용을 켜면 이 인자도 문법으로 묶인다. 사람이 읽는 채팅은 그 사이를 잇는 설명일 뿐이다.

운영 현장의 실태는 2025년 12월 공개되고 ICML 2026에 실린 "Measuring Agents in Production"이 보여 준다. UC 버클리 등 25명의 저자가 26개 도메인의 운영 시스템 20개를 심층 인터뷰하고 86개 배치 시스템 실무자를 조사했다. 20개 사례 중 16개(80%)가 미리 정의된 구조화 워크플로 안에서 돌고, 68%는 사람이 개입하기 전까지 10단계 이하만 실행한다. 70%는 가중치를 손대지 않고 기성 모델을 프롬프트로 쓰고, 74%는 평가를 주로 사람에게 맡기며, 75%는 공식 벤치마크 없이 A/B 테스트와 전문가 피드백으로 검증한다. 저자들은 이 설계를 "자율성을 통제 가능성과 맞바꿔 신뢰성을 얻는 것"으로 요약했다([arXiv](https://arxiv.org/abs/2512.04123), [Paper Notes](https://en.papernotes.org/ICML2026/llm_agent/measuring_agents_in_production/)).

이 숫자는 에이전트가 정규적인 결과를 못 만든다는 뜻이 아니다. 만들 수 있지만, 한 번 맞는 것과 매번 맞는 것이 다르다는 것을 현장이 알고 있어서 짧게 끊고 사람을 붙인다는 뜻이다. 문제의 핵심은 포맷이 아니라 다음 절의 재현성이다.

## 온도 0에도 1,000번 중 80가지: 재현성

같은 입력에 같은 출력이 나오지 않는 것은 확률 샘플링 때문이라는 설명이 오래 통용됐고, 그래서 온도(temperature)를 0으로 두면 결정적이 된다고 믿어졌다. Thinking Machines Lab이 2025년 9월 10일 공개한 "Defeating Nondeterminism in LLM Inference"는 이 믿음이 틀렸음을 실험으로 보였다. Qwen3-235B 모델에 "리처드 파인만에 대해 말해 달라"는 같은 프롬프트를 온도 0으로 1,000번 보내 1,000토큰씩 받았더니 80가지 서로 다른 답이 나왔고, 가장 흔한 답도 78번뿐이었다. 1,000개 답은 102번째 토큰까지 같다가 103번째에서 갈렸다. "파인만은 1918년 5월 11일"까지 쓴 뒤 992개는 "뉴욕 퀸스에서", 8개는 "뉴욕시에서"로 이어졌다([Thinking Machines Lab](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)).

원인도 통념과 달랐다. 흔히 부동소수점 덧셈의 비결합성과 GPU 스레드의 실행 순서를 지목하지만, 글은 언어 모델의 순전파에는 원자적 덧셈이 거의 없어 같은 데이터에 같은 연산을 하면 비트 단위로 같은 결과가 나온다고 설명한다. 진짜 원인은 배치 불변성의 부재다. 서버는 여러 사용자의 요청을 묶어 처리하는데, 묶인 요청 수에 따라 행렬곱·정규화·어텐션 커널이 덧셈 순서를 달리 잡는다. 사용자 한 명의 입장에서 다른 사용자가 몇 명인지는 알 수 없으므로, "부하가, 따라서 배치 크기가 비결정적으로 변한다"([Simon Willison](https://simonwillison.net/2025/Sep/11/defeating-nondeterminism/)). 같은 질문을 혼잡한 시간과 한가한 시간에 보내면 다른 답이 나올 수 있다는 뜻이다.

고칠 수는 있다. 저자들이 배치 크기와 무관하게 같은 순서로 계산하는 커널을 만들어 끼우자 1,000번의 답이 모두 같아졌다. 비용은 속도다. Qwen3-8B로 1,000개 문장을 생성하는 데 기본 vLLM이 26초, 결정적 버전이 55초, 어텐션 커널을 손본 뒤에도 42초였다. 상용 API가 이런 커널을 기본으로 켜 둔다는 공개 자료는 없고, 여러 사용자의 요청을 묶어 처리량을 올리는 구조 자체가 수익 모델이다. 결국 "같은 입력에 같은 결과"는 모델이 확률적이어서가 아니라, 추론 서비스가 그것을 팔지 않기 때문에 안 나온다.

## 스키마는 맞는데 값이 다르다

재현성 문제는 틀을 맞춘 뒤에도 남는다. Sierra 연구진이 2024년 6월 낸 τ-bench는 항공권 변경, 소매 반품 같은 과제에서 에이전트가 사용자와 대화하며 도구를 호출해 데이터베이스를 올바른 최종 상태로 만드는지 평가한다. 함께 제안한 pass^k는 같은 과제를 k번 독립 시도해 모두 성공하는 비율이다. 최고 수준 모델인 GPT-4o도 과제의 50% 미만에서만 성공했고, 소매 과제에서 한 번 성공률은 60% 안팎이었지만 8번 연속 성공은 25% 미만이었다([arXiv](https://arxiv.org/abs/2406.12045)). 매번 JSON은 유효했을 것이다. 문제는 그 안의 값과 호출 순서가 시도마다 달랐다는 점이다. 고객센터나 정산처럼 같은 요청에 같은 처리가 필요한 시스템에서 중요한 숫자는 pass^1이 아니라 pass^k다.

틀을 더 세게 묶는 것이 답도 아니다. 대만 국립대만대 등 연구진이 2024년 8월 낸 "Let Me Speak Freely?"는 JSON 모드 같은 형식 제약 아래서 모델의 추론 능력이 뚜렷이 떨어지고, 제약이 강할수록 하락이 크다고 보고했다. 반면 분류 과제에서는 형식 제약이 답 선택 오류를 줄여 정확도를 올렸다([arXiv](https://arxiv.org/abs/2408.02442)). 포맷 보장과 내용 품질이 서로 당기는 관계여서, 자연어로 먼저 답하게 한 뒤 형식으로 변환하는 2단계 설계가 대안으로 제시됐다. 구조화 출력을 켜는 것은 공짜가 아니다.

## 현장은 어떻게 대응하나

실무 조사는 이 두 층을 따로 다루지 않고 "품질"과 "신뢰성"이라는 한 단어로 묶지만, 숫자의 방향은 같다. LangChain이 2025년 11~12월 1,340명을 조사해 2026년 6월 낸 보고서에서 에이전트를 운영 중인 비율은 57.3%였고, 운영 진입의 최대 장벽은 품질(32%)과 지연(20%)이었다. 관측 도구를 붙인 곳은 89%인데 오프라인 평가를 돌리는 곳은 52.4%, 온라인 평가는 37.3%에 그쳤다([LangChain](https://www.langchain.com/state-of-agent-engineering)).

VentureBeat Intelligence가 100인 이상 기업 140명을 대상으로 한 8월 조사는 더 직접적이다. 사전 평가를 운영하는 응답자 가운데 61%가 지난 12개월 안에 내부 평가를 통과한 에이전트나 LLM 기능이 고객 대면 장애를 일으킨 경험이 있다고 답했고, 그중 22%는 두 번 이상이었다. 에이전트를 배포한 조직 중 자동 평가만으로 운영 반영을 허용하거나 그렇게 가려는 비율은 7월 75%에서 8월 56%로 떨어졌고, 사람 검토자를 유지하겠다는 비율은 20%에서 42%로 올랐다. 운영 모니터링을 실시간 품질 검사 중심으로 짠 곳은 29%뿐이고 53%는 추적 로그와 게이트웨이 지표, 즉 출력의 정확성이 아니라 시스템 상태를 본다([VentureBeat](https://venturebeat.com/resources/agentic-reliability-and-evaluations-fewer-enterprises-plan-to-let-ai-agents-ship-production-changes-on-automated-checks-alone-56-allow-it-or-plan-to-down-from-75-in-july)).

한편 Datadog이 LLM 관측 고객 수천 곳의 텔레메트리로 낸 2026년 보고서에서 LLM 호출 실패의 1위는 출력 오류가 아니라 속도 제한(rate limit)이었다. 2026년 2월 LLM 호출의 5%가 오류였고 그중 60%가 속도 제한 초과였으며, 3월에는 오류율 2%에 속도 제한이 약 3분의 1, 840만 건에 달했다([Datadog](https://www.datadoghq.com/state-of-ai-engineering/)). 포맷이 깨져 터지는 시스템보다 용량이 모자라 터지는 시스템이 많다는 뜻이고, 이것도 "확률 모델의 한계"와는 무관한 인프라 문제다.

이 조사들이 가리키는 실무 패턴은 일관된다. 구조화 출력으로 틀을 고정하고, 값은 애플리케이션 쪽 검증과 재시도로 거르고, 한 번에 맡기는 단계를 10개 안팎으로 자르고, 그 뒤에 사람을 둔다. 모델을 믿는 설계가 아니라 모델을 감싸는 설계다.

## 의미

- "확률 모델이라 정규 포맷을 못 지킨다"는 2024년 8월 이전의 문제다. 제약 디코딩은 샘플링 전에 틀 밖의 선택지를 지우므로 확률 모델이라는 사실과 충돌하지 않는다. 지금 JSON이 깨진다면 기능을 안 켰거나 스키마가 지원 범위를 벗어난 것이다.
- "매번 같은 결과가 안 나온다"는 지금도 맞다. 다만 이유가 통념과 다르다. 온도 0에서도 서버 부하가 출력을 바꾸고, 상용 API는 배치 불변성을 보장하지 않는다. 결정적 실행이 필요하면 자체 추론 서버에서 속도를 치르고 사야 한다.
- 정보시스템이 요구하는 것은 틀이 아니라 틀 안의 값이 매번 같은 것이다. 이 요구에 대한 공개 지표는 pass^k이고, 모델 발표가 내세우는 pass^1과는 다른 숫자다. 시스템을 설계할 때 물어야 할 것은 "JSON이 나오느냐"가 아니라 "100번 돌리면 몇 번 같은 처리를 하느냐"다.
- 현장은 이미 답을 냈다. 자율성을 줄이고 단계를 자르고 사람을 붙인다. 에이전트가 정규적인 결과를 못 만들어서가 아니라, 매번 만든다는 보장이 없음을 알기 때문이다.

## 확인할 점

- OpenAI의 스키마 일치 100%는 2024년 8월 자체 평가의 수치이며 공개된 독립 재현은 확인하지 못했다. 구조화 출력은 잘림과 거부를 보장 밖에 두므로 실제 서비스의 유효 출력률은 100%보다 낮을 수 있다.
- Thinking Machines 실험은 오픈 모델과 vLLM 환경에서 수행됐다. OpenAI·Anthropic·Google의 상용 API가 어떤 커널을 쓰는지는 공개되지 않았고, 이 기사는 이들이 배치 불변성을 보장한다는 자료를 찾지 못했다는 수준에서 썼다.
- τ-bench의 pass^8 수치는 2024년 6월 GPT-4o 기준이다. 이후 모델은 pass^1이 크게 올랐지만, 최신 모델의 pass^k 공식 수치는 이 기사에서 확인하지 못했다. 후속 벤치마크 τ²·τ³-bench 성적표에 pass^k가 함께 공개되는지 확인이 필요하다.
- "Let Me Speak Freely?"는 2024년 중반 모델로 한 실험이며, 제약 디코딩 구현이 바뀐 2026년 모델에서 같은 폭의 하락이 나는지는 별도 검증이 필요하다.
- Measuring Agents in Production의 수치는 20개 인터뷰와 86개 설문의 자기 보고에 기반하며 시스템을 직접 감사하지 않았다. VentureBeat 조사는 독자 패널 140명의 자기 선택 표본이다.
- LangChain 보고서는 자사 도구 사용자 중심 표본이어서 운영 비율 57.3%는 상한으로 읽는 것이 안전하다.

## 출처

- [OpenAI, Introducing Structured Outputs in the API (2024-08-06)](https://openai.com/index/introducing-structured-outputs-in-the-api/)
- [Anthropic, Structured outputs (Claude API 문서)](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Thinking Machines Lab, Defeating Nondeterminism in LLM Inference (2025-09-10)](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)
- [Simon Willison, Defeating Nondeterminism in LLM Inference (2025-09-11)](https://simonwillison.net/2025/Sep/11/defeating-nondeterminism/)
- [Yao et al., τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (arXiv 2406.12045, 2024-06-17)](https://arxiv.org/abs/2406.12045)
- [Tam et al., Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models (arXiv 2408.02442, 2024-08-05)](https://arxiv.org/abs/2408.02442)
- [Pan et al., Measuring Agents in Production (arXiv 2512.04123, 2025-12-02, v4 2026-06-04)](https://arxiv.org/abs/2512.04123)
- [Paper Notes, Measuring Agents in Production 요약 (ICML 2026)](https://en.papernotes.org/ICML2026/llm_agent/measuring_agents_in_production/)
- [LangChain, State of Agent Engineering (2026-06-12)](https://www.langchain.com/state-of-agent-engineering)
- [VentureBeat, Agentic reliability and evaluations: fewer enterprises plan to let AI agents ship production changes on automated checks alone (2026-10-05)](https://venturebeat.com/resources/agentic-reliability-and-evaluations-fewer-enterprises-plan-to-let-ai-agents-ship-production-changes-on-automated-checks-alone-56-allow-it-or-plan-to-down-from-75-in-july)
- [Datadog, State of AI Engineering (2026)](https://www.datadoghq.com/state-of-ai-engineering/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
