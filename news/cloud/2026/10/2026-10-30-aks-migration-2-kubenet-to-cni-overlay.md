---
title: kubenet에서 Azure CNI Overlay로…되돌릴 수 없는 한 번의 명령, 전후에 확인할 것
slug: 2026-10-30-aks-migration-2-kubenet-to-cni-overlay
topic: cloud
published_at: 2026-10-30T01:01:00+09:00
tags:
  - AKS 실전 이전
  - AKS
  - Azure
  - Kubernetes
  - 네트워킹
  - Cilium
summary: AKS 실전 이전 가이드 5회 연재의 2회. kubenet은 2028년 3월 31일 은퇴한다. 이전은 명령 한 줄이지만 되돌릴 수 없고 모든 노드풀이 동시에 다시 만들어진다. 전제 조건, 네트워크 정책 처리, IP 대역 설계, Cilium으로의 2단계 전환을 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# kubenet에서 Azure CNI Overlay로…되돌릴 수 없는 한 번의 명령, 전후에 확인할 것

## 한눈에 보기

kubenet은 2028년 3월 31일 은퇴한다([Azure/AKS](https://github.com/Azure/AKS/issues/4859)). 시간은 남았지만 미룰 이유도 적다. kubenet 클러스터는 최대 400노드까지인 반면 Azure CNI Overlay는 5,000노드까지 늘릴 수 있고, kubenet은 Windows 노드풀과 Application Gateway for Containers를 지원하지 않는다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/concepts-network-azure-cni-overlay)). 이전은 `az aks update` 한 줄이다. 하지만 **되돌릴 수 없고, 모든 노드풀이 동시에 다시 만들어진다.** 그래서 명령 전후의 준비가 전부다.

[1회](https://now.zeta4.net/a/2026-10-30-aks-migration-1-nginx-to-gateway-api)에 이은 이번 회는 [AKS 입문 3회 네트워킹](https://now.zeta4.net/a/2026-10-30-aks-103-networking)의 내용을 전제로 한다.

## 0단계: 지금 무엇을 쓰고 있나

```bash
az aks show --resource-group $RG --name $CLUSTER --query "networkProfile" --output table
```

`networkPlugin`이 `kubenet`이면 이전 대상이다. `networkPolicy` 값과 `podCidr`도 함께 적어 둔다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-network-policies)).

## 1단계: 전제 조건 점검

Microsoft의 [이전 문서](https://learn.microsoft.com/en-us/azure/aks/update-azure-cni)가 요구하는 조건은 다음과 같다.

| 조건 | 확인할 것 |
|---|---|
| Kubernetes 1.27 이상 | 낮으면 먼저 업그레이드 |
| 동적 IP 할당 미사용 | 해당 시 이전 불가 |
| 네트워크 정책 없음 | 있으면 먼저 제거(아래) |
| Docker 런타임 Windows 노드풀 없음 | Windows는 OS 빌드 20348.1668 이상 권장 |
| 사용자 할당 관리 ID | 시스템 할당 ID 클러스터는 지원 안 됨 |

관리 ID 조건은 라우트 테이블 때문이다. kubenet은 노드마다 pod 경로를 라우트 테이블에 적어 두는데, 이전하면서 이를 떼어내야 한다. 사용자가 만든 라우트 테이블이면 pod 경로만 지워지고, AKS가 만든 라우트 테이블이면 테이블 자체가 지워진다. 같은 라우트 테이블에 방화벽 경로 같은 다른 규칙을 함께 두었다면 이전 뒤에도 남는지 확인한다.

## 2단계: 네트워크 정책 처리

이전 문서는 네트워크 정책이 켜져 있지 않아야 한다고 적었다. 그래서 먼저 정책 엔진을 끈다.

```bash
az aks update --resource-group $RG --name $CLUSTER --network-policy none
```

이 명령은 Calico CRD와 정책 리소스를 지우지 않는다. 리소스는 남지만 **강제되지 않는다.** 이전이 끝나고 새 정책 엔진(권장은 Cilium)을 켤 때까지는 pod 사이 트래픽이 모두 허용된다는 뜻이다. 이 공백 시간을 짧게 잡는다.

참고로 Microsoft 문서끼리 이 부분이 엇갈린다. 네트워크 정책 문서에는 kubenet+Calico를 Azure CNI Overlay+Calico로 올릴 때의 동작 설명이 있다(Calico가 정책 전용으로 바뀌고, pod 시작 직후 아웃바운드 허용이 잠시 늦을 수 있음). 이 글은 이전 절차 문서를 따라 정책을 먼저 제거하는 보수적인 순서를 권한다.

## 3단계: pod 대역 설계

Overlay에서는 노드마다 pod 대역에서 고정된 `/24`를 받는다. 노드당 최대 250 pod다. 대역을 고를 때 지킬 것은 다음과 같다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/concepts-network-azure-cni-overlay)).

