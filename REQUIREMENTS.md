# Draw.io カスタムアイコンライブラリ提供サービス - 要件定義

## 📋 プロジェクト概要

### ビジョン

Draw.io Integration VS Code 拡張機能のユーザーに対して、最新かつ豊富なアイコンセット（Azure、AWS、GCP 等）をカスタムライブラリとして簡単に利用できるようにするサービス

### 解決する課題

| 課題                         | 影響                                   | 優先度 |
| ---------------------------- | -------------------------------------- | ------ |
| 公式アイコンが古い           | ドキュメントの品質低下、手動更新の手間 | 高     |
| アイコン数が少ない           | 表現の幅が制限される                   | 中     |
| カスタムライブラリ設定が煩雑 | 導入障壁が高い                         | 中     |

---

## 🎯 機能要件の優先順位付け

### Phase 1: MVP（最小実行可能製品）

**目標**: 最も需要の高い Azure アイコンを最新の状態で提供する

| 機能                   | 説明                                               | 必須/任意 |
| ---------------------- | -------------------------------------------------- | --------- |
| Azure アイコン自動取得 | Microsoft 公式サイトから最新アイコンをダウンロード | 必須      |
| XML 自動生成           | SVG → Draw.io カスタムライブラリ形式への変換       | 必須      |
| 静的ホスティング       | 生成した XML を HTTPS URL で公開                   | 必須      |
| 定期更新               | 週次/月次でアイコンを自動更新                      | 必須      |
| カテゴリ分類           | サービスカテゴリごとにライブラリを分割             | 任意      |

### Phase 2: 拡張

**目標**: 複数のクラウドプロバイダーと一般アイコンセットをサポート

| 機能                     | 説明                                   | 必須/任意 |
| ------------------------ | -------------------------------------- | --------- |
| AWS アイコン対応         | AWS Architecture Icons の取得・変換    | 必須      |
| GCP アイコン対応         | Google Cloud Icons の取得・変換        | 必須      |
| プラグインアーキテクチャ | 新しいアイコンソースを追加しやすい設計 | 必須      |
| Material Icons 対応      | 汎用 UI アイコンの提供                 | 任意      |
| アイコン検索 API         | 特定アイコンを検索できる API           | 任意      |

### Phase 3: ユーザー体験向上

**目標**: より使いやすいインターフェースの提供

| 機能             | 説明                                | 必須/任意 |
| ---------------- | ----------------------------------- | --------- |
| VS Code 拡張機能 | ワンクリックでライブラリを追加      | 任意      |
| Web ポータル     | ライブラリのプレビュー・URL 取得 UI | 任意      |
| カスタムビルド   | ユーザーが必要なアイコンだけを選択  | 任意      |

---

## 🏗️ プラットフォーム選定

### 推奨アーキテクチャ: **GitHub Pages + GitHub Actions**

#### 選定理由

| 観点           | 評価                                   |
| -------------- | -------------------------------------- |
| 初期コスト     | ◎ 無料（GitHub Pages の無料枠）        |
| 運用コスト     | ◎ GitHub Actions の無料枠で十分        |
| 信頼性         | ○ GitHub のインフラに依存              |
| 拡張性         | ○ 必要に応じて Cloudflare 等に移行可能 |
| 開発速度       | ◎ シンプルな構成で素早く MVP 構築      |
| メンテナンス性 | ◎ コードベースで管理、PR/Issue で運用  |

#### 代替案の比較

| プラットフォーム           | メリット                                 | デメリット               | MVP 適性 |
| -------------------------- | ---------------------------------------- | ------------------------ | -------- |
| **GitHub Pages + Actions** | 無料、シンプル、コミュニティ貢献しやすい | 大規模アクセスに制限あり | ◎        |
| Azure Static Web Apps      | Azure エコシステムとの統合               | オーバースペック         | △        |
| Cloudflare Pages           | 高速 CDN、無料枠大きい                   | 設定がやや複雑           | ○        |
| VS Code 拡張機能           | UX 最高                                  | 開発工数大、配布審査あり | △        |
| CLI                        | ローカル実行可能                         | ユーザー導入障壁高い     | △        |

---

