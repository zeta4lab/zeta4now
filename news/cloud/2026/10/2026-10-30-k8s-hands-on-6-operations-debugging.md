---
title: Pending·CrashLoopBackOff·ImagePullBackOff를 고치는 순서…자원 요청량, 헬스 체크, 자동 확장까지
slug: 2026-10-30-k8s-hands-on-6-operations-debugging
topic: cloud
published_at: 2026-10-30T10:55:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - 디버깅
summary: 「쿠버네티스 손으로 익히기」 6회. requests와 limits가 스케줄링과 OOMKilled에 미치는 영향, liveness·readiness·startup probe의 차이, metrics-server와 HPA로 하는 자동 확장을 정리하고, 일부러 세 가지 방식으로 고장 낸 Pod을 get→describe→logs 순서로 진단한다.
generated_by: claude
model: claude-opus-5-5
---

# Pending·CrashLoopBackOff·ImagePullBackOff를 고치는 순서…자원 요청량, 헬스 체크, 자동 확장까지

## 한눈에 보기

지금까지 만든 앱은 노트북에서는 잘 돌지만, 운영에 올리려면 세 가지가 더 필요하다. 쿠버네티스가 자리를 제대로 잡도록 자원 요청량을 알려 주고, 앱이 살아 있는지와 트래픽을 받을 준비가 됐는지를 헬스 체크로 알려 주고, 부하에 따라 Pod 수를 조절하는 것이다. 그리고 무엇보다 고장 났을 때 원인을 찾는 순서가 몸에 배어 있어야 한다. 이번 회는 그 순서를 일부러 고장 낸 Pod으로 연습한다.

연재 순서: [1회 선언형과 조정 루프](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile), [2회 클러스터 해부도](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-2-cluster-anatomy), [3회 워크로드 고르기](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-3-workloads), [4회 네트워킹](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-4-networking), [5회 설정과 저장소](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-5-config-storage), 6회 운영과 디버깅, [7회 보안과 배포 파이프라인](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-7-security-delivery).

## requests와 limits

컨테이너마다 CPU와 메모리를 두 값으로 적는다([Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)).

- `requests`: 이만큼은 꼭 필요하다는 예약. 스케줄러는 노드에 남은 requests 여유를 보고 Pod을 배치한다. 실제 사용량이 아니라 예약 합계로 판단한다는 점이 중요하다.
- `limits`: 이 이상은 쓰지 못하게 하는 상한. CPU는 상한에 닿으면 느려지고(throttling), 메모리는 상한을 넘으면 컨테이너가 강제 종료된다(`OOMKilled`).

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    memory: 256Mi
```

`100m`은 CPU 코어 0.1개다. 두 값을 어떻게 적었느냐에 따라 Pod의 QoS 등급이 정해진다. 모든 컨테이너의 requests와 limits가 같으면 `Guaranteed`, 일부만 적었으면 `Burstable`, 아무것도 없으면 `BestEffort`다. 노드 메모리가 모자라면 `BestEffort`부터 쫓겨난다([Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)). 그러니 운영 Pod에는 최소한 requests를 적는다.

## 세 가지 probe

kubelet은 probe로 컨테이너 상태를 주기적으로 확인한다. 셋은 목적이 다르다([Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)).

| probe | 실패하면 | 쓰임 |
|---|---|---|
| liveness | 컨테이너를 재시작한다 | 교착 상태처럼 프로세스는 살아 있지만 회복할 수 없는 상태를 끊는다 |
| readiness | Service 대상에서 뺀다(재시작하지 않음) | 시작 직후나 일시적 과부하 때 트래픽을 받지 않게 한다. 3회의 롤링 업데이트도 이 값을 기다린다 |
| startup | 성공할 때까지 나머지 probe를 미룬다 | 시작이 오래 걸리는 앱이 liveness에 걸려 계속 재시작되는 것을 막는다 |

```yaml
readinessProbe:
  httpGet:
    path: /
    port: 80
  periodSeconds: 5
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 10
  periodSeconds: 10
```

흔한 실수는 liveness probe가 데이터베이스 같은 외부 의존성까지 확인하게 만드는 것이다. DB가 잠깐 느려지면 모든 Pod이 동시에 재시작되어 장애가 커진다. liveness는 "이 프로세스 자체가 살아 있는가"만 묻고, 의존성 확인은 readiness에 둔다.

## 자동 확장: HPA

HorizontalPodAutoscaler(HPA)는 CPU 사용률 같은 지표를 보고 Deployment의 `replicas`를 조절하는 컨트롤러다. 사용률은 requests 대비로 계산하므로, requests가 없으면 HPA가 동작하지 않는다. 지표는 metrics-server가 모은다([Kubernetes 문서](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)). kind에는 metrics-server가 없으므로 설치한다. kind의 kubelet 인증서는 metrics-server가 검증할 수 없어서 실습 환경에서만 `--kubelet-insecure-tls`를 덧붙인다.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl -n kube-system patch deployment metrics-server --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl top nodes
```

`kubectl top nodes`에 숫자가 나오면, `web`에 위의 `resources`를 넣고 HPA를 건다.

