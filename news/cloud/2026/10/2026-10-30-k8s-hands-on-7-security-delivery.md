---
title: kubectl을 손에서 놓는 것이 마지막 단계다…RBAC·Pod 보안·Helm·GitOps, 그리고 쿠버네티스가 필요 없는 경우
slug: 2026-10-30-k8s-hands-on-7-security-delivery
topic: cloud
published_at: 2026-10-30T10:56:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - GitOps
summary: 「쿠버네티스 손으로 익히기」 마지막 7회. RBAC와 ServiceAccount로 권한을 최소화하고 Pod Security Standards로 위험한 Pod을 막는 법, Helm과 Kustomize로 매니페스트를 패키징하고 Argo CD·Flux로 Git을 배포의 기준으로 삼는 GitOps를 정리한 뒤, 쿠버네티스를 고르지 않는 편이 나은 경우를 짚는다.
generated_by: claude
model: claude-opus-5-5
---

# kubectl을 손에서 놓는 것이 마지막 단계다…RBAC·Pod 보안·Helm·GitOps, 그리고 쿠버네티스가 필요 없는 경우

## 한눈에 보기

지금까지는 관리자 권한으로 `kubectl`을 직접 쳐서 클러스터를 바꿨다. 혼자 쓰는 실습 클러스터에서는 괜찮지만, 팀이 운영하는 클러스터에서는 두 가지가 문제가 된다. 누구나 무엇이든 할 수 있다는 것, 그리고 클러스터의 실제 상태가 누가 언제 친 명령의 누적이라 아무도 전체를 모른다는 것이다. 마지막 회는 권한을 좁히는 RBAC와 Pod 보안, 그리고 Git에 적힌 상태만 클러스터에 반영되게 하는 패키징과 GitOps를 다룬다. 끝으로 쿠버네티스를 쓰지 않는 편이 나은 경우를 정리한다.

연재 순서: [1회 선언형과 조정 루프](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile), [2회 클러스터 해부도](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-2-cluster-anatomy), [3회 워크로드 고르기](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-3-workloads), [4회 네트워킹](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-4-networking), [5회 설정과 저장소](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-5-config-storage), [6회 운영과 디버깅](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-6-operations-debugging), 7회 보안과 배포 파이프라인.

## RBAC: 누가 무엇을 할 수 있나

2회에서 API 서버는 모든 요청에 대해 "이 일을 해도 되는가"를 확인한다고 했다. 그 판단 규칙이 RBAC(Role-Based Access Control)다. 네 객체로 구성된다([Kubernetes 문서](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)).

- **Role / ClusterRole**: 허용할 동작의 목록. 예를 들어 "Pod을 조회(get, list, watch)할 수 있다". Role은 한 네임스페이스 안에서, ClusterRole은 클러스터 전체에서 쓴다.
- **RoleBinding / ClusterRoleBinding**: 그 목록을 사용자, 그룹, ServiceAccount에 연결한다.

