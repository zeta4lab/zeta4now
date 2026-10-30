---
title: Pod IP는 믿지 말고 Service 이름을 불러라…ClusterIP·DNS부터 Ingress 이후의 Gateway API까지
slug: 2026-10-30-k8s-hands-on-4-networking
topic: cloud
published_at: 2026-10-30T10:53:00+09:00
tags:
  - 쿠버네티스 손으로 익히기
  - Kubernetes
  - Gateway API
summary: 「쿠버네티스 손으로 익히기」 4회. 쿠버네티스 네트워크 모델, Service의 종류와 클러스터 DNS, 기능 추가가 멈춘 Ingress와 2026년 3월 지원이 끝난 Ingress NGINX, 그 대안인 Gateway API, 그리고 NetworkPolicy를 정리하고 서비스 두 개를 이름으로 연결하는 실습을 한다.
generated_by: claude
model: claude-opus-5-5
---

# Pod IP는 믿지 말고 Service 이름을 불러라…ClusterIP·DNS부터 Ingress 이후의 Gateway API까지

## 한눈에 보기

Pod은 언제든 죽고 새로 만들어지며, 그때마다 IP가 바뀐다. 그러니 Pod IP를 설정 파일에 적어 두는 순간 장애가 예약된다. 쿠버네티스는 바뀌는 Pod 묶음 앞에 고정된 주소를 세우는 Service, 그 주소를 이름으로 찾게 해 주는 DNS, 바깥 트래픽을 받아들이는 Gateway API(또는 Ingress)로 이 문제를 푼다. 이번 회는 이 세 겹을 차례로 쌓는다.

