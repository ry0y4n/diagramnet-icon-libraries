# Diagrams.net Icon Libraries

[![Update Icon Libraries](https://github.com/ry0y4n/diagramnet-icon-libraries/actions/workflows/update-icons.yml/badge.svg)](https://github.com/ry0y4n/diagramnet-icon-libraries/actions/workflows/update-icons.yml)

最新のクラウドサービスアイコン（Azure、AWS、GCP 等）を [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) VS Code 拡張機能で利用できるカスタムライブラリとして提供します。

> 📝 Draw.io は現在 [diagrams.net](https://www.diagrams.net/) に改名されていますが、VS Code 拡張機能は引き続き "Draw.io Integration" という名前で提供されています。

## 🚀 クイックスタート

### VS Code での設定

1. [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) 拡張機能をインストール

2. `settings.json` に以下を追加:

```json
{
  "hediet.vscode-drawio.customLibraries": [
    {
      "entryId": "Azure - Compute",
      "libName": "Azure - Compute",
      "url": "https://raw.githubusercontent.com/ry0y4n/diagramnet-icon-libraries/main/output/azure/compute.xml"
    },
    {
      "entryId": "Azure - Networking",
      "libName": "Azure - Networking",
      "url": "https://raw.githubusercontent.com/ry0y4n/diagramnet-icon-libraries/main/output/azure/networking.xml"
    }
  ]
}
```

3. Draw.io エディタを開くと、左側のパネルに新しいライブラリが表示されます！

> 💡 **全カテゴリのスニペット**: [ポータルサイト](https://ry0y4n.github.io/diagramnet-icon-libraries/) でコピー可能なsettings.jsonスニペットを取得できます。

## 📦 利用可能なライブラリ

### Azure Architecture Icons

| カテゴリ                | URL                                   |
| ----------------------- | ------------------------------------- |
| AI + Machine Learning   | `azure/ai-and-machine-learning.xml`   |
| Analytics               | `azure/analytics.xml`                 |
| App Services            | `azure/app-services.xml`              |
| Compute                 | `azure/compute.xml`                   |
| Containers              | `azure/containers.xml`                |
| Databases               | `azure/databases.xml`                 |
| DevOps                  | `azure/devops.xml`                    |
| Identity                | `azure/identity.xml`                  |
| Integration             | `azure/integration.xml`               |
| IoT                     | `azure/iot.xml`                       |
| Management + Governance | `azure/management-and-governance.xml` |
| Networking              | `azure/networking.xml`                |
| Security                | `azure/security.xml`                  |
| Storage                 | `azure/storage.xml`                   |
| Web                     | `azure/web.xml`                       |
| その他                  | [全カテゴリ一覧](output/azure/)       |

> 💡 ベース URL: `https://raw.githubusercontent.com/ry0y4n/diagramnet-icon-libraries/main/output/`
>
> 📋 全カテゴリのコピペ用スニペットは [ポータルサイト](https://ry0y4n.github.io/diagramnet-icon-libraries/) で取得できます。

## 🔄 更新スケジュール

- **Azure**: 毎週日曜日 00:00 UTC に自動更新
- アイコンは [Microsoft 公式サイト](https://learn.microsoft.com/azure/architecture/icons/) から取得

## 🛠️ ローカルで実行

```bash
# リポジトリをクローン
git clone https://github.com/ry0y4n/diagramnet-icon-libraries.git
cd diagramnet-icon-libraries

# 仮想環境を作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# ライブラリを生成
python -m src.main

# 生成されたファイルは output/ に保存されます
```

## 📁 プロジェクト構成

```
diagramnet-icon-libraries/
├── .github/workflows/     # GitHub Actions ワークフロー
├── src/
│   ├── fetchers/          # アイコン取得プラグイン
│   │   ├── base.py        # 基底クラス
│   │   └── azure.py       # Azure fetcher
│   ├── converters/        # 変換ロジック
│   │   └── svg_to_drawio.py
│   └── main.py            # メインスクリプト
├── output/                # 生成されたXMLファイル（raw.githubusercontent.com経由で配信）
│   └── azure/
├── docs/                  # GitHub Pagesポータルサイト
│   └── index.html
└── requirements.txt
```

## 🗺️ ロードマップ

- [x] Azure Architecture Icons
- [ ] AWS Architecture Icons
- [ ] Google Cloud Icons
- [ ] Material Design Icons

## 📄 ライセンス

このプロジェクトは MIT ライセンスで公開されています。

**注意**: 各アイコンセットは元のライセンスに従います：

- Azure Icons: [Microsoft 利用規約](https://learn.microsoft.com/azure/architecture/icons/)
- AWS Icons: AWS 利用規約
- GCP Icons: Google Cloud 利用規約

## 🤝 コントリビューション

Issue や Pull Request を歓迎します！

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/aws-icons`)
3. 変更をコミット (`git commit -m 'Add AWS icons fetcher'`)
4. プッシュ (`git push origin feature/aws-icons`)
5. Pull Request を作成
