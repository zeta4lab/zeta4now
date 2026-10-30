---
title: AKS 관리형 NGINX에서 Gateway API로…11월 지원 종료 전 무중단 이전 절차
slug: 2026-10-30-aks-migration-1-nginx-to-gateway-api
topic: cloud
published_at: 2026-10-30T01:00:00+09:00
tags:
  - AKS 실전 이전
  - AKS
  - Azure
  - Kubernetes
  - Gateway API
  - NGINX
summary: AKS 실전 이전 가이드 5회 연재의 첫 편. 애플리케이션 라우팅 애드온의 관리형 NGINX는 2026년 11월 이후 Azure 지원을 받지 못한다. Microsoft 공식 이전 가이드를 따라 Gateway API 구현을 나란히 띄우고, ingress2gateway로 변환하고, DNS로 전환하는 순서를 정리한다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-12-01
      note: 관리형 NGINX 지원 종료(11월) 이후 기존 클러스터 처리에 대한 공식 안내 확인
---

# AKS 관리형 NGINX에서 Gateway API로…11월 지원 종료 전 무중단 이전 절차

## 한눈에 보기

[AKS 입문 3회](https://now.zeta4.net/a/2026-10-30-aks-103-networking)에서 짚었듯, AKS 애플리케이션 라우팅 애드온의 관리형 NGINX는 2026년 11월까지만 중요 보안 패치를 받는다. Microsoft 문서는 관리형 NGINX를 쓰고 있다면 11월까지 이전해야 한다고 적었다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-gateway-api)). 이 연재는 입문편에서 "옮겨야 한다"고 한 것들을 실제 절차로 푼다. 첫 편은 가장 급한 인그레스 이전이다.

연재 순서: 1회 관리형 NGINX에서 Gateway API로, [2회 kubenet에서 Azure CNI Overlay로](https://now.zeta4.net/a/2026-10-30-aks-migration-2-kubenet-to-cni-overlay), [3회 pod 관리 ID에서 워크로드 ID로](https://now.zeta4.net/a/2026-10-30-aks-migration-3-pod-identity-to-workload-id), [4회 2027년 6월 강제 업그레이드 대비](https://now.zeta4.net/a/2026-10-30-aks-migration-4-upgrade-before-2027), [5회 노드 OS 이전](https://now.zeta4.net/a/2026-10-30-aks-migration-5-node-os).

## 11월 이후 무슨 일이 생기나

공식 자료가 말하는 것은 세 가지다. 관리형 NGINX는 11월 이후 Azure 지원이 끝나고, 보안 패치가 더 나오지 않으며, AKS 블로그에 따르면 11월 이후에는 새로 배포하지 않아 기본으로 보이지 않게 된다([AKS 블로그](https://blog.aks.azure.com/2026/06/10/app-routing-gateway-api-ga)). 기존 클러스터에서 강제로 지워지는지, 정확한 종료일이 언제인지는 공식 자료에 나와 있지 않다. 당장 트래픽이 끊기지는 않더라도, 인터넷에 노출된 구성 요소가 패치 없이 남는다는 점이 핵심 위험이다. 커뮤니티 ingress-nginx는 이미 2026년 3월에 유지보수가 끝났다.

## 어디로 옮길까

| 선택지 | 맞는 경우 |
|---|---|
| 애플리케이션 라우팅 Gateway API 구현(`approuting-istio`) | 클러스터 안에서 도는 관리형 게이트웨이를 원할 때. 2026년 4월 GA |
| Application Gateway for Containers(AGC) | WAF, mTLS가 필요하거나, Ingress API를 유지한 채 단계적으로 옮기고 싶을 때. Azure가 클러스터 밖에서 운영 |

`approuting-istio`는 헤더·본문 크기 제한, Lua, 속도 제한, EnvoyFilter를 지원하지 않는다. NGINX에서 `proxy-body-size`나 속도 제한을 쓰고 있었다면 AGC를 먼저 검토한다. AGC는 Ingress API와 Gateway API를 모두 지원하고 WAF, 헤더·URL 재작성, 트래픽 분할, 재시도를 제공한다. 리스너 포트는 80과 443만 쓸 수 있고, 한국 중부 리전에서 쓸 수 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/overview)). 이 글은 Microsoft가 공식 이전 가이드를 낸 `approuting-istio` 경로를 따른다.

## 이전 절차: 나란히 띄우고 DNS로 바꾼다

Microsoft의 [이전 가이드](https://learn.microsoft.com/en-us/azure/aks/app-routing-nginx-to-gateway-api-migration)는 두 데이터 플레인을 함께 띄운 뒤 DNS로 전환하는 방식을 쓴다. 두 게이트웨이는 서로 다른 부하 분산기 IP를 받는다. 가이드는 NGINX의 IP를 새 게이트웨이로 그대로 옮기는 방법은 없다고 못 박는다. 그래서 방화벽 허용 목록이나 Front Door 원본처럼 IP를 직접 가리키는 곳도 함께 바꿔야 한다.

**1단계: 목록 만들기.** 바꿔야 할 대상을 먼저 센다.

```bash
kubectl get nginxingresscontrollers
kubectl get ingress -A
```

IP나 호스트 이름을 참조하는 Front Door, Traffic Manager, 방화벽 규칙도 적어 둔다.

**2단계: Gateway API 켜기.** Azure CLI 2.86.0 이상이 필요하다.

```bash
az aks update --resource-group $RG --name $CLUSTER --enable-gateway-api
az aks update --resource-group $RG --name $CLUSTER --enable-app-routing-istio
kubectl -n aks-istio-system rollout status deploy/istiod --timeout=5m
kubectl get gatewayclass approuting-istio
```

Gateway API CRD는 AKS가 관리한다. 직접 설치한 CRD는 지원되지 않으며, experimental 채널 CRD가 있으면 먼저 지워야 한다. Istio 서비스 메시 애드온과는 함께 켤 수 없다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/managed-gateway-api)).

**3단계: DNS TTL 낮추기.** 전환과 롤백을 빠르게 하려고 해당 레코드의 TTL을 60초로 낮추고, 기존 TTL이 다 지나갈 때까지 기다린다.

**4단계: Ingress를 Gateway와 HTTPRoute로 바꾸기.** 손으로 옮겨도 되고 ingress2gateway 1.0을 써도 된다. 2026년 3월 나온 1.0은 ingress-nginx 어노테이션 30여 개를 변환한다([Kubernetes 블로그](https://kubernetes.io/blog/2026/03/20/ingress2gateway-1-0-release/)). AKS 애플리케이션 라우팅의 Ingress 클래스는 `nginx`가 아니므로 클래스를 꼭 지정해야 한다. 지정하지 않으면 변환 대상에서 빠진다.

```bash
ingress2gateway print --providers=ingress-nginx \
  --ingress-nginx-ingress-class=webapprouting.kubernetes.azure.com > gwapi.yaml
```

변환 결과는 반드시 사람이 검토한다.

| NGINX 어노테이션 | Gateway API 변환 |
|---|---|
| `rewrite-target` | URLRewrite(정규식 캡처 그룹은 경고) |
| `ssl-redirect`, `permanent-redirect` | RequestRedirect |
| `upstream-vhost` | RequestHeaderModifier |
| `proxy-*-timeout` | `timeouts.request`(근사치라 검증 필요) |
| `canary-weight`, `canary-by-header` | 가중치·헤더 매치 |
| `backend-protocol: GRPC` | GRPCRoute |
| `configuration-snippet`, `custom-headers` | 변환 안 됨(경고만) |
| `proxy-body-size` | 표준 변환 없음, `approuting-istio`에서 지원 안 함 |

인증 계열 어노테이션은 변환 대상 목록에 없다([ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway/blob/main/pkg/i2gw/providers/ingressnginx/README.md)). 한 규칙 안에서 URLRewrite와 RequestRedirect를 함께 쓸 수 없다는 점도 기억한다([Gateway API](https://gateway-api.sigs.k8s.io/guides/getting-started/migrating-from-ingress/)).

**5단계: TLS 구성.** 인증서를 Key Vault에 두고 리스너 옵션에 Key Vault URI와 서비스 계정을 적으면, 운영자가 시크릿과 인증서 참조를 자동으로 만든다. 워크로드 ID, OIDC 발급자, Key Vault CSI 애드온이 필요하다. 예전 `--attach-kv`, `--attach-zones`는 NGINX 전용이라 이 경로에서는 쓰이지 않는다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-gateway-api-dns-tls)).

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
spec:
  gatewayClassName: approuting-istio
  listeners:
  - name: https
    hostname: app.example.com
    port: 443
    protocol: HTTPS
    tls:
      mode: Terminate
      options:
        kubernetes.azure.com/tls-cert-keyvault-uri: https://<vault>.vault.azure.net/certificates/<cert>
        kubernetes.azure.com/tls-cert-service-account: web-sa
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
spec:
  parentRefs:
  - name: web-gateway
  hostnames: ["app.example.com"]
  rules:
  - matches:
    - path: {type: PathPrefix, value: /}
    backendRefs:
    - name: web
      port: 80
```

**6단계: DNS를 바꾸기 전에 검증하기.** `curl --resolve`로 DNS를 바꾸지 않고 새 게이트웨이 IP에 직접 요청을 보낸다. 모든 호스트와 경로, 실제 인증서로 HTTPS, POST, WebSocket, gRPC를 몇 분간 반복해서 확인한다.

```bash
GW_IP=$(kubectl get gateway web-gateway -o jsonpath='{.status.addresses[0].value}')
curl -sS -o /dev/null -w '%{http_code}\n' --resolve "app.example.com:443:${GW_IP}" https://app.example.com/
```

**7단계: 전환.** DNS A 레코드와 IP를 참조하는 상위 구성을 새 게이트웨이로 바꾸고, NGINX 쪽 요청 지표가 0이 될 때까지 지켜본다. 문제가 생기면 DNS만 되돌리면 된다.

**8단계: 정리.** NGINX 트래픽이 완전히 끊긴 것을 확인한 뒤 지운다. 이 단계를 지나면 DNS 롤백도 할 수 없으니 서두르지 않는다.

```bash
az aks approuting update --resource-group $RG --name $CLUSTER --nginx None
kubectl delete nginxingresscontrollers.approuting.kubernetes.azure.com --all
```

## 정리

- 11월 이후 관리형 NGINX는 패치 없이 남는다. 지금 이전 일정을 잡는다.
- 크기 제한·속도 제한·Lua가 필요하면 `approuting-istio` 대신 AGC를 검토한다.
- 나란히 띄우고, `curl --resolve`로 검증하고, DNS로 바꾸고, NGINX는 마지막에 지운다.
- ingress2gateway 결과물은 출발점일 뿐이다. 경고가 난 어노테이션은 하나씩 확인한다.

다음 회에서는 되돌릴 수 없는 작업인 kubenet에서 Azure CNI Overlay로의 이전을 다룬다.

## 출처

- [Application routing Gateway API implementation — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-gateway-api)
- [Migrate from application routing NGINX to Gateway API — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-nginx-to-gateway-api-migration)
- [Managed Gateway API installation — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/managed-gateway-api)
- [DNS and TLS for application routing Gateway API — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-gateway-api-dns-tls)
- [Application routing Gateway API is GA — AKS 블로그(2026-06-10)](https://blog.aks.azure.com/2026/06/10/app-routing-gateway-api-ga)
- [Ingress NGINX update — AKS 블로그(2025-11-13)](https://blog.aks.azure.com/2025/11/13/ingress-nginx-update)
- [What is Application Gateway for Containers? — Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/for-containers/overview)
- [Ingress2Gateway 1.0 — Kubernetes 블로그(2026-03-20)](https://kubernetes.io/blog/2026/03/20/ingress2gateway-1-0-release/)
- [ingress-nginx provider — ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway/blob/main/pkg/i2gw/providers/ingressnginx/README.md)
- [Migrating from Ingress — Gateway API](https://gateway-api.sigs.k8s.io/guides/getting-started/migrating-from-ingress/)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