연재 순서: [1회 선언형과 조정 루프](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-1-declarative-reconcile), [2회 클러스터 해부도](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-2-cluster-anatomy), [3회 워크로드 고르기](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-3-workloads), 4회 네트워킹, [5회 설정과 저장소](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-5-config-storage), [6회 운영과 디버깅](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-6-operations-debugging), [7회 보안과 배포 파이프라인](https://now.zeta4.net/a/2026-10-30-k8s-hands-on-7-security-delivery).

## 네트워크 모델: 모든 Pod은 서로 직접 닿는다

쿠버네티스의 네트워크 모델은 단순한 약속에서 출발한다. 모든 Pod은 클러스터 안에서 고유한 IP를 받고, 어느 노드에 있든 NAT 없이 다른 모든 Pod과 직접 통신할 수 있어야 한다([Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/)). 이 약속을 실제로 구현하는 것은 쿠버네티스 본체가 아니라 CNI(Container Network Interface) 플러그인이다. Calico, Cilium, 클라우드별 플러그인 등이 있고, kind는 kindnet을 기본으로 쓴다.

## Service: 바뀌는 Pod 앞의 고정 주소

Service는 레이블 셀렉터로 고른 Pod 묶음에 고정된 가상 IP와 이름을 붙인다. Pod이 바뀌면 Service 뒤의 목록(EndpointSlice)만 갱신되고, 부르는 쪽은 아무것도 바꿀 필요가 없다([Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/service/)).

| 종류 | 누가 접근하나 | 쓰임 |
|---|---|---|
| ClusterIP(기본값) | 클러스터 안에서만 | 서비스 사이의 내부 호출 |
| NodePort | 모든 노드의 특정 포트(기본 30000~32767)로 바깥에서 | 실습, 단순한 외부 노출 |
| LoadBalancer | 클라우드 로드밸런서를 통해 바깥에서 | 클라우드에서 서비스를 직접 노출 |
| Headless(`clusterIP: None`) | 가상 IP 없이 Pod IP 목록을 DNS로 | StatefulSet처럼 개별 Pod을 찾아야 할 때 |

## DNS: 이름으로 찾기

클러스터에는 DNS 서버(보통 CoreDNS)가 함께 돈다. Service를 만들면 `<서비스>.<네임스페이스>.svc.cluster.local`이라는 이름이 자동으로 생긴다. 같은 네임스페이스에서는 `<서비스>`만, 다른 네임스페이스에서는 `<서비스>.<네임스페이스>`까지만 써도 찾아간다([Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)).

## 실습: 서비스 두 개를 이름으로 연결하기

1회의 `web` Deployment에 Service를 붙인다.

```bash
kubectl expose deployment web --port=80 --target-port=80
kubectl get svc web
kubectl get endpointslices -l kubernetes.io/service-name=web
```

EndpointSlice에 `web` Pod들의 IP가 보인다. 이제 다른 Pod에서 이름으로 불러 본다.

```bash
kubectl run client --rm -it --image=busybox:1.37 --restart=Never -- sh
# 안에서
wget -qO- http://web | head -5
nslookup web
exit
```

`http://web`만으로 nginx 첫 화면이 돌아오고, `nslookup`은 `web.default.svc.cluster.local`과 Service의 가상 IP를 보여 준다. 다른 터미널에서 `kubectl delete pod -l app=web`으로 Pod을 모두 지워도, 새 Pod이 뜨면 같은 이름과 같은 Service IP로 다시 응답한다.

노트북 브라우저에서 확인하려면 포트 포워딩을 쓴다. 디버깅용 터널이며 운영 노출 방법은 아니다.

```bash
kubectl port-forward svc/web 8080:80
# 브라우저에서 http://localhost:8080
```

## 바깥 트래픽: Ingress에서 Gateway API로

HTTP 서비스 여러 개를 하나의 입구에서 호스트명과 경로로 나눠 받는 기능은 오랫동안 Ingress가 맡았다. 하지만 공식 문서는 현재 Ingress API에 기능 추가를 멈췄고(frozen), 새 기능은 Gateway API에 들어간다고 안내한다([Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/ingress/)). 가장 널리 쓰이던 Ingress 컨트롤러인 Ingress NGINX도 은퇴했다. 쿠버네티스 SIG Network와 보안대응위원회는 2025년 11월, 2026년 3월까지만 최선의 노력으로 유지보수하고 그 뒤로는 보안 취약점 수정도 내지 않는다고 발표했다. 기존 설치는 계속 동작하지만, 프로젝트는 Gateway API로 옮기길 권한다([Kubernetes 블로그](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)).

Gateway API는 역할에 따라 객체를 나눈다.

- **GatewayClass**: 어떤 구현(Envoy Gateway, Istio, Cilium, 클라우드 로드밸런서 등)을 쓸지. 보통 플랫폼 제공자가 정한다.
- **Gateway**: 실제 입구. 어떤 포트와 프로토콜, 인증서로 받을지. 클러스터 운영자가 관리한다.
- **HTTPRoute**: 어떤 호스트와 경로를 어느 Service로 보낼지. 앱 개발자가 자기 네임스페이스에서 관리한다.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web
spec:
  parentRefs:
    - name: shared-gateway
  hostnames:
    - "web.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: web
          port: 80
```

Ingress 하나에 몰려 있던 설정을 역할별로 나눈 덕분에, 앱 팀은 공용 입구를 건드리지 않고 자기 라우팅만 바꿀 수 있다. Gateway API는 쿠버네티스 본체가 아니라 별도 CRD로 설치하며, 2026년 10월 29일(UTC) v1.7.0이 나왔다([Gateway API](https://gateway-api.sigs.k8s.io/)). 실습하려면 GatewayClass를 제공할 구현체를 하나 설치해야 하므로, 이 연재에서는 개념과 매니페스트 모양까지만 다룬다. 기존 Ingress 설정은 Ingress2Gateway 도구로 변환을 시작할 수 있다.

## NetworkPolicy: 기본은 모두 열려 있다

앞의 네트워크 모델 때문에 기본 상태에서는 모든 Pod이 모든 Pod에 닿는다. 데이터베이스 Pod에 아무 Pod이나 접속할 수 있다는 뜻이다. NetworkPolicy로 이를 제한한다. 아래 정책은 `app: db` Pod으로 들어오는 트래픽을 `app: api` Pod에서 온 5432 포트만 허용한다.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-allow-api
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes: ["Ingress"]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api
      ports:
        - port: 5432
```

주의할 점은 NetworkPolicy가 CNI 플러그인이 지원해야만 동작한다는 것이다. 지원하지 않는 플러그인에서는 객체가 만들어져도 아무 효과가 없다([Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/network-policies/)). 정책을 적용했다면 실제로 막히는지 반드시 시험해 본다.

## 정리

- Pod IP는 바뀐다. 클러스터 안에서는 Service 이름으로 부른다.
- 바깥 노출은 실습이면 `port-forward`나 NodePort, 클라우드면 LoadBalancer, HTTP 라우팅이면 Gateway API다. 새로 시작한다면 Ingress NGINX는 고르지 않는다.
- 기본 네트워크는 모두 열려 있다. 민감한 Pod부터 NetworkPolicy로 닫고, 쓰는 CNI가 지원하는지 확인한다.

다음 회에서는 이미지에 넣으면 안 되는 설정과 비밀값, 그리고 Pod이 사라져도 남아야 하는 데이터를 다룬다.

## 출처

- [Services, Load Balancing, and Networking — Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/)
- [Service — Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/service/)
- [DNS for Services and Pods — Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Ingress — Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Ingress NGINX Retirement: What You Need to Know — Kubernetes 블로그](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)
- [Gateway API — Kubernetes SIG Network](https://gateway-api.sigs.k8s.io/)
- [Gateway API v1.7.0 릴리스 — kubernetes-sigs/gateway-api](https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.7.0)
- [Network Policies — Kubernetes 문서](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
