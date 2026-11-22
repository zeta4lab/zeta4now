---
title: 리만 가설의 증명은 기계가 확인했고, 설명은 아직 아무도 하지 못했다…AI가 '옳음'을 검사기에 넘기자 수학에 남은 일은 '이해'다
slug: 2026-11-22-riemann-hypothesis-claude-lean-correct-not-understood
topic: ai
published_at: 2026-11-22T13:37:00+09:00
summary: 앤트로픽 소속 수학자 레벤트 알푀게가 20일 Claude와 함께 리만 가설을 증명했다며 사람이 읽을 논문 없이 Lean 형식 증명만 공개했고, Lean·Mathlib 커뮤니티는 다음 날 증명이 옳다고 인증했다. 그러나 저자는 증명의 일부 분야에 통달하지 못했다고 썼고, 인증 성명은 새 아이디어를 설명하는 일을 앞으로의 과제로 남겼다. 이 글은 수학에서 '옳다'와 '이해했다'가 처음으로 갈라졌다고 본다. AI는 기계 검증기가 있는 곳에서 먼저 이기고, 사람에게 남는 일은 정답을 내는 것이 아니라 설명하는 것이다.
tags:
  - 리만 가설
  - Claude
  - 앤트로픽
  - Lean
  - 형식 검증
  - 수학
  - AI 연구
  - METR
generated_by: claude
model: claude-opus-5-5
---

# 리만 가설의 증명은 기계가 확인했고, 설명은 아직 아무도 하지 못했다…AI가 '옳음'을 검사기에 넘기자 수학에 남은 일은 '이해'다

> **이해관계 고지**: Zeta4 Now의 기사는 앤트로픽의 Claude로 초안을 작성하고 사람이 검토해 발행한다. 이 기사는 앤트로픽 소속 수학자가 Claude와 함께 낸 결과와, 앤트로픽 모델이 포함된 평가를 다룬다.

## 판단: 증명은 확인됐고, 이해는 아직이다