## 📐 システムアーキテクチャ（MVP）

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │  GitHub Actions │    │   GitHub Pages  │                │
│  │  (Scheduled)    │───▶│   (Hosting)     │                │
│  └────────┬────────┘    └────────┬────────┘                │
│           │                      │                          │
│           ▼                      ▼                          │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ Icon Fetchers   │    │ Generated XMLs  │                │
│  │ (Plugins)       │    │ /azure/*.xml    │                │
│  │ - Azure         │    │ /aws/*.xml      │                │
│  │ - AWS           │    │ /gcp/*.xml      │                │
│  │ - GCP           │    │ ...             │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    VS Code + Draw.io                        │
│  settings.json:                                             │
│  "hediet.vscode-drawio.customLibraries": [                  │
│    { "url": "https://xxx.github.io/azure/compute.xml" }     │
│  ]                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 ディレクトリ構成案

```
drawio-icon-libraries/
├── .github/
│   └── workflows/
│       └── update-icons.yml      # 定期更新ワークフロー
├── src/
│   ├── fetchers/                 # アイコン取得プラグイン
│   │   ├── base.py
│   │   ├── azure.py
│   │   ├── aws.py
│   │   └── gcp.py
│   ├── converters/               # XML変換ロジック
│   │   └── svg_to_drawio.py
│   └── main.py                   # エントリーポイント
├── output/                       # 生成されるXML（GitHub Pagesで公開）
│   ├── azure/
│   │   ├── compute.xml
│   │   ├── networking.xml
│   │   └── ...
│   ├── aws/
│   └── gcp/
├── docs/                         # ドキュメント・ポータル
│   ├── index.html                # ライブラリ一覧ページ
│   └── usage.md
├── config.yaml                   # アイコンソース設定
├── requirements.txt
└── README.md
```

---

## 🔧 技術仕様

### アイコンソース設定（config.yaml）

```yaml
sources:
  azure:
    name: "Azure Architecture Icons"
    url: "https://arch-center.azureedge.net/icons/Azure_Public_Service_Icons_V*.zip"
    schedule: "weekly"
    categories:
      - name: "Compute"
        pattern: "Compute/*.svg"
      - name: "Networking"
        pattern: "Networking/*.svg"

  aws:
    name: "AWS Architecture Icons"
    url: "https://d1.awsstatic.com/webteam/architecture-icons/q1-2024/Asset-Package*.zip"
    schedule: "monthly"

  gcp:
    name: "Google Cloud Icons"
    url: "https://cloud.google.com/static/icons/..."
    schedule: "monthly"
```

### 生成されるライブラリ URL 形式

```
https://<user>.github.io/drawio-icon-libraries/azure/compute.xml
https://<user>.github.io/drawio-icon-libraries/azure/networking.xml
https://<user>.github.io/drawio-icon-libraries/aws/compute.xml
...
```

---

## ✅ 非機能要件

| 項目         | 要件                                           |
| ------------ | ---------------------------------------------- |
| 可用性       | GitHub Pages SLA 準拠（99.9%以上）             |
| 更新頻度     | Azure: 週次、AWS/GCP: 月次                     |
| レスポンス   | XML ファイルサイズ < 5MB（1 ライブラリあたり） |
| セキュリティ | HTTPS 必須、アイコンは公式ソースからのみ取得   |
| ライセンス   | 各アイコンのライセンス条件を遵守・明記         |

---

## ⚠️ 考慮すべきリスクと対策

| リスク                    | 影響度 | 対策                             |
| ------------------------- | ------ | -------------------------------- |
| アイコンソースの URL 変更 | 高     | 定期的な監視、複数ソース対応     |
| ライセンス問題            | 高     | 各ベンダーの利用規約を確認・明記 |
| GitHub Pages 帯域制限     | 中     | CDN（Cloudflare）への移行準備    |
| Draw.io 仕様変更          | 中     | 拡張機能の更新を追跡             |

---

## 📅 開発ロードマップ

```
Week 1-2: MVP開発
├── リポジトリセットアップ
├── Azure Fetcher実装
├── SVG→XML変換ロジック（既存スクリプトベース）
├── GitHub Actions定期実行設定
└── GitHub Pagesデプロイ

Week 3-4: ドキュメント・公開
├── README作成
├── 簡易ポータルページ
├── VS Code設定例の提供
└── コミュニティへの公開（Reddit, X等）

Week 5-8: Phase 2
├── AWS Fetcher実装
├── GCP Fetcher実装
├── プラグインアーキテクチャのリファクタリング
└── カテゴリ分類の改善
```

---

## 🚀 次のステップ

1. **リポジトリ作成**: `drawio-icon-libraries` または適切な名前で作成
2. **Azure Fetcher 実装**: 最新の Azure アイコンを取得するスクリプト作成
3. **GitHub Actions 設定**: 週次実行のワークフロー構築
4. **動作確認**: 生成した XML が Draw.io で正常に読み込めるか検証
