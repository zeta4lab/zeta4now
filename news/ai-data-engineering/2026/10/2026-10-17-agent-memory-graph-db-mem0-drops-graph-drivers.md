---
title: "에이전트 메모리 최대 투자 Mem0, 오픈소스에서 그래프 DB 코드 4,000줄 삭제…파일과 grep만 쓴 에이전트가 74.0%로 그래프 메모리 68.5%를 이기고, Zep·Mem0는 벤치마크 수치를 놓고 공방"
slug: 2026-10-17-agent-memory-graph-db-mem0-drops-graph-drivers
topic: ai-data-engineering
published_at: 2026-10-17T23:37:00+09:00
tags:
  - 그래프DB
  - 에이전트메모리
  - Mem0
  - Zep
  - Graphiti
  - 벤치마크
  - Claude Code
summary: "그래프 DB 벤더의 메시지가 2025~2026년 GraphRAG에서 '에이전트 메모리'로 옮겨갔지만 증거는 더 약하다. Zep과 Mem0의 논문은 그래프 변형이 전체 점수에서 앞서면서도 single-hop·multi-hop에서는 뒤지고 전체 컨텍스트 투입이 둘 다 이기는 결과를 담았고, 그래프는 지연 3배·토큰 2배를 요구했다. 두 회사는 서로의 LoCoMo 수치를 문제 삼았고 Zep은 84%를 75.14%로 정정했다. Letta는 대화 기록을 파일에 넣고 grep만 준 에이전트가 74.0%로 Mem0 그래프 변형 68.5%를 앞섰다고 보고했다. 2,400만 달러를 조달한 Mem0는 오픈소스에서 Neo4j·Memgraph·Kuzu·Neptune 드라이버 약 4,000줄을 제거했고, AWS·Anthropic의 메모리 서버와 Claude Code·Cursor는 그래프 DB를 쓰지 않는다. 그래프 DB 시리즈 2편."
generated_by: claude
model: claude-fable-5-1
---

# 에이전트 메모리 최대 투자 Mem0, 오픈소스에서 그래프 DB 코드 4,000줄 삭제…파일과 grep만 쓴 에이전트가 74.0%로 그래프 메모리 68.5%를 이기고, Zep·Mem0는 벤치마크 수치를 놓고 공방

## 한눈에 보기

- 그래프 DB 벤더의 AI 메시지는 2025~2026년 GraphRAG에서 "에이전트 메모리"로 옮겨갔다. 에이전트가 사용자와 나눈 대화에서 사실을 뽑아 엔터티와 관계로 저장하고, 나중에 그래프를 탐색해 기억을 되살린다는 구상이다. 1편이 다룬 GraphRAG보다 증거는 더 약하다.
- 그래프 DB를 실제로 쓰는 대표 사례는 Zep의 오픈소스 Graphiti(Neo4j, FalkorDB, Amazon Neptune 백엔드)와 Cognee다. 반면 AWS Bedrock AgentCore Memory는 추출 사실 목록을 쓰고, Anthropic MCP 메모리 서버는 "knowledge graph"라는 이름이지만 저장은 JSONL 파일이다.
- Zep 논문은 LongMemEval에서 전체 컨텍스트 투입 60.2% 대비 71.2%(gpt-4o)를 보고했지만 단일 세션 어시스턴트 유형에서는 전체 컨텍스트가 더 높았다. Mem0 논문의 그래프 변형은 전체 68.44로 기본 66.88보다 높지만 single-hop과 multi-hop에서는 기본보다 낮고, 전체 컨텍스트 72.90이 둘 다 이겼다. 그래프는 검색 지연을 0.148초에서 0.476초로, 질의당 토큰을 1,764개에서 3,616개로 늘렸다.
- 두 회사는 서로의 수치를 문제 삼았다. Mem0 CTO는 Zep의 LoCoMo 84%가 분모 계산 오류로 과대 산정됐다고 지적했고 Zep은 75.14%로 정정했으나 합의 없이 끝났다. Mem0 저장소에는 논문 점수가 오픈소스로 재현되지 않는다는 이슈가 쌓였고 메인테이너는 유료 플랫폼 기준이라고 답했다.
- Letta는 LoCoMo 대화를 파일 하나에 넣고 grep과 검색 도구만 준 에이전트가 74.0%로 Mem0의 그래프 변형 68.5%를 앞섰다며 "메모리는 검색 메커니즘보다 컨텍스트 관리의 문제"라고 썼다. 2026년 1월의 통제 실험은 그래프 추출에 1,781분이 걸려 평면 방식 452분의 4배였고 벤치마크에 따라 그래프가 크게 뒤진다고 보고했다.
- 가장 상징적인 신호는 2025년 10월 2,400만 달러를 조달한 Mem0가 오픈소스 SDK에서 Neo4j, Memgraph, Kuzu, Apache AGE, Neptune 드라이버와 관련 코드 약 4,000줄을 제거한 것이다. 그래프 메모리는 유료 플랫폼 전용 기능이 됐다. 그래프 네이티브인 Zep은 분석기관 451 Research 집계로 ARR 100만 달러에 근접하는 수준이다.
- 코딩 에이전트도 그래프를 쓰지 않는다. Claude Code는 벡터 인덱스를 시험한 뒤 "모델이 모는 glob과 grep이 모든 것을 이겼다"며 인덱스 없는 검색을 택했고, Cursor 문서는 검색용 임베딩을 저장하지 않는다고 적는다. 코드 그래프를 명시한 곳은 코드 리뷰 제품 Greptile과 Sourcegraph 정도다.

