---
title: 영국 안에서만 도는 AI 에이전트 50개, 그리고 더 싸진 GPT‑5.6·Gemini 3.7 Flash
slug: 2026-08-14-ai-data-engineering-daily
topic: ai-data-engineering
published_at: '2026-08-14T06:00:00+09:00'
updated_at: '2026-10-11T17:30:00+09:00'
tags:
- AI와 데이터 엔지니어링
- AI 에이전트
- 데이터 주권
- 오픈소스 보안
- GPT-5.6
- Gemini 3.7 Flash
summary: 영국 OneAdvanced는 AWS 런던 리전에서 직접 호스팅한 공개 모델로 AI 에이전트 50여 개를 운영하고, GitHub은 오픈소스 보안 기금 성과를 공개했다. 같은 날 OpenAI와 Google은 에이전트 비용을 크게 낮춘 GPT‑5.6 가이드와 Gemini 3.7 Flash를 내놨다.
generated_by: claude
model: claude-opus-5-5
---

# 영국 안에서만 도는 AI 에이전트 50개, 그리고 더 싸진 GPT‑5.6·Gemini 3.7 Flash

## 한눈에 보기

영국 기업용 소프트웨어 업체 OneAdvanced가 데이터를 영국 밖으로 내보내지 않으면서 AI 에이전트 50여 개를 운영하는 구조를 공개했다. GitHub은 오픈소스 보안 기금 네 번째 기수의 결과를 내놨고, 누적 188개 프로젝트에서 새 CVE 533건이 공개됐다. 같은 날 OpenAI와 Google은 에이전트 비용을 크게 낮춘 모델을 소개했다. 데이터 주권, 공급망 보안, 비용이라는 세 방향에서 에이전트를 실제 업무에 넣는 조건이 바뀌고 있다.

## 1. OneAdvanced: 영국 리전 안에서만 도는 에이전트 50여 개

OneAdvanced는 AWS 런던 리전(eu-west-2)에 Strands Agents SDK로 만든 에이전트 50여 개를 배포했다고 8월 12일 AWS 블로그에서 밝혔다. 외부 모델 API 대신 Llama 4 Maverick과 Llama Guard 4를 Amazon SageMaker AI 엔드포인트에 vLLM으로 직접 올려, 프롬프트와 데이터가 영국 리전 밖으로 나가지 않게 했다.

에이전트와 도구 계층은 Amazon ECS 컨테이너에서 돌고, 에이전트마다 다른 시스템 프롬프트와 도구 설정은 Amazon DynamoDB에 둔다. 검색 증강 생성(RAG)은 Aurora PostgreSQL의 pgvector로 처리한다. 사용자 입력은 본 모델에 닿기 전에 Llama Guard 4가 먼저 걸러 낸다. 앞서 쓰던 Llama Guard 3는 정상 요청까지 거부하는 비율이 높아 교체했다고 한다.

