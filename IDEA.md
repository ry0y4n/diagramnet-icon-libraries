# 命令

新しいアプリの種を思いついたのですが、どのような機能・プラットフォーム（Web・VS Code 拡張機能・CLI）で提供するかなどが整理できていないので手伝ってください。

# 背景

[Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) という VS Code 拡張機能を使用して、VS Code 内で Draw.io の図を作成・編集できるようにしています。この拡張機能は非常に便利なのですが、以下のような不満点があります。

- 公式で提供されているアイコン（例えば Azure）が古かったり、少なかったりする

# アイデアの種

この拡張機能ではカスタムでアイコンを追加できる機能があります。settings.json に以下のように設定することで、独自のアイコンセットを追加できます。

```json
"hediet.vscode-drawio.customLibraries": [
    {
      "entryId": "MOMOSUKE Libraries",
      "libName": "MOMOSUKE ICON",
      "url": "https://raw.githubusercontent.com/ry0y4n/test-icon/refs/heads/main/Sample-Library.xml"
    }
]
```

上記の XML ファイルは SVG アイコンをエンコードしたりして Draw.io 用のカスタムライブラリ形式で保存したものです。参考までに SVG アイコンを拡張機能用の XML に変換する Python スクリプトを以下に示します。

```python
#!/usr/bin/env python3
"""
SVGファイルからdraw.io（Diagrams.net）カスタムライブラリXMLを生成するスクリプト

使用方法:
  python svg-to-drawio-library.py <svg_folder> <output_library.xml>

例:
  python svg-to-drawio-library.py ./my-icons ./MyLibrary.xml
"""

import os
import sys
import json
import zlib
import base64
import re
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET


def get_svg_dimensions(svg_content: str) -> tuple[int, int]:
    """SVGからwidth/heightを取得（デフォルト: 48x48）"""
    try:
        # XML宣言を除去してパース
        svg_content_clean = re.sub(r'<\?xml[^>]*\?>', '', svg_content)
        root = ET.fromstring(svg_content_clean)

        # width/height属性を取得
        width = root.get('width', '48')
        height = root.get('height', '48')

        # 単位を除去して数値に変換
        width = int(re.sub(r'[^0-9.]', '', width) or 48)
        height = int(re.sub(r'[^0-9.]', '', height) or 48)

        return width, height
    except Exception:
        return 48, 48


def svg_to_mxgraph_xml(svg_content: str, width: int, height: int) -> str:
    """SVGをmxGraphのXML形式に変換"""
    # SVGをBase64エンコード
    svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')

    # URLエンコード（draw.ioの形式）
    svg_data = quote(svg_base64, safe='')

    # mxGraph XML構造を作成
    mxgraph_xml = f'''<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="2" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image=data:image/svg+xml,{svg_data};" vertex="1" parent="1">
      <mxGeometry width="{width}" height="{height}" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>'''

    return mxgraph_xml


def compress_and_encode(xml_content: str) -> str:
    """XMLをdeflate圧縮してBase64エンコード"""
    # deflate圧縮（raw deflate, no header）
    compressed = zlib.compress(xml_content.encode('utf-8'), level=9)[2:-4]
    # Base64エンコード
    encoded = base64.b64encode(compressed).decode('utf-8')
    return encoded


def create_library_entry(svg_path: Path, default_size: int = 48) -> dict:
    """SVGファイルからライブラリエントリを作成"""
    # SVGを読み込み
    svg_content = svg_path.read_text(encoding='utf-8')

    # サイズを取得
    width, height = get_svg_dimensions(svg_content)

    # 最大サイズを制限（大きすぎる場合はスケール）
    max_size = 80
    if width > max_size or height > max_size:
        scale = max_size / max(width, height)
        width = int(width * scale)
        height = int(height * scale)

    # mxGraph XMLに変換
    mxgraph_xml = svg_to_mxgraph_xml(svg_content, width, height)

    # 圧縮・エンコード
    encoded_xml = compress_and_encode(mxgraph_xml)

    # タイトル（ファイル名から拡張子を除去）
    title = svg_path.stem.replace('-', ' ').replace('_', ' ').title()

    return {
        "xml": encoded_xml,
        "w": width,
        "h": height,
        "title": title,
        "aspect": "fixed"
    }


def create_library_xml(entries: list[dict]) -> str:
    """ライブラリエントリからdraw.ioライブラリXMLを生成"""
    # JSON配列として出力（draw.ioの形式）
    json_content = json.dumps(entries, ensure_ascii=False, separators=(',', ':'))

    # mxlibrary形式でラップ
    library_xml = f'<mxlibrary>{json_content}</mxlibrary>'

    return library_xml


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\n使用例:")
        print("  # フォルダ内のすべてのSVGをライブラリに変換")
        print("  python svg-to-drawio-library.py ./icons ./MyLibrary.xml")
        print("")
        print("  # 単一のSVGファイルを変換")
        print("  python svg-to-drawio-library.py ./icon.svg ./MyLibrary.xml")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # SVGファイルを収集
    svg_files = []
    if input_path.is_file() and input_path.suffix.lower() == '.svg':
        svg_files = [input_path]
    elif input_path.is_dir():
        svg_files = sorted(input_path.glob('*.svg'))
    else:
        print(f"エラー: {input_path} はSVGファイルまたはディレクトリではありません")
        sys.exit(1)

    if not svg_files:
        print(f"エラー: {input_path} にSVGファイルが見つかりません")
        sys.exit(1)

    print(f"処理中: {len(svg_files)} 個のSVGファイル")

    # 各SVGをライブラリエントリに変換
    entries = []
    for svg_file in svg_files:
        try:
            entry = create_library_entry(svg_file)
            entries.append(entry)
            print(f"  ✓ {svg_file.name} → {entry['title']} ({entry['w']}x{entry['h']})")
        except Exception as e:
            print(f"  ✗ {svg_file.name}: {e}")

    # ライブラリXMLを生成して保存
    library_xml = create_library_xml(entries)
    output_path.write_text(library_xml, encoding='utf-8')

    print(f"\n完了! ライブラリを保存しました: {output_path}")
    print(f"  → draw.ioで File > Open Library from > Device から読み込めます")


if __name__ == "__main__":
    main()
```

