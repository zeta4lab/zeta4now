---
title: 구글 Hydrogen이 검색에서 더 낫게 느껴지는 이유는 더 알아서가 아니라 덜 지어내서다…코딩 격차의 상대는 OpenAI 모델이 아니라 Anthropic과 시장
slug: 2026-11-15-gemini-4-hydrogen-search-fabricates-less
topic: ai
published_at: 2026-11-15T19:55:00+09:00
summary: 구글이 12일 검색 AI 모드의 기본 모델로 넣은 Gemini 4 Hydrogen은 독립 평가에서 지식 문제를 절반가량만 맞혔지만, 틀린 답을 지어내는 비율은 8.5%로 GPT·Claude 모델의 4분의 1 이하였다. 지식을 검색 엔진이 대 주는 자리에서는 이 성질이 곧 품질이 된다. 코딩에서 구글 최상위 모델은 OpenAI를 앞섰지만 기업 API 지출 점유율은 9%로 떨어졌고, 빠른 모델 값을 올린 곳은 구글뿐이다.
tags:
  - 구글
  - Gemini
  - Hydrogen
  - AI 검색
  - 환각
  - 코딩 에이전트
  - 네이버
generated_by: claude
model: claude-opus-5-5
---

# 구글 Hydrogen이 검색에서 더 낫게 느껴지는 이유는 더 알아서가 아니라 덜 지어내서다…코딩 격차의 상대는 OpenAI 모델이 아니라 Anthropic과 시장

## 판단: 검색에 필요한 것은 아는 양이 아니라 멈출 줄 아는 것이다

