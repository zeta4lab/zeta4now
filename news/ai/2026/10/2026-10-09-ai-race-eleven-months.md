---
title: 1년이 10년 같았던 11개월…코딩 에이전트에서 'AI가 만드는 AI'까지, AI는 왜 이렇게 빨라졌나
slug: 2026-10-09-ai-race-eleven-months
topic: ai
published_at: 2026-10-09T21:02:00+09:00
tags:
  - AI
  - LLM
  - 코딩 에이전트
  - 중국 AI
  - 분석
summary: 2025년 11월 코딩 에이전트가 실무에서 쓸 만해진 뒤 11개월 동안 미국과 중국 AI 기업은 수십 개의 모델을 쏟아냈다. 연혁을 정리하고, 강화학습의 확장과 AI가 AI 개발을 돕는 순환 구조 등 발전이 빨라진 이유를 분석했다.
generated_by: claude
model: claude-opus-5-5
---

# 1년이 10년 같았던 11개월…코딩 에이전트에서 'AI가 만드는 AI'까지, AI는 왜 이렇게 빨라졌나

## 한눈에 보기

많은 개발자는 2025년 11월을 생성형 AI가 "진짜 쓸 만해진" 시점으로 기억한다. 구글 Gemini 3 Pro(11월 18일), OpenAI GPT-5.1-Codex-Max(11월 19일), Anthropic Claude Opus 4.5(11월 24일)가 일주일 사이에 잇달아 나왔고, 코딩 에이전트에게 실제 업무를 맡기는 방식이 이때부터 빠르게 퍼졌다. 그 뒤 2026년 10월 9일까지 11개월 동안 미국과 중국 기업은 수십 개의 모델을 내놓았고, AI가 혼자 해낼 수 있는 작업의 길이는 석 달마다 두 배씩 늘었다.

이 글은 그 11개월의 연혁을 정리하고, 발전이 이렇게 빨라진 이유를 다섯 가지로 나눠 분석한다. 근거는 METR·Epoch AI 같은 독립 연구기관의 측정치와 각 회사의 공식 발표다. 회사가 스스로 밝힌 성능은 '회사 주장'으로 구분했다.

## 전환점: 2025년 11월

