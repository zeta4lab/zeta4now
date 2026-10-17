---
title: "GraphRAG '정확도 3배'는 벤더 수치…독립 벤치마크는 그래프 이득을 멀티홉·요약 +3~13pt로 좁히고 단순 질의는 벡터 RAG 우세, 운영 성과를 직접 공개한 기업은 LinkedIn '해결 시간 -28.6%' 하나"
slug: 2026-10-17-graphrag-vendor-claims-vs-independent-benchmarks
topic: ai-data-engineering
published_at: 2026-10-17T23:35:00+09:00
tags:
  - 그래프DB
  - GraphRAG
  - RAG
  - 지식그래프
  - 벤치마크
  - Neo4j
  - Microsoft
summary: "AI에 그래프 DB가 필요하다는 주장의 근거를 2026년 10월 시점에서 추적했다. 도입 기업이 운영 기간과 비즈니스 지표를 함께 1차 자료로 공개한 GraphRAG 사례는 LinkedIn 고객지원(약 6개월 운영, 이슈 해결 시간 중앙값 -28.6%) 하나에 가깝고, Klarna·Trend Micro 등 나머지는 Neo4j·AWS 고객 사례 채널을 거친 수치다. 벤더 벤치마크는 '+30pt', '3배'를 말하지만 2025~2026년 독립 평가는 그래프 이득을 멀티홉·전역 요약 질의의 +3~13pt로 좁히고, 단순 사실 질의에서는 벡터 RAG가 동급 또는 우세하며, 인덱싱 시간 41~57배, 질의당 토큰 377배의 비용을 측정했다. LLM 판정 편향을 보정하면 LightRAG의 승률은 66.7%에서 39.1%로 역전된다. 그래프 DB 시리즈 1편."
generated_by: claude
model: claude-fable-5-1
---

# GraphRAG '정확도 3배'는 벤더 수치…독립 벤치마크는 그래프 이득을 멀티홉·요약 +3~13pt로 좁히고 단순 질의는 벡터 RAG 우세, 운영 성과를 직접 공개한 기업은 LinkedIn '해결 시간 -28.6%' 하나

## 한눈에 보기

- "AI에는 그래프 DB가 필요하다"는 말이 2024년 Microsoft GraphRAG 공개 이후 벤더 메시지의 중심이 됐다. 이 시리즈는 그 말의 근거를 2026년 10월 시점에서 벤더 주장, 당사자 공개, 독립 측정으로 나눠 추적한다. 1편은 지식그래프 기반 검색증강(GraphRAG), 2편은 AI 에이전트 메모리, 3편은 사기 탐지·보안·추천과 그래프 DB 시장을 다룬다.
- 도입 기업이 "얼마나 오래 운영했고 무엇이 얼마나 좋아졌는가"를 스스로 밝힌 GraphRAG 사례는 LinkedIn 고객지원이 사실상 유일하다. 2024년 SIGIR 논문은 약 6개월 운영 뒤 이슈당 해결 시간 중앙값이 28.6% 줄었다고 보고했다. 다만 어떤 그래프 DB 제품을 썼는지는 밝히지 않았다.
- Klarna, Trend Micro, Cedars-Sinai 같은 유명 사례의 수치는 Neo4j, AWS, Memgraph의 고객 사례 채널을 거쳤다. 같은 Trend Micro 사례가 당사자 인용에서는 "답변 품질 +20%", AWS 임원 발언에서는 "정확도 70%→90%"로 달라지고, Memgraph 블로그는 Cedars-Sinai 논문에 없는 "94.2%"를 적었다.
- 벤더 벤치마크는 크다. Writer는 86.31% vs 75.89%, AWS 블로그의 Lettria는 80% vs 50.83%, Neo4j 후원 연구는 "80% 더 진실하다"고 썼다. 독립 측정은 다르다. Han 등 12인의 통일 프로토콜 평가에서 Natural Questions F1은 벡터 RAG 64.78 vs Microsoft GraphRAG 63.01이었고, 그래프는 멀티홉에서 1.6~3.0점만 앞섰다. 그래프 구축 시간은 RAG의 41~57배였다.
- ICLR 2026에 실린 GraphRAG-Bench는 "단순 사실 검색에서는 기본 RAG가 GraphRAG와 비슷하거나 더 낫다"를 첫 관찰로 두고, 복잡 추론과 요약에서만 그래프가 10~13점 앞선다고 측정했다. 질의당 프롬프트 토큰은 기본 RAG 879개 vs Microsoft GraphRAG 글로벌 검색 331,375개였다.
- 평가 방법 자체가 승률을 만든다. LLM 판정의 길이·위치 편향을 제거하면 LightRAG의 기본 RAG 대비 승률은 66.70%에서 39.06%로 떨어져 역전된다. Microsoft도 2024년 11월 기존 GraphRAG의 인덱싱 비용이 "일부 사용자에게는 감당하기 어려울 수 있다"고 인정하며 비용을 0.1%로 낮춘 LazyGraphRAG를 냈다.