```bash
kubectl autoscale deployment web --cpu-percent=50 --min=2 --max=8
kubectl get hpa web -w
```

4회의 `client` Pod처럼 임시 Pod에서 `while true; do wget -qO- http://web >/dev/null; done`으로 부하를 주면 `REPLICAS`가 늘어나고, 부하를 멈추면 몇 분 뒤 다시 줄어든다. HPA는 Pod 수를 늘릴 뿐 노드를 늘리지 않는다. 노드까지 늘리려면 클러스터 오토스케일러나 Karpenter 같은 노드 단위 확장 도구가 따로 필요하다.

## 진단 순서: get → describe → logs → events

장애를 만나면 아래 순서로 좁혀 간다([Kubernetes 문서](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)).

1. `kubectl get pods` — 상태(`STATUS`)와 재시작 횟수(`RESTARTS`)로 증상을 분류한다.
2. `kubectl describe pod <이름>` — 맨 아래 `Events`에 스케줄러와 kubelet이 남긴 이유가 있다. 2회에서 본 사슬의 어디서 멈췄는지 여기서 드러난다.
3. `kubectl logs <이름>` — 앱이 남긴 에러. 이미 재시작된 컨테이너라면 `--previous`로 직전 실행의 로그를 본다.
4. `kubectl get events --sort-by=.lastTimestamp` — 네임스페이스 전체에서 무슨 일이 있었는지 시간순으로 본다.
5. `kubectl exec` 또는 `kubectl debug` — 컨테이너 안에서 직접 확인한다. 셸이 없는 이미지라면 `kubectl debug -it <이름> --image=busybox:1.37 --target=<컨테이너>`로 임시 디버그 컨테이너를 붙인다.

| 증상 | 사슬의 위치 | 흔한 원인 |
|---|---|---|
| `Pending` | 스케줄러 | requests를 받아 줄 노드가 없음, PVC가 묶이지 않음, taint·nodeSelector 불일치 |
| `ImagePullBackOff` | kubelet(이미지) | 태그 오타, 비공개 레지스트리 인증 없음, 레지스트리 접근 불가 |
| `CrashLoopBackOff` | 앱 | 앱이 시작하자마자 종료, 설정·Secret 누락, liveness probe 오설정 |
| `OOMKilled` | 앱(자원) | 메모리 limits가 실제 사용량보다 작음 |
| `Running`인데 응답 없음 | Service·readiness | 셀렉터 레이블 불일치, readiness 실패로 대상에서 빠짐 |

## 실습: 세 번 고장 내고 고치기

아래 세 Pod을 만들고, 정답을 보기 전에 위의 순서로 원인을 찾아본다.

```bash
# 1. 너무 큰 요청
kubectl run greedy --image=nginx:1.29 --overrides='{"spec":{"containers":[{"name":"greedy","image":"nginx:1.29","resources":{"requests":{"cpu":"64"}}}]}}'
# 2. 시작하자마자 죽는 앱
kubectl run crasher --image=busybox:1.37 -- sh -c 'echo "DATABASE_URL이 없습니다" >&2; exit 1'
# 3. 메모리 상한 초과
kubectl run hog --image=busybox:1.37 --overrides='{"spec":{"containers":[{"name":"hog","image":"busybox:1.37","command":["tail","/dev/zero"],"resources":{"limits":{"memory":"64Mi"}}}]}}'
kubectl get pods
```

- `greedy`는 `Pending`이다. `kubectl describe pod greedy`의 Events에 `FailedScheduling`과 `Insufficient cpu`가 보인다. 노트북에 CPU 64개는 없다. requests를 줄이면 해결된다.
- `crasher`는 `CrashLoopBackOff`다. `kubectl logs crasher --previous`에 앱이 남긴 메시지가 그대로 있다. 재시작 간격은 실패할 때마다 길어진다.
- `hog`는 `OOMKilled`를 거쳐 재시작을 반복한다. `kubectl describe pod hog`의 `Last State`에 `Reason: OOMKilled`가 찍혀 있다.

확인이 끝나면 `kubectl delete pod greedy crasher hog`로 정리한다.

## 정리

- 운영 Pod에는 최소한 requests를 적는다. 스케줄링, QoS, HPA가 모두 이 값에 기댄다.
- liveness는 프로세스 자체만, 외부 의존성은 readiness로 확인한다.
- 장애는 get → describe → logs → events 순서로 좁힌다. 증상 이름이 사슬의 어느 단계인지 알려 준다.

마지막 회에서는 누가 무엇을 할 수 있는지 정하는 RBAC와 Pod 보안, 그리고 이 모든 매니페스트를 Helm과 GitOps로 반복 가능하게 배포하는 법을 다룬다.

## 출처

- [Resource Management for Pods and Containers — Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Pod Quality of Service Classes — Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)
- [Liveness, Readiness, and Startup Probes — Kubernetes 문서](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Horizontal Pod Autoscaling — Kubernetes 문서](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [metrics-server — kubernetes-sigs](https://github.com/kubernetes-sigs/metrics-server)
- [Debug Pods — Kubernetes 문서](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug Running Pods — Kubernetes 문서](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
