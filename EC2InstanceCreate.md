# 稼働させるEC2インスタンスの構築について

## 前提として
OICD使ったパイプライン.xlsxに沿って、以下の必要なAWSリソースを作っておいてください。
- EC2にアタッチするIAMロール
- OpenIDプロバイダ
- Githubアクション用IAMロール

## EC2インスタンスの作成
**ContrastのAWS Salesで作業する場合は、OktaSEAdminのロールが必要です。**  
- Name: TeamServerForLibraryDataCheck
- AMI: Amazon Linux 2023 AMI
- アーキテクチャ: 64ビット(x86)
- インスタンスタイプ: xlarge以上（ここではt3a.xlargeで作成)
- キーペア: 任意
- VPC: 任意（ここではvpc-a3d686c4）
- サブネット: igwついてるのであれば（ここではsubnet-4c051805）
- パブリックIP: 不要（あとでEIPを割り当てるので）
- セキュリティグループ: 任意（ここではsg-051f5883c38394259）
  インバウンドに22, 80ポートが必要
- ストレージ: 500GB以上
- IAMインスタンスロール: 既に作ってあるEC2アタッチ用IAMロール（ここではTeamServerForLibraryDataCheckInstanceRole）
あとはお任せ。

## EC2起動後作業（AWSコンソール）