## 운영 성과를 1차 자료로 공개한 곳: LinkedIn 하나

GraphRAG는 그래프 DB가 AI에서 가장 많이 거론되는 활용처지만, 도입 기업이 운영 기간과 비즈니스 지표를 함께 밝힌 사례는 드물다. 두 조건을 모두 충족하는 것은 LinkedIn이 2024년 4월 공개하고 SIGIR 2024에 실은 논문이다. 과거 고객지원 티켓으로 지식그래프를 만들고 각 이슈의 내부 구조와 이슈 간 연결을 보존한 뒤, 질의가 들어오면 관련 서브그래프를 꺼내 답을 생성하는 구조다. 오프라인 평가에서 MRR이 베이스라인보다 77.6% 높았고 BLEU는 0.32 올랐으며, 고객지원팀에 약 6개월 배포한 결과 이슈당 해결 시간 중앙값이 28.6% 줄었다([arXiv 2404.17723](https://arxiv.org/abs/2404.17723)). 초록에 그래프 DB 제품명은 없다. 이 사례는 "상용 그래프 DB의 효용"이 아니라 "지식그래프 구조의 효용"을 보여 주는 근거로 읽어야 한다.

## 벤더 채널을 거친 사례들

나머지 유명 사례는 벤더가 공개했다. Klarna의 내부 어시스턴트 Kiki는 Neo4j 지식그래프에 OpenAI 모델을 연결해 2023년 6월 출시 뒤 25만 건 이상의 질문에 답하고 직원 85%가 쓰며 SaaS 도구 1,200개 이상을 없앴다고 한다. 이 수치는 CEO 세바스티안 시미아트코프스키의 발언을 Neo4j가 고객 사례로 옮긴 것이고, 절감된 시간은 정량화되지 않았다([Neo4j](https://neo4j.com/customer-stories/klarna/)).

Trend Micro의 보안 플랫폼 Vision One에 붙은 "Companion"은 Amazon Neptune을 지식그래프 겸 경험 계층으로 쓰고 Bedrock의 Claude로 대화에서 엔터티와 관계를 추출한다. AWS 고객 사례에서 당사자인 선임 아키텍트는 "답변 품질 20% 개선"을 말했고 비용과 지연 수치는 없다([AWS](https://aws.amazon.com/solutions/case-studies/trendmicro/)). 같은 사례를 AWS 임원 브래드 비비는 "정확도 70%에서 90%로"라고 말했는데, 이는 AWS 측 발언이고 지표의 정의도 다르다([The Stack](https://www.thestack.technology/amazon-neptune-ai-accuracy-graphrag-brad-bebee/)).

벤더 재인용에서 수치가 바뀌는 사례도 있다. Cedars-Sinai의 알츠하이머 지식그래프 AlzKB와 그 위의 ESCARGOT(Memgraph 기반) 논문은 개방형 2-hop 질문에서 정확도 85.8%로 기본 RAG 23.1%를 크게 앞섰지만, 참·거짓 2-hop 질문에서는 RAG 75.6%가 ESCARGOT 74.1%보다 높았다([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11796095/)). Memgraph 블로그는 이 사례를 "94.2% vs ChatGPT 49.9%"로 소개했는데, 이 숫자는 논문에 없다([Memgraph](https://memgraph.com/blog/graphrag-vs-standard-rag-success-stories)).

Uber, Netflix, Cisco 같은 이름은 아키텍처만 공개했다. Uber는 2025년 GraphSummit NYC에서 Neo4j 기반 제품 설정 지식그래프와 GraphRAG·MCP 통합을 발표했지만 수치와 프로덕션 여부는 없다([Neo4j](https://neo4j.com/videos/graphsummit-nyc-25-ubers-config-knowledge-graph-genai-with-graphrag-and-mcp/)). Netflix의 2025년 지식그래프 콘퍼런스 세션은 LLM으로 그래프를 구축하는 이야기여서, 그래프로 LLM을 보강하는 GraphRAG와 방향이 반대다([KGC 2025](https://watch.knowledgegraph.tech/videos/day-4-auditorium-scaling-netflix-entertainment-knowledge-graphs-with-llms-made-with-clipchamp-720p)). Cisco의 고객지원 GraphRAG 발표는 2026년 11월 예정이라 아직 결과가 없다([Neo4j](https://neo4j.com/videos/nodes-ai-2026-the-graphrag-system-that-asks-back-intelligent-probing-with-contextual-answers/)). SAP는 레거시 코드 마이그레이션용 지식그래프로 벡터 단독 대비 최대 15% 개선을 보고했지만 오프라인 LLM 판정 평가다([arXiv 2507.03226](https://arxiv.org/abs/2507.03226v3)). Microsoft GraphRAG를 프로덕션에 채택했다고 공개한 이름 있는 기업은 찾지 못했다.

| 사례 | 그래프 저장소 | 보고된 성과 | 근거 등급 |
|---|---|---|---|
| LinkedIn 고객지원 | 자체 구현(제품명 미공개) | 해결 시간 중앙값 -28.6%, MRR +77.6% | 1차 논문, 약 6개월 운영 |
| Klarna Kiki | Neo4j | 25만+ 질문, 직원 85% 사용 | CEO 발언을 Neo4j가 재인용 |
| Trend Micro Companion | Amazon Neptune | 답변 품질 +20% | AWS 고객 사례, 당사자 인용 |
| Cedars-Sinai ESCARGOT | Memgraph | 개방형 2-hop 23.1%→85.8%, 참·거짓 2-hop은 RAG 우세 | 1차 논문, 연구 환경 |
| SAP 코드 마이그레이션 | 미공개 | 벡터 대비 최대 +15% | 1차 논문, 오프라인 평가 |
| Uber, Netflix, Cisco | Neo4j, 자체 | 수치 없음 | 벤더 행사 발표 |

## 벤더 벤치마크: +30포인트와 3배

벤더가 낸 비교 수치는 큼직하다. Writer는 자체 평가에서 RobustQA 기준 자사 지식그래프 방식 86.31% 대비 LlamaIndex와 Weaviate 조합 75.89%를 보고했다([Writer](https://writer.com/blog/rag-benchmark/)). AWS 머신러닝 블로그의 Lettria 사례는 전체 정답률 GraphRAG 80% vs 벡터 RAG 50.83%를 내놓았지만, 제목의 "최대 35%"가 무엇을 가리키는지 정의하지 않았고 질문 수와 채점자도 밝히지 않았다([AWS](https://aws.amazon.com/blogs/machine-learning/improving-retrieval-augmented-generation-accuracy-with-graphrag/)). Neo4j가 후원한 NICD 연구는 진실성 점수 63 vs 35를 "80% 더 진실하다"로 표현했고 한계 절이 없다([Neo4j](https://neo4j.com/blog/agentic-ai/study-graphrag-ai-agents-80-percent-more-truthful/)). 자주 인용되는 data.world의 "지식그래프가 LLM의 SQL 정확도를 3배 높인다"는 약 40개 질문에 기반한다([data.world](https://medium.com/datadotworld/benchmark-report-the-role-of-large-language-models-in-enterprise-sql-database-queries-d1a282b4669d)).

## 독립 벤치마크: 멀티홉에서만, 비용은 수십 배

독립 평가의 그림은 다르다. 미시간주립대와 Meta 등 12인의 Han 등은 2025년 2월 통일 프로토콜로 벡터 RAG와 Microsoft GraphRAG, 지식그래프 기반 GraphRAG를 비교했다. Natural Questions에서 F1은 RAG 64.78 vs GraphRAG 로컬 검색 63.01로 벡터 RAG가 앞섰고, HotpotQA에서는 그래프 계열이 1.6~3.0점 우세했으며, 답이 없는 질의에서는 RAG가 96.01로 올바르게 거절한 반면 GraphRAG 로컬은 80.07, 글로벌은 19.27로 무너졌다. 그래프 구축 시간은 RAG 135초 vs 5,560~7,702초로 41~57배였고, NQ에서 정답 문자열이 검색 컨텍스트에 들어 있는 비율은 RAG 86.70% vs GraphRAG 로컬 42.20%에 그쳐 LLM이 만든 그래프가 원문 정보를 많이 잃는다는 점이 드러났다([arXiv 2502.11371](https://arxiv.org/html/2502.11371v3)).

ICLR 2026에 채택된 GraphRAG-Bench는 "단순 사실 검색 과제에서는 기본 RAG가 GraphRAG와 비슷하거나 더 낫다"를 첫 관찰로 적었다. 그래프가 앞선 곳은 복잡 추론과 문맥 요약이다. 복잡 추론에서 HippoRAG2는 53.38로 reranker를 붙인 RAG 42.93보다 높았고 요약에서도 10~13점 차이가 났다. 비용 차이는 극단적이다. 질의당 평균 프롬프트 토큰이 기본 RAG 879개 vs Microsoft GraphRAG 글로벌 검색 331,375개로 약 377배였다([arXiv 2506.05690](https://arxiv.org/html/2506.05690v3)).

보고된 승률이 평가 방법의 산물이라는 감사도 나왔다. Zeng 등은 기존 GraphRAG 평가가 코퍼스와 무관한 질문을 만들고 LLM 판정의 위치·길이 편향을 방치했다고 지적했다. 편향을 제거하자 LightRAG의 기본 RAG 대비 승률은 66.70%에서 39.06%로 떨어져 손익분기점 아래로 내려갔다. 같은 방법의 두 인스턴스를 기존 프레임워크로 비교했을 때 90% 대 10%라는 가짜 격차가 나올 정도였다([arXiv 2506.06331](https://arxiv.org/html/2506.06331v2)).

Microsoft 자신도 비용을 인정했다. 2024년 11월 공개한 LazyGraphRAG 글은 기존 GraphRAG의 선행 인덱싱 비용이 "일부 사용자에게는 감당하기 어려울 수 있다"고 쓰고, 인덱싱 비용을 벡터 RAG와 같은 수준, 즉 기존 GraphRAG의 0.1%로 낮춘 대안을 내놓았다([Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag/)). 2026년 9월의 EffiRAG는 그래프를 생성 입력이 아니라 증거 위치 탐색에만 쓰면 LightRAG 대비 120문항에서 93승 7패를 거두며 총비용을 57% 줄일 수 있다고 보고하고, "구조는 유익하다고 가정하지 말고 비용 대비 정당화해야 한다"고 결론지었다([arXiv 2609.18099](https://arxiv.org/abs/2609.18099)). 반대 방향의 결과도 있다. 통신 규격 O-RAN 문서 벤치마크에서는 GraphRAG 변형이 벡터 RAG보다 사실 정확도 8%, 문맥 관련성 7% 앞섰다([arXiv 2507.03608](https://arxiv.org/html/2507.03608v1)).

## 한국 기업은 공개 근거가 없다

국내 대기업의 생성형 AI 사례에서 그래프 DB는 보이지 않는다. LG CNS의 사내 지식관리 서비스는 Azure OpenAI GPT-4에 질의 유사도 상위 5개 자료를 넘기는 벡터 유사도 방식이고([CIO Korea](https://www.cio.com/article/3507827/lg-cns-%EC%83%9D%EC%84%B1%ED%98%95-ai%EB%A1%9C-%EC%82%AC%EB%82%B4-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B0%BE%EB%8A%94-ai%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-km-%ED%98%81%EC%8B%A0.html)), SKT는 텔코 LLM과 RAG를 고객센터에 적용했으나 지식그래프 사용은 확인되지 않는다([SKT 뉴스룸](https://news.sktelecom.com/208493)). 네이버, 카카오, 삼성SDS는 한국어·영어 검색 모두에서 GraphRAG 프로덕션 근거를 찾지 못했다. 이는 "없다"가 아니라 "공개 근거를 찾지 못했다"로 읽어야 한다.

## 의미

- "그래프가 RAG 정확도를 3배 높인다"류의 수치는 전부 벤더 또는 벤더 후원 평가에서 나왔다. 독립 측정의 효과 크기는 멀티홉 +1.6~10점, 요약 +13점, 단순 질의 -1~-13점이며, 어느 쪽이 나오는지는 질의 유형이 결정한다.
- 비용은 정확도보다 격차가 크다. 구축 시간 41~57배, 질의당 토큰 377배는 Microsoft가 LazyGraphRAG를 낸 이유이기도 하다. 2026년 연구 흐름은 그래프를 "진실의 저장소"에서 "증거 위치를 찾는 가벼운 색인"으로 격하하는 쪽이다.
- 유일한 운영 1차 자료인 LinkedIn은 원천 데이터가 이미 구조화된 티켓이었다. LLM이 비정형 문서에서 즉석으로 그래프를 뽑는 경로와는 조건이 다르며, 이 차이가 시리즈 전체를 관통하는 변수다.
- 도입 전에 reranker와 반복 검색을 붙인 벡터 RAG를 먼저 측정하고, 질의 로그에서 멀티홉·전역 요약 질의의 비율이 유의미할 때만 그래프를 추가하는 것이 2026년 10월의 증거에 부합한다.

## 확인할 점

- LinkedIn 논문은 초록에 그래프 저장소 제품명이 없어 "상용 그래프 DB"의 효용 근거로는 쓸 수 없다.
- Trend Micro의 "20%"와 "70%→90%"는 지표 정의가 다른 두 발언이며 어느 쪽도 측정 방법이 공개되지 않았다.
- Han 등의 평가는 2025년 2월 시점 모델과 Microsoft GraphRAG 구현 기준이고, GraphRAG-Bench 수치는 논문 v3 기준이다. 이후 구현 개선이 격차를 줄였을 수 있다.
- Writer, Lettria, NICD, data.world 수치는 질문 수나 채점 방식이 비공개 또는 소규모여서 독립 재현이 확인되지 않았다.
- 한국 기업의 그래프 DB 미사용은 공개 자료 부재에 근거한 판단이며, 비공개 도입을 배제하지 못한다.

## 출처

- [Xu et al., Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering (arXiv 2404.17723, SIGIR 2024)](https://arxiv.org/abs/2404.17723)
- [Neo4j, Klarna customer story](https://neo4j.com/customer-stories/klarna/)
- [AWS, Trend Micro case study](https://aws.amazon.com/solutions/case-studies/trendmicro/)
- [The Stack, Amazon Neptune GM Brad Bebee on GraphRAG accuracy](https://www.thestack.technology/amazon-neptune-ai-accuracy-graphrag-brad-bebee/)
- [Matsumoto et al., ESCARGOT (Bioinformatics 2025, PMC11796095)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11796095/)
- [Memgraph, GraphRAG vs Standard RAG success stories](https://memgraph.com/blog/graphrag-vs-standard-rag-success-stories)
- [Neo4j, GraphSummit NYC 2025: Uber's Config Knowledge Graph](https://neo4j.com/videos/graphsummit-nyc-25-ubers-config-knowledge-graph-genai-with-graphrag-and-mcp/)
- [KGC 2025, Scaling Netflix Entertainment Knowledge Graphs with LLMs](https://watch.knowledgegraph.tech/videos/day-4-auditorium-scaling-netflix-entertainment-knowledge-graphs-with-llms-made-with-clipchamp-720p)
- [Neo4j, NODES AI 2026: Cisco session](https://neo4j.com/videos/nodes-ai-2026-the-graphrag-system-that-asks-back-intelligent-probing-with-contextual-answers/)
- [SAP, Knowledge graph for legacy code migration (arXiv 2507.03226)](https://arxiv.org/abs/2507.03226v3)
- [Writer, RAG benchmark](https://writer.com/blog/rag-benchmark/)
- [AWS ML Blog, Improving RAG accuracy with GraphRAG (Lettria)](https://aws.amazon.com/blogs/machine-learning/improving-retrieval-augmented-generation-accuracy-with-graphrag/)
- [Neo4j, Study: GraphRAG AI agents 80% more truthful (NICD)](https://neo4j.com/blog/agentic-ai/study-graphrag-ai-agents-80-percent-more-truthful/)
- [data.world, Benchmark report: LLMs in enterprise SQL database queries](https://medium.com/datadotworld/benchmark-report-the-role-of-large-language-models-in-enterprise-sql-database-queries-d1a282b4669d)
- [Han et al., RAG vs. GraphRAG: A Systematic Evaluation and Key Insights (arXiv 2502.11371 v3)](https://arxiv.org/html/2502.11371v3)
- [Xiang et al., GraphRAG-Bench (arXiv 2506.05690 v3, ICLR 2026)](https://arxiv.org/html/2506.05690v3)
- [Zeng et al., Unbiased evaluation of GraphRAG (arXiv 2506.06331 v2)](https://arxiv.org/html/2506.06331v2)
- [Microsoft Research, LazyGraphRAG (2024-11-25)](https://www.microsoft.com/en-us/research/blog/lazygraphrag/)
- [EffiRAG (arXiv 2609.18099, 2026-09)](https://arxiv.org/abs/2609.18099)
- [GraphRAG for O-RAN specifications (arXiv 2507.03608)](https://arxiv.org/html/2507.03608v1)
- [CIO Korea, LG CNS 생성형 AI 사내 KM 혁신](https://www.cio.com/article/3507827/lg-cns-%EC%83%9D%EC%84%B1%ED%98%95-ai%EB%A1%9C-%EC%82%AC%EB%82%B4-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B0%BE%EB%8A%94-ai%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-km-%ED%98%81%EC%8B%A0.html)
- [SKT 뉴스룸, 텔코 LLM 고객센터 적용](https://news.sktelecom.com/208493)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
