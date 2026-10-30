---
title: 쿠버네티스는 명령을 실행하지 않고 상태를 맞춘다…지운 Pod이 되살아나는 이유
slug: 2026-10-30-k8s-hands-on-1-declarative-reconcile
topic: cloud
published_at: 2026-10-30T10:50:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - kind
summary: Docker는 써 봤지만 쿠버네티스는 처음인 개발자를 위한 7회 실습 연재의 첫 편. 컨테이너가 늘어나면 생기는 문제, 선언형 설정과 조정 루프(reconciliation)라는 핵심 원리, 노트북에 kind로 실습 클러스터를 만드는 방법을 다룬다.
generated_by: claude
model: claude-opus-5-5
---

# 쿠버네티스는 명령을 실행하지 않고 상태를 맞춘다…지운 Pod이 되살아나는 이유

## 한눈에 보기

컨테이너 하나는 `docker run`으로 충분하다. 문제는 서버 열 대에 컨테이너 백 개를 띄우고, 그중 몇 개가 죽거나 서버 한 대가 꺼져도 서비스가 유지되게 만들 때 생긴다. 쿠버네티스는 이 문제를 "무엇을 하라"는 명령이 아니라 "이런 상태여야 한다"는 선언으로 푼다. 이 연재는 Docker를 써 본 개발자가 노트북 한 대로 쿠버네티스를 직접 만지며 익히도록 7회로 구성했다. 첫 편은 연재 전체를 관통하는 원리인 선언형 설정과 조정 루프를 다루고, 실습 클러스터를 만든다.

연재 순서는 다음과 같다. 1회 선언형과 조정 루프, [2회 클러스터 해부도](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-2-cluster-anatomy), [3회 워크로드 고르기](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-3-workloads), [4회 네트워킹](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-4-networking), [5회 설정과 저장소](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-5-config-storage), [6회 운영과 디버깅](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-6-operations-debugging), [7회 보안과 배포 파이프라인](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-7-security-delivery).

## 컨테이너가 많아지면 생기는 일

