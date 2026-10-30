---
title: Pod을 직접 만들지 마라…Deployment로 롤링 업데이트하고 잘못된 배포를 되돌리는 법
slug: 2026-10-30-k8s-hands-on-3-workloads
topic: cloud
published_at: 2026-10-30T10:52:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - Deployment
summary: 「쿠버네티스 손으로 익히기」 3회. Pod·ReplicaSet·Deployment의 관계와 롤링 업데이트 설정, 일부러 잘못된 이미지로 배포한 뒤 롤백하는 실습, 그리고 Job·CronJob·StatefulSet·DaemonSet을 언제 쓰는지 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# Pod을 직접 만들지 마라…Deployment로 롤링 업데이트하고 잘못된 배포를 되돌리는 법

## 한눈에 보기

쿠버네티스에서 컨테이너가 실행되는 최소 단위는 Pod이지만, 운영에서 Pod을 직접 만드는 일은 거의 없다. Pod은 한 번 노드에 배정되면 그 노드에서 끝까지 살다가 사라지는 일회용 객체이고, 직접 만든 Pod은 죽어도 아무도 다시 만들지 않는다. 그래서 Pod을 대신 만들고 관리하는 워크로드 객체를 쓴다. 이번 회는 가장 많이 쓰는 Deployment로 업데이트와 롤백을 실습하고, 나머지 워크로드를 고르는 기준을 정리한다.

연재 순서: [1회 선언형과 조정 루프](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile), [2회 클러스터 해부도](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-2-cluster-anatomy), 3회 워크로드 고르기, [4회 네트워킹](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-4-networking), [5회 설정과 저장소](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-5-config-storage), [6회 운영과 디버깅](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-6-operations-debugging), [7회 보안과 배포 파이프라인](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-7-security-delivery).

## Pod, ReplicaSet, Deployment

Pod은 하나 이상의 컨테이너를 묶은 단위다. 같은 Pod의 컨테이너는 네트워크(IP와 포트 공간)와 볼륨을 공유한다. 보통은 컨테이너 하나에 Pod 하나지만, 로그 수집기나 프록시처럼 본 컨테이너를 돕는 사이드카를 함께 넣기도 한다([Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/)).

ReplicaSet은 "이 템플릿의 Pod이 N개 떠 있어야 한다"를 지키는 객체다. Deployment는 ReplicaSet 위에서 버전 교체를 관리한다. 이미지를 바꾸면 Deployment는 새 ReplicaSet을 만들고, 새 쪽을 늘리면서 옛 쪽을 줄인다. 옛 ReplicaSet은 0개로 줄인 채 남겨 두기 때문에 언제든 되돌릴 수 있다([Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)).

## 롤링 업데이트의 두 손잡이

Deployment의 기본 전략은 `RollingUpdate`이고, 교체 속도를 두 값으로 조절한다.

- `maxSurge`: 업데이트 중 원하는 개수보다 최대 몇 개를 더 띄울 수 있는가. 기본값 25%.
- `maxUnavailable`: 업데이트 중 원하는 개수보다 최대 몇 개가 모자라도 되는가. 기본값 25%.