공공 부문과 규제 산업 고객은 데이터가 어디서 처리되는지를 계약 조건으로 요구한다. 이 사례는 그런 조건에서도 상용 API 대신 공개 모델을 직접 호스팅해 에이전트를 운영할 수 있음을 보여 준다. OneAdvanced는 AI 거버넌스 표준인 ISO 42001 인증을 보유하고 있다고 밝혔다. [AWS 원문](https://aws.amazon.com/blogs/machine-learning/how-oneadvanced-deployed-over-50-ai-agents-on-uk-sovereign-aws/)

## 2. GitHub: 오픈소스 보안 기금 누적 188개 프로젝트, 새 CVE 533건

GitHub은 8월 13일 Secure Open Source Fund 네 번째 기수의 결과를 공개했다. 이번 기수에는 50개 프로젝트(22개국 메인테이너 71명)에 50만 달러 이상을 지원했고, 참여 프로젝트의 92%가 시크릿 스캐닝, 코드 스캐닝, 보호 브랜치, 비공개 취약점 신고, Dependabot을 켠 상태로 과정을 마쳤다.

2026년 8월까지 누적으로는 188개 프로젝트에 188만 달러가 지원됐다. 그동안 새 CVE 533건이 공개됐고, 노출된 시크릿 650건 이상이 해결됐으며, Dependabot 보안 업데이트는 1,500건을 넘었다.

GitHub이 꼽은 교훈은 AI가 메인테이너의 조사, 우선순위 판단, 대응을 빠르게 한다는 것이다. 참여 프로젝트들은 GitHub Copilot을 취약점 분류, 위협 모델링, 코드 리뷰, 수정에 써 봤다. 다만 최종 판단은 메인테이너가 한다는 점을 분명히 했다. AI로 코드가 빨리 늘어나는 만큼, 이를 지키는 쪽에도 같은 도구가 필요하다는 이야기다. [GitHub 원문](https://github.blog/open-source/maintainers/what-50-open-source-projects-taught-us-about-security-in-the-ai-era/)

## 3. GPT‑5.6과 Gemini 3.7 Flash: 에이전트 단가가 내려간다

OpenAI는 8월 13일 스타트업들이 GPT‑5.6을 프로덕션에 적용한 경험을 정리한 개발자 가이드를 냈다. GPT‑5.6 제품군은 Sol, Terra, Luna로 나뉘며, 작은 모델도 추론 연산을 늘리면 훨씬 낮은 비용으로 이전 플래그십에 가까운 성능을 낸다는 것이 핵심이다. 검색 벤치마크 BrowseComp에서 GPT‑5.5(Extra High)는 84.36%를 내는 데 33.27달러가 들었지만, GPT‑5.6 Luna(Extra High)는 84.04%를 1.33달러로 냈다.

Responses API에는 턴 사이 추론 유지와 컨텍스트 압축, 네이티브 멀티 에이전트 오케스트레이션, 모델이 JavaScript로 도구 호출을 묶어 처리하는 프로그래밍 방식 도구 호출이 들어갔다. 프롬프트 캐시 유지 시간도 최소 30분으로 늘었다. OpenAI는 ARC-AGI-3에서 추론 유지와 컨텍스트 압축을 켜자 GPT‑5.6 Sol의 점수가 13.3%에서 38.3%로 오르고 출력 토큰은 약 6배 줄었다고 밝혔다.

같은 날 Google은 Gemini 3.7 Flash를 공개했다. 3.6 Flash가 나온 지 3주 만으로, 코딩과 에이전트용 주력 모델을 내세웠다. DeepSWE v1.1에서 65.3%(3.6 Flash 49.0%)를 기록하는 등 코딩 지표가 크게 올랐다. 가격은 2026년 말까지 입력 100만 토큰당 0.75달러, 출력 100만 토큰당 3.75달러이고, 2027년부터 각각 1.50달러, 7.50달러가 된다. Gemini API(Google AI Studio), Android Studio, Google Antigravity 등에서 쓸 수 있다.

두 발표 모두 무게중심을 "가장 큰 모델을 쓴다"에서 "작업마다 맞는 모델과 설정을 고른다"로 옮기고 있다. 에이전트 비용을 줄이려면 모델 선택, 추론 수준, 캐시, 도구 호출 구조를 함께 봐야 한다. [OpenAI 원문](https://openai.com/index/builders-guide-to-gpt-5-6) · [Google 원문](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)

## 갱신 기록

- 2026-10-11: zeta4now-mcp(gemma4:31b) 자동 생성본을 운영자 검토로 다시 썼다. 제목과 요약을 구체화했고, ISO 42001을 "아키텍처가 인증을 지원"에서 "회사가 인증을 보유"로, "노출된 비밀번호"를 "노출된 시크릿"으로 정정했다. GPT‑5.6과 Gemini 3.7 Flash의 내용을 원문 수치로 보강하고, 본문에서 다루지 않은 Hugging Face 출처를 뺐다.

## 출처

- [AWS Machine Learning — How OneAdvanced deployed over 50 AI agents on UK-sovereign AWS](https://aws.amazon.com/blogs/machine-learning/how-oneadvanced-deployed-over-50-ai-agents-on-uk-sovereign-aws/) · 2026-08-12
- [GitHub — What 50 open source projects taught us about security in the AI era](https://github.blog/open-source/maintainers/what-50-open-source-projects-taught-us-about-security-in-the-ai-era/) · 2026-08-13
- [OpenAI — The builder’s guide to GPT‑5.6](https://openai.com/index/builders-guide-to-gpt-5-6) · 2026-08-13
- [Google — Introducing Gemini 3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) · 2026-08-13

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