컨테이너를 직접 관리하면 사람이 다음 질문에 계속 답해야 한다. 어느 서버에 띄울까, 죽으면 누가 다시 띄울까, 새 버전은 어떻게 하나씩 교체할까, 다른 컨테이너는 바뀌는 IP를 어떻게 찾을까. 쿠버네티스 공식 문서는 쿠버네티스가 제공하는 것으로 서비스 디스커버리와 부하 분산, 스토리지 연결, 자동 롤아웃과 롤백, 자원에 맞춘 배치(bin packing), 자가 치유(self-healing), 시크릿과 설정 관리를 꼽는다([Kubernetes 문서](https://kubernetes.io/docs/concepts/overview/)).

같은 문서는 쿠버네티스가 하지 않는 것도 분명히 적는다. 애플리케이션 소스 코드를 빌드하지 않고, 데이터베이스나 메시지 큐 같은 미들웨어를 기본으로 제공하지 않으며, 로깅·모니터링 솔루션을 정해 주지 않는다. 쿠버네티스는 완성된 플랫폼(PaaS)이 아니라 플랫폼을 만드는 재료에 가깝다. 이 점은 7회에서 "쿠버네티스가 필요 없는 경우"를 다룰 때 다시 꺼낸다.

## 명령형과 선언형

`docker run -d nginx`를 세 번 실행하면 컨테이너가 세 개 생긴다. 이것이 명령형이다. 하나가 죽으면 누군가 다시 실행해야 한다. 쿠버네티스에서는 "nginx가 세 개 떠 있어야 한다"는 문서(매니페스트)를 API 서버에 제출한다. 이것이 선언형이다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.29
```

모든 쿠버네티스 객체에는 사용자가 원하는 상태인 `spec`과 지금 실제 상태인 `status`가 있다. 위 문서에서 `replicas: 3`은 spec이다. 쿠버네티스는 status가 spec과 같아지도록 계속 일한다([Kubernetes 문서](https://kubernetes.io/docs/concepts/overview/working-with-objects/)).

## 조정 루프: 쿠버네티스의 심장

이 "계속 일한다"를 맡는 것이 컨트롤러다. 공식 문서는 컨트롤러를 실내 온도 조절기에 비유한다. 사용자가 원하는 온도를 정하면 온도 조절기는 현재 온도를 재고, 차이가 있으면 난방을 켜거나 끈다. 컨트롤러도 클러스터의 현재 상태를 보고, 원하는 상태와 다르면 그 차이를 줄이는 동작을 한다. 그리고 이 과정을 끝없이 반복한다([Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/controller/)).

이 구조에서 세 가지 성질이 나온다.

- **자가 치유**: Pod 하나가 죽으면 "3개여야 하는데 2개"라는 차이가 생기고, 컨트롤러가 하나를 새로 만든다. 사람이 개입하지 않는다.
- **멱등성**: 같은 매니페스트를 열 번 적용해도 결과는 같다. "3개를 더 만들어라"가 아니라 "3개여야 한다"이기 때문이다.
- **Git으로 관리하기 쉬움**: 원하는 상태가 파일이므로 버전 관리, 코드 리뷰, 롤백이 자연스럽다. 7회에서 다룰 GitOps가 여기서 출발한다.

## 실습 1: kind로 클러스터 만들기

kind(Kubernetes in Docker)는 Docker 컨테이너를 노드처럼 써서 노트북에 쿠버네티스 클러스터를 띄우는 도구다. 쿠버네티스 자체를 테스트하려고 만든 도구라 가볍고 빠르다. 2026년 10월 현재 최신 안정 버전은 v0.33.0이고, 기본 노드 이미지는 쿠버네티스 v1.37.0이다([kind](https://kind.sigs.k8s.io/docs/user/quick-start/)). Docker(또는 Podman)와 `kubectl`이 필요하다.

```bash
# macOS 예시. 다른 OS는 kind 빠른 시작 문서를 따른다.
brew install kind kubectl
kind create cluster --name lab
kubectl cluster-info --context kind-lab
kubectl get nodes
```

`kubectl get nodes`에 `lab-control-plane` 노드가 `Ready`로 보이면 준비가 끝났다. 연재의 모든 실습은 이 클러스터에서 한다. 다 쓰면 `kind delete cluster --name lab`으로 지운다.

## 실습 2: Pod을 지워 보기

위의 Deployment 매니페스트를 `web.yaml`로 저장하고 적용한다.

```bash
kubectl apply -f web.yaml
kubectl get pods -l app=web
```

Pod 세 개가 `Running`이 되면, 터미널 하나에서 `kubectl get pods -l app=web -w`로 지켜보면서 다른 터미널에서 하나를 지운다.

```bash
kubectl delete pod <pod 이름 하나>
```

지운 Pod이 `Terminating`이 되는 것과 거의 동시에 새 이름의 Pod이 `ContainerCreating`을 거쳐 `Running`이 된다. 누구도 "다시 만들어라"라고 명령하지 않았다. 컨트롤러가 "3개여야 하는데 2개"를 보고 차이를 메웠을 뿐이다. 이번에는 `web.yaml`의 `replicas`를 5로 고쳐 다시 `kubectl apply`하면 두 개가 늘어난다. 같은 파일을 한 번 더 적용하면 아무 일도 일어나지 않는다.

## 버전을 읽는 법

쿠버네티스 프로젝트는 가장 최근 세 개의 마이너 버전에 릴리스 브랜치를 유지하고, 1.19 이후 버전은 약 1년 동안 패치를 받는다([Kubernetes](https://kubernetes.io/releases/)). 마이너 버전은 대체로 1년에 세 번 나온다. 2026년 10월 현재 1.37, 1.36, 1.35가 유지보수 중이고, 1.34는 2026년 10월 27일에 지원이 끝났다. 관리형 서비스는 자체 지원 일정을 따로 두므로, 실제 운영에서는 쓰는 클라우드의 정책을 확인해야 한다. AKS의 경우는 [AKS 입문 1회](https://now.zeta4.net/a/2026-10-30-aks-101-what-aks-manages)에서 정리했다.

## 정리

- 쿠버네티스에 주는 것은 명령이 아니라 원하는 상태다. 객체의 `spec`이 원하는 상태, `status`가 현재 상태다.
- 컨트롤러는 둘의 차이를 끝없이 줄인다. 자가 치유, 멱등성, GitOps가 모두 여기서 나온다.
- 실습 클러스터는 `kind create cluster --name lab` 한 줄이면 된다.

다음 회에서는 `kubectl apply` 한 번에 클러스터 안의 어떤 부품이 어떤 순서로 움직이는지 따라간다.

## 출처

- [Overview — Kubernetes 문서](https://kubernetes.io/docs/concepts/overview/)
- [Objects In Kubernetes — Kubernetes 문서](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [Controllers — Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Releases — Kubernetes](https://kubernetes.io/releases/)
- [kind Quick Start — kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [kind 기본 노드 이미지 정의 — kubernetes-sigs/kind](https://github.com/kubernetes-sigs/kind/blob/main/pkg/apis/config/defaults/image.go)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