사람이 아니라 Pod 안의 앱이 API 서버를 부를 때는 ServiceAccount라는 신원을 쓴다. 모든 네임스페이스에는 `default` ServiceAccount가 있고, 따로 지정하지 않은 Pod은 이것을 쓴다. 앱마다 전용 ServiceAccount를 만들고 꼭 필요한 권한만 붙이는 것이 원칙이다. API 서버를 부를 일이 없는 앱이라면 `automountServiceAccountToken: false`로 토큰을 아예 넣지 않는다([Kubernetes 문서](https://kubernetes.io/docs/concepts/security/service-accounts/)).

```bash
kubectl create namespace team-a
kubectl -n team-a create serviceaccount reader
kubectl -n team-a create role pod-reader --verb=get,list,watch --resource=pods
kubectl -n team-a create rolebinding reader-can-read --role=pod-reader --serviceaccount=team-a:reader
kubectl auth can-i list pods -n team-a --as=system:serviceaccount:team-a:reader
kubectl auth can-i delete pods -n team-a --as=system:serviceaccount:team-a:reader
kubectl auth can-i list secrets -n team-a --as=system:serviceaccount:team-a:reader
```

첫 줄은 `yes`, 나머지 두 줄은 `no`가 나온다. 5회에서 Secret을 읽을 권한을 좁히라고 한 것이 바로 이 작업이다. `kubectl auth can-i`는 권한을 설계할 때와 "왜 거부되지?"를 조사할 때 모두 쓰인다.

## Pod Security Standards: 위험한 Pod을 입구에서 막기

RBAC는 누가 Pod을 만들 수 있는지를 정하지만, 어떤 Pod을 만들 수 있는지는 정하지 않는다. 특권(privileged) 컨테이너나 노드의 파일 시스템을 마운트한 Pod은 노드 전체를 장악할 수 있다. 쿠버네티스는 Pod 보안 수준을 세 단계로 정의하고, 내장된 Pod Security Admission이 네임스페이스 레이블에 따라 이를 강제한다([Kubernetes 문서](https://kubernetes.io/docs/concepts/security/pod-security-standards/)).

| 수준 | 의미 |
|---|---|
| privileged | 제한 없음. 시스템 구성 요소용 |
| baseline | 알려진 권한 상승 경로(특권 컨테이너, 호스트 네트워크 등)를 막는 최소 기준 |
| restricted | root가 아닌 사용자로 실행, 권한(capabilities) 제거 등 강화된 기준 |

```bash
kubectl label namespace team-a pod-security.kubernetes.io/enforce=restricted
kubectl -n team-a run web --image=nginx:1.29
```

두 번째 명령은 거부되고, 메시지에 restricted 기준의 어느 항목을 어겼는지가 나열된다. `kubectl run`으로 만든 Pod에는 restricted가 요구하는 보안 설정이 하나도 적혀 있지 않기 때문이다. 기준을 맞추려면 root가 아닌 사용자로 동작하는 이미지를 쓰고 `securityContext`에 `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, `seccompProfile.type: RuntimeDefault`를 적어 기준을 맞춘다. 처음 도입할 때는 `enforce` 대신 `warn`이나 `audit` 레이블로 경고만 받아 보며 기존 워크로드를 정리하는 방법을 권한다.

## 매니페스트 패키징: Helm과 Kustomize

연재를 따라오면서 YAML이 꽤 쌓였다. 환경마다 이미지 태그, 복제본 수, 도메인만 다른 YAML을 복사해 관리하면 금방 어긋난다. 두 가지 대표 도구가 있다.

- **Helm**: 템플릿 방식의 패키지 관리자. 매니페스트를 템플릿으로 만들고 `values.yaml`로 값을 바꿔 끼운다. 이렇게 묶은 것을 차트(chart)라 하고, 설치한 인스턴스를 릴리스(release)라 한다. 공개된 차트로 다른 사람이 만든 소프트웨어를 설치할 때도 쓴다. 2026년 10월 현재 최신 버전은 v4.3.1이다([Helm](https://helm.sh/docs/), [GitHub 릴리스](https://github.com/helm/helm/releases)).
- **Kustomize**: 템플릿 없이 기본 YAML(base) 위에 환경별 차이(overlay)를 덧붙이는 방식. `kubectl`에 내장되어 있어 `kubectl apply -k <디렉터리>`로 바로 쓴다([Kubernetes 문서](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)).

```bash
helm create webchart
helm install web-dev ./webchart --set replicaCount=2 -n team-dev --create-namespace
helm upgrade web-dev ./webchart --set image.tag=1.29-alpine -n team-dev
helm history web-dev -n team-dev
helm rollback web-dev 1 -n team-dev
```

`helm create`가 만든 기본 차트에는 지금까지 다룬 Deployment, Service, ServiceAccount, HPA, probe가 모두 들어 있다. `templates/` 디렉터리를 열어 1~6회에서 본 필드를 찾아보면 좋은 복습이 된다. 기본 차트의 nginx 이미지는 root로 실행되므로, 앞에서 restricted 레이블을 붙인 `team-a`가 아니라 새 네임스페이스에 설치했다. 외부 차트를 쓸지 직접 만들지는 팀 상황에 따르지만, 일반적으로 우리 앱은 Kustomize나 단순한 자체 차트로, 남이 만든 소프트웨어는 공식 Helm 차트로 설치하는 조합이 많다.

## GitOps: Git이 기준이 되게

3회에서 `kubectl rollout undo`는 클러스터만 되돌리고 파일은 그대로라고 했다. GitOps는 이 어긋남을 구조적으로 없앤다. 원하는 상태를 Git 저장소에 두고, 클러스터 안의 에이전트가 저장소를 지켜보다가 클러스터를 그 상태에 맞춘다. 1회의 조정 루프를 Git과 클러스터 사이로 넓힌 것이다. 배포는 `kubectl apply`가 아니라 Git 커밋과 리뷰가 되고, 롤백은 `git revert`가 된다. 누가 클러스터에서 직접 무언가를 바꾸면 에이전트가 차이를 감지해 알리거나 되돌린다.

대표 도구는 Argo CD와 Flux다. 둘 다 CNCF 졸업(graduated) 프로젝트다([CNCF Argo](https://www.cncf.io/projects/argo/), [CNCF Flux](https://www.cncf.io/projects/flux/)). Argo CD는 동기화 상태를 보여 주는 웹 화면이 강점이고, Flux는 쿠버네티스 컨트롤러 묶음으로 가볍게 동작한다. 둘 다 Helm 차트와 Kustomize를 그대로 읽는다. GitOps를 쓰면 사람의 `kubectl` 쓰기 권한을 대부분 회수하고 조회 권한만 남길 수 있다. 앞의 RBAC와 이렇게 이어진다.

## 쿠버네티스가 필요 없는 경우

1회에서 쿠버네티스는 완성된 플랫폼이 아니라 플랫폼을 만드는 재료라고 했다. 재료를 다룰 사람과 시간이 없다면 다른 선택이 낫다.

- **서비스가 한두 개이고 팀이 작다**: Google Cloud Run, Azure Container Apps, AWS App Runner나 Fly.io 같은 컨테이너 실행 서비스가 운영 부담이 훨씬 적다.
- **운영 담당자가 없다**: 3회의 롤백, 5회의 Secret 암호화, 6회의 진단, 그리고 1년에 한 번 이상 돌아오는 버전 업그레이드를 맡을 사람이 필요하다. 관리형 쿠버네티스도 이 일을 대신하지 않는다([AKS 입문 1회](https://now.zeta4.net/a/2026-10-30-aks-101-what-aks-manages)).
- **상태가 핵심인 시스템 하나뿐이다**: 데이터베이스를 쿠버네티스에 올려 직접 운영하는 것보다 관리형 DB가 대개 안전하다.

반대로 서비스가 많고, 여러 팀이 같은 플랫폼에서 배포 방식과 보안 기준을 통일해야 하며, 특정 클라우드에 묶이지 않고 싶다면 쿠버네티스가 그 비용을 충분히 갚는다. 그 판단을 내릴 수 있게 된 것이 이 연재의 목표였다.

## 연재를 마치며

7회 동안 다룬 것을 한 줄씩 묶으면 다음과 같다.

1. 쿠버네티스는 원하는 상태를 받아 조정 루프로 맞춘다.
2. 모든 부품은 API 서버를 거쳐 대화한다.
3. Pod은 직접 만들지 않고 워크로드로 관리하며, 배포는 되돌릴 수 있어야 한다.
4. Pod IP 대신 Service 이름을 부르고, 바깥 입구는 Gateway API로 연다.
5. 설정·비밀값·데이터는 Pod 밖에 두고, Secret은 기본으로 암호화되지 않음을 기억한다.
6. requests, probe, 진단 순서가 운영의 기본기다.
7. 권한은 최소로, 배포는 Git으로.

실습 클러스터는 `kind delete cluster --name lab`으로 지운다. 실제 클라우드에서 이어 가려면 [AKS 입문 연재](https://now.zeta4.net/a/2026-10-30-aks-101-what-aks-manages)가 이 연재의 다음 단계로 이어진다.

## 출처

- [Using RBAC Authorization — Kubernetes 문서](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Service Accounts — Kubernetes 문서](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [Pod Security Standards — Kubernetes 문서](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Pod Security Admission — Kubernetes 문서](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- [Declarative Management of Kubernetes Objects Using Kustomize — Kubernetes 문서](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Helm 문서 — Helm](https://helm.sh/docs/)
- [Helm 릴리스 — helm/helm](https://github.com/helm/helm/releases)
- [Argo — CNCF](https://www.cncf.io/projects/argo/)
- [Flux — CNCF](https://www.cncf.io/projects/flux/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
