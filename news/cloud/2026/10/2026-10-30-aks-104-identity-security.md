---
title: AKS ID와 보안…로컬 계정을 끄고 Entra ID로, pod 인증은 워크로드 ID로, 시크릿은 Key Vault로
slug: 2026-10-30-aks-104-identity-security
topic: cloud
published_at: 2026-10-30T00:33:00+09:00
tags:
  - AKS 입문
  - AKS
  - Azure
  - Kubernetes
  - 보안
  - Microsoft Entra
summary: AKS 입문 6회 연재의 4회. 사람의 클러스터 접근(Entra ID와 Azure RBAC, 로컬 계정 끄기), 클러스터와 kubelet의 관리 ID, pod가 Azure 자원에 접근하는 워크로드 ID, Key Vault 시크릿, 배포 안전장치와 Defender for Containers, 노드 OS 보안 패치를 정리한다.
generated_by: claude
model: claude-opus-5-5
---

# AKS ID와 보안…로컬 계정을 끄고 Entra ID로, pod 인증은 워크로드 ID로, 시크릿은 Key Vault로

## 한눈에 보기

AKS 보안은 "누가 무엇으로 인증하는가"를 셋으로 나눠 보면 정리된다. 사람이 클러스터에 들어오는 길, 클러스터 자체가 Azure 자원을 다루는 길, pod 안의 앱이 데이터베이스나 Key Vault에 접근하는 길이다. 2026년의 권장 답은 각각 Microsoft Entra ID와 Azure RBAC, 관리 ID, 워크로드 ID다. 여기에 배포 규칙을 강제하는 안전장치와 런타임 보호, 노드 패치가 더해진다. AKS Automatic은 이 가운데 대부분을 기본으로 켜 둔다.

## 사람의 접근: Entra ID와 Azure RBAC

`--enable-aad --enable-azure-rbac`로 클러스터를 만들면 사용자는 Microsoft Entra ID로 로그인하고, 권한은 Azure 역할 할당으로 관리된다. 기본 제공 역할은 Azure Kubernetes Service RBAC Reader, Writer, Admin, Cluster Admin 넷이다. Reader는 Secret을 읽을 수 없다. 역할은 네임스페이스 단위로도 줄 수 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/entra-id-authorization)).

```bash
az role assignment create --role "Azure Kubernetes Service RBAC Reader" \
  --assignee <사용자나 그룹 ID> --scope $AKS_ID/namespaces/dev
```

역할 할당이 반영되기까지 최대 5분이 걸릴 수 있다. 할당 직후 권한 오류가 나도 잠시 기다려 본다.

## 로컬 계정은 끈다

AKS는 기본으로 로컬 관리자 계정을 켠 채 만들어진다. `az aks get-credentials --admin`으로 받는 그 자격 증명이다. Microsoft 문서는 이를 "감사할 수 없는 뒷문"이라고 부른다. Entra ID 연동을 했다면 `--disable-local-accounts`로 끄는 것이 좋다. 그러면 `--admin` 자격 증명 발급이 실패한다. 기존 클러스터에서 끌 때는 클러스터 인증서를 교체(rotate)해 이미 나간 자격 증명을 무효로 만든다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/local-accounts)). 로컬 계정을 끄기 전에 Entra 관리자 그룹(`--aad-admin-group-object-ids`)을 지정해 두지 않으면 아무도 클러스터를 관리하지 못하는 상황이 생길 수 있다.

## 클러스터의 ID: 두 개의 관리 ID

AKS 클러스터에는 관리 ID가 두 개 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/managed-identity-overview)).

- **클러스터(컨트롤 플레인) ID**: 부하 분산기, 디스크처럼 클러스터가 필요로 하는 Azure 자원을 만든다. 기본은 시스템 할당이고 직접 만든 사용자 할당 ID를 줄 수도 있다. 직접 만든 VNet을 쓰면 이 ID에 서브넷의 Network Contributor 권한이 필요하다.
- **kubelet ID**: 노드가 쓰는 ID다. 주로 Azure Container Registry(ACR)에서 이미지를 받을 때 쓴다.

서비스 주체(service principal)로도 클러스터를 만들 수 있지만, 문서는 관리 ID를 권장한다. 비밀번호 만료와 교체를 신경 쓸 필요가 없기 때문이다.

## pod의 ID: 워크로드 ID

pod 안의 앱이 Azure Storage나 Key Vault에 접근해야 할 때, 연결 문자열이나 키를 Secret에 넣는 대신 **Microsoft Entra 워크로드 ID**를 쓴다. Kubernetes 서비스 계정과 Azure 관리 ID를 OIDC 페더레이션으로 연결하는 방식이다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)).

1. 클러스터에서 `--enable-oidc-issuer --enable-workload-identity`를 켠다.
2. 관리 ID에 클러스터 OIDC 발급자와 서비스 계정을 잇는 페더레이션 자격 증명을 만든다. 관리 ID 하나에 최대 20개까지 만들 수 있다.
3. 서비스 계정에 `azure.workload.identity/client-id` 주석을, pod에 `azure.workload.identity/use: "true"` 레이블을 붙인다.

