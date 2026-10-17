---
title: OpenAI, 미공개 모델이 쓴 수학 원고 722편 공개…Lean 검증은 상위 결과의 42%, 이튿날 부호 오류로 3편 철회
slug: 2026-10-17-openai-internal-model-722-math-manuscripts
topic: ai
published_at: 2026-10-17T10:34:00+09:00
tags:
  - OpenAI
  - AI 수학
  - Lean
  - 리만 제타 함수
  - 행렬 곱셈
  - 프런티어 모델
summary: OpenAI가 10월 6일 미공개 내부 모델이 약 4,000개 문제를 풀어 만든 수학 원고 722편(372개 결과군)을 GitHub에 올렸다. Lean 형식 증명은 상위 결과의 약 42%에만 붙었고, 이튿날 부호 오류로 3편이 철회됐다. 제타 함수 영점 부재 영역(Re s > 7/8)과 행렬곱 지수 상한 9/4 같은 주장은 저장소 안의 Lean 검사만 거친 상태이며, 수학계 반응은 "이해의 시작"과 "힘의 과시"로 갈렸다.
generated_by: claude
model: claude-fable-5-1
---

# OpenAI, 미공개 모델이 쓴 수학 원고 722편 공개…Lean 검증은 상위 결과의 42%, 이튿날 부호 오류로 3편 철회

## 한눈에 보기

