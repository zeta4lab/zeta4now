---
title: kubectl apply 한 번에 부품 다섯 개가 움직인다…API 서버·etcd·스케줄러·컨트롤러·kubelet의 분업
slug: 2026-10-30-k8s-hands-on-2-cluster-anatomy
topic: cloud
published_at: 2026-10-30T10:51:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - kubectl
summary: 「쿠버네티스 손으로 익히기」 2회. 컨트롤 플레인(kube-apiserver, etcd, kube-scheduler, kube-controller-manager)과 노드(kubelet, 컨테이너 런타임, kube-proxy)의 역할을 정리하고, Deployment 하나를 적용했을 때 Pod이 실행되기까지의 순서를 kind 클러스터에서 직접 추적한다.
generated_by: claude
model: claude-opus-5-5
---

# kubectl apply 한 번에 부품 다섯 개가 움직인다…API 서버·etcd·스케줄러·컨트롤러·kubelet의 분업

## 한눈에 보기

[1회](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile)에서 쿠버네티스는 원하는 상태를 받아 컨트롤러가 현재 상태를 맞춘다고 했다. 이번 회는 그 일을 실제로 나눠 맡는 부품들을 연다. 핵심은 하나다. 모든 부품은 API 서버를 통해서만 대화하고, 서로에게 직접 명령하지 않는다. 각자 API 서버를 지켜보다가 자기 일이 생기면 처리하고 결과를 다시 API 서버에 적는다. 이 구조를 알면 6회에서 다룰 장애 진단이 훨씬 쉬워진다.

연재 순서: [1회 선언형과 조정 루프](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile), 2회 클러스터 해부도, [3회 워크로드 고르기](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-3-workloads), [4회 네트워킹](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-4-networking), [5회 설정과 저장소](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-5-config-storage), [6회 운영과 디버깅](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-6-operations-debugging), [7회 보안과 배포 파이프라인](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-7-security-delivery).

## 두 구역: 컨트롤 플레인과 노드

