---
title: 제타포랩, Rust로 만든 그래프 데이터베이스 Zeta4j를 Apache 2.0으로 공개
slug: 2026-11-01-zeta4j-open-source
topic: zeta4
published_at: 2026-11-01T08:35:00+09:00
tags:
  - zeta4j
  - open-source
  - Apache-2.0
  - graph-database
  - Rust
  - openCypher
summary: 제타포랩이 openCypher 질의와 전문·벡터 색인을 한 트랜잭션에서 다루는 Rust 그래프 데이터베이스 Zeta4j를 Apache 2.0으로 GitHub에 공개하고 첫 버전 0.1.0을 냈다.
generated_by: claude
model: claude-opus-5-5
---

# 제타포랩, Rust로 만든 그래프 데이터베이스 Zeta4j를 Apache 2.0으로 공개

## 한눈에 보기

제타포랩(zeta4lab, 대표 최강유, 사업자등록번호 570-35-01460)이 2026년 10월 30일 그래프 데이터베이스 `Zeta4j`를 Apache License 2.0으로 [GitHub에 공개](https://github.com/zeta4lab/zeta4j)하고 첫 릴리스 [0.1.0](https://github.com/zeta4lab/zeta4j/releases/tag/v0.1.0)을 냈다. 저장소 설명은 "Zeta4j graph database (community edition)"이며, [NOTICE](https://github.com/zeta4lab/zeta4j/blob/main/NOTICE) 파일은 저작권자를 제타포랩 대표 최강유(Choi Kangyou)로 밝힌다.

Zeta4 Now 역시 제타포랩이 운영한다. 제타포랩은 10월 9일 데이터 작업 런타임 [zeta4s](https://now.zeta4.net/a/2026-10-09-zeta4s-open-source)를 공개한 데 이어 3주 만에 두 번째 오픈소스 프로젝트를 내놓았다. 이 글은 공개 저장소의 문서와 릴리스 정보를 바탕으로 정리했다.

## 무엇을 하는 도구인가

[README](https://github.com/zeta4lab/zeta4j/blob/main/README.md)에 따르면 Zeta4j는 Rust로 작성한 속성 그래프(property graph) 데이터베이스다. 데이터베이스 하나를 임베디드 저장소 [redb](https://github.com/cberner/redb) 파일 하나에 담고, [openCypher](https://opencypher.org/) 질의를 Bolt 프로토콜과 HTTP API로 받는다. 전문 검색(Tantivy) 색인과 벡터(HNSW) 색인을 그래프 데이터와 같은 트랜잭션 안에서 갱신하는 것이 특징이다.

그래프 관계 탐색, 키워드 검색, 임베딩 유사도 검색을 한 서버와 한 질의 언어로 처리할 수 있어, 별도 검색 엔진이나 벡터 DB와 정합성을 맞추는 수고를 줄일 수 있다.

## 주요 기능

0.1.0 릴리스 노트와 README가 밝힌 기능은 다음과 같다.

- **질의**: openCypher 질의, 트랜잭션, 스키마 명령을 지원한다.
- **접속 경로**: Bolt 프로토콜과 HTTP 트랜잭션 API로 질의하고, 관리는 gRPC로 한다. 기본 포트는 HTTP `9044`, Bolt `9045`, gRPC `9046`이다.
- **전문 검색**: BM25 점수와 언어 분석기를 쓰는 전문 색인을 만든다.
- **벡터 검색**: HNSW 색인으로 코사인·유클리드·내적 거리를 지원한다.
- **다중 데이터베이스**: 서버 하나에 여러 논리 데이터베이스를 둔다.
- **인증과 암호화**: 비밀번호 인증과 Ed25519로 서명한 세션 토큰을 쓰고, 모든 리스너에서 TLS 1.3을 켤 수 있다.
- **배포**: 서버 `zeta4jd`와 클라이언트 `z4j`(서버 제어, Cypher 셸, 인증, 관리) 두 실행 파일, Dockerfile과 단일 서버용 compose 파일을 제공한다.

## 설치와 시작

0.1.0은 미리 빌드한 실행 파일 없이 소스로 배포된다. Rust 1.99 이상과 `protoc`가 필요하며, 다음 명령으로 빌드한다.

```bash
cargo build --release -p zeta4j -p zeta4j-cli
```

처음 서버를 띄울 때는 Ed25519 토큰 서명 키를 만들고 `z4j server init --generate-bootstrap-credential`로 첫 사용자용 일회성 자격 증명을 받는다. 이 자격 증명은 15분 뒤 만료되므로 그 안에 서버를 시작하고 비밀번호를 바꿔야 한다. 인증 없이 로컬에서만 시험하려면 `z4j server start --profile local-test --no-auth`를 쓰며, 이 방식은 루프백 주소에서만 허용된다.

질의 예시는 다음과 같다.

```cypher
CREATE FULLTEXT INDEX person_text FOR (n:Person) ON EACH [n.name, n.bio] ANALYZER english;

CALL db.index.fulltext.queryNodes('person_text', 'compiler')
YIELD node, score
RETURN node.name, score;
```

저장소의 `examples/`에는 영화·소셜 그래프, 트랜잭션, 서브쿼리, 동시성, 성능 등을 다룬 예제가 있다.

## 확인할 점

- 첫 버전(0.1.0)이므로 운영에 쓰기 전 충분히 시험하고 사용할 버전을 고정하는 편이 안전하다.
- 저장소 설명이 "community edition"이라고 밝히고 있다. 다른 에디션의 범위나 계획은 공개 자료에서 확인되지 않았다.
- 라이선스 전문은 [LICENSE](https://github.com/zeta4lab/zeta4j/blob/main/LICENSE)에, 실행 파일에 포함된 서드파티 Rust 크레이트의 허용 라이선스 목록은 `deny.toml`에 있다.

## 출처

- [zeta4lab/zeta4j — GitHub 저장소](https://github.com/zeta4lab/zeta4j)
- [Zeta4j README](https://github.com/zeta4lab/zeta4j/blob/main/README.md)
- [Zeta4j 0.1.0 릴리스](https://github.com/zeta4lab/zeta4j/releases/tag/v0.1.0)
- [Zeta4j NOTICE](https://github.com/zeta4lab/zeta4j/blob/main/NOTICE)
- [Zeta4j LICENSE (Apache License 2.0)](https://github.com/zeta4lab/zeta4j/blob/main/LICENSE)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