OpenAI는 10월 6일(현지 시각) "내부 프런티어 모델"이 만든 수학 결과를 GitHub 저장소 `openai/math`에 공개했다. 저장소 README 기준으로 원고는 372개 결과군(family)으로 묶이고, 모델에는 평가 기간에 약 4,000개 문제가 주어졌으며, 결과 하나당 평균 "ChatGPT Pro 사고 연산 3시간"에 해당하는 연산을 썼다([OpenAI](https://openai.com/index/sharing-ai-progress-in-mathematics/), [GitHub](https://github.com/openai/math)). 공개 당시 원고 수는 722편이었고, 이튿날인 10월 7일 부호 오류로 대수기하 원고 3편이 철회돼 현재 README는 719편으로 적는다([GitHub history.md](https://raw.githubusercontent.com/openai/math/main/history.md)).

핵심 쟁점은 검증이다. OpenAI는 "많은 증명"의 Lean 형식화를 함께 올렸지만 전부는 아니며, README는 "형식화되지 않은 결과 일부는 문제가 있을 수 있다(could have issues)"고 경고한다. 저장소의 갱신 기록은 상위 결과 719건 가운데 300건(약 42%)이 형식화됐다고 밝힌다. 리만 제타 함수의 영점 없는 반평면(Re s > 7/8)과 복소수 위 행렬곱 지수 상한 9/4처럼 화제가 된 주장은 Lean 형식화가 붙은 쪽이지만, 그 검사는 저장소 안에서 OpenAI가 제공한 것이고 외부의 인간 검토는 이제 시작 단계다.

OpenAI는 "결과를 만든 모델을 책임 있게 공개하기 위해 작업 중"이라고 했을 뿐 시점은 밝히지 않았고, 워크숍·학회·특별 프로그램을 지원하겠다는 약속은 10월 15일 Simons Foundation의 1,500만 달러 계획으로 구체화됐다([Simons Foundation](https://www.simonsfoundation.org/news/simons-foundation-launches-15m-effort-to-help-mathematicians-navigate-ai-era/)).

## 무엇을 공개했나

OpenAI 공식 글은 짧다. 기존 수학 평가가 포화돼 공개 연구 문제로 평가를 넓혔고, 그 결과를 Institute for Advanced Study(IAS)의 독립 자문기구 Advisory Group on Mathematics and Artificial Intelligence(AGMAI)의 조언과 공개 권고를 참고해 GitHub에 올린다는 내용이다. 투명성을 위해 추론 요약 10건, ChatGPT Pro 사용량 기준 연산 추정, 시도한 문제 수 통계를 함께 공개한다고 했다([OpenAI](https://openai.com/index/sharing-ai-progress-in-mathematics/)).

세부 수치는 저장소 README에 있다. 결과군은 수학 분야별로 분류되고, 한 결과군에는 주 결과와 보조 논증, 귀결, 대안 증명이 함께 들어가므로 722편이 722개의 해결된 문제는 아니다. 대부분의 결과는 미공개 내부 모델에 같은 절차를 적용해 얻었고, 예외는 둘이다. 리만 제타 함수의 영점 없는 영역 작업과 CM 아벨 다양체에 대한 Hodge 추측 증명이다. 이 가운데 Re(s) > 11/12 영역 원고는 "가독성을 위해 사람이 편집했다"고 README가 밝힌다([GitHub](https://github.com/openai/math)). 저장소 라이선스는 Apache-2.0이며, 수정과 철회는 새 버전으로 기록하고 이전 버전을 남긴다.

OpenAI 대변인은 Scientific American에 "거의 모든 결과가 단일 에이전트에 건넨 단일 프롬프트로 나왔고, 일부는 여러 번 시도했다"고 설명했다. 같은 기사에서 OpenAI는 AGMAI 권고를 "진지하게 받아들이지만 구속되지는 않는다"고 했고, 결과별 프롬프트와 연산 시간 대신 평균치만 공개했다([Scientific American](https://www.scientificamerican.com/article/openai-unleashes-hundreds-more-math-results-upon-a-field-already-in-shock/)).

## Lean 검증: 붙은 것과 안 붙은 것

저장소 갱신 기록의 10월 7일 항목은 원고 3편 철회, 14편 수정, 인용 갱신 13편, Lean 형식화 6건 추가를 적고, 상위 결과 719건 중 300건이 형식화됐다고 밝힌다. 철회 사유는 하나의 부호 오류가 안정화 대각합 상쇄 논증을 무너뜨렸고, 그 구성을 쓴 두 편이 함께 무효가 됐기 때문이다([GitHub history.md](https://raw.githubusercontent.com/openai/math/main/history.md)). Quanta Magazine은 철회된 3편이 모두 대수기하 분야이며 "빠진 마이너스 부호" 때문이라고 전했다([Quanta Magazine](https://www.quantamagazine.org/updates/transformation/)).

형식화 비율은 세는 기준에 따라 다르게 보도됐다. Decrypt는 저장소의 형식화 목록을 근거로 722편 중 162편만 주 결과가 컴퓨터로 검사됐다고 썼고([Decrypt](https://decrypt.co/380366/openai-secret-ai-model-cracked-hundreds-math-problems-one-prompt)), OpenAI 쪽 수치는 "상위 결과" 기준 42%다. 두 수치는 분모가 다르므로 직접 비교할 수 없다. 한국어 기술 블로그 braindetox.kr도 722·719·372라는 숫자가 각각 무엇을 세는지, Lean 링크가 결과군의 모든 정리를 덮는지는 별도 확인이 필요하다는 점을 정리했다([braindetox.kr](https://braindetox.kr/posts/openai_722_math_research_manuscripts_2026.html)).

Lean 증명이 있다고 끝은 아니다. Quanta는 Lean 형식화 전문가 Johan Commelin의 말을 빌려 "일부 형식화는 논문의 주장보다 약한 명제를 증명하는 것으로 보인다"고 전했고, "Lean 증명의 존재가 최종 판단은 아니다"라고 썼다([Quanta Magazine](https://www.quantamagazine.org/updates/transformation/)). Thomas Hales는 10월 9일 Terence Tao 블로그의 기고에서 "Lean 증명은 커널이 검사하기 전에는 믿어선 안 되며", 커널을 통과했더라도 Lean 명제가 의도한 수학과 일치하는지 "사람이 감사(audit)하기 전에는 받아들이면 안 된다"고 썼다. 그는 2026년 여름 Lean 커널에서 발견돼 수정된 건전성 버그 사례도 들었다([Terence Tao 블로그](https://terrytao.wordpress.com/2026/10/09/what-mathematicians-should-know-about-the-lean-theorem-proverquestions-of-reliability-and-ai/)). OpenAI 개발자 포럼에는 제타 함수 결과의 Lean 정리를 비교기(comparator) 설정으로 다시 돌려 통과했다는 보고가 올라왔지만, 신원이 확인되지 않은 이용자의 1회 실행 결과이며 "논문이 아니라 Lean 증명"만 검사했다는 단서가 붙어 있다([OpenAI Developer Community](https://community.openai.com/t/first-look-at-mathematics-manuscripts-from-an-internal-frontier-model-at-openai/1403886)).

## 화제의 주장: 제타 함수 영점과 행렬곱 지수

가장 많이 회자된 결과는 결과군 003 "준 리만 가설(quasi-Riemann hypothesis)"이다. 저장소 목록에 따르면 9월 30일자 원고는 리만 제타 함수를 포함한 모든 Dirichlet L-함수와 Q(√−3) 위의 유한 차수 Hecke L-함수가 반평면 Re s > 7/8에서 영점이 없다고 주장하고(s = 1의 극은 허용), 10월 5일자 동반 원고는 Re s > 11/12에 대한 다른 증명을 준다([GitHub CONTENTS.md](https://github.com/openai/math/blob/main/CONTENTS.md)). Lean 형식화 범위 문서는 7/8 경계가 제타 함수와 모든 Dirichlet L-함수에 대해 형식화됐고, 논문 뒷부분의 응용은 포함되지 않았다고 적는다([GitHub lean/docs/003.md](https://raw.githubusercontent.com/openai/math/main/lean/docs/003.md)). 리만 가설은 모든 비자명 영점이 Re s = 1/2 위에 있다는 주장이므로, 7/8은 그와 거리가 멀다. Decrypt는 722편 가운데 이 결과만이 "중대한 돌파구로 볼 만한 유일한 문제"라고 평가했다([Decrypt](https://decrypt.co/380366/openai-secret-ai-model-cracked-hundreds-math-problems-one-prompt)).

행렬곱 지수는 결과군 107이다. 10월 2일자 원고 "An Upper Bound of 9/4 for the Matrix Multiplication Exponent"는 복소수 위에서 ω ≤ 9/4를 주장하고, 9월 24일자 보조 원고는 표수 0인 모든 체에서 ω < 2.258을 다룬다. Lean 범위 문서는 ω(ℂ) ≤ 9/4와 함께 모든 체에서 ω < 2.371054886006746을 형식화했다고 적으면서, 이것이 "비트 복잡도나 실용적 교차 크기가 아니라 산술 복잡도에 관한 결과"라고 못 박는다([GitHub lean/docs/107.md](https://github.com/openai/math/blob/main/lean/docs/107.md)). 지수의 상한이므로 값이 작을수록 강한 결과이며, 9/4 = 2.25는 그동안 알려진 2.37 안팎의 상한보다 눈에 띄게 낮다. Zvi Mowshowitz는 Steven Strogatz의 X 게시글("종전 세계 기록은 2.37 정도")을 인용하면서도 "실제로 더 빠른 시나리오는 아직 찾지 못했다"고 덧붙였다([Zvi Mowshowitz](https://thezvi.substack.com/p/new-math-from-openai)). 이 주장도 외부 검토가 아니라 저장소 안의 Lean 검사만 거친 상태다.

## 독립 검토와 수학계 반응

OpenAI의 AI 수학 결과를 다룬 독립 감사 논문으로는 arXiv 2608.14673 "A Human Audit of OpenAI's AI-Generated Mathematical Proofs"(Mikołaj Sienicki·Krzysztof Sienicki, 9월 9일 v3)가 있다. 다만 이 논문이 다루는 것은 이번 722편이 아니라 OpenAI가 8월 1일 발표한 결과 10건이다. 18건의 장별 검토를 살핀 결과 주 결과에서 확정된 실질적 오류는 남아 있지 않지만 검토 깊이가 고르지 않고 일부 의존 관계는 부분적으로만 점검됐으며, 신뢰는 "형식 검사, 인간의 재구성, 독립적인 수학적 활용, 그리고 증명과 검토 모두의 오류를 고칠 수 있는 공개 기록" 위에 세워야 한다고 결론짓는다([arXiv](https://arxiv.org/abs/2608.14673)). 10월 6일 공개분에 대한 같은 수준의 감사는 아직 없다.

자문기구 AGMAI(Timothy Gowers, Edward Witten, Martin Hairer, Melanie Matchett Wood 등 9명)는 10월 6일 성명에서 이번 공개를 "인간의 이해와 수학 지식으로의 편입 과정의 완성이 아니라 시작"이라고 규정하고, 자신들의 조언이 결과나 "OpenAI가 결과를 얻은 과정에 대한 보증"은 아니라고 선을 그었다([AGMAI](https://agmai.org/)). TechCrunch는 AGMAI의 9월 29일 권고 첫 항목이 "독점 모델로 고급 수학 문제를 시험하지 말라"였는데 OpenAI가 이를 따르지 않았고, 추론 과정(chain of thought)을 공개한 원고도 719편 중 10편뿐이라고 짚었다. Wood는 TechCrunch에 "공개 시점에는 인간의 이해가 없으며, 이제 작업이 시작된다"고 말했다([TechCrunch](https://techcrunch.com/2026/10/08/openais-math-solutions-arent-meeting-the-fields-standards-yet/)).

Terence Tao는 공개 당일 Mathstodon에 4편짜리 글을 올려 "문제들이 분야 자체에는 관심 없는 AI 프롬프터들에 의해 자율적으로 풀리고 있다"며 "열린 문제의 해답이 지속 불가능한 방식으로 대규모로 수확되고 있다"고 썼다([Terence Tao, Mathstodon](https://mathstodon.xyz/@tao/117395267721642920)). Association for Human Mathematics(AHM)는 10월 7일 Tao 블로그에 재게시된 성명에서 700편 넘는 파일을 한꺼번에 푼 것은 "학문이 아니라 힘의 과시"라며 수학자들에게 OpenAI와의 협력을 중단하라고 촉구했다([Terence Tao 블로그](https://terrytao.wordpress.com/2026/10/07/ahm-statement-on-openais-october-6-release-of-mathematical-documents/)). 반면 MIT의 Andrew Sutherland는 "모델이 공개돼 다른 사람이 결과를 재현할 수 있기 전까지는 단일 에이전트로 한 번에 풀었다는 주장은 검증되지 않은 것으로 봐야 한다"며 "영수증을 요구해야 한다"고 했고, 토론토대의 Daniel Litt는 답을 숨길 이유가 없다며 "수학에 좋은 일"이 될 것이라고 봤다([Scientific American](https://www.scientificamerican.com/article/openai-unleashes-hundreds-more-math-results-upon-a-field-already-in-shock/)). Quanta는 Jeremy Avigad의 "OpenAI 공개에 중대한 진전이 포함된 것은 분명하다"는 평가와 Litt의 "현 단계에서는 '연구 발견' 또는 '원자료'에 가깝다"는 말을 함께 실었다([Quanta Magazine](https://www.quantamagazine.org/updates/transformation/)).

## OpenAI의 다음 계획

OpenAI는 공식 글에서 "AI가 만든 주요 결과의 이해를 둘러싼 워크숍, 학회, 특별 프로그램을 연이어 지원하겠다"며 "곧 더 알리겠다"고 했고, 과학자들에게 최첨단 역량을 직접 주기 위해 "이 결과를 만든 모델을 책임 있게 공개하기 위해 작업 중"이라고 밝혔다. 모델 이름과 공개 시점은 없다([OpenAI](https://openai.com/index/sharing-ai-progress-in-mathematics/)). Quanta는 OpenAI가 이름 없는 내부 모델을 "안전하다고 판단하면 가까운 시일 안에" 공개할 뜻이라고 전했다([Quanta Magazine](https://www.quantamagazine.org/updates/transformation/)).

워크숍 지원은 열흘 뒤 형태를 갖췄다. Simons Foundation은 10월 15일 Anthropic·OpenAI와 함께 총 1,500만 달러 규모의 "AI Initiative for Mathematicians"를 발표했다. 재단이 공모를 통해 기금을 관리·배분하고, 최근의 AI 보조 결과를 평가하고 새 도구를 배우며 공동 기준을 만드는 워크숍과 사업을 지원하며, 두 회사는 재단 지원 연구자에게 AI 도구와 연산 자원을 제공한다([Simons Foundation](https://www.simonsfoundation.org/news/simons-foundation-launches-15m-effort-to-help-mathematicians-navigate-ai-era/)). Euronews는 이 가운데 OpenAI 몫이 500만 달러이며, OpenAI가 "최근 발표한 결과"를 수학자들이 검토하고 발전시키도록 돕는 것이 목적이라고 보도했다([Euronews](https://www.euronews.com/2026/10/16/openai-tries-to-solve-mathematician-backlash-problem-by-pledging-5-million-to-math-foundat)).

## 의미

이번 공개의 무게는 722라는 숫자보다 검증 구조에 있다. OpenAI는 자신이 만든 Lean 라이브러리와 비교기, 버전 기록을 함께 올려 "확인 가능한 공개"의 틀을 제시했지만, 그 안에서 형식화된 것은 상위 결과의 절반이 안 되고, 형식화된 것조차 명제가 논문의 주장과 일치하는지는 사람이 확인해야 한다. 첫 24시간 안에 부호 오류 하나로 3편이 무너진 사실은 README의 "문제가 있을 수 있다"는 경고가 의례적 문구가 아님을 보여 준다. 모델이 공개되지 않은 이상 외부에서 재현할 길은 없고, 검토 비용은 수학계가 떠안는다. Simons Foundation 기금은 그 비용의 일부를 OpenAI와 Anthropic이 부담하겠다는 신호다.

## 확인할 점

- OpenAI 공식 글(openai.com)은 자동화 도구 접근을 차단해 본문은 Internet Archive 사본과 보도로 대조했다. 원문 링크는 브라우저로 직접 확인해야 한다.
- 형식화 비율은 출처마다 다르다. 저장소 갱신 기록은 상위 결과 719건 중 300건(약 42%), Decrypt는 형식화 목록 기준 722편 중 162편, Quanta 10월 6일자는 "약 절반"이라고 썼다. 분모가 달라 어느 하나로 단정하지 않았다.
- 원고 수는 공개 당시 722편, 10월 7일 철회 뒤 719편이다. "377개 주장"(Quanta)과 "372개 결과군"(README)의 차이는 원문에서 설명되지 않았다.
- 제타 함수 결과의 Lean 검사는 OpenAI 저장소의 자체 검사와 신원 미확인 포럼 이용자의 재실행 보고뿐이며, 수학자의 공개 검토 결과는 확인되지 않았다. 행렬곱 9/4 상한도 마찬가지다.
- arXiv 2608.14673은 8월 1일 발표분 10건에 대한 감사이며 10월 6일 공개분을 다루지 않는다. 10월 공개분에 대한 독립 감사 논문은 찾지 못했다.
- 모델 공개 시점, 워크숍 일정, Simons Foundation 공모 마감일은 모두 발표되지 않았다.
- DataCamp 기사에 실린 Dana Moshkovitz 등의 발언과 Tristan Buckmaster의 Navier-Stokes 관련 문제 제기는 원 발언 출처를 직접 확인하지 못해 본문에서 뺐다.

## 출처

- [Sharing AI progress in mathematics — OpenAI](https://openai.com/index/sharing-ai-progress-in-mathematics/)
- [openai/math README — GitHub](https://github.com/openai/math)
- [openai/math history.md — GitHub](https://raw.githubusercontent.com/openai/math/main/history.md)
- [openai/math CONTENTS.md — GitHub](https://github.com/openai/math/blob/main/CONTENTS.md)
- [openai/math lean/docs/003.md(준 리만 가설 형식화 범위) — GitHub](https://raw.githubusercontent.com/openai/math/main/lean/docs/003.md)
- [openai/math lean/docs/107.md(행렬곱 지수 형식화 범위) — GitHub](https://github.com/openai/math/blob/main/lean/docs/107.md)
- [A Human Audit of OpenAI's AI-Generated Mathematical Proofs — arXiv](https://arxiv.org/abs/2608.14673)
- [First look at mathematics manuscripts from an internal frontier model at OpenAI — OpenAI Developer Community](https://community.openai.com/t/first-look-at-mathematics-manuscripts-from-an-internal-frontier-model-at-openai/1403886)
- [On OpenAI's Release of Mathematical Results — AGMAI](https://agmai.org/)
- [OpenAI's math solutions aren't meeting the field's standards yet — TechCrunch](https://techcrunch.com/2026/10/08/openais-math-solutions-arent-meeting-the-fields-standards-yet/)
- [Transformation(Deluge of 377 OpenAI proofs / Cracks appear in OpenAI's wall of proofs) — Quanta Magazine](https://www.quantamagazine.org/updates/transformation/)
- [OpenAI unleashes hundreds more math results upon a field already in shock — Scientific American](https://www.scientificamerican.com/article/openai-unleashes-hundreds-more-math-results-upon-a-field-already-in-shock/)
- [OpenAI Says a Secret AI Model Cracked Hundreds of Open Math Problems in One Prompt — Decrypt](https://decrypt.co/380366/openai-secret-ai-model-cracked-hundreds-math-problems-one-prompt)
- [In traditional mathematics (or "Math 1.0")… — Terence Tao, Mathstodon](https://mathstodon.xyz/@tao/117395267721642920)
- [AHM Statement on OpenAI's October 6 Release of Mathematical Documents — Terence Tao 블로그](https://terrytao.wordpress.com/2026/10/07/ahm-statement-on-openais-october-6-release-of-mathematical-documents/)
- [What mathematicians should know about the Lean theorem prover: questions of reliability and AI — Thomas Hales, Terence Tao 블로그](https://terrytao.wordpress.com/2026/10/09/what-mathematicians-should-know-about-the-lean-theorem-proverquestions-of-reliability-and-ai/)
- [Simons Foundation Launches $15M Effort To Help Mathematicians Navigate AI Era — Simons Foundation](https://www.simonsfoundation.org/news/simons-foundation-launches-15m-effort-to-help-mathematicians-navigate-ai-era/)
- [OpenAI tries to solve mathematician backlash problem by pledging $5 million to math foundation — Euronews](https://www.euronews.com/2026/10/16/openai-tries-to-solve-mathematician-backlash-problem-by-pledging-5-million-to-math-foundat)
- [New Math from OpenAI — Zvi Mowshowitz](https://thezvi.substack.com/p/new-math-from-openai)
- [OpenAI 수학 원고 722편은 무엇을 세는 숫자인가 — braindetox.kr](https://braindetox.kr/posts/openai_722_math_research_manuscripts_2026.html)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