- 최대 노드 수만큼 `/24`를 담을 크기여야 한다. 예를 들어 `/16`이면 `/24` 256개다.
- 클러스터 서브넷, VNet 피어링, ExpressRoute, VPN 대역과 겹치면 안 된다.
- RFC 1918 또는 RFC 6598 사설 대역을 쓴다. `169.254.0.0/16`, `172.30.0.0/16`, `172.31.0.0/16`, `192.0.2.0/24`는 쓸 수 없다.
- 여러 클러스터가 같은 pod 대역을 재사용해도 된다.
- 나중에 Linux 전용 클러스터에서 더 큰 대역으로 넓힐 수는 있지만, 줄이거나 바꿀 수는 없다.

kubenet에서 이전할 때 `--pod-cidr`를 빼면 기존 pod 대역을 그대로 쓴다. 클러스터를 키울 계획이 있으면 이때 더 큰 대역을 준다.

서브넷 NSG에 거부 규칙이 있다면 노드↔노드, 노드→pod, pod↔pod 통신을 허용하는 규칙이 있는지 확인한다. 사용자 지정 `azure-ip-masq-agent` 설정이 있다면 그 대역으로의 연결이 끊길 수 있고, 남아 있는 `azure-ip-masq-agent-config` ConfigMap은 미리 정리한다.

## 4단계: 이전 실행

```bash
az aks update --name $CLUSTER --resource-group $RG \
  --network-plugin azure --network-plugin-mode overlay \
  --pod-cidr 192.168.0.0/16
```

이 명령은 **모든 노드풀을 동시에 다시 만든다(reimage).** 노드풀별로 나눠 할 수 없다. 영향은 노드 이미지 업그레이드나 Kubernetes 버전 업그레이드와 비슷하다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/update-azure-cni)). 그래서 다음을 미리 갖춘다.

- 레플리카 2개 이상, PodDisruptionBudget, readiness probe([AKS 입문 6회](https://now.zeta4.net/a/2026-10-30-aks-106-operations-and-cost) 참고)
- 트래픽이 적은 시간대의 작업 창
- 같은 구성의 스테이징 클러스터에서 먼저 실행

이전 뒤에는 Azure CNI Node Subnet 방식으로 돌아갈 수 없다. kubenet으로도 당연히 돌아갈 수 없다.

## 5단계: Cilium으로 (별도 작업)

IP 관리 방식과 데이터 플레인은 한 번에 바꿀 수 없다. Overlay 이전이 끝나고 안정된 것을 확인한 뒤 따로 실행한다(Azure CLI 2.52.0 이상).

```bash
az aks update --name $CLUSTER --resource-group $RG --network-dataplane cilium
```

이 단계도 노드풀을 동시에 다시 만든다. Windows 노드풀이 있는 클러스터는 지원되지 않고, 노드 자동 프로비저닝(NAP)을 쓰고 있다면 끄고 전환한 뒤 다시 켠다. 기존 Azure NPM이나 Calico는 제거되고 Cilium 네트워크 정책으로 대체된다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/update-azure-cni)). 2단계에서 강제가 멈춘 정책이 Cilium 아래에서 다시 적용되는지 확인한다. Calico 전용 리소스로 쓴 정책이 있었다면 특히 주의한다.

Azure NPM 사용자에게도 같은 경로가 필요하다. NPM은 Windows 노드에서 2026년 9월 30일 지원이 끝났고, Linux 노드에서 2028년 9월 30일 은퇴한다.

## 정리: 이전 점검표

- `networkProfile` 확인, 사용자 할당 관리 ID 여부 확인
- 네트워크 정책 제거, 공백 시간 최소화 계획
- pod 대역 설계와 NSG 규칙 점검
- 스테이징에서 리허설, 앱의 PDB·레플리카 확인
- 이전 실행 → 안정화 → Cilium 전환 → 정책 재적용

다음 회에서는 이미 지원이 끝난 pod 관리 ID를 워크로드 ID로 바꾸는 방법을 다룬다.

## 출처

- [Update Azure CNI IPAM mode and data plane — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/update-azure-cni)
- [Azure CNI Overlay networking concepts — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/concepts-network-azure-cni-overlay)
- [Secure traffic between pods with network policies — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-network-policies)
- [Kubenet retires on March 31, 2028 — Azure/AKS GitHub](https://github.com/Azure/AKS/issues/4859)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
