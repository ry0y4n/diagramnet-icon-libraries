# SVG to diagrams.net Library Converter 🎨

[![Update Icon Libraries](https://github.com/ry0y4n/vscode-diagrams-icon-builder/actions/workflows/update-icons.yml/badge.svg)](https://github.com/ry0y4n/vscode-diagrams-icon-builder/actions/workflows/update-icons.yml)
[![Try Online](https://img.shields.io/badge/🌐_Try-Online_Converter-blue?style=flat)](https://ry0y4n.github.io/vscode-diagrams-icon-builder/)
[![3200+ Icons](https://img.shields.io/badge/📦_Pre--built-3200+_Icons-green?style=flat)](https://ry0y4n.github.io/vscode-diagrams-icon-builder/)

Convert your SVG icons into custom libraries for [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio). Browser-based, no coding required.

![Portal Overview](docs/images/converter.png)

## ✨ Features

- 🌐 **Browser Conversion**: Instant conversion with online tool
- 📦 **Ready-to-Use Libraries**: 3200+ Microsoft product icons available
- 🔄 **Auto-Updates**: Weekly releases via GitHub Actions
- 🚀 **Easy Integration**: Seamless setup with VS Code + Draw.io Integration

## 🚀 Quick Start

### Option 1: Use Online Converter (Recommended)

![Online Converter](docs/images/converter-demo.gif)
_Drag & drop your SVG files and get diagrams.net libraries instantly_

1. Visit **[Online Converter](https://ry0y4n.github.io/vscode-diagrams-icon-builder/)**
2. Drag & drop your SVG files
3. Download the XML
4. Add to your VS Code `settings.json`:

```json
{
  "hediet.vscode-drawio.customLibraries": [
    {
      "entryId": "My Custom Icons",
      "libName": "My Custom Icons",
      "file": "${workspaceFolder}/icons/my-icons.xml"
    }
  ]
}
```

<details>
<summary><b>Note: Path for WSL2 + Windows Environment</b></summary>

If you're using VS Code on Windows with WSL2, use UNC path format:

```json
{
  "hediet.vscode-drawio.customLibraries": [
    {
      "entryId": "My Custom Icons",
      "libName": "My Custom Icons",
      "file": "\\\\wsl.localhost\\Ubuntu\\home\\user\\project\\icons\\my-icons.xml"
    }
  ]
}
```

</details>

### Option 2: Use Pre-built Libraries

Directly use pre-generated libraries. For example, to add Azure Compute and Networking categories:

```json
{
  "hediet.vscode-drawio.customLibraries": [
    {
      "entryId": "Azure - Compute",
      "libName": "Azure - Compute",
      "url": "https://raw.githubusercontent.com/ry0y4n/vscode-diagrams-icon-builder/main/output/azure/compute.xml"
    },
    {
      "entryId": "Azure - Networking",
      "libName": "Azure - Networking",
      "url": "https://raw.githubusercontent.com/ry0y4n/vscode-diagrams-icon-builder/main/output/azure/networking.xml"
    }
  ]
}
```

> 📋 **All Categories**: Get snippets for all 46 categories at [Library Portal](https://ry0y4n.github.io/vscode-diagrams-icon-builder/)

## 📦 Pre-built Libraries (3200+ Icons)

Ready-to-use libraries with weekly auto-updates:

![Library Portal](docs/images/prebuilt-custom-icon-demo.gif)
_Browse all categories and copy URLs instantly_

| Provider                     | Icons | Categories | Main Categories                                    |
| ---------------------------- | ----- | ---------- | -------------------------------------------------- |
| **Azure Architecture Icons** | 705   | 29         | Compute, Networking, Databases, AI/ML, Security... |
| **Microsoft 365**            | 963   | 11         | Teams, SharePoint, Planner, Project...             |
| **Microsoft Fabric**         | 1505  | 1          | Data Platform Icons                                |
| **Dynamics 365**             | 29    | 3          | Apps, Mixed Reality, Product Family                |
| **Microsoft Entra**          | 14    | 2          | Identity & Access Management                       |

> 📋 **Full List**: Browse and copy all categories at [Library Portal](https://ry0y4n.github.io/vscode-diagrams-icon-builder/)

## 🛠️ Create Custom Libraries

### Browser Conversion (Easiest)

1. Visit **[Online Converter](https://ry0y4n.github.io/vscode-diagrams-icon-builder/)**
2. Upload your SVG files (multiple files supported)
3. Preview the icons
4. Download the XML
5. Place in your project and reference from `settings.json`

### Local Conversion (For Developers)

```bash
# Clone the repository
git clone https://github.com/ry0y4n/vscode-diagrams-icon-builder.git
cd vscode-diagrams-icon-builder

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Convert SVG folder
python -m src.converters.svg_to_drawio my-icons/ output/custom.xml

# Use the generated file in VS Code
```

## 🔄 Update Schedule

Pre-built libraries are automatically updated on the following schedule:

- **Azure Architecture Icons**: Every Sunday at 00:00 UTC
  - Source: [Microsoft Learn](https://learn.microsoft.com/azure/architecture/icons/)
- **Microsoft 365**: Every Sunday at 00:00 UTC
  - Source: [Microsoft Official Repository](https://github.com/microsoft/Microsoft-365-Architecture-Icons)
- **Dynamics 365**: Every Sunday at 00:00 UTC
  - Source: [Microsoft Learn](https://learn.microsoft.com/dynamics365/get-started/icons)
- **Microsoft Fabric**: Every Sunday at 00:00 UTC
  - Source: [Fabric Samples](https://github.com/microsoft/fabric-samples)
- **Microsoft Entra**: Every Sunday at 00:00 UTC
  - Source: [Microsoft Learn](https://learn.microsoft.com/entra/architecture/architecture-icons)

## 📁 Project Structure

```
vscode-diagrams-icon-builder/
├── .github/workflows/
│   └── update-icons.yml      # Auto-update workflow
├── src/
│   ├── fetchers/             # Icon fetcher plugins
│   │   ├── base.py           # Base class
│   │   ├── azure.py          # Azure fetcher
│   │   ├── microsoft365.py   # Microsoft 365 fetcher
│   │   ├── dynamics365.py    # Dynamics 365 fetcher
│   │   ├── fabric.py         # Fabric fetcher
│   │   └── entra.py          # Entra fetcher
│   ├── converters/
│   │   └── svg_to_drawio.py  # SVG → diagrams.net conversion logic
│   └── main.py               # Main script
├── output/                   # Generated libraries (served via GitHub)
│   ├── index.json            # Metadata
│   ├── azure/
│   ├── microsoft365/
│   ├── dynamics365/
│   ├── fabric/
│   └── entra/
├── docs/
│   └── index.html            # Online converter + portal
└── requirements.txt
```

## 🗺️ Roadmap

- [x] **Core Features**

  - [x] SVG to Draw.io conversion engine
  - [x] Online browser converter
  - [x] VS Code integration guide

- [x] **Microsoft Ecosystem**

  - [x] Azure Architecture Icons (705 icons)
  - [x] Microsoft 365 Icons (963 icons)
  - [x] Dynamics 365 Icons (29 icons)
  - [x] Microsoft Fabric Icons (1505 icons)
  - [x] Microsoft Entra Icons (14 icons)

- [ ] **Other Cloud Providers**

  - [ ] AWS Architecture Icons
  - [ ] Google Cloud Icons
  - [ ] Kubernetes Icons

- [ ] **Extensions**
  - [ ] Icon preview feature
  - [ ] Batch conversion API
  - [ ] VS Code extension

## 💡 FAQ

<details>
<summary><b>Q: What is diagrams.net Integration?</b></summary>

[diagrams.net Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) is a VS Code extension that lets you edit diagrams.net diagrams directly in VS Code. The custom library feature allows you to add your own icon sets.

</details>

<details>
<summary><b>Q: Should I use local files or URLs?</b></summary>

- **URL**: For team sharing and auto-updates
- **Local Files**: For private icons, offline work, or custom icons

</details>

<details>
<summary><b>Q: Does it work with WSL2 + Windows VS Code?</b></summary>

Yes. Use UNC path format:

```json
{
  "file": "\\\\wsl.localhost\\Ubuntu\\home\\user\\project\\icons.xml"
}
```

</details>

<details>
<summary><b>Q: Can I use this commercially?</b></summary>

The tool itself is MIT licensed. However, each icon set follows its original license:

- Microsoft product icons: [Microsoft Terms](https://learn.microsoft.com/azure/architecture/icons/)
- Custom icons: Follow your own license terms

</details>

<details>
<summary><b>Q: Can I change the icon size?</b></summary>

Icons are automatically optimized during conversion (default 80px). For custom sizing, adjust the `max_size` parameter in the local script.

</details>

## 🤝 Contributing

Issues and Pull Requests are welcome!

### How to Contribute

1. **Add New Icon Sets**

   - Implement a new fetcher in `src/fetchers/`
   - Extend `BaseFetcher` and implement `fetch()` and `get_categories()`

2. **Improve Converter**

   - Optimize SVG parsing
   - Enhance compression algorithms

3. **Documentation**
   - Add usage examples
   - Expand FAQ

### Development Flow

```bash
# 1. Fork & Clone
git clone https://github.com/YOUR_USERNAME/vscode-diagrams-icon-builder.git

# 2. Create Branch
git checkout -b feature/aws-icons

# 3. Develop
# ... make changes ...

# 4. Generate XML Files
python -m src.main --clean

# 5. Generate Copy-Paste Snippets
python local-dev/generate_drawio_local_settings

# 6. Test
## Load custom library in VS Code and verify

# 7. Commit & Push
git commit -m 'feat: add AWS icons fetcher'
git push origin feature/aws-icons

# 8. Create Pull Request
```

## 📄 License

This project is licensed under the MIT License.

**Important**: Each icon set follows its original license:

| Icon Set         | License         | Source                                                                             |
| ---------------- | --------------- | ---------------------------------------------------------------------------------- |
| Azure Icons      | Microsoft Terms | [Official Page](https://learn.microsoft.com/azure/architecture/icons/)             |
| Microsoft 365    | Microsoft Terms | [GitHub](https://github.com/microsoft/Microsoft-365-Architecture-Icons)            |
| Dynamics 365     | Microsoft Terms | [Official Page](https://learn.microsoft.com/dynamics365/get-started/icons)         |
| Microsoft Fabric | Microsoft Terms | [GitHub](https://github.com/microsoft/fabric-samples)                              |
| Microsoft Entra  | Microsoft Terms | [Official Page](https://learn.microsoft.com/entra/architecture/architecture-icons) |
| Custom SVG       | Your License    | -                                                                                  |