예전 방식인 **pod 관리 ID(pod-managed identity)는 더 이상 쓰면 안 된다.** 오픈소스 프로젝트는 2022년 10월 deprecated됐고, AKS 애드온 지원도 2025년 9월로 끝났다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-azure-ad-pod-identity)). 아직 쓰고 있다면 워크로드 ID로 옮겨야 한다.

## 시크릿: Key Vault를 볼륨으로

Kubernetes Secret은 기본적으로 base64 인코딩일 뿐이다. 민감한 값은 Azure Key Vault에 두고 Secrets Store CSI 드라이버로 pod에 볼륨으로 연결하는 것이 권장된다. `--enable-addons azure-keyvault-secrets-provider`로 켜고, 드라이버의 ID(또는 워크로드 ID)에 Key Vault Secrets User 역할을 준다. 값이 바뀌면 자동으로 교체하는 기능과, 필요하면 Kubernetes Secret으로 동기화하는 기능도 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-driver)).

## 배포 안전장치와 런타임 보호

**배포 안전장치(Deployment Safeguards)**는 Azure Policy 애드온(Gatekeeper 기반) 위에서 동작하며, 위험한 배포를 경고(`Warn`)하거나 막고 고친다(`Enforce`). 예를 들어 리소스 요청이 없는 컨테이너에 기본값을 넣고 `latest` 태그 이미지를 막는다. Pod Security Standards 수준도 함께 정한다. 기본형 클러스터는 Privileged가 기본이고, Automatic은 Baseline에 Enforce로 고정된다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/deployment-safeguards)).

```bash
az aks safeguards create --resource-group $RG --name $CLUSTER --level Warn
az aks safeguards update --resource-group $RG --name $CLUSTER --level Warn --pss-level Baseline
```

처음에는 `Warn`으로 켜서 어떤 워크로드가 걸리는지 본 뒤 `Enforce`로 올리는 순서가 안전하다. Gatekeeper가 응답하지 않으면 검사를 건너뛴다(fail-open)는 점도 알아 두자.

**Defender for Containers**는 보안 태세 점검, 레지스트리 이미지·실행 중 컨테이너·노드의 취약점 평가, 센서 기반 런타임 보호(바이너리 변조 탐지·차단, 악성코드 탐지)를 제공한다. 취약한 이미지 배포를 감사하거나 막는 기능도 있다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-containers-introduction)). 이미지 서명 검증(Image Integrity)은 아직 preview이며 문서는 운영 환경에 쓰지 말라고 한다.

## 노드 OS 보안 패치

[2회](https://now.zeta4.net/a/2026-10-30-aks-102-cluster-and-node-pools)에서 본 노드 OS 업그레이드 채널은 보안과 직결된다. 기본값 `NodeImage`는 매주 보안·버그 수정이 들어간 새 노드 이미지로 교체한다. `SecurityPatch`는 보안 패치만 더 빠르게 적용하며 일부는 재부팅 없이 반영하지만 Windows에서는 쓸 수 없다([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-node-os-image)). 채널을 `None`으로 두면 패치 적용은 전적으로 사용자 책임이 된다.

## 정리: 보안 기본 설정 한 번에

```bash
az aks create -g $RG -n $CLUSTER \
  --enable-aad --enable-azure-rbac --aad-admin-group-object-ids <관리자 그룹 ID> \
  --disable-local-accounts \
  --enable-oidc-issuer --enable-workload-identity \
  --enable-addons azure-keyvault-secrets-provider \
  --node-os-upgrade-channel NodeImage --generate-ssh-keys
```

- 사람은 Entra ID로, 권한은 네임스페이스 단위 Azure RBAC로 준다. 로컬 계정은 끈다.
- 앱의 Azure 접근은 워크로드 ID로 하고, pod 관리 ID는 걷어낸다.
- 비밀 값은 Key Vault에 둔다.
- 배포 안전장치는 Warn으로 시작해 Enforce로 올린다.

다음 회에서는 이렇게 준비한 클러스터에 앱을 배포하고 부하에 맞춰 늘리고 줄이는 방법을 다룬다.

## 출처

- [Use Azure RBAC for Kubernetes authorization — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/entra-id-authorization)
- [Manage local accounts with AKS-managed Microsoft Entra integration — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/local-accounts)
- [Managed identities in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/managed-identity-overview)
- [Microsoft Entra Workload ID with AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)
- [Use Microsoft Entra pod-managed identities in AKS — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/use-azure-ad-pod-identity)
- [Use the Azure Key Vault provider for Secrets Store CSI Driver — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/csi-secrets-store-driver)
- [Deployment safeguards — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/deployment-safeguards)
- [Overview of Defender for Containers — Microsoft Learn](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-containers-introduction)
- [Autoupgrade node OS images — Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-node-os-image)

---

이 글은 공개 출처를 바탕으로 AI가 자동 생성한 초안을 검토해 발행했으며, 중요한 판단 전에는 연결된 원문을 확인해야 합니다.