## 그래프를 쓰는 곳과 쓰지 않는 곳

"에이전트 메모리에 그래프"를 가장 충실히 구현한 것은 Zep의 Graphiti다. Neo4j, FalkorDB, Amazon Neptune을 백엔드로 삼아 대화 에피소드, 엔터티, 커뮤니티의 세 층 서브그래프를 만들고, 각 사실에 유효 기간을 붙이는 bi-temporal 모델로 "지금 참인 것"과 "과거에 참이었던 것"을 구분한다. 검색은 의미 임베딩, BM25, 그래프 탐색을 섞은 하이브리드다([getzep/graphiti](https://github.com/getzep/graphiti)). Cognee도 그래프, 벡터, 관계형 저장소를 함께 쓰는 오픈소스 메모리 엔진으로 2026년 2월 750만 달러 시드를 받았다.

그러나 하이퍼스케일러와 모델 회사는 다른 길을 택했다. AWS Bedrock AgentCore Memory는 대화에서 추출한 사실 목록과 전략 기반 장기 메모리를 제공하며 그래프 언급이 없다([AWS](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-strategies.html)). Anthropic의 MCP 메모리 서버는 "knowledge graph 기반"이라고 소개하지만 저장은 JSONL 평문 파일이다([modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)). 이름이 자주 혼동되는 LangGraph는 에이전트 실행 흐름을 그래프로 표현하는 오케스트레이션 런타임이고 그래프 DB와는 무관하다.

## 논문 수치: 전체 점수는 앞서고, 세부에서는 뒤진다

Zep이 2025년 1월 낸 논문은 LongMemEval에서 전체 컨텍스트를 그대로 넣은 베이스라인 대비 55.4%에서 63.8%(gpt-4o-mini), 60.2%에서 71.2%(gpt-4o)로 정확도를 높이고 지연을 약 90% 줄였다고 보고했다. 같은 표에서 단일 세션 어시스턴트 유형은 두 모델 모두 전체 컨텍스트보다 낮았다([arXiv 2501.13956](https://arxiv.org/html/2501.13956v1)). Mem0가 2025년 4월 낸 논문에서 그래프 변형 Mem0^g의 LoCoMo 종합 점수는 68.44로 기본 Mem0 66.88보다 높았지만 single-hop과 multi-hop에서는 기본보다 낮았고, 대화 전체를 컨텍스트에 넣는 방식이 72.90으로 둘 다 이겼다. 비용은 그래프 쪽이 컸다. 검색 p50 지연은 0.148초에서 0.476초로, 질의당 토큰은 1,764개에서 3,616개로 늘었다([arXiv 2504.19413](https://arxiv.org/html/2504.19413v1)).

## 공방과 재현 실패

두 회사의 수치는 서로 충돌한다. Zep은 Mem0가 자사 베이스라인을 잘못 돌렸다고 반박했고, Mem0 CTO는 Zep의 LoCoMo 84%가 분모 계산 때문에 약 25.56점 과대 산정됐다고 이슈를 열었다. Zep은 계산 오류를 인정해 75.14%로 정정했으나 양측은 합의 없이 종결했다([getzep/zep-papers issue #5](https://github.com/getzep/zep-papers/issues/5)). Mem0 저장소 이슈 #2800에는 오픈소스로 논문 점수가 나오지 않고 유료 플랫폼에서도 0.49, 0.42, 심지어 0.20이 나왔다는 사용자 보고가 쌓였고, 메인테이너는 논문 점수가 플랫폼 전용 기능에 기반한다고 답했다([mem0ai/mem0 issue #2800](https://github.com/mem0ai/mem0/issues/2800)).

제3자 결과는 그래프 쪽에 불리하다. Letta는 2025년 8월 LoCoMo 대화를 파일 하나로 올리고 grep, 검색, 열기 도구만 준 에이전트가 gpt-4o-mini로 74.0%를 기록해 Mem0의 최고 성적 그래프 변형 68.5%를 앞섰다며, "메모리는 정확한 검색 메커니즘보다 에이전트가 컨텍스트를 어떻게 관리하는가의 문제"라고 썼다([Letta](https://www.letta.com/blog/benchmarking-ai-agent-memory)). 2026년 1월의 통제 실험 "Does Memory Need Graphs?"는 LongMemEval-S에서 그래프가 Recall@5 0.9690으로 평면 방식 0.9284를 앞섰지만 HaluMem에서는 0.4742 vs 0.8057로 크게 뒤졌고, 그래프 검색 지연은 574ms vs 240ms, 추출 시간은 1,781분 vs 452분이었다. 저자들은 "부적절한 그래프 구축이나 검색 전략은 결과를 악화시킨다"고 결론지었다([arXiv 2601.01280](https://arxiv.org/html/2601.01280v3)). Redis가 2026년 9월 낸 벤치마크 보고서는 동일 판정자로 재현하면 "발표된 수치는 종종 재현되지 않는다"며 차이가 +3점에서 -28점이라고 밝히고, 저장 구조를 구현 세부사항으로 취급했다([Redis](https://redis.io/resources/agent-memory-benchmark-report/)).

## Mem0의 선택과 시장 크기

가장 상징적인 신호는 Mem0의 결정이다. Mem0는 2025년 10월 Y Combinator, Peak XV 등에서 2,400만 달러를 조달해 이 분야 최대 자금을 확보했다([TechCrunch](https://techcrunch.com/2025/10/28/mem0-raises-24m-from-yc-peak-xv-and-basis-set-to-build-the-memory-layer-for-ai-apps/)). 그런데 현재 Mem0 공식 문서는 오픈소스 SDK에서 "모든 외부 그래프 저장소 드라이버(Neo4j, Memgraph, Kuzu, Apache AGE, Neptune)와 그 코드 경로(약 4,000줄)"를 제거했다고 적고, 그래프 메모리는 오픈소스 대체물 없이 유료 플랫폼 기능으로만 남겼다고 밝힌다. 플랫폼의 하이브리드 검색에 추가된 "entity matching"은 그래프 메모리와 별개의 세 번째 점수 신호라고 문서는 명시한다([Mem0 docs](https://docs.mem0.ai/open-source/graph_memory/overview)). 가장 많은 돈을 모은 회사가 오픈소스 이용자에게는 그래프 DB를 권하지 않게 된 셈이다.

그래프 네이티브인 Zep의 규모는 작다. 451 Research의 2026년 4월 보고서에 따르면 누적 조달액은 740만 달러, ARR은 100만 달러에 근접하는 수준이며, 분석가는 "에이전트 메모리 시장이 여전히 얼마나 작은지 놀랍다"고 평했다([451 Research](https://www.getzep.com/downloads/451Research_Reprint_ZepSoftware_10APR2026.pdf)).

## 코딩 에이전트는 grep을 택했다

코드를 다루는 에이전트는 그래프 인덱스의 가장 자연스러운 수요처로 여겨졌지만 실제 선택은 반대다. Claude Code 개발자 보리스 체르니는 2026년 3월 인터뷰에서 로컬 벡터 DB 등 여러 인덱스를 시험한 결과 "모델이 모는 평범한 glob과 grep이 모든 것을 이겼다"며 인덱스 없는 검색을 택했다고 밝혔다([Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)). Cursor의 현재 문서는 코드베이스 검색용 임베딩을 저장하지 않는다고 적는다([Cursor](https://cursor.com/docs/context/codebase-indexing)). 코드 그래프를 명시적으로 쓰는 곳은 코드 리뷰와 영향 분석 제품인 Greptile과 Sourcegraph 정도다([Greptile](https://www.greptile.com/docs/how-greptile-works/graph-based-codebase-context)).

## 의미

- 에이전트 메모리에서 그래프의 이득은 벤더 자체 벤치마크에서도 세부 항목과 전체 컨텍스트 비교에서 갈리고, 제3자 재현은 발표 수치를 깎는다. 1편의 GraphRAG와 같은 구도가 더 작은 시장에서 반복된다.
- 저장 구조보다 컨텍스트 관리와 도구 사용이 점수를 좌우한다는 것이 Letta, Redis, 2026년 통제 실험의 공통 결론이다. 그래프는 추출과 검색에 2~4배의 비용을 요구하면서 그 비용을 정당화할 만큼의 일관된 이득을 보여 주지 못했다.
- 가장 많은 자금을 모은 Mem0가 오픈소스에서 그래프 DB를 걷어낸 것은 시장이 내린 판단에 가깝다. 그래프 메모리를 쓰려면 유료 플랫폼이나 ARR 100만 달러 규모의 Zep을 택해야 한다.
- 개인 사용자나 소규모 팀이 에이전트에 기억을 붙일 때 그래프 DB를 먼저 세울 이유는 현재 증거로는 약하다. 파일과 검색 도구, 또는 평면 사실 저장으로 시작해 멀티세션·시간 추론이 실제 병목으로 확인될 때 그래프를 검토하는 순서가 증거에 부합한다.

## 확인할 점

- Zep과 Mem0의 논문 수치는 모두 자체 보고이며 양측이 서로의 재현을 문제 삼았다. 어느 쪽 수치도 제3자가 독립 재현한 결과는 확인하지 못했다.
- Mem0 문서의 그래프 드라이버 제거 안내에는 날짜와 버전 번호가 없다. 제거 시점은 문서 갱신 이력으로 확인해야 한다.
- Letta의 74.0%는 Letta 자신이 돌린 실험이고 Mem0 68.5%는 Mem0 논문에서 가져온 수치여서 평가 환경이 같지 않다.
- 451 Research의 Zep 수치는 Zep이 배포한 리프린트에서 확인했다.
- Claude Code와 Cursor의 인덱스 방식은 2026년 3월 인터뷰와 현재 문서 기준이며 이후 바뀔 수 있다.

## 출처

- [getzep/graphiti README](https://github.com/getzep/graphiti)
- [AWS, Bedrock AgentCore Memory strategies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-strategies.html)
- [modelcontextprotocol/servers, memory server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
- [Rasmussen et al., Zep: A Temporal Knowledge Graph Architecture for Agent Memory (arXiv 2501.13956)](https://arxiv.org/html/2501.13956v1)
- [Chhikara et al., Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory (arXiv 2504.19413)](https://arxiv.org/html/2504.19413v1)
- [getzep/zep-papers issue #5](https://github.com/getzep/zep-papers/issues/5)
- [mem0ai/mem0 issue #2800](https://github.com/mem0ai/mem0/issues/2800)
- [Letta, Benchmarking AI Agent Memory (2025-08-12)](https://www.letta.com/blog/benchmarking-ai-agent-memory)
- [Does Memory Need Graphs? (arXiv 2601.01280 v3)](https://arxiv.org/html/2601.01280v3)
- [Redis, Agent Memory Benchmark Report (2026-09)](https://redis.io/resources/agent-memory-benchmark-report/)
- [TechCrunch, Mem0 raises $24M (2025-10-28)](https://techcrunch.com/2025/10/28/mem0-raises-24m-from-yc-peak-xv-and-basis-set-to-build-the-memory-layer-for-ai-apps/)
- [Mem0 docs, Graph Memory overview and migration](https://docs.mem0.ai/open-source/graph_memory/overview)
- [451 Research, Zep Software reprint (2026-04-10)](https://www.getzep.com/downloads/451Research_Reprint_ZepSoftware_10APR2026.pdf)
- [Pragmatic Engineer, Building Claude Code with Boris Cherny (2026-03)](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)
- [Cursor docs, Codebase indexing](https://cursor.com/docs/context/codebase-indexing)
- [Greptile docs, Graph-based codebase context](https://www.greptile.com/docs/how-greptile-works/graph-based-codebase-context)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