구글은 11월 12일(현지시각) Gemini 3.8 Flash의 후속 모델 Gemini 4 Hydrogen을 내놓으면서 'Flash'라는 이름을 버렸다. 구글 검색에는 "모든 사용자"에게 배포했고, 로비 스타인 검색 제품 부사장은 X에서 Hydrogen이 AI 모드의 기본 모델이며 AI 개요(AI Overviews)에서도 "가장 어려운 질문"에 쓰인다고 했다([Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/), [Search Engine Journal](https://www.searchenginejournal.com/google-gemini-4-hydrogen-default-ai-mode/597096/)).

이 사이트 편집자가 써 본 체감은 이렇다. 코딩과 에이전트 작업에서는 OpenAI·Anthropic에 미치지 못하지만, 일상 검색에서 받는 답은 전에 써 본 Flash보다 좋았다. 측정이 아니라 사용 소감이다. 그런데 독립 평가 수치를 보면 이 체감에는 구체적인 이유가 있다.

외부 평가 기관 Artificial Analysis의 AA-Omniscience는 검색 없이 지식 문제 3,000개를 묻는다. 여기서 Hydrogen(최고 추론 설정)이 맞힌 비율은 50.5%로 경쟁 모델보다 낮다. 대신 문제의 44%에는 아예 답하지 않았고, 맞히지 못한 문제에서 모른다고 하지 않고 틀린 답을 낸 비율(환각률)은 8.5%였다. 같은 평가에서 GPT-6.1 Sol은 51.9%, Claude Fable 5.2는 59.3%였다([Artificial Analysis](https://artificialanalysis.ai/evaluations/omniscience)).

| 모델(설정) | 정답률 | 응답 시도율 | 환각률 |
|---|---|---|---|
| Gemini 4 Hydrogen (Xhigh) | 50.5% | 56.0% | 8.5% |
| Gemini 4 Carbon (High) | 58.3% | 64.3% | 11.4% |
| GPT-6.1 Terra (Max) | 47.6% | 68.4% | 34.5% |
| Claude Sonnet 5.5 (Max) | 51.5% | 76.3% | 43.3% |
| GPT-6.1 Sol (Max) | 61.8% | 83.5% | 51.9% |
| Claude Fable 5.2 (Max) | 79.1% | 94.8% | 59.3% |

이 글의 판단은 이렇다. **Hydrogen은 아는 것이 많은 모델이 아니라, 모르면 멈추는 모델이다.** 단순 계산으로 Hydrogen이 답한 문제의 약 90%는 정답이었다. 반면 Fable 5.2는 거의 모든 문제에 답해 정답률이 훨씬 높지만, 답한 문제 가운데 정답은 약 83%였다. 코딩이나 연구에서는 많이 아는 쪽이 이긴다. 그러나 검색에서는 지식을 검색 엔진이 대 주므로, 모델에게 필요한 것은 결과를 읽고 없는 것을 지어내지 않는 능력이다. 검색 회사가 자기 자리에 맞춰 만든 모델로 보인다. 이는 해석이다.

## 검색은 모델이 다 알지 않아도 되는 자리다

구글이 이 자리를 고른 이유는 규모에 있다. 순다르 피차이 CEO는 5월 I/O에서 AI 개요의 월간 사용자가 25억 명을 넘었다고 했고, 7월에는 AI 모드가 월간 사용자 10억 명을 넘었다고 했다. 10월 말 3분기 실적 발표에서는 Gemini 앱 사용자가 10억 명이라고 밝혔다([Google I/O](https://blog.google/innovation-and-ai/sundar-pichai-io-2026/), [2분기](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/), [3분기](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/)).

사람들이 AI에 묻는 것도 대부분 코딩이 아니다. OpenAI와 하버드 연구진이 ChatGPT 메시지를 분석한 연구(2025년 7월까지의 데이터)에서 정보 찾기는 24%였고, 연구진은 이를 "웹 검색의 매우 가까운 대체재"라고 불렀다. 프로그래밍은 4.2%였다([NBER](https://www.nber.org/papers/w34255)). Anthropic은 3월 보고서에서 Claude.ai 대화 가운데 컴퓨터·수학 업무 비중이 35%로 줄었고 코딩은 API 쪽으로 옮겨 가고 있다고 했다([Anthropic](https://www.anthropic.com/research/economic-index-march-2026-report)). 일상 질문의 기본값을 쥔 쪽에는 코딩 순위보다 '지어내지 않는 답'이 더 중요하다.

다만 체감이 어디서 나오는지는 구분해야 한다. Gemini 앱의 무료 사용자는 대부분 Flash-Lite로 답을 받고, 자동 모델 선택이 필요하다고 판단할 때만 Hydrogen이 쓰인다([Google 도움말](https://support.google.com/gemini/answer/18648722)). 무료로 Hydrogen을 확실히 만나는 곳은 앱이 아니라 검색 AI 모드다.

## 코딩: 구글이 뒤진 상대는 OpenAI 모델이 아니다

코딩에서 구글이 뒤처졌다는 말은 절반만 맞다. 터미널 작업 벤치마크 Terminal-Bench 4.1 공식 순위에서 1위는 Claude Opus 5.5와 Fable 5.2(65.8%)다. 구글 최상위 모델 Gemini 4 Carbon은 64.5%로 3위이고, GPT-6.1 Sol(60.9%)과 GPT-6 Astra(60.3%)보다 높다. Hydrogen은 56.4%로, 같은 중간 등급의 GPT-6.1 Terra(53.3%)보다 높고 Claude Sonnet 5.5(63.9%)보다 낮다([Terminal-Bench](https://www.tbench.ai/leaderboard)). 코딩 도구와 모델 조합을 함께 평가하는 Artificial Analysis 코딩 에이전트 지수에서도 Claude Code 조합이 58점대로 상위를 차지했고, Antigravity CLI와 Carbon 조합은 55.5점으로 Codex와 Astra 조합(53.1점)을 앞섰다([Artificial Analysis](https://artificialanalysis.ai/agents/coding-agents)).

구글 스스로도 경쟁 우위를 내세우지 않았다. 구글이 낸 평가표는 Hydrogen을 Sonnet 5.5, Terra와만 비교했는데, Terminal-Bench 4.1(57.0% 대 63.9%)과 컴퓨터 조작 평가 OSWorld-2.1(77.6% 대 83.9%)에서 Sonnet 5.5에 졌다([Google 평가 자료](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_hydrogen_model_evaluation.pdf)).

격차가 분명한 곳은 모델이 아니라 시장이다. 멘로벤처스가 9월 미국 기업 약 400곳을 조사한 결과, 기업 LLM API 지출 점유율은 Anthropic 55%, OpenAI 31%, 구글 9%였다. 구글은 1년 전 21%에서 반 아래로 줄었다([Menlo Ventures](https://menlovc.com/perspective/2026-the-state-of-enterprise-ai/)). 스택오버플로 2026 개발자 조사에서 지난 1년간 써 본 코딩 에이전트로는 Claude Code가 65.5%, OpenAI Codex가 29.5%였고 구글 Antigravity는 16.0%였다([Stack Overflow](https://survey.stackoverflow.co/2026/ai/data/ai-code-agent)).

이 글은 구글의 코딩 문제를 성능이 아니라 습관의 문제로 본다. 개발자는 벤치마크 점수가 아니라 매일 쓰는 도구로 모델을 고른다. Carbon이 일반에 공개된 것은 11월 10일이다([Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)). 9월 조사에 잡힐 수 없었고, 이미 Claude Code에 익숙해진 손을 점수 몇 점으로 옮기기도 어렵다. 이는 해석이다.

## 값을 올린 곳은 구글뿐이다

Hydrogen의 API 가격은 100만 토큰당 입력 1.5달러, 출력 7.5달러다. 지금 3.8 Flash(0.75달러·3.75달러)의 두 배이고, 3.8 Flash도 내년 1월 1일부터 같은 값으로 오른다. 플래그십 Argon과 Carbon도 12월 1일부터 입력 2달러·출력 10달러에서 4달러·20달러로 오른다([Google 가격표](https://aistudio.google.com/docs/pricing)). 같은 시기 OpenAI의 중간 등급 GPT-6.1 Terra는 전작의 2달러·12달러에서 1달러·5달러로 내렸고([OpenAI](https://developers.openai.com/api/docs/pricing)), Anthropic의 Sonnet 5.5는 2달러·10달러, Haiku 5.5는 0.1달러·0.5달러로 전작보다 내렸다([Anthropic](https://platform.claude.com/docs/en/about-claude/pricing)). Hydrogen은 말도 많다. Artificial Analysis의 종합 지수를 돌리는 데 출력 토큰을 3억 400만 개 썼는데, 비슷한 모델의 중간값은 7,730만 개였다([Artificial Analysis](https://artificialanalysis.ai/models/gemini-4-hydrogen)).

값을 올리는 쪽의 계산은 분명하다. 구글에게 Hydrogen의 주 무대는 개발자 API가 아니라 자기 검색창이고, 검색에서 드는 비용은 API 가격표와 관계가 없다. 그러나 기업 시장 점유율이 21%에서 9%로 떨어진 상황에서 가장 싼 축이던 Flash 계열의 값을 올리면, 그 계산의 대가는 개발자 시장에서 치를 가능성이 크다. 이는 해석이다.

## 한국에서는 이 계산이 다르다

구글 AI 모드는 2025년 9월부터 한국어를 지원한다([구글코리아](https://blog.google/intl/ko-kr/products/explore-get-answers/ai-mode-in-korean)). 그러나 한국 검색의 기본값은 구글이 아닐 수 있다. 인터넷트렌드 집계로 10월 15일부터 11월 13일까지 국내 검색 점유율은 네이버 65.24%, 구글 28.66%였다([인터넷트렌드](https://internettrend.co.kr/reports/search-engine)). 같은 10월 스탯카운터 집계는 구글 48.48%, 네이버 42.25%로 정반대다([StatCounter](https://gs.statcounter.com/search-engine-market-share/all/south-korea)). 측정 방식에 따라 1위가 바뀌는 시장이다. 네이버는 AI 브리핑을 월 3,000만 명 이상이 쓰고, 대화형 검색 AI탭 이용자가 7월 1,000만 명을 넘었다고 밝혔다([파이낸셜뉴스](https://www.fnnews.com/news/202607150901017615)). 앱에서는 9월 기준 ChatGPT 월간 사용자가 2,470만 명으로, Gemini(987만 명)의 2.5배였다([바이라인네트워크(와이즈앱·리테일)](https://byline.network/2026/10/13_2918273-4/)).

그래서 Hydrogen이 한국에 주는 교훈은 구글보다 네이버에 더 가깝다. 한국에서 일상 검색의 기본값을 쥔 쪽은 네이버이고, 사용자가 검색 AI를 판단하는 기준도 코딩 점수가 아니라 틀린 답을 내놓느냐다. 구글이 자기 검색창에 맞춰 '멈출 줄 아는 모델'을 만들었듯, 국내 검색 AI의 경쟁력도 모델 순위보다 지어내지 않는 비율에서 갈릴 것이다. 이는 해석이다.

## 확인하지 못한 것

- Hydrogen이 AI 모드의 기본 모델이라는 내용은 스타인 부사장의 X 게시물을 인용한 Search Engine Journal·9to5Google 보도로만 확인했다. 구글 검색 블로그는 "모든 사용자에게 제공"이라고만 썼고 '기본'이나 AI 개요를 언급하지 않았다. 한국어 AI 모드에 Hydrogen이 적용됐는지도 공식 확인이 없다.
- 구글이 말한 "지어낸 주장 5분의 1 이하"는 3.8 Flash 대비 수치이며 원 수치를 공개하지 않았다. 모델 카드에도 사실성 벤치마크가 없다.
- AA-Omniscience는 검색 없이 기억만으로 답하는 평가다. 검색을 붙인 AI 모드의 답 품질을 독립적으로 잰 결과는 찾지 못했다. LMArena 검색 순위는 공식 페이지 접속이 막혀 확인하지 못했다.
- 구글이 밝힌 Terminal-Bench 4.1 57.0%는 부정행위 보정 수치이고, 공식 순위표 수치는 56.4%다.
- 3분기 구글 검색 광고 매출 증가율은 12%로 2분기 17%보다 낮아졌다. 검색 질의는 5년 만에 가장 많이 늘었는데도 그렇다. 배포 우위가 매출로 이어지는지는 아직 알 수 없다.
- 한국 검색 점유율은 집계 기관마다 크게 다르다. 앱 사용자 수는 모바일 표본조사다.

## 출처

- [Google, Introducing Gemini 4 Hydrogen (2026-11-12)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/)
- [Google, Gemini 4 Hydrogen in Search (2026-11-12)](https://blog.google/products-and-platforms/products/search/gemini-4-hydrogen-search-upgrade)
- [Google, Build with Gemini 4 Hydrogen (2026-11-12)](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/)
- [Google DeepMind, Gemini 4 Hydrogen 모델 카드](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Hydrogen-Model-Card.pdf)
- [Google DeepMind, Gemini 4 Hydrogen 평가 자료](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_hydrogen_model_evaluation.pdf)
- [Google AI Studio, Gemini API 가격](https://aistudio.google.com/docs/pricing)
- [Google, Gemini 앱 모델 선택 도움말](https://support.google.com/gemini/answer/18648722)
- [Google, Gemini 4 Carbon now available](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)
- [Search Engine Journal, Gemini 4 Hydrogen default in AI Mode (2026-11-12)](https://www.searchenginejournal.com/google-gemini-4-hydrogen-default-ai-mode/597096/)
- [9to5Google, Google announces Gemini 4 Hydrogen (2026-11-12)](https://9to5google.com/2026/11/12/gemini-4-hydrogen-launch/)
- [Artificial Analysis, AA-Omniscience](https://artificialanalysis.ai/evaluations/omniscience)
- [Artificial Analysis, Gemini 4 Hydrogen](https://artificialanalysis.ai/models/gemini-4-hydrogen)
- [Artificial Analysis, Coding Agent Index](https://artificialanalysis.ai/agents/coding-agents)
- [Terminal-Bench, Leaderboard](https://www.tbench.ai/leaderboard)
- [Google, Sundar Pichai I/O 2026 (2026-05-19)](https://blog.google/innovation-and-ai/sundar-pichai-io-2026/)
- [Google, Alphabet Q2 2026 earnings CEO remarks (2026-07-22)](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/)
- [Google, Alphabet Q3 2026 earnings CEO remarks (2026-10-28)](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/)
- [NBER, How People Use ChatGPT (w34255)](https://www.nber.org/papers/w34255)
- [Anthropic, Economic Index March 2026 report](https://www.anthropic.com/research/economic-index-march-2026-report)
- [Menlo Ventures, 2026: The State of Enterprise AI (2026-11-03)](https://menlovc.com/perspective/2026-the-state-of-enterprise-ai/)
- [Stack Overflow, 2026 Developer Survey: AI code agents](https://survey.stackoverflow.co/2026/ai/data/ai-code-agent)
- [OpenAI, API pricing](https://developers.openai.com/api/docs/pricing)
- [Anthropic, Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [구글코리아, AI 모드를 이제 한국에서도 만나볼 수 있습니다 (2025-09-08)](https://blog.google/intl/ko-kr/products/explore-get-answers/ai-mode-in-korean)
- [인터넷트렌드, 검색엔진 점유율](https://internettrend.co.kr/reports/search-engine)
- [StatCounter, Search engine market share South Korea](https://gs.statcounter.com/search-engine-market-share/all/south-korea)
- [파이낸셜뉴스, 네이버 AI탭 이용자 1000만명 돌파 (2026-07-15)](https://www.fnnews.com/news/202607150901017615)
- [바이라인네트워크, 2026년 9월 생성형 AI 모바일 앱 MAU (2026-10-13)](https://byline.network/2026/10/13_2918273-4/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
