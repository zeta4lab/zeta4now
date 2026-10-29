---
title: AKS 네트워킹…기본은 Azure CNI Overlay, kubenet은 2028년 은퇴, 관리형 NGINX는 11월까지 옮겨야
slug: 2026-10-30-aks-103-networking
topic: cloud
published_at: 2026-10-30T00:32:00+09:00
tags:
  - AKS 입문
  - AKS
  - Azure
  - Kubernetes
  - 네트워킹
  - Gateway API
summary: AKS 입문 6회 연재의 3회. pod IP를 주는 방식(Overlay와 Flat), 기본값이 된 Azure CNI Overlay와 Cilium 데이터 플레인, kubenet과 Azure NPM의 은퇴 일정, ingress-nginx 은퇴 뒤의 인그레스 선택지, 비공개 API server와 아웃바운드 방식을 정리한다.
generated_by: claude
model: claude-opus-5-5
tracking:
  status: ongoing
  checkpoints:
    - date: 2026-12-01
      note: 애플리케이션 라우팅 애드온의 관리형 NGINX 보안 패치 종료(11월) 후속 안내 확인
---

# AKS 네트워킹…기본은 Azure CNI Overlay, kubenet은 2028년 은퇴, 관리형 NGINX는 11월까지 옮겨야

## 한눈에 보기

AKS 네트워킹에서 내릴 결정은 크게 넷이다. pod에 IP를 어떻게 줄지(CNI), pod 사이 트래픽을 어떻게 막을지(네트워크 정책), 바깥 요청을 어떻게 받을지(인그레스), 클러스터가 바깥으로 어떻게 나갈지(아웃바운드)다. 2026년 현재 답은 상당히 정리됐다. 기본값은 Azure CNI Overlay이고, 정책 엔진은 Cilium을 권장하며, 인그레스는 Gateway API 쪽으로 옮겨 가는 중이다. 특히 애플리케이션 라우팅 애드온의 관리형 NGINX를 쓰고 있다면 이번 달 안에 이전 계획이 있어야 한다.

## pod IP: Overlay와 Flat

AKS의 네트워킹 모델은 두 가지다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/concepts-network-cni-overview)).

- **Overlay**: pod는 VNet과 별개인 pod 전용 대역(CIDR)에서 IP를 받는다. 클러스터 밖으로 나갈 때는 노드 IP로 주소가 바뀐다(SNAT). VNet IP를 아낄 수 있다.
- **Flat**: pod가 VNet 서브넷에서 직접 IP를 받는다. 다른 VNet 자원이 pod IP로 바로 접근할 수 있지만, pod 수만큼 VNet IP가 필요하다.

Microsoft는 "대부분의 시나리오"에 **Azure CNI Overlay**를 권장한다. Flat이 필요하면 Azure CNI Pod Subnet을 쓴다. Azure CNI Node Subnet과 kubenet은 레거시로 분류된다. `--network-plugin`을 생략하고 클러스터를 만들면 Azure CNI Overlay가 적용된다. 반대로 `--network-plugin azure`만 주고 `--network-plugin-mode`를 빼면 하위 호환을 위해 Node Subnet 모드가 되니 주의한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/azure-cni-overlay)).

**kubenet은 2028년 3월 31일 은퇴한다.** 이전 경로는 Azure CNI Overlay다. kubenet은 Windows 노드풀과 Application Gateway for Containers도 지원하지 않는다.

Overlay는 노드당 최대 250 pod를 지원하고, pod 대역 기본값은 `10.244.0.0/16`이다. `169.254.0.0/16`, `192.0.2.0/24`, `172.30.0.0/16`, `172.31.0.0/16`은 예약 대역이라 pod 대역으로 쓸 수 없다. 예를 들어 `172.16.0.0/12`처럼 이 범위를 포함하는 대역은 거부된다. 사내망과 겹치지 않는 대역을 미리 정해 두자.

## Cilium 데이터 플레인

Azure CNI powered by Cilium은 IP 관리 방식(Overlay, Pod Subnet, Node Subnet)과 조합하는 **데이터 플레인** 선택지다. eBPF로 동작하며 kube-proxy를 대체한다. Linux 노드에서만 쓸 수 있다. AKS Automatic은 Overlay와 Cilium 조합이 기본이다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/azure-cni-powered-by-cilium)).

```bash
az aks create -g $RG -n $CLUSTER --network-plugin azure --network-plugin-mode overlay \
  --pod-cidr 192.168.0.0/16 --network-dataplane cilium --generate-ssh-keys
```

예전 플래그 `--enable-ebpf-dataplane`은 deprecated이니 `--network-dataplane cilium`을 쓴다. FQDN 기반 필터링이나 L7 정책을 쓰려면 Advanced Container Networking Services(ACNS)를 따로 켜야 한다.

## 네트워크 정책: 기본은 "모두 허용"

