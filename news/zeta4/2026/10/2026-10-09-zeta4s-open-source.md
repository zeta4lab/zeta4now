---
title: zeta4s, Apache 2.0 오픈소스로 공개… AI 에이전트가 만든 계약을 실행하는 런타임
slug: 2026-10-09-zeta4s-open-source
topic: zeta4
published_at: 2026-10-09T16:05:00+09:00
tags:
  - zeta4s
  - open-source
  - Apache-2.0
  - AI-agent
  - data-pipeline
summary: 제타포랩이 LLM과의 대화만으로 데이터 처리 프로세스를 만들고 운영하기 위해 개발한 런타임 엔진 zeta4s를 Apache 2.0 라이선스로 GitHub에 공개했다.
generated_by: claude
model: claude-opus-5-5
---

# zeta4s, Apache 2.0 오픈소스로 공개… AI 에이전트가 만든 계약을 실행하는 런타임

## 한눈에 보기

제타포랩(zeta4lab)이 2026년 10월 9일 데이터 작업 런타임 엔진 `zeta4s`를 Apache License 2.0으로 [GitHub에 공개](https://github.com/zeta4lab/zeta4s)했다. AI 에이전트나 사용자가 YAML·SQL·dbt 파일로 작성한 프로젝트 계약을 검증해 Step Graph로 바꾸고, 같은 계약으로 배포·실행·관측까지 이어 가는 것이 핵심이다. 공개와 함께 1.0.22 릴리스의 설치 파일과 컨테이너 이미지도 내려받을 수 있다.

Zeta4 Now 역시 zeta4lab이 운영하며, zeta4s는 이 사이트의 자동 기사 생성 옵션 경로에도 쓰인다. 이 글은 공개 저장소의 문서와 릴리스 정보를 바탕으로 정리했다.

## 왜 만들었나

zeta4s를 개발한 제타포랩은 LLM과 대화하는 것만으로 데이터 처리 프로세스를 만들고 운영할 수 있는 실행 기반이 필요해 zeta4s를 만들었다고 밝혔다. 사람이 대화로 요구 사항을 설명하면 AI 에이전트가 계약 파일을 작성하고, zeta4s가 그 계약을 검증해 실제 실행까지 맡는 구조다.

## 무엇을 하는 도구인가

zeta4s는 스스로를 "AI Agent가 생성한 계약(Contract)을 Step Graph로 실행하는 범용 Runtime Engine"으로 소개한다. 작업 정의의 정본은 `project.yml`, `jobs/*.yml`, SQL·dbt 파일이고, 데이터베이스 접속 정보는 workspace의 `profiles/`에서 따로 관리한다. [README](https://github.com/zeta4lab/zeta4s/blob/main/README.md)에 따르면 zeta4s의 핵심 책임은 이 계약을 검증 가능한 실행 계약으로 바꾸고, 같은 계약으로 배포·실행·관측하는 것이다.

이렇게 하면 AI 에이전트가 만든 파이프라인도 사람이 쓴 것과 같은 방식으로 실행 전에 정적 검증을 거친다. 예약 실행 도구에 맞춘 코드를 따로 생성할 필요도 없다.

## 주요 기능

[로드맵 문서](https://github.com/zeta4lab/zeta4s/blob/main/docs/roadmap/00-step-graph-runtime-roadmap.md)가 완성된 범위로 밝힌 기능은 다음과 같다.

- **Airflow와 Prefect 동시 지원**: 두 스케줄러를 같은 외부 backend 계약으로 연결한다. profile에서 어느 쪽을 쓸지 고르고, 일정은 같은 시간대 규칙으로 해석한다. 내부 실행 계약(`ExecutionPlan`)은 스케줄러와 독립적이다.
- **내장 step type**: ClickHouse·Oracle·Elasticsearch 추출·적재, SQL·dbt 변환, HTTP 조회(`http.lookup`)를 기본 제공한다.
- **외부 step type 플러그인**: `zeta4s.step_types` entry point를 선언한 Python 패키지를 설치하면 새 step type이 등록되고, CLI·API·Airflow·Prefect에서 내장 type과 같은 계약으로 실행된다.
- **장애 복구**: 스케줄러 실행은 Iceberg snapshot과 step 단위 체크포인트로 외부 backend 장애 뒤에도 같은 실행 안에서 재개한다.
- **비밀 정보 관리**: secret은 AES-GCM 256 keyring으로 암호화하고, 키 회전 시 재암호화한다.
- **배포 구성**: Docker Compose로 로컬 검증 환경을, `deploy/k3s/`로 단일 노드 k3s 배포 구성을 제공한다.

## 설치와 시작

배포물은 두 가지로 나뉜다. 호스트에서 쓰는 `z4s` 명령줄 도구(`zeta4s-cli`)와, API 서버 및 스케줄러 연결 계층(`zeta4s-api`)이다. wheel과 소스 배포본은 [1.0.22 릴리스](https://github.com/zeta4lab/zeta4s/releases/tag/1.0.22)에, `zeta4s-api` 이미지는 `ghcr.io/zeta4lab/zeta4s-api:1.0.22`(linux/amd64, linux/arm64)로 받을 수 있다.

README의 빠른 시작 절차는 다음과 같다.

```bash
bash scripts/install_cli.sh
.venv/bin/z4s work init
.venv/bin/z4s profile init dev
.venv/bin/z4s project init my_project
.venv/bin/z4s project check my_project --profile dev
```

Docker 스택을 띄운 뒤에는 `z4s api deploy`로 프로젝트와 일정을 함께 배포한다.

## 확인할 점

- 프로젝트는 버전 태그가 "구현 묶음의 표식이며 하위 호환 보장을 뜻하지 않는다"고 명시한다. 운영에 쓰려면 사용할 버전을 고정하는 편이 안전하다.
- 기여는 `main`을 향한 pull request로 받으며, `ci`와 Docker 스택 기반 `release-gate` 검사를 통과해야 한다. 작업 원칙은 저장소의 `AGENTS.md`에 있다.
- 라이선스 전문은 [LICENSE](https://github.com/zeta4lab/zeta4s/blob/main/LICENSE)에 있다.

## 출처

- [zeta4lab/zeta4s — GitHub 저장소](https://github.com/zeta4lab/zeta4s)
- [zeta4s README](https://github.com/zeta4lab/zeta4s/blob/main/README.md)
- [Step Graph Runtime Roadmap](https://github.com/zeta4lab/zeta4s/blob/main/docs/roadmap/00-step-graph-runtime-roadmap.md)
- [zeta4s 1.0.22 릴리스](https://github.com/zeta4lab/zeta4s/releases/tag/1.0.22)
- [zeta4s LICENSE (Apache License 2.0)](https://github.com/zeta4lab/zeta4s/blob/main/LICENSE)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
