---
title: "그래프 DB가 값을 한 곳은 사기 탐지와 클라우드 보안…Wiz는 Neptune에 수천억 관계, Capitec은 하루 350만 건, 그러나 TigerGraph 430→130명·Kuzu는 Apple 인수 뒤 아카이브, PostgreSQL 19가 그래프 질의를 흡수"
slug: 2026-10-17-graph-db-value-fraud-security-market-signals
topic: ai-data-engineering
published_at: 2026-10-17T23:39:00+09:00
tags:
  - 그래프DB
  - 사기탐지
  - 보안
  - 추천시스템
  - GNN
  - Neo4j
  - PostgreSQL
  - 시장
summary: "측정 가능한 성과가 가장 자주 나오는 곳은 LLM과 무관한 그래프 ML이다. Wiz는 Amazon Neptune에 수천억 개 관계를 저장해 20여 리전에서 운영하고, 남아공 Capitec은 Memgraph로 하루 350만 건을 스코어링하며, Delivery Hero는 Neptune으로 차단 사기를 32% 늘렸다. 반면 Spotify(+46%), Pinterest(+2.5%) 같은 웹스케일 추천 GNN은 상용 그래프 DB가 아닌 자체 그래프 컴퓨트 위에서 돌고, Revolut과 카카오뱅크는 그래프 없이 사기 탐지 성과를 냈다. 시장은 양극화됐다. Neo4j는 ARR 2억 달러를 넘겼지만 IPO는 없고, TigerGraph는 인원을 70% 줄였으며, Kuzu는 Apple 인수 뒤 저장소가 아카이브됐다. PostgreSQL 19와 Spanner, Oracle은 그래프 질의를 범용 DB 기능으로 흡수하고 있다. 그래프 DB 시리즈 3편(끝)."
generated_by: claude
model: claude-fable-5-1
---

# 그래프 DB가 값을 한 곳은 사기 탐지와 클라우드 보안…Wiz는 Neptune에 수천억 관계, Capitec은 하루 350만 건, 그러나 TigerGraph 430→130명·Kuzu는 Apple 인수 뒤 아카이브, PostgreSQL 19가 그래프 질의를 흡수

## 한눈에 보기

- 1편(GraphRAG)과 2편(에이전트 메모리)에서 그래프의 이득은 벤더 수치와 독립 측정 사이에서 쪼그라들었다. 3편은 LLM 바깥에서 그래프 DB가 실제로 돈을 번 곳과 그래프 DB 시장이 보내는 신호를 본다.
- 클라우드 보안은 상용 그래프 DB가 운영 핵심에 들어간 가장 뚜렷한 영역이다. Wiz Security Graph는 Amazon Neptune에 수천억 개 관계를 저장하고 20개 이상 리전에서 수백 개 클러스터를 운영한다. Google은 2025년 Wiz를 320억 달러에 인수했다. 다만 AWS 사례가 말하는 "조사 시간 40% 단축"은 그래프가 아니라 Bedrock 기반 가이드에 귀속된 수치다.
- 사기 탐지에서는 남아공 Capitec이 Memgraph로 2024년 4월 첫 그래프를 가동한 뒤 2026년 라이브 그래프 7개로 하루 350만 건 이상을 스코어링하고, Delivery Hero는 Neptune으로 차단된 사기 구매를 32% 늘렸다. 둘 다 벤더 채널 공개다. 반면 Revolut은 Couchbase 위에서 96% 적발률을, 카카오뱅크는 시퀀스 모델로 월평균 사기 예방 4.4배를 냈다. 그래프는 사기 탐지의 필수 조건이 아니다.
- 추천 GNN의 성과는 크지만 그래프 DB와 무관하다. Spotify 오디오북 신규 시작률 +46%, Pinterest 리핀 +2.5%, LinkedIn 광고 CTR +2%는 모두 자체 그래프 컴퓨트 위의 결과다. 운영 그래프 DB를 쓰는 대규모 추천은 LinkedIn의 자체 개발 LIquid(2,700억 엣지)가 유일하다.
- 실무자 불만은 저장소가 아니라 그래프를 채우는 일에 집중된다. LLM이 뽑은 그래프는 "중복으로 가득한 더러운 지식그래프"라는 평이 나왔고, 2026년 10월 한 회고는 "entity-resolution debt"와 "verification debt"라는 말로 지식 획득 병목이 "해결된 게 아니라 옮겨갔다"고 썼다.
- 시장은 양극화됐다. Neo4j는 2024년 11월 ARR 2억 달러 돌파를 발표했지만 당시 언급한 IPO는 2026년 10월까지 없다. TigerGraph는 2024년 4월 12개월 안에 세 번째 CEO를 맞으며 인원을 430명에서 130명으로 줄였고, 임베디드 그래프 DB Kuzu는 2025년 10월 Apple 인수 직후 저장소가 아카이브됐다. 2026년 10월 DB-Engines 그래프 DBMS 순위에서 전용 그래프 DB 중 2점 이상은 Neo4j(48.88)뿐이다.
- 그래프 질의는 범용 DB로 흡수되고 있다. PostgreSQL 19에 ISO 표준 SQL/PGQ 패치가 2026년 3월 커밋됐고, Google Spanner Graph는 2025년 1월 GA, Oracle 23ai는 SQL/PGQ를 지원한다. AWS는 Bedrock의 GraphRAG를 추가 요금 없이 번들했다. 국내에서는 비트나인이 2024년 AgensGraph 대신 PostgreSQL 기반 아젠스SQL로 AI 사업을 확대한다고 선언했다.