네트워크 정책이 없으면 클러스터 안의 모든 pod가 서로 통신할 수 있다. 정책 엔진은 Cilium(권장), Azure NPM, Calico 세 가지다. Azure NPM은 Windows 노드에서 2026년 9월 30일 지원이 끝났고, Linux 노드에서는 2028년 9월 30일 은퇴한다. 새로 시작한다면 Cilium 네트워크 정책을 쓴다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-network-policies)).

## 인그레스: NGINX 다음은 Gateway API

인그레스는 지금 가장 크게 바뀌는 영역이다.

- 커뮤니티 **ingress-nginx는 2026년 3월 유지보수가 끝났다.**
- AKS 애플리케이션 라우팅 애드온의 **관리형 NGINX는 2026년 11월까지만** 중요 보안 패치를 받는다. Microsoft 문서는 11월까지 이전하라고 안내한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-gateway-api)).

이전할 곳은 두 갈래다.

| 선택지 | 특징 |
|---|---|
| 애플리케이션 라우팅의 Gateway API 구현 | 클러스터 안에서 도는 Istio 기반 게이트웨이(`gatewayClassName: approuting-istio`), 사이드카 주입 없음. 관리형 Gateway API CRD와 Azure CLI 2.86.0 이상 필요. AKS 1.36부터 새 Automatic 클러스터의 기본 |
| Application Gateway for Containers | Azure가 호스팅하는 L7 부하 분산기. Ingress API와 Gateway API 모두 지원 |

애플리케이션 라우팅의 Gateway API 구현은 헤더·본문 크기 제한, Lua 스크립트, 속도 제한(rate limiting), EnvoyFilter를 지원하지 않는다. NGINX 설정에서 이런 기능을 쓰고 있었다면 이전 전에 대안을 확인해야 한다. 기존 Application Gateway Ingress Controller(AGIC)는 은퇴 공지가 없지만, 문서는 새 구성에 Application Gateway for Containers를 검토하라고 권한다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview)).

참고로 AKS의 인그레스 개념 문서 일부는 아직 예전 설명이 남아 있다. 서로 다른 문서가 엇갈리면 날짜가 더 최근인 기능별 문서를 기준으로 삼는다.

## API server를 비공개로: VNet 통합과 비공개 클러스터

기본 AKS 클러스터의 API server는 공용 엔드포인트를 가진다. **API Server VNet Integration**을 켜면 API server가 위임된 서브넷(최소 `/28`)의 내부 부하 분산기 뒤에 놓여, 노드와 API server 사이 트래픽이 VNet 안에 머문다. 공용 클러스터와 비공개 클러스터(`--enable-private-cluster`) 모두에 쓸 수 있다. 기존 클러스터에 켜면 되돌릴 수 없고, 클러스터를 한 번 정지했다가 다시 시작해야 한다. AKS Automatic에는 기본으로 구성돼 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/api-server-vnet-integration)).

## 아웃바운드: 클러스터가 밖으로 나가는 길

`outboundType`은 노드와 pod가 인터넷으로 나가는 방식을 정한다. 기본은 `loadBalancer`이고, `managedNATGateway`, `userAssignedNATGateway`, `userDefinedRouting`(방화벽 경유), 네트워크 격리 클러스터용 `none`이 있다. 이제 클러스터를 만든 뒤에도 바꿀 수 있다. 2026년 3월 31일부터 AKS가 관리하는 VNet으로 만든 새 클러스터는 서브넷의 기본 아웃바운드 접근이 꺼진 상태로 만들어진다. 직접 만든 VNet을 쓰는 클러스터는 영향이 없다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype)).

아웃바운드 연결이 많은 서비스는 부하 분산기의 SNAT 포트가 모자랄 수 있어 NAT 게이트웨이를 고려한다. 고정된 출구 IP가 필요하거나 모든 트래픽을 방화벽으로 검사해야 하면 `userDefinedRouting`을 쓴다.

## 정리

- 새 클러스터는 Azure CNI Overlay + Cilium으로 시작한다. pod 대역은 사내망과 겹치지 않게 미리 정한다.
- kubenet(2028-03-31)과 Azure NPM(Linux 2028-09-30)을 쓰고 있다면 이전 계획을 세운다.
- 관리형 NGINX 인그레스는 2026년 11월까지 Gateway API 또는 Application Gateway for Containers로 옮긴다.
- 네트워크 정책 없이는 모든 pod가 서로 통한다는 점을 기억한다.

다음 회에서는 누가 클러스터에 접근하고 pod가 어떻게 Azure 자원에 접근하는지, ID와 보안을 다룬다.

## 출처

- [CNI networking overview for AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/concepts-network-cni-overview)
- [Azure CNI Overlay networking in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/azure-cni-overlay)
- [Kubenet retirement — Azure/AKS GitHub](https://github.com/Azure/AKS/issues/4859)
- [Azure CNI powered by Cilium — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/azure-cni-powered-by-cilium)
- [Secure traffic between pods with network policies — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-network-policies)
- [Application routing Gateway API implementation — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/app-routing-gateway-api)
- [Application Gateway Ingress Controller overview — Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview)
- [API Server VNet Integration — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/api-server-vnet-integration)
- [Customize cluster egress with outbound types — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