```yaml
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

위처럼 `maxUnavailable: 0`이면 새 Pod이 준비되기 전에는 옛 Pod을 하나도 내리지 않는다. 느리지만 가용성이 가장 안전하다. 반대로 자원이 빠듯한 클러스터에서는 `maxSurge: 0`으로 새 Pod을 먼저 띄우지 않게 할 수 있다. 모든 Pod을 한꺼번에 내리고 다시 띄우는 `Recreate` 전략도 있는데, 두 버전이 동시에 떠 있으면 안 되는 앱에 쓴다. 여기서 "준비됐다"는 판단은 6회에서 다룰 readiness probe가 결정한다.

## 실습: 망가뜨리고 되돌리기

1회의 `web` Deployment에 위의 `strategy` 블록과 `replicas: 4`를 넣고 적용한 뒤, 이미지를 정상 버전으로 한 번 올린다. `--record` 플래그는 폐기되었으므로, 변경 이유는 `kubernetes.io/change-cause` 주석으로 남긴다.

```bash
kubectl apply -f web.yaml
kubectl set image deployment/web nginx=nginx:1.29-alpine
kubectl annotate deployment/web kubernetes.io/change-cause="alpine 이미지로 교체"
kubectl rollout status deployment/web
kubectl rollout history deployment/web
```

이제 존재하지 않는 태그로 배포해 보자.

```bash
kubectl set image deployment/web nginx=nginx:does-not-exist
kubectl get pods -l app=web
kubectl rollout status deployment/web --timeout=60s
```

새 Pod 하나가 `ErrImagePull`을 거쳐 `ImagePullBackOff`에 머물고, 옛 Pod 네 개는 그대로 `Running`이다. `maxUnavailable: 0` 덕분에 새 Pod이 준비되지 않으면 옛 Pod을 내리지 않기 때문이다. 서비스는 끊기지 않았지만 배포는 멈췄다. 기본 설정에서 Deployment는 600초(`progressDeadlineSeconds`) 동안 진행이 없으면 상태에 `ProgressDeadlineExceeded`를 남긴다. 자동으로 되돌리지는 않으므로 직접 되돌린다.

```bash
kubectl rollout undo deployment/web
kubectl rollout status deployment/web
kubectl get rs -l app=web
```

`kubectl get rs`를 보면 버전마다 ReplicaSet이 하나씩 남아 있고, 지금 쓰는 하나만 4개를 갖고 있다. 특정 버전으로 가려면 `kubectl rollout undo deployment/web --to-revision=<번호>`를 쓴다. 다만 이 방식은 클러스터만 되돌리고 `web.yaml` 파일은 그대로다. 파일과 클러스터가 어긋나는 문제는 7회의 GitOps에서 해결한다.

## 나머지 워크로드는 언제 쓰나

| 워크로드 | 이럴 때 쓴다 | 핵심 특징 |
|---|---|---|
| Deployment | 웹 서버, API처럼 상태를 Pod 밖에 두는 앱 | Pod은 서로 바꿔 써도 된다. 이름이 무작위다 |
| StatefulSet | 데이터베이스, 메시지 브로커처럼 각 인스턴스가 고유한 앱 | `db-0`, `db-1`처럼 고정된 이름과 순서, Pod마다 따로 붙는 볼륨 |
| DaemonSet | 로그 수집기, 모니터링 에이전트처럼 노드마다 하나씩 필요한 것 | 노드가 늘면 자동으로 따라 붙는다 |
| Job | 마이그레이션, 일괄 처리처럼 끝나는 작업 | 성공할 때까지 재시도하고 완료되면 멈춘다 |
| CronJob | 매일 밤 백업처럼 주기적인 작업 | 일정마다 Job을 만든다 |

([Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/))

입문자가 흔히 하는 실수는 데이터베이스를 Deployment로 띄우는 것이다. 복제본이 하나면 당장은 돌아가지만, Pod이 바뀔 때 볼륨을 누가 쥐는지, 복제본을 늘리면 데이터가 어떻게 되는지가 정의되지 않는다. StatefulSet은 이 문제를 위해 만들어졌다. 그래도 운영 데이터베이스는 클라우드의 관리형 DB를 쓰는 편이 대개 더 안전하다.

Job은 간단히 확인해 볼 수 있다.

```bash
kubectl create job hello --image=busybox:1.37 -- sh -c 'echo 안녕, 쿠버네티스; sleep 3'
kubectl get job hello -w
kubectl logs job/hello
```

`COMPLETIONS`가 `1/1`이 되면 Pod은 `Completed` 상태로 남고 로그를 읽을 수 있다.

## 정리

- Pod은 직접 만들지 않는다. 오래 도는 앱은 Deployment, 고유한 인스턴스가 필요하면 StatefulSet, 노드마다는 DaemonSet, 끝나는 작업은 Job이다.
- 롤링 업데이트 속도는 `maxSurge`와 `maxUnavailable`로 조절한다. 가용성이 중요하면 `maxUnavailable: 0`.
- 배포가 실패해도 쿠버네티스는 자동으로 되돌리지 않는다. `kubectl rollout undo`를 손에 익혀 둔다.

다음 회에서는 이렇게 떠 있는 Pod들을 다른 Pod과 바깥 세상이 어떻게 찾아오는지, Service와 DNS, Gateway API를 다룬다.

## 출처

- [Pods — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Deployments — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Workload Management — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/)
- [StatefulSets — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Jobs — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/controllers/job/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