Anthropic은 11월 24일 Claude Opus 4.5를 내놓으며 ["코딩·에이전트·컴퓨터 사용에서 세계 최고의 모델"](https://www.anthropic.com/news/claude-opus-4-5)이라고 소개했다. 회사 채용 과제를 정해진 2시간 안에 역대 어느 지원자보다 높은 점수로 풀었다고 밝혔고, 가격은 이전 Opus의 3분의 1 수준인 100만 토큰당 입력 5달러, 출력 25달러로 낮췄다.

변화는 개발자의 작업 방식에서 먼저 드러났다. 테슬라 AI 책임자 출신 안드레이 카파시는 2025년 11월에는 손으로 짜는 코드가 80%, 에이전트가 20%였는데 12월에는 이 비율이 [뒤집혔다고 밝혔다](https://the-decoder.com/former-tesla-ai-chief-andrej-karpathy-now-codes-mostly-in-english-just-three-months-after-calling-ai-agents-useless/). 그는 "이제는 대부분 영어로 프로그래밍한다"고 말했다.

독립 측정도 같은 흐름을 보여 준다. AI가 사람 기준으로 몇 시간짜리 작업을 절반의 확률로 해내는지 재는 METR의 '시간 지평' 지표에서, Opus 4.5는 [약 320분(5시간 20분)](https://metr.org/blog/2026-1-29-time-horizon-1-1/)을 기록해 당시 최고치를 세웠다.

## 11개월 연표

### 미국·유럽

| 날짜 | 회사 | 출시 | 의미 |
|---|---|---|---|
| 2025-11-18 | 구글 | Gemini 3 Pro | 에이전트 개발 플랫폼 Antigravity 공개 |
| 2025-11-19 | OpenAI | GPT-5.1-Codex-Max | 24시간 넘게 이어지는 코딩 작업 시연 |
| 2025-11-24 | Anthropic | Claude Opus 4.5 | 가격을 3분의 1로 낮춘 최상위 모델 |
| 2025-12-11 | OpenAI | GPT-5.2 | Gemini 3 이후 '코드 레드' 속 출시 보도 |
| 2026-02-05 | Anthropic·OpenAI | Claude Opus 4.6, GPT-5.3-Codex | 약 1시간 차이로 같은 날 발표, 코딩 에이전트 경쟁 본격화 |
| 2026-02-19 | 구글 | Gemini 3.1 Pro | 추론 성능 대폭 향상(회사 주장) |
| 2026-03-05 | OpenAI | GPT-5.4 | 3월 중순 소형 모델 추가 |
| 2026-04-07 | Anthropic | Claude Mythos Preview | 일반 공개 없이 사이버 방어 협력사에만 제공 |
| 2026-04-08 | 메타 | Muse Spark | 슈퍼인텔리전스 연구소의 첫 모델, 폐쇄형으로 전환 |
| 2026-04-23 | OpenAI | GPT-5.5 | |
| 2026-06-02 | 마이크로소프트 | MAI 모델 7종 | 자체 추론 모델 첫 출시 |
| 2026-06-09 | Anthropic | Claude Fable 5 | Mythos급 모델의 첫 일반 공개 |
| 2026-07-09 | OpenAI | GPT-5.6 Sol·Terra·Luna | 정부 요청에 따른 제한 공개 뒤 일반 공개 |
| 2026-07-24 | Anthropic | Claude Opus 5 | |
| 2026-08-10 | 메타 | Muse Glimmer | 30B 오픈 웨이트로 개방형 복귀 |
| 2026-09-03 | OpenAI | GPT-6 Astra | 컴퓨터 사용 강화, 사이버 능력 '위험' 단계 첫 모델 |
| 2026-09-22 | Anthropic·OpenAI | Claude Opus 5.5, GPT-6 Sol·Luna | 약 90분 차이로 같은 날 발표, 가격 인하 경쟁 |
| 2026-09-30 | 구글 | Gemini 4 Argon | 사이버 방어자 대상 제한 프리뷰 |
| 2026-10-06 | 미스트랄 | Mistral Large 4 프리뷰 | 약 1조 파라미터, 유럽에서 학습 |

xAI는 Grok 4.1(2025년 11월)에서 Grok 4.5(2026년 7월), 4.7(9월)로 이어졌지만 예고했던 Grok 5는 아직 내놓지 않았다. 2026년 2월 스페이스X에 합병됐다.

### 중국

| 날짜 | 회사 | 출시 | 의미 |
|---|---|---|---|
| 2025-11-06 | 문샷 | Kimi K2 Thinking | 1조 파라미터 오픈 웨이트, 수백 번 연속 도구 사용 |
| 2025-12-01 | 딥시크 | DeepSeek-V3.2 | GPT-5급을 주장한 오픈 웨이트 |
| 2025-12-22 | 즈푸 | GLM-4.7 | 코딩 특화 오픈 웨이트 |
| 2026-01-27 | 문샷 | Kimi K2.5 | 하위 에이전트 최대 100개 동시 실행 |
| 2026-02-11 | Z.ai(즈푸) | GLM-5 | 오픈 웨이트 |
| 2026-02-14 | 바이트댄스 | Doubao-Seed-2.0 | GPT-5.2·Gemini 3 Pro급 주장, 낮은 가격 |
| 2026-02-16 | 알리바바 | Qwen3.5 | 앱을 조작하는 에이전트 기능 |
| 2026-04-24 | 딥시크 | DeepSeek-V4 프리뷰 | 1.6조 파라미터, 100만 토큰 문맥, 화웨이 어센드 칩 지원 |
| 2026-06-01 | 미니맥스 | MiniMax-M3 | 100만 토큰 문맥 오픈 웨이트 |
| 2026-07 | 문샷 | Kimi K3 | 2.8조 파라미터, 공개된 최대 규모 오픈 웨이트 |
| 2026-08 | 알리바바 | Qwen3.8-Max | 최상위급 첫 오픈 웨이트 |
| 2026-09-10 | 딥시크 | DeepSeek-V4.1-Flash | 낮은 가격의 고성능 모델 |
| 2026-09-22 | 샤오미 | MiMo-V2.6-Pro | 출시 시점 오픈 웨이트 1위(Artificial Analysis 기준) |

같은 기간 중국에서는 즈푸와 미니맥스가 2026년 1월 홍콩 증시에 상장했다. 니케이아시아는 2026년 9월 한 달에만 딥시크와 샤오미 등 중국 기업이 [16개 모델을 출시했다](https://asia.nikkei.com/business/technology/artificial-intelligence/china-s-deepseek-peers-launch-16-ai-models-in-month-despite-anthropic-warning)고 보도했다.

## 숫자로 본 11개월

- **작업 길이**: METR은 2026년 1월 분석에서 AI가 해낼 수 있는 작업 길이가 2024년 이후 [약 89일마다 두 배](https://metr.org/blog/2026-1-29-time-horizon-1-1/)로 늘었다고 집계했다. 2023년 이후로 보면 131일, 전체 기간으로 보면 약 196일이다. 배가 속도 자체가 빨라지고 있다는 뜻이다. METR은 이후 최신 모델들이 16시간 이상으로 측정되자 현재 과제 세트로는 더 재기 어렵다고 밝혔다.
- **벤치마크 포화**: 실제 깃허브 이슈를 고치는 SWE-bench Verified에서 2025년 11월 최고 점수는 70%대 중반이었지만, 2026년 9월에는 [90% 후반](https://www.vals.ai/benchmarks/swebench)까지 올라 측정 기관이 더는 쓰지 않기로 했다. 2026년 3월 나온 새 추론 시험 ARC-AGI-3는 출시 당시 최고 모델도 1%를 넘지 못했지만, 9월 OpenAI는 GPT-6 Astra가 표준 방식으로 66%를 기록했다고 [밝혔다](https://fortune.com/2026/09/03/openai-debuts-gpt-6-astra-computer-use-greg-brockman-says-start-of-agi/)(회사 주장).
- **가속**: Epoch AI는 2026년 4월 분석에서 네 가지 지표 중 세 가지에서 [발전이 빨라졌다는 강한 증거](https://epoch.ai/publications/have-ai-capabilities-accelerated)를 찾았고, 추론 모델 등장 이후 추세가 2~3배 빨라졌다고 봤다.
- **가격**: Epoch AI에 따르면 같은 성능을 내는 비용은 2023년 이후 [분기마다 약 47%, 1년에 약 13배](https://epoch.ai/publications/the-plunging-price-of-thought) 떨어졌다. 2025년 1월 문항당 약 30센트 들던 과학 문제 풀이 성능을 18개월 뒤에는 0.04센트에 낼 수 있게 됐다.
- **AI가 쓰는 코드**: Anthropic은 2026년 5월 기준 자사 코드베이스에 병합되는 코드의 [80% 이상을 Claude가 작성한다](https://www.anthropic.com/institute/recursive-self-improvement)고 밝혔다(회사 주장). Claude Code를 내놓은 2025년 2월에는 한 자릿수였다.

## 왜 이렇게 빠른가

### 1. 강화학습이 사전학습처럼 커졌다

2024년까지 AI 성능은 주로 더 많은 글을 읽히는 사전학습의 규모로 좌우됐다. 지금은 모델이 직접 문제를 풀고 정답 여부로 보상을 받는 강화학습이 성능을 끌어올리는 핵심 도구가 됐다. 다리오 아모데이 Anthropic CEO는 2026년 2월 인터뷰에서 ["사전학습에서 봤던 것과 같은 규모의 확장을 강화학습에서 보고 있다"](https://www.dwarkesh.com/p/dario-amodei-2)고 말했다.

이 방식은 코드와 수학처럼 정답을 자동으로 확인할 수 있는 분야에서 특히 잘 통한다. Epoch AI도 최근의 가속이 프로그래밍과 수학처럼 [정답을 검증하기 쉬운 영역에 집중돼 있다](https://epoch.ai/publications/have-ai-capabilities-accelerated)고 분석했다. 코딩 에이전트가 가장 먼저, 가장 크게 발전한 이유다.

### 2. 답하기 전에 더 오래 생각한다

추론 모델은 답을 내기 전에 긴 사고 과정을 거친다. 더 어려운 문제에는 더 많은 연산을 쓰는 방식이라, 같은 모델이라도 생각할 시간을 늘리면 성능이 오른다. 최근 모델들이 '노력 수준'을 고를 수 있게 한 것도 이 때문이다. 추론 시간 연산과 강화학습, 긴 사고 과정은 같은 시기에 함께 발전해 어느 쪽이 얼마나 기여했는지 나누기 어렵다고 Epoch AI는 지적한다.

### 3. AI가 AI를 만드는 순환

코딩 에이전트가 쓸 만해지자, AI 기업들은 자신의 다음 모델을 만드는 데 그 에이전트를 썼다. Anthropic은 [AI가 이미 AI 시스템 개발을 가속하고 있다](https://www.anthropic.com/institute/recursive-self-improvement)고 밝히며, 엔지니어 1인당 하루 병합 코드량이 2024년의 약 8배라고 했다(회사 주장, 줄 수는 품질을 반영하지 않는다는 단서 포함). 2026년 2월 OpenAI는 GPT-5.3-Codex를 "자기 개발에 크게 관여한 첫 모델"로 소개했고, 9월 개발자 행사에서는 2025년 10월 세운 'AI 연구 인턴' 목표를 [달성했다고 주장했다](https://thenextweb.com/news/sam-altman-openai-ai-research-intern-devday-keynote). 더 좋은 모델이 더 좋은 모델을 더 빨리 만드는 고리가 돌기 시작한 셈이다.

### 4. 돈과 전기

빅테크의 2026년 설비투자 계획은 [알파벳 1950억~2050억 달러](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm), [메타 1300억~1450억 달러](https://www.sec.gov/Archives/edgar/data/0001326801/000162828026050596/meta-06302026xexhibit991.htm), 아마존 약 2200억 달러다. 알파벳과 메타는 2025년의 두 배 수준이다. 엔비디아의 2026년 5~7월 분기 매출은 [962억 달러로 1년 새 두 배](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)가 됐다. Epoch AI가 추적하는 데이터센터 가운데 가장 큰 xAI의 멤피스 Colossus 2는 [약 946메가와트](https://epoch.ai/data/ai-data-centers)의 IT 전력을 쓴다.

### 5. 경쟁이 출시 주기를 당겼다

경쟁은 출시 일정에서도 보인다. Anthropic과 OpenAI는 2026년 2월 5일 약 1시간 차이로, 9월 22일 약 [90분 차이로](https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/) 새 모델을 내놓았다. 중국의 오픈 웨이트 모델은 가격을 끌어내렸다. 누구나 내려받아 쓸 수 있는 모델이 몇 달 뒤처진 성능을 훨씬 싼 값에 제공하자, 미국 기업들도 신모델마다 가격을 낮췄다. 9월 OpenAI는 GPT-6 Sol·Luna의 API 가격을 이전 세대의 절반 수준으로 내렸고, Anthropic은 Opus 5.5의 실행 비용을 Opus 5보다 [40% 줄였다고 밝혔다](https://www.anthropic.com/news/claude-opus-5-5).

## 중국의 부상

중국 AI는 공개 모델 생태계를 장악했다. 허깅페이스는 지난 1년간 [모델 다운로드의 41%가 중국 모델](https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026)이었다고 밝혔고, 알리바바 Qwen 계열의 파생 모델만 11만 3000개가 넘는다. 2026년 9월 기준 오픈 웨이트 성능 상위권은 대부분 중국 모델이다.

다만 최전선의 격차는 남아 있다. Epoch AI는 2023년 이후 중국 모델이 미국 최고 성능에 [평균 7개월(4~14개월) 뒤처졌다](https://epoch.ai/data-insights/us-vs-china-eci)고 분석했고, 미국 국립표준기술연구원(NIST) 산하 기관은 2026년 5월 딥시크 V4가 [약 8개월 뒤처진다](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro)고 평가했다. 앨런AI연구소의 네이선 램버트는 9월 중국 오픈 웨이트 모델이 미국 폐쇄형 최전선보다 [2~5개월 뒤처진다](https://www.interconnects.ai/p/the-current-balance-of-power-in-open)고 봤다.

중국이 빠르게 따라잡은 이유로 전문가들은 칩 수출 통제가 오히려 효율화 연구를 밀어붙인 점, 기술을 공개해 생태계 전체가 빠르게 배우는 구조, 빠른 출시 주기를 꼽는다. 딥시크는 V4를 화웨이 어센드 칩에서 돌아가도록 맞춰 미국 칩 의존을 줄였다. 한편 Anthropic은 2026년 2월 중국 기업들이 가짜 계정으로 Claude와 대량 대화해 모델을 '증류'하려 했다고 주장했지만, 해당 기업은 부인했고 독립적으로 검증되지 않았다. 브루킹스연구소의 카일 챈은 증류가 기여했더라도 중국의 진전을 [완전히 설명하지는 못한다](https://www.brookings.edu/articles/competing-ai-strategies-for-the-us-and-china/)고 봤다.

## 속도를 늦추자는 목소리

속도가 빨라지면서 업계 안에서 제동을 거는 목소리도 커졌다. 아모데이는 2026년 9월 12일 에세이 ["We Must Pace the Frontier"](https://rits.shanghai.nyu.edu/ai/amodei-calls-to-pace-the-frontier-altman-and-musk-agree/)에서 업계가 능력 향상 속도를 의도적으로 조절해야 한다고 주장했다. 개발을 멈추자는 것이 아니라, 모델을 정렬하고 안전장치를 갖추고 제3자 평가를 받을 시간을 확보하자는 취지다. 샘 올트먼 OpenAI CEO와 일론 머스크도 동조하는 뜻을 밝혔다.

실제 출시 방식도 바뀌었다. 가장 강력한 모델을 사이버 방어자에게 먼저 제한적으로 공개하는 사례가 늘었다. Anthropic의 Mythos Preview(4월), 구글의 Gemini 4 Argon(9월)이 그렇게 나왔고, OpenAI는 GPT-6 Astra를 사이버 능력 '위험' 단계에 해당하는 첫 모델로 분류했다. 미국 정부는 2026년 6월 최첨단 모델을 출시 전에 정부가 검토하는 자발적 제도를 마련했다.

## 반론과 한계

- **벤치마크가 따라가지 못한다**: 주요 벤치마크가 잇달아 포화되거나 오염 문제로 폐기되면서, 측정 도구 자체가 발전 속도를 따라잡지 못하고 있다. 높은 점수가 실제 업무 능력과 같지 않을 수 있다.
- **검증하기 쉬운 분야에 쏠린 발전**: Epoch AI는 정답을 확인하기 어려운 과제에서는 [같은 속도의 발전이 나타나지 않았을 수 있다](https://epoch.ai/publications/have-ai-capabilities-accelerated)고 지적했다.
- **실제 생산성은 아직 논쟁 중**: METR이 2025년 초 숙련 개발자를 대상으로 한 실험에서는 AI를 쓰면 오히려 작업이 19% 느려졌다. 2025년 말 후속 연구에서는 빨라졌다는 결과가 나왔지만 METR은 [신뢰하기 어려운 신호](https://metr.org/blog/2026-02-24-uplift-update/)라고 단서를 달았다.
- **거품과 에너지**: 영란은행은 AI 관련 자산 가치가 큰 조정에 취약하다고 경고했다. 국제에너지기구(IEA)는 데이터센터 전력 소비가 2030년까지 약 두 배로 늘 것으로 [내다봤다](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary).

## 확인할 점

- 이 글은 Anthropic이 만든 AI인 Claude가 작성했다. Anthropic은 이 글이 다루는 경쟁의 당사자이므로, Anthropic에 관한 서술은 회사 발표임을 밝히고 다른 회사와 같은 기준으로 다루려 했다.
- 연표의 성능 비교와 '세계 최고' 같은 표현은 각 회사의 주장이다. 같은 벤치마크라도 측정 방식에 따라 점수가 크게 다르다.
- 일부 출시일은 출처에 따라 하루 이틀 차이가 난다. OpenAI 공식 페이지는 직접 열람하지 못해 주요 매체 보도를 따랐다.
- 매출과 기업가치, 증류 의혹 등은 회사 발표나 보도에 근거하며 독립적으로 검증되지 않았다.

## 출처

- [Introducing Claude Opus 4.5 — Anthropic](https://www.anthropic.com/news/claude-opus-4-5)
- [Introducing Claude Opus 5.5 — Anthropic](https://www.anthropic.com/news/claude-opus-5-5)
- [When AI builds itself — Anthropic](https://www.anthropic.com/institute/recursive-self-improvement)
- [Time Horizon 1.1 — METR](https://metr.org/blog/2026-1-29-time-horizon-1-1/)
- [Uplift update — METR](https://metr.org/blog/2026-02-24-uplift-update/)
- [Have AI capabilities accelerated? — Epoch AI](https://epoch.ai/publications/have-ai-capabilities-accelerated)
- [The plunging price of thought — Epoch AI](https://epoch.ai/publications/the-plunging-price-of-thought)
- [Chinese AI models have lagged the US frontier by 7 months — Epoch AI](https://epoch.ai/data-insights/us-vs-china-eci)
- [AI data centers — Epoch AI](https://epoch.ai/data/ai-data-centers)
- [SWE-bench Verified — Vals.ai](https://www.vals.ai/benchmarks/swebench)
- [Andrej Karpathy now codes mostly in English — The Decoder](https://the-decoder.com/former-tesla-ai-chief-andrej-karpathy-now-codes-mostly-in-english-just-three-months-after-calling-ai-agents-useless/)
- [Dario Amodei 인터뷰 — Dwarkesh Podcast](https://www.dwarkesh.com/p/dario-amodei-2)
- [OpenAI debuts GPT-6 Astra — Fortune](https://fortune.com/2026/09/03/openai-debuts-gpt-6-astra-computer-use-greg-brockman-says-start-of-agi/)
- [OpenAI launches GPT-6 Sol and Luna — TechCrunch](https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/)
- [Sam Altman: OpenAI AI research intern — The Next Web](https://thenextweb.com/news/sam-altman-openai-ai-research-intern-devday-keynote)
- [Gemini 4 Argon — Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)
- [DeepSeek-V4 Preview — DeepSeek](https://api-docs.deepseek.com/news/news260424)
- [State of Open Source: Spring 2026 — Hugging Face](https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026)
- [CAISI evaluation of DeepSeek V4 Pro — NIST](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro)
- [The current balance of power in open models — Interconnects](https://www.interconnects.ai/p/the-current-balance-of-power-in-open)
- [Competing AI strategies for the US and China — Brookings](https://www.brookings.edu/articles/competing-ai-strategies-for-the-us-and-china/)
- [China's DeepSeek, peers launch 16 AI models in a month — Nikkei Asia](https://asia.nikkei.com/business/technology/artificial-intelligence/china-s-deepseek-peers-launch-16-ai-models-in-month-despite-anthropic-warning)
- [Amodei calls to 'Pace the Frontier'; Altman and Musk agree — NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/amodei-calls-to-pace-the-frontier-altman-and-musk-agree/)
- [NVIDIA second quarter fiscal 2027 results — NVIDIA](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027)
- [Alphabet 2026년 2분기 실적 — SEC](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm)
- [Meta 2026년 2분기 실적 — SEC](https://www.sec.gov/Archives/edgar/data/0001326801/000162828026050596/meta-06302026xexhibit991.htm)
- [Key Questions on Energy and AI — IEA](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
