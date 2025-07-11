# 稼働させるEC2インスタンスの構築について

## 前提として
OICD使ったパイプライン.xlsxに沿って、以下の必要なAWSリソースを作っておいてください。
- EC2にアタッチするIAMロール
- OpenIDプロバイダ
- Githubアクション用IAMロール

## EC2インスタンスの作成
**ContrastのAWS Salesで作業する場合は、OktaSEAdminのロールが必要です。**  
- Nameタグ: `ForTeamServerLibraryDataTest-`で始まる名前に必ずしてください。  
  Githubアクション用IAMロールの許容EC2インスタンスのルールとして`ForTeamServerLibraryDataTest-`で始めることを前提にしています。
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
1. EIPを作成する
2. 上で作ったEC2インスタンスに関連付ける
3. sshで接続してみる。
   ```bash
   # pemはEC2作成時に指定したキーペアとしてください。
   # IPアドレスは関連付けたEIPとしてください。
   ssh -i Taka.pem ec2-user@18.176.117.9
   ```
## EC2起動後作業（インスタンス内）
1. ホスト名の設定
   ```bash
   hostnamectl set-hostname teamserver4ldc
   ```
2. タイムゾーンの設定
   ```bash
   timedatectl set-timezone Asia/Tokyo
   ```
3. dockerのインストール
   ```bash
   # インストール可能なバージョンを確認する場合
   dnf search --showduplicates docker
   # dockerインストール
   dnf install -y docker-20.10.25-1.amzn2023.0.1.x86_64
   # docker-composeのインストール
   curl -L "https://github.com/docker/compose/releases/download/v2.33.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose
   # 確認
   docker -v
   docker-compose -v
   ```
   Docker起動と自動起動設定
   ```bash
   service docker restart
   systemctl enable docker
   systemctl is-enabled docker
   ```
4. vimの初期設定（任意）
   ```bash
   vim ~/.vimrc
   ```
   ```
   set nu
   set noai
   set nobackup
   set paste
   set expandtab
   set tabstop=4
   set shiftwidth=4
   set noswapfile
   syntax on
   ```
5. 本Githubリポジトリのgit clone
   ```bash
   dnf install -y git
   ```
   ```bash
   mkdir git && cd git
   git clone https://github.com/turbou/TeamServerLibraryDataTest.git
   ```
6. Contrast Hubの認証情報の環境変数を`.bash_profile`に設定
   ```bash
   vim ~/.bash_profile
   ```
   ```bash
   # User specific environment and startup programs
   export HUB_USERNAME=xxxx.yyyyyy@contrastsecurity.com
   export HUB_PASSWORD=XXXXXXXXXXXXXXXXXX
   ```
7. Hubへのアクセスのdisable対応（その１）
   ```bash
   vim /etc/hosts
   ```
   ```
   # 以下を追加
   127.0.0.1   ardy.contrastsecurity.com
   ```
   その２に関しては、TeamServerの設定画面にあるので、パイプラインで実施されます。

以上