앤트로픽 소속 수학자 레벤트 알푀게는 20일 "Claude와 함께 작업해 리만 가설의 증명을 발견했다고 믿는다"고 밝혔다. 그는 이 방법이 일반화 리만 가설까지 확장되며 "Claude와 나는 가정 없이 논증을 형식화했다"고 썼다. 공개한 것은 4쪽짜리 소개 글과 증명 보조기 Lean으로 쓴 형식 증명뿐이다. 사람이 읽을 수 있는 논문은 없다([알푀게 소개 글](https://alpo.ge/remark.pdf)).

다음 날 Lean과 Mathlib 커뮤니티는 Lean FRO와 Mathlib 이니셔티브가 지지한 공동 성명에서 "리만 가설의 명제와 증명이 모두 옳음을 인증한다"고 했다. 1,700만 줄 분량의 증명은 두 개의 독립 도구로 Mathlib에 정의된 리만 가설 명제와 정확히 같은지 대조됐고, Lean 공식 커널과 서로 다른 언어로 만든 여러 검사기를 통과했다. 성명의 마지막 문장은 이렇다. "이 증명의 새로운 아이디어를 설명하는 데 도움이 될 수학계의 모든 활동을 기대한다"([Lean 커뮤니티](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)).

이 글의 판단은 세 가지다. **첫째, 수학에서 처음으로 '옳다'와 '이해했다'가 갈라졌다.** 167년 된 문제의 증명이 옳다는 판단은 이제 학술지 심사위원이 아니라 기계 검사기가 내렸고, 그 증명이 왜 성립하는지는 저자를 포함해 아직 아무도 설명하지 못했다. **둘째, 이것은 리만 가설만의 일이 아니다.** AI는 기계 검증기가 있는 분야에서 먼저, 그리고 빠르게 이기고 있다. **셋째, 그렇다면 사람에게 남는 일은 정답을 내는 것이 아니라 설명하는 것이다.** 같은 주 한국이 수능에서 AI가 정답을 대신 내는 일을 막느라 애쓴 것과 같은 질문이다. 세 가지 모두 해석이다.

## 저자도 통달하지 못한 증명

알푀게의 소개 글은 승리 선언이라기보다 고백에 가깝다. 그는 "이번에는 결승선 근처에서 Claude가 나를 훨씬 앞질렀다"고 썼다. 자신은 장난감 같은 설정에 대응하는 올바른 상황으로 방향을 잡았고, "그다음부터 Claude가 나를 경탄하게 했다"는 것이다. 그러면서 "나는 그 주변의 방대한 수학을 통달하기 전에 완결된 논증을 세상에 내놓고 있다"며 "고차 계수 군의 보형 형식에 통달하지 못했다"고 했다. 각주에는 Claude가 전문가인 부분은 Claude의 요약을 바꿔 말한 것이어서 "전혀 말이 안 될 수도 있다"며 사과하고, "Lean이면 모든 걸 밝히기에 충분할 것"이라고 적었다([알푀게 소개 글](https://alpo.ge/remark.pdf)).

논문을 내지 않은 이유도 같은 데 있다. 그는 형식화는 끝났고 충분히 자세하지만 읽을 수 없는 거대한 문서를 만드는 것은 일상적인 일이라며, "거대하고 읽을 수 없는 '슬롭'을 올리는 것은 분명히 부적절하므로 Lean만 공개하기로 했다"고 썼다. 재미 삼아 만들어 본 문서는 25만 쪽을 넘었다. 그는 "이 논증과 앞으로 나올 단순화를 이해하고 그 이해를 전하며, 제대로 글로 쓰기 위해 최선을 다하겠다"고 했다.

발표는 앤트로픽이 나스닥에 상장한 다음 날 나왔다. 알푀게는 "시점이 정말 끔찍하다"며, 일요일 밤 다리오 아모데이 CEO에게 발표할 수 있는지 물었고 "지켜야 할 제약이 있었다"고 썼다. 그는 "시점과 관련된 뻔한 냉소적 시각이 있지만 그것은 틀렸다"고 했다. 이 글은 그 해명을 그대로 전하고 의도를 판단하지 않는다.

## 확인은 기계가, 확인 작업도 AI가

검증의 사슬에도 사람은 드물다. MIT 수학자 앤드루 서덜랜드는 독립적으로 증명을 다시 빌드해 175,187개 모듈이 오류 없이 컴파일되고, 표준 공리 세 개 외에 다른 공리를 쓰지 않았으며, 네트워크를 끊은 환경에서 다시 만든 결과물이 공개본과 바이트 단위로 같다는 것을 확인했다. 그가 확인한 정리는 리만 가설과 디리클레 L-함수에 대한 일반화 리만 가설이다. 그의 검증 페이지 맨 위에는 "Claude Code로 실행한 검사"라고 적혀 있다([서덜랜드](https://math.mit.edu/~drew/grh/)). AI가 찾은 증명을 사람이 만든 검사기가 확인하고, 그 확인 작업을 다시 AI가 돌렸다.

서덜랜드는 사이언티픽아메리칸에 "내게 이것은 인간의 승리이고 축하할 날"이라면서도 "증명의 수학적 세부를 이해하려면 할 일이 많다"고 했다. 그는 "증명에서 가장 중요한 단계는 아마 생각하는 기계를 만든 것이었다"고 덧붙였다([사이언티픽아메리칸](https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/)). 테렌스 타오는 블로그에서 초기 분석으로는 이 증명이 "랑글랜즈 프로그램과 산술기하의 현대적 성과를 전력으로 쓰는 것 같다"며 "소화 과정에 시간이 걸릴 것"이라고 했고, "적어도 소통할 인간 저자는 있다"고 썼다([타오 블로그](https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/)).

이 글은 이 장면이 수학이라는 제도의 기본 가정을 바꾼다고 본다. 지금까지 증명이 옳다는 것은 전문가 몇 사람이 그것을 이해했다는 뜻이었다. 이해가 곧 검증이었다. 이번에는 둘이 분리됐다. 기계 검사기는 각 단계가 논리적으로 맞물린다는 것을 보증하지만, 왜 그 길이 통하는지는 말하지 않는다. 이는 해석이다.

## '해결'의 정의는 여전히 사람의 이해다

제도는 아직 이 분리를 받아들이지 않았다. 리만 가설에 100만 달러를 걸어 둔 클레이수학연구소는 해법을 검토하기 전에 세 조건을 요구한다. 적격 매체에 게재될 것, 게재 뒤 2년 이상 지날 것, 세계 수학계의 일반적 수용을 받을 것이다([클레이수학연구소](https://www.claymath.org/millennium-problems/rules/)). 학술지 게재도 수학계의 수용도 결국 사람들이 그 증명을 읽고 이해했다는 표시다. Lean 커뮤니티가 인증 기준으로 든 글도 "이것이 대응하는 문서에도 옳은 증명이 들어 있다는 뜻은 아니다"라고 선을 그었다([제나 프로젝트](https://xenaproject.wordpress.com/2026/11/12/and-the-proof-is-checked-in-lean/)).

같은 날 다른 증명도 나왔다. 스탠퍼드의 라비 바킬 교수는 박사후연구원 알레산드로 마술로가 12년에 걸쳐 쓴 일반화 리만 가설 증명을 공개하며 "모두 사람이 했고 AI는 없다"고 했다. TechCrunch는 "Lean으로 표현되지 않아서 증명이 맞는지 말하기 이르고, 누가 이해하는지는 더더욱 그렇다"고 썼다([TechCrunch](https://techcrunch.com/2026/11/20/ai-claimed-a-solution-to-the-167-year-old-riemann-hypothesis-and-a-human-did-too/)). 두 증명은 정반대 위치에 있다. 하나는 기계가 옳다고 확인했지만 사람이 설명하지 못했고, 다른 하나는 사람이 쓴 설명이지만 아직 아무도 옳다고 확인하지 못했다.

## 검증기가 있는 곳에서 먼저 진다

리만 가설은 하나의 사례다. 9월 OpenAI는 내부 모델이 3차원 나비에-스토크스 방정식의 유한시간 폭발을 외력이 있는 조건에서 증명했다고 발표했고 Lean으로 인증했다고 밝혔다([OpenAI 논문](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)). 외력을 둔 조건이 문제 문구의 허점이라는 비판도 나왔다. 석 달 사이 밀레니엄 문제 두 개에서 AI 쪽 결과가 나왔고, 두 경우 모두 기계 검증기가 있었다.

평가 기관 METR가 20일 낸 4분기 평가도 같은 방향을 가리킨다. METR는 AI가 절반의 확률로 끝낼 수 있는 과제의 길이가 전체적으로 약 3.61개월마다 두 배가 되는데, 자동으로 채점할 수 있는 과제만 따로 보면 약 1.65개월마다 두 배가 된다고 추정했다. METR는 후자의 수치에 다른 설명도 가능하다고 단서를 달았다. 반면 빠른 피드백이 없는 판단 과제에서는 "모든 공개 모델이 15분을 쓴 전문가의 추정 일치 수준에 아직 못 미친다"고 했다. 모델이 다른 모델의 결과를 채점하게 하면, 과제를 만든 모델이 비슷하거나 더 강할 때 점수를 부적절하게 높게 준다는 결과도 냈다([METR](https://metr.org/blog/2026-11-20-q4-2026-capability-update/)).

반도체 설계도 같다. OpenAI는 18일 자사 모델로 AMD 그래픽칩의 회로 설계 코드를 다시 써 플래그십 설계에서 기준선보다 최대 14% 개선했다고 밝혔다. 다시 쓴 코드마다 블록의 동작이 보존됐는지 시놉시스 도구로 검증했고, AMD는 일부 변경을 최근 제조에 넘긴 설계에 반영했다. OpenAI는 이 작업의 목적을 "신뢰할 수 있는 평가기에 모델 개발의 기반을 두는 것"이라고 했다([OpenAI](https://openai.com/index/advancing-chip-design-with-our-models/)). OpenAI는 AMD 주식을 살 수 있는 워런트를 갖고 있다.

이 글은 AI가 어떤 일을 먼저 대신하는지가 일의 난이도가 아니라 '검증기가 있느냐'로 정해진다고 본다. 수학의 Lean, 칩 설계의 동작 검증 도구, 소프트웨어의 테스트처럼 옳고 그름을 기계가 즉시 판정할 수 있는 곳에서는 AI가 스스로 시도하고 실패하고 고치는 회로를 사람보다 훨씬 빨리 돈다. 판정이 사람의 판단에 달린 곳에서는 그 회로가 돌지 않는다. 이는 해석이다.

## 한국에 남는 질문

9월 허준이 교수와 테렌스 타오를 포함한 필즈상 수상자들은 AI 업계가 수학 문제 풀이에 집중하는 것이 "수학의 본래 목적인 개념적 이해와 통찰을 훼손"할 수 있다고 경고했다([뉴시스](https://newsis.com/view/NISX20260912_0003786891)). 두 달 만에 그 경고는 구체적인 모습이 됐다. 정답은 나왔고, 개념적 이해는 뒤에 남았다.

같은 주 한국은 수능에서 AI가 정답을 대신 내는 것을 막는 데 국가의 힘을 쏟았다([관련 기사](https://now.zeta4.net/a/2026-11-19-ai-exam-cheating-after-the-exam)). 리만 가설의 일주일은 그 노력이 지키려는 것이 무엇인지 묻는다. 기계가 확인할 수 있는 정답을 사람이 혼자 내는 능력은 점점 AI가 더 잘하는 영역이 되고 있다. 사람의 몫으로 남는 것은 그 정답이 왜 맞는지 설명하고, 어떤 질문을 던질지 고르는 능력이다. 한국의 시험과 연구 평가가 여전히 정답의 산출을 재고 있다면, 그 평가는 AI가 가장 먼저 이기는 능력을 재고 있는 셈이다. 이는 해석이다.

## 확인하지 못한 것

- Lean 커뮤니티 성명이 인증한 것은 리만 가설이다. 디리클레 L-함수에 대한 일반화 리만 가설은 서덜랜드의 검증 페이지로 확인했고, 데데킨트·헤케·일반 보형 L-함수는 검사 대상이 아니었다.
- 사용한 Claude 모델의 이름은 공개되지 않았다. 알푀게의 소개 글에는 상장(IPO)이라는 단어가 없고, 상장과의 연결은 언론의 해석이다.
- 이 증명은 학술지 동료평가를 거치지 않았고, 클레이수학연구소의 공식 입장은 찾지 못했다. 네이처 등 일부 보도의 수학자 반응은 원문을 열지 못해 쓰지 않았다.
- 필즈상 수상자 성명의 원문은 열지 못해 보도로 확인했고, 구체적인 요구 사항은 쓰지 않았다. 허준이 교수 등 국내 수학자의 이번 증명에 대한 반응은 찾지 못했다.
- METR의 1.65개월은 자동 채점 가능한 과제 부분집합의 추정치이며 신뢰구간이 넓다. OpenAI의 칩 설계 결과와 나비에-스토크스 결과는 회사 발표에 기댄다.

## 출처

- [A remark on the Riemann Hypothesis — 레벤트 알푀게 (2026-11-20)](https://alpo.ge/remark.pdf)
- [Joint statement on the Riemann Hypothesis — Lean·Mathlib 커뮤니티 (2026-11-21)](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)
- [Checking the RH/GRH formalization — 앤드루 서덜랜드(MIT)](https://math.mit.edu/~drew/grh/)
- [And the proof is checked in Lean — 제나 프로젝트 (2026-11-12)](https://xenaproject.wordpress.com/2026/11/12/and-the-proof-is-checked-in-lean/)
- [Anthropic mathematician proves Riemann hypothesis — 사이언티픽아메리칸 (2026-11-20)](https://www.scientificamerican.com/article/anthropic-mathematician-claims-to-prove-riemann-hypothesis-most-famous-problem-in-all-of-math/)
- [Unforced Euler singularity, unforced Navier-Stokes singularity, and the generalized Riemann hypothesis — 테렌스 타오 (2026-11-20)](https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/)
- [AI claimed a solution to the 167-year-old Riemann hypothesis, and a human did too — TechCrunch (2026-11-20)](https://techcrunch.com/2026/11/20/ai-claimed-a-solution-to-the-167-year-old-riemann-hypothesis-and-a-human-did-too/)
- [Millennium Prize Problems rules — 클레이수학연구소](https://www.claymath.org/millennium-problems/rules/)
- [Q4 2026 capability update — METR (2026-11-20)](https://metr.org/blog/2026-11-20-q4-2026-capability-update/)
- [Advancing chip design with our models — OpenAI (2026-11-18)](https://openai.com/index/advancing-chip-design-with-our-models/)
- [Navier-Stokes 논문 — OpenAI (2026-09)](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)
- [필즈상 수상자들 "인간 역할 위협" 경고 — 뉴시스 (2026-09-12)](https://newsis.com/view/NISX20260912_0003786891)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
