# ライブラリデータの検証環境の手順

## オンプレ版TeamServerの起動
**eopディレクトリ内で作業をします。**
1. TeamServerのバージョンを指定します。
   ```bash
   vim .env
   ```
   ```properties
   EOP_VERSION=3.11.9.11922092237
   ```
   このバージョンは、[EOPバージョン一覧](https://github.com/orgs/contrast-security-inc/packages/container/package/contrast) から確認してください。

2. TeamServerを起動
   ```bash
   docker-compose up -d
   ```
   http://13.113.20.198/Contrast な感じで、TeamServerに接続できます。  
   contrast_superadmin@contrastsecurity.com/XXXXXX でログインできます。XXXXXXは何方かに聞いてください。

## ライブラリデータの取得
**playwrightディレクトリ内で作業をします。**
1. ライブラリデータのバージョンを指定します。
   ```bash
   vim lib_date.env
   ```
   ```properties
   LIB_DATA_DATE=03/28/2025
   ```
   バージョンはMM/DD/YYYYのフォーマットです。
   このバージョンはContrast Hubのライブラリデータのダウンロードページで確認してください。
2. ライブラリデータを取得します。
   ```bash
   docker-compose up
   ```
   ホスト側では、/opt/contrast/work下（コンテナでは/work下）にzipとmd5sum.txtがダウンロードされます。  
   この/opt/contrast/workはTeamServerのコンテナでも、/workとしてマウントされています。

## ライブラリデータの読み込み
1. ライブラリデータzipを解凍して、TeamServerコンテナの/opt/contrast/data/libraries下に配置します。
   ```bash
   # コンテナに入ります。
   docker exec -it contrast.teamserver bash
   ```
   ```bash
   # コンテナ内で
   cd /work
   unzip Contrast-Data-Export-202503121005.zip -d /opt/contrast/data/libraries/
   ```
2. TeamServerを再起動します。
   ホスト側のeop/下で作業します。
   ```bash
   docker-compose restart teamserver
   ```
3. ログを監視します。
   これもホスト側のeop/下で実行します。
   ```bash
   docker-compose logs -f teamserver | egrep 'Beginning CSV import|completed,|complete,'
   ```
   このログが出たら読み込み完了です。一応、/opt/contrast/data/libraries/下が空っぽになっていることも確認してください。
   ```
   (LicenseImporter.java:167) Insert records complete, time: 29628.671443673s
   ```
   まっさらな状態から始めると約20時間かかります。二回目以降だと7時間ほど。
   念の為さらに確認する場合は、アプリをオンボードして、ライブラリのライセンスやCVEが出るなども確認してください。