## 사기 탐지: 그래프 DB 운영 사례와 그래프 없는 대조 사례

사기 탐지는 거래, 계정, 기기, 주소가 서로 연결된 데이터여서 그래프의 전통적 영역이다. 그래프 DB를 운영 핵심에 둔 공개 사례는 남아공 은행 Capitec이 대표적이다. Memgraph 고객 사례에 따르면 2024년 4월 첫 그래프를 가동한 뒤 2026년 기준 라이브 그래프 7개를 운영하며 하루 350만 건 이상을 스코어링하고, 설계한 그래프 피처 195개 중 27개를 테이블 피처 23개와 섞어 SageMaker에서 모델을 돌린다([Memgraph](https://memgraph.com/customer-stories/capitec-graph-machine-learning-fraud-detection)). "레거시 대비 최대 50% 더 많은 의심 활동 탐지, 조사 시간 30~40% 단축"은 Memgraph CTO가 기고한 글의 수치다([Retail Banker International](https://www.retailbankerinternational.com/comment/time-to-get-serious-graphs-banking-cybersecurity/)). Delivery Hero는 Amazon Neptune으로 신규 고객 바우처 남용을 탐지해 차단된 사기 구매가 32% 늘었고 Neptune 쿼리 지연은 약 15ms였다고 AWS 블로그에 공동 집필로 밝혔다([AWS](https://aws.amazon.com/blogs/database/empowering-fraud-detection-at-delivery-hero-with-amazon-neptune)).

큰 숫자일수록 근거는 약하다. Mastercard의 "탐지율 평균 20%, 최대 300% 향상, 오탐 85% 감소"는 전부 자체 주장이며, CNBC 보도에는 "graph"라는 단어 자체가 없다([CNBC via NBC Connecticut](https://www.nbcconnecticut.com/news/business/money-report/mastercard-jumps-into-generative-ai-race-with-model-it-says-can-boost-fraud-detection-by-up-to-300/3208183/)). 대조 사례도 있다. Revolut의 사기 탐지 시스템은 문서 DB인 Couchbase 위에서 96% 적발률을 낸다([Couchbase](https://www.couchbase.com/customers/revolut/)). 국내에서는 카카오뱅크가 2026년 6월 어텐션 기반 시퀀스 모델로 월평균 사기 예방 건수를 4.4배 늘렸다고 보도됐는데 이 역시 그래프 방식이 아니다([헤럴드경제](https://www.heraldk.com/article/2026060816545972524)). 그래프는 사기 탐지에 유용한 도구이지만 필수 조건은 아니다.

## 클라우드 보안: 상용 그래프 DB의 가장 뚜렷한 성공

클라우드 보안은 상용 그래프 DB가 제품의 중심에 들어간 가장 뚜렷한 영역이다. Wiz의 Security Graph는 Amazon Neptune에 수천억 개의 관계를 저장하고 20개 이상 리전에서 수백 개 클러스터를 운영하며, AWS 사례는 Bedrock 기반 가이드로 조사 시간을 40% 줄이고 ElastiCache로 비용을 20% 절감했다고 전한다([AWS](https://aws.amazon.com/solutions/case-studies/wiz-neptune)). Google은 2025년 Wiz를 320억 달러에 인수했다([Converge Digest](https://convergedigest.com/google-bolsters-cloud-security-with-32b-wiz-acquisition/)). 두 가지를 구분해야 한다. 40%는 그래프가 아니라 생성형 AI 가이드에 귀속된 수치이고, 이 인수를 "그래프의 검증"으로 읽은 것은 TigerGraph 블로그라는 벤더 해석이다.

규모의 경계도 보인다. CrowdStrike Threat Graph는 하루 1조 건 이상의 이벤트와 2조 정점을 자체 구축 그래프 DB로 처리하고([CrowdStrike](https://www.crowdstrike.com/en-us/platform/threat-graph/)), Microsoft Security Exposure Management는 전용 그래프 DB 대신 Kusto 질의 언어의 `make-graph` 연산자로 질의 시점에 메모리 안에 그래프를 만든다([Microsoft Learn](https://learn.microsoft.com/en-us/security-exposure-management/query-enterprise-exposure-graph)). 최대 규모에서는 상용 그래프 DB가 아니라 자체 엔진이나 범용 분석 엔진이 선택됐다.

## 추천 GNN: 성과는 크고 그래프 DB는 없다

그래프 신경망(GNN) 추천의 성과는 A/B 테스트로 측정돼 있다. Pinterest의 OmniSage는 사이트 전역 리핀을 약 2.5% 올렸고([arXiv 2504.17811](https://arxiv.org/abs/2504.17811)), LinkedIn의 LiGNN은 광고 클릭률 약 2%, 구직 응답률 약 1%를 높였다([arXiv 2402.11139](https://arxiv.org/abs/2402.11139)). Spotify의 2T-HGNN은 신규 오디오북 시작률 +46%, 스트리밍률 +23%를 보고했다([arXiv 2403.05185](https://arxiv.org/abs/2403.05185)). 그러나 이들은 전부 자체 GNN 플랫폼 위에서 돌아간다. Uber Eats의 GraphSAGE 변형은 AUC를 12% 올렸지만 저장은 HDFS의 Parquet, 학습은 Spark와 TensorFlow였다([Uber](https://www.uber.com/blog/uber-eats-graph-learning/)).

운영 그래프 DB를 쓰는 대규모 추천 사례는 LinkedIn의 자체 개발 LIquid가 유일하다. 2,700억 엣지와 초당 200만 질의를 처리하며, "알 수도 있는 사람" 기능을 LIquid로 옮겨 지연을 1초 이상에서 평균 50ms 미만으로 줄였다([InfoQ](https://www.infoq.com/news/2023/06/linkedin-liquid-graph-database/)). 효과 크기의 분포도 시사적이다. Spotify 오디오북처럼 콜드스타트가 큰 신규 카테고리에서는 수십 퍼센트, 성숙한 피드와 광고에서는 0.1~2%로, GNN은 관계 정보가 희소한 신호를 보완할 때 값이 크다. 카카오가 만든 HBase 기반 그래프 DB S2Graph는 2020년 Apache 인큐베이터에서 퇴역했다([Apache S2Graph](https://s2graph.apache.org)).

제약 분야에서 임상 단계 성과를 지식그래프에 귀속시키는 1차 자료는 BenevolentAI가 AstraZeneca에 신규 타깃 5개를 전달한 것([Business Wire](https://www.businesswire.com/news/home/20221005005625/en/BenevolentAI-Achieves-Further-Milestones-in-AI-enabled-Target-Identification-Collaboration-With-AstraZeneca))과 Insilico의 rentosertib 3상 개시([Insilico](https://insilico.com/news/xmjsn4l091-insilico-initiates-phase-iii-clinical-tr))인데, 둘 다 자체 플랫폼이고 상용 그래프 DB 벤더명은 밝히지 않았다.

## 실무자의 불만: 병목은 저장소가 아니라 지식 획득

효용이 없거나 부정적이었다는 증거는 실무자 커뮤니티에서 모인다. Hacker News의 Microsoft GraphRAG 공개 스레드(282점)에서는 "웬만한 크기의 데이터셋에서 이 연산량은 감당이 안 되지 않나"는 질문과, LLM에 그래프를 맡기면 "중복으로 가득한 매우 '더러운' 지식그래프"가 나온다는 반응이 나왔고, 자체 데이터로 GraphRAG가 RAG를 이겼다는 댓글은 없었다([Hacker News](https://news.ycombinator.com/item?id=40857174)). 지식 증강 생성(KAG) 스레드에서는 그래프 구축이 "어려운 문제(the Hard Problem)"이며 채우는 일은 "여전히 사람 전문가의 영역"이라는 지적이 반복됐다([Hacker News](https://news.ycombinator.com/item?id=42547133)).

2026년 10월 17일 Bret Kerr의 회고는 이 불만을 개념화했다. LLM이 추출을 싸게 만들었지만 기계 속도로 생산되는 중복·혼동 노드라는 "entity-resolution debt"와, 추출된 엣지가 참인지 확인할 저렴한 방법이 없는 "verification debt"를 낳았으며, 1985년에 지적된 지식 획득 병목은 "해결된 게 아니라 옮겨갔다"는 것이다([Bret Kerr](https://bretkerr.substack.com/p/the-graph-was-never-the-hard-part)). 학계도 확인한다. HippoRAG 2 논문에서 LightRAG의 단순 사실 QA 평균 F1은 6.6으로 임베딩 베이스라인 57.0에 비해 붕괴했고, 저자들은 LLM 생성 노이즈가 원인이라고 설명했다([arXiv 2502.14802](https://arxiv.org/html/2502.14802v2)). Neo4j 공식 블로그조차 LLM 그래프 변환기에서 노드와 관계 타입을 제한해야 노이즈가 줄어든다고 안내한다([Neo4j](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)). 다만 회사명과 수치를 밝히고 "GraphRAG를 걷어냈다"고 쓴 기업 블로그는 찾지 못했다.

## 시장 신호: 1강, 감원, 인수, 흡수

Neo4j는 2024년 11월 ARR 2억 달러 돌파와 벤더 의뢰 추정 점유율 44%를 발표했다([Neo4j](https://neo4j.com/press-releases/neo4j-revenue-milestone-2024/)). 당시 CEO가 언급한 IPO는 2026년 10월까지 신청되지 않았다([StockAnalysis](https://stockanalysis.com/private/neo4j/)). 2위권은 흔들렸다. TigerGraph는 2024년 4월 새 CEO 하미드 아자위가 "12개월 안에 세 번째 CEO"로 취임하며 인원을 430명에서 130명으로 줄였다고 밝혔다([TechTarget](https://www.techtarget.com/searchdatamanagement/news/366582681/TigerGraph-unveils-GenAI-assistant-introduces-new-CEO)). 임베디드 그래프 DB Kuzu는 2025년 10월 9일 Apple이 전체 주식을 인수하는 계약을 맺었고 다음 날 GitHub 저장소가 아카이브됐으며 웹사이트도 닫혔다. 이 사실은 Apple의 EU 신고로 2026년 2월에 알려졌다([BetaKit](https://betakit.com/apple-strikes-deal-to-acquire-canadian-database-software-startup-kuzu/)). Hacker News의 반응은 "이래서 데이터베이스는 SQLite나 PostgreSQL을 고수한다"였다([Hacker News](https://news.ycombinator.com/item?id=45560036)). Dgraph는 2025년 10월 DB 벤더가 아닌 Istari Digital로 넘어갔다([Istari Digital](https://www.istaridigital.com/resources/istari-acquires-dgraph)). 2026년 10월 DB-Engines 그래프 DBMS 순위에서 전용 그래프 DB 중 2점 이상은 Neo4j(48.88)뿐이고 TigerGraph 1.95, Memgraph 1.89, NebulaGraph 1.68은 모두 2점 미만이다([DB-Engines](https://db-engines.com/en/ranking/graph+dbms)).

동시에 그래프 질의는 범용 DB로 흡수되고 있다. PostgreSQL 19에 ISO 표준 SQL/PGQ 패치가 2026년 3월 커밋되어 `GRAPH_TABLE` 질의와 프로퍼티 그래프 정의가 들어갔고([depesz](https://www.depesz.com/2026/07/31/waiting-for-postgresql-19-sql-property-graph-queries-sql-pgq/)), Google Spanner Graph는 2025년 1월 GA([Google Cloud](https://cloud.google.com/blog/products/databases/announcing-spanner-graph-general-availability)), Oracle 23ai는 SQL/PGQ를 네이티브로 지원한다([Oracle](https://blogs.oracle.com/database/post/first-quarterly-update-on-oracle-graph-2025)). AWS는 2025년 3월 Bedrock Knowledge Bases의 GraphRAG를 추가 요금 없이 정식 제공했다([AWS](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-knowledge-bases-graphrag-generally-available)). 그래프 기능이 독립 제품이 아닌 플랫폼 기능으로 상품화되고 있다는 뜻이다. 한계도 있다. PostgreSQL 확장 Apache AGE에 대해서는 "성능에서 Neo4j에 근접하지 못한다"는 실사용 평가가 있어 깊은 탐색에서는 전용 DB가 남는다([Hacker News](https://news.ycombinator.com/item?id=48355891)). 국내에서는 비트나인이 2024년 1월 AgensGraph 대신 PostgreSQL 기반 아젠스SQL로 AI 사업을 확대하겠다고 밝혔고([바이라인네트워크](https://byline.network/2024/01/240122_002)), 엔코아가 2025년 8월 Neo4j 리셀러가 된 것 외에 2024~2026년 공개된 국내 그래프 DB 도입 사례는 확인되지 않는다([바이라인네트워크](https://byline.network/2025/08/21-495/)).

## 의미

- 세 편의 증거를 한 줄로 꿰면, 그래프의 효용은 "누가 그래프를 만들었는가"가 결정한다. 성과가 측정된 사례(LinkedIn 티켓, Wiz 클라우드 자산, Capitec과 Delivery Hero 거래, LIquid 회원 관계)는 모두 원천 데이터가 이미 관계형으로 구조화돼 있고 운영 흐름에서 자동 적재되는 경우다. 비판과 실패는 LLM이 비정형 문서에서 즉석으로 그래프를 뽑는 경로에 집중된다.
- "AI에는 그래프 DB가 필요하다"는 명제는 2026년 10월 시점에서 벤더 주장이다. 측정으로 뒷받침되는 것은 "구조화된 관계 데이터가 있고 질의가 멀티홉·시간·전역 요약 중심인 워크로드에서 그래프가 값을 한다"는 좁은 명제다.
- 시장 신호는 같은 방향이다. 1강 Neo4j는 성장하지만 IPO는 미뤄졌고, 2위권은 감원과 인수로 정리됐으며, 그래프 질의는 PostgreSQL과 Spanner, Oracle의 기능이 되고 있다. 전용 그래프 DB의 자리는 깊은 탐색과 대규모 관계 데이터로 좁아지고 있다.
- 실무 순서는 명확하다. 벡터 RAG에 reranker를 붙인 베이스라인을 먼저 측정하고, 질의 로그에서 멀티홉 비율을 확인하고, 그래프가 필요하다고 판단되면 PostgreSQL 19의 SQL/PGQ나 LazyGraphRAG류 저비용 구조부터 시작한다. 전용 그래프 DB는 그 다음이다.
- 판단을 바꿀 수 있는 관찰 지점은 세 가지다. Cisco의 2026년 11월 NODES 발표가 실측치를 내놓는지, Mem0 플랫폼의 2026년 수치가 제3자 재현을 통과하는지, Neo4j가 IPO 서류에서 GraphRAG와 에이전트 메모리 매출 비중을 공개하는지다.

## 확인할 점

- Capitec, Delivery Hero, Wiz의 수치는 Memgraph와 AWS 고객 사례 채널을 거쳤으며 당사자가 독립 발표한 것은 아니다. Capitec의 "50%, 30~40%"는 Memgraph CTO 기고문의 수치다.
- Wiz의 "조사 시간 40%"는 그래프 DB가 아닌 Bedrock 가이드에 귀속된 수치이며, 그래프 자체의 효용을 따로 측정한 공개 자료는 없다.
- 추천 GNN 수치는 각사 논문의 A/B 테스트 결과이며 실험 기간과 대상 사용자 비율은 논문마다 다르다.
- Neo4j ARR 2억 달러는 2024년 11월 기준이고 2025~2026년 수치는 공개되지 않았다. 점유율 44%는 Neo4j가 의뢰한 추정이다.
- DB-Engines 점수는 검색량과 구인 공고 등 관심도 지표이며 매출이나 설치 수가 아니다.
- Kuzu 인수 조건과 Apple의 활용 계획은 공개되지 않았다.
- Reddit 실무자 토론은 접근이 차단돼 확인하지 못했다. "GraphRAG를 걷어냈다"는 기업 사례 부재는 검색 범위 안의 판단이다.

## 출처

- [Memgraph, Capitec graph machine learning fraud detection](https://memgraph.com/customer-stories/capitec-graph-machine-learning-fraud-detection)
- [Retail Banker International, Time to get serious: graphs, banking and cybersecurity](https://www.retailbankerinternational.com/comment/time-to-get-serious-graphs-banking-cybersecurity/)
- [AWS Database Blog, Empowering fraud detection at Delivery Hero with Amazon Neptune](https://aws.amazon.com/blogs/database/empowering-fraud-detection-at-delivery-hero-with-amazon-neptune)
- [CNBC via NBC Connecticut, Mastercard generative AI fraud model](https://www.nbcconnecticut.com/news/business/money-report/mastercard-jumps-into-generative-ai-race-with-model-it-says-can-boost-fraud-detection-by-up-to-300/3208183/)
- [Couchbase, Revolut customer story](https://www.couchbase.com/customers/revolut/)
- [헤럴드경제, 카카오뱅크 AI 기반 FDS 성과 (2026-06-08)](https://www.heraldk.com/article/2026060816545972524)
- [AWS, Wiz and Amazon Neptune case study](https://aws.amazon.com/solutions/case-studies/wiz-neptune)
- [Converge Digest, Google bolsters cloud security with $32B Wiz acquisition](https://convergedigest.com/google-bolsters-cloud-security-with-32b-wiz-acquisition/)
- [CrowdStrike, Threat Graph](https://www.crowdstrike.com/en-us/platform/threat-graph/)
- [Microsoft Learn, Query the enterprise exposure graph](https://learn.microsoft.com/en-us/security-exposure-management/query-enterprise-exposure-graph)
- [Pinterest, OmniSage (arXiv 2504.17811)](https://arxiv.org/abs/2504.17811)
- [LinkedIn, LiGNN (arXiv 2402.11139)](https://arxiv.org/abs/2402.11139)
- [Spotify, 2T-HGNN (arXiv 2403.05185)](https://arxiv.org/abs/2403.05185)
- [Uber, Food Discovery with Uber Eats: Using Graph Learning](https://www.uber.com/blog/uber-eats-graph-learning/)
- [InfoQ, LinkedIn LIquid graph database (2023-06)](https://www.infoq.com/news/2023/06/linkedin-liquid-graph-database/)
- [Apache S2Graph](https://s2graph.apache.org)
- [Business Wire, BenevolentAI–AstraZeneca milestones (2022-10-05)](https://www.businesswire.com/news/home/20221005005625/en/BenevolentAI-Achieves-Further-Milestones-in-AI-enabled-Target-Identification-Collaboration-With-AstraZeneca)
- [Insilico Medicine, Phase III initiation (2026-07-07)](https://insilico.com/news/xmjsn4l091-insilico-initiates-phase-iii-clinical-tr)
- [Hacker News, GraphRAG release thread](https://news.ycombinator.com/item?id=40857174)
- [Hacker News, KAG thread](https://news.ycombinator.com/item?id=42547133)
- [Bret Kerr, The graph was never the hard part (2026-10-17)](https://bretkerr.substack.com/p/the-graph-was-never-the-hard-part)
- [Gutiérrez et al., HippoRAG 2 (arXiv 2502.14802 v2)](https://arxiv.org/html/2502.14802v2)
- [Neo4j, Knowledge graph extraction challenges](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)
- [Neo4j, Revenue milestone press release (2024-11-19)](https://neo4j.com/press-releases/neo4j-revenue-milestone-2024/)
- [StockAnalysis, Neo4j private company page](https://stockanalysis.com/private/neo4j/)
- [TechTarget, TigerGraph unveils GenAI assistant, introduces new CEO (2024-04-30)](https://www.techtarget.com/searchdatamanagement/news/366582681/TigerGraph-unveils-GenAI-assistant-introduces-new-CEO)
- [BetaKit, Apple strikes deal to acquire Kuzu (2026-02-12)](https://betakit.com/apple-strikes-deal-to-acquire-canadian-database-software-startup-kuzu/)
- [Hacker News, Kuzu shutdown thread](https://news.ycombinator.com/item?id=45560036)
- [Istari Digital, Istari acquires Dgraph (2025-10-23)](https://www.istaridigital.com/resources/istari-acquires-dgraph)
- [DB-Engines, Graph DBMS ranking](https://db-engines.com/en/ranking/graph+dbms)
- [depesz, Waiting for PostgreSQL 19: SQL/PGQ (2026-07-31)](https://www.depesz.com/2026/07/31/waiting-for-postgresql-19-sql-property-graph-queries-sql-pgq/)
- [Google Cloud, Spanner Graph general availability (2025-01-30)](https://cloud.google.com/blog/products/databases/announcing-spanner-graph-general-availability)
- [Oracle, First quarterly update on Oracle Graph 2025](https://blogs.oracle.com/database/post/first-quarterly-update-on-oracle-graph-2025)
- [AWS, Bedrock Knowledge Bases GraphRAG generally available (2025-03)](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-knowledge-bases-graphrag-generally-available)
- [Hacker News, Apache AGE discussion](https://news.ycombinator.com/item?id=48355891)
- [바이라인네트워크, 비트나인 아젠스SQL (2024-01-22)](https://byline.network/2024/01/240122_002)
- [바이라인네트워크, 엔코아 Neo4j 리셀러 (2025-08-21)](https://byline.network/2025/08/21-495/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