쿠버네티스 클러스터는 클러스터 전체를 결정하는 컨트롤 플레인과, 실제로 컨테이너를 돌리는 워커 노드로 나뉜다([Kubernetes 문서](https://kubernetes.io/docs/concepts/overview/components/)).

| 구역 | 부품 | 하는 일 |
|---|---|---|
| 컨트롤 플레인 | kube-apiserver | 클러스터의 유일한 입구. 인증·인가·검증을 거쳐 객체를 저장하고 변경을 알린다 |
| 컨트롤 플레인 | etcd | 클러스터의 모든 상태를 담는 키-값 저장소. API 서버만 직접 접근한다 |
| 컨트롤 플레인 | kube-scheduler | 아직 노드가 정해지지 않은 Pod에 알맞은 노드를 고른다 |
| 컨트롤 플레인 | kube-controller-manager | Deployment, ReplicaSet, Node 등 여러 컨트롤러를 한 프로세스로 돌린다 |
| 컨트롤 플레인 | cloud-controller-manager | 클라우드에서만 쓴다. 로드밸런서, 노드 수명 같은 클라우드 API 연동을 맡는다 |
| 노드 | kubelet | 자기 노드에 배정된 Pod의 컨테이너를 실제로 띄우고 상태를 보고한다 |
| 노드 | 컨테이너 런타임 | containerd, CRI-O 등. kubelet이 CRI라는 표준 인터페이스로 호출한다 |
| 노드 | kube-proxy | Service로 들어온 트래픽을 Pod으로 보내는 규칙을 노드에 만든다. 일부 네트워크 플러그인은 이 역할을 대신한다 |

관리형 쿠버네티스(AKS, EKS, GKE)에서는 컨트롤 플레인을 클라우드가 운영하므로 사용자는 노드 구역만 보게 된다. 그래도 부품의 역할은 같다.

## Deployment 하나가 실행되기까지

`kubectl apply -f web.yaml`을 실행하면 다음 순서로 일이 진행된다.

1. **kubectl → API 서버**: kubectl이 매니페스트를 HTTPS 요청으로 보낸다. API 서버는 요청자가 누구인지(인증), 이 일을 해도 되는지(인가, 7회의 RBAC), 내용이 정책에 맞는지(어드미션 컨트롤)를 확인한 뒤 Deployment 객체를 etcd에 저장한다.
2. **Deployment 컨트롤러**: 새 Deployment를 보고, 그에 맞는 ReplicaSet 객체를 API 서버에 만든다.
3. **ReplicaSet 컨트롤러**: ReplicaSet이 원하는 개수만큼 Pod 객체를 만든다. 이 시점의 Pod에는 실행할 노드(`spec.nodeName`)가 비어 있다.
4. **스케줄러**: 노드가 비어 있는 Pod을 발견하고, 자원 요청량, 노드 조건, 친화성 규칙을 따져 노드를 고른 뒤 결과를 API 서버에 기록(binding)한다.
5. **kubelet**: 자기 노드에 배정된 Pod을 발견하고, 컨테이너 런타임에 이미지를 받아 컨테이너를 띄우라고 요청한다. 실행 결과는 Pod의 `status`로 API 서버에 보고한다.

이 다섯 단계에서 누구도 다음 단계를 직접 호출하지 않는다는 점이 중요하다. 각 부품은 API 서버에 걸어 둔 watch로 변경을 알아차린다. 그래서 스케줄러가 잠시 멈춰도 Pod 객체는 그대로 남아 있다가, 스케줄러가 돌아오면 이어서 처리된다. 이것이 1회에서 본 조정 루프가 클러스터 전체 규모로 동작하는 모습이다([Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/controller/)).

## 실습 1: 컨트롤 플레인 들여다보기

kind 클러스터의 컨트롤 플레인 부품은 `kube-system` 네임스페이스의 Pod으로 떠 있다.

```bash
kubectl get pods -n kube-system -o wide
```

`etcd-lab-control-plane`, `kube-apiserver-lab-control-plane`, `kube-scheduler-lab-control-plane`, `kube-controller-manager-lab-control-plane`, 그리고 노드마다 하나씩 뜨는 `kube-proxy-*`가 보인다. 컨트롤 플레인 부품은 kubelet이 노드의 파일(`/etc/kubernetes/manifests`)을 읽어 직접 띄우는 정적 Pod(static Pod)이다. kind의 노드는 Docker 컨테이너이므로 안으로 들어가 확인할 수 있다.

```bash
docker exec lab-control-plane ls /etc/kubernetes/manifests
docker exec lab-control-plane crictl ps
```

`crictl ps`는 kubelet이 컨테이너 런타임(containerd)에 띄운 컨테이너 목록이다. `docker ps`가 아니라 `crictl`인 이유는 쿠버네티스가 Docker가 아니라 CRI 표준으로 런타임과 대화하기 때문이다([Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/cri/)).

## 실습 2: 이벤트로 순서 추적하기

1회의 Deployment를 지우고, 이벤트를 지켜보면서 다시 적용한다.

```bash
kubectl delete -f web.yaml
kubectl get events -w &
kubectl apply -f web.yaml
```

이벤트의 `OBJECT`와 `REASON` 열을 보면 위의 순서가 그대로 드러난다. Deployment에 `ScalingReplicaSet`, ReplicaSet에 `SuccessfulCreate`(Pod 생성), Pod에 `Scheduled`(노드 배정)가 남고, 이어서 kubelet이 남기는 `Pulling`, `Pulled`, `Created`, `Started`가 차례로 나온다. 어느 부품이 남긴 이벤트인지까지 보려면 `kubectl get events -o wide`의 `SOURCE` 열을 본다. 확인이 끝나면 `kill %1`로 감시를 멈춘다.

객체 사이의 소유 관계도 확인해 보자.

```bash
kubectl get pod -l app=web -o jsonpath='{.items[0].metadata.ownerReferences[0].kind}{"\n"}'
kubectl get rs -l app=web -o jsonpath='{.items[0].metadata.ownerReferences[0].kind}{"\n"}'
```

Pod의 주인은 `ReplicaSet`, ReplicaSet의 주인은 `Deployment`로 나온다. Deployment를 지우면 소유 관계를 따라 ReplicaSet과 Pod이 함께 정리된다(가비지 컬렉션).

## 정리

- 모든 부품은 API 서버를 거쳐서만 대화하고, 상태는 etcd 한 곳에 있다.
- `apply` 한 번은 API 서버 저장 → Deployment 컨트롤러 → ReplicaSet 컨트롤러 → 스케줄러 → kubelet 순으로 이어진다.
- 문제가 생기면 이 사슬의 어디서 멈췄는지를 이벤트로 찾는다. 노드가 안 정해졌으면 스케줄러 단계, 이미지를 못 받으면 kubelet 단계다.

다음 회에서는 Deployment 말고도 Job, StatefulSet, DaemonSet 같은 워크로드를 언제 쓰는지, 그리고 배포를 되돌리는 법을 다룬다.

## 출처

- [Kubernetes Components — Kubernetes 문서](https://kubernetes.io/docs/concepts/overview/components/)
- [Cluster Architecture — Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/)
- [Controllers — Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Container Runtime Interface (CRI) — Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/cri/)
- [Garbage Collection — Kubernetes 문서](https://kubernetes.io/docs/concepts/architecture/garbage-collection/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