つまり、XML 形式でカスタムライブラリをホスティングする URL を指定すれば、そのライブラリを Draw.io 内で利用できるようになります（ちなみに `file:///` 形式は使えません）。

この機能を利用して、最新の Azure アイコンセットやその他のよく使われるアイコンセットを提供するアプリを作成できるのではないかと考えています。

例として Azure であればアイコンをダウンロードしているサイトがあります（https://learn.microsoft.com/ja-jp/azure/architecture/icons/）。

ここから最新のアイコンを定期的にダウンロードし、Draw.io 用のカスタムライブラリ XML を生成してホスティングするアプリを作成することが考えられます。

# 検討事項

もとは Azure アイコンで考えましたが、他のクラウドサービス（AWS、GCP など）や一般的な UI アイコンセット（Material Icons など）も対象にできるかもしれません。そうすると、Azure アイコンをダウンロードする部分をプラグイン化して、他のアイコンセットも同様にダウンロード・XML 生成できるようにすることが考えられます。

また、提供方法としては以下のような選択肢が考えられます。

- Web アプリケーションとしてホスティングし、ユーザーが自分で URL を取得して settings.json に追加する
- VS Code 拡張機能として提供し、インストールするだけで自動的にカスタムライブラリが追加されるようにする
- CLI ツールとして提供し、ユーザーが自分の環境でホスティングできるようにする
- GitHub Actions として提供し、リポジトリに追加するだけで自動的に最新のアイコンセットが生成されるようにする
- その他

# 要求

これらのアイデアをもとに、以下の点について整理・検討を手伝ってください。

1. 提供する機能の優先順位付け
2. 最適なプラットフォームの選定
3. その他考慮すべき点や改善案
