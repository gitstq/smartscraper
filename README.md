# 🦞 SmartScraper

<p align="center">
  <b>Zero-config intelligent web scraping framework</b><br>
  <b>零配置智能网页抓取框架</b><br>
  <b>零配置智慧網頁抓取框架</b>
</p>

<p align="center">
  <a href="#-english">English</a> | 
  <a href="#-简体中文">简体中文</a> | 
  <a href="#-繁體中文">繁體中文</a>
</p>

---

## 🇺🇸 English

### 🎉 Introduction

**SmartScraper** is a zero-configuration intelligent web scraping framework that lets you extract data from any webpage using natural language descriptions or simple CSS selectors. No more writing complex XPath queries or dealing with anti-bot mechanisms — just describe what you want, and SmartScraper handles the rest.

**Inspiration**: This project was inspired by [Scrapling](https://github.com/D4Vinci/Scrapling) (59K+ stars), addressing its complexity and steep learning curve by providing a truly zero-config experience with AI-powered selector generation.

**Key Differentiators**:
- 🧠 **AI-Powered Selectors**: Describe what you want in plain English/Chinese
- ⚡ **Zero Configuration**: Single URL, single command — no setup required
- 🛡️ **Built-in Anti-Detection**: Automatic retries, User-Agent rotation, polite delays
- 📦 **Multiple Export Formats**: JSON, CSV, Markdown, TXT out of the box
- 🎯 **Smart Extraction**: Auto-detects articles, links, images, tables, and meta data

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧠 **Natural Language Scraping** | `scrape(url, "extract all article titles")` — no selectors needed |
| 🎯 **CSS Selector Support** | Full CSS3 selector support for precise extraction |
| 🛡️ **Smart Retry & Rotation** | Exponential backoff with jitter, rotating User-Agents |
| 📦 **Batch Processing** | Scrape multiple URLs in one command |
| 🎨 **Rich CLI Output** | Beautiful terminal output with progress indicators |
| 📤 **Multi-Format Export** | JSON, CSV, Markdown, TXT with one line |
| 🔗 **Link Extraction** | Extract and filter links with regex patterns |
| ⚡ **Zero Dependencies** | Core functionality requires only `requests` and `bs4` |

### 🚀 Quick Start

#### Requirements
- Python 3.8+
- pip

#### Installation

```bash
pip install smartscraper-cli
```

Or install from source:

```bash
git clone https://github.com/gitstq/smartscraper.git
cd smartscraper
pip install -e ".[dev]"
```

#### Basic Usage

```python
from smartscraper import SmartScraper

# One-liner quick scrape
result = SmartScraper.quick_scrape("https://example.com")
print(result.to_json())

# Natural language scraping
scraper = SmartScraper()
result = scraper.scrape(
    "https://news.ycombinator.com",
    description="extract all article titles and links"
)
result.save("hackernews.json")

# CSS selector scraping
result = scraper.scrape(
    "https://example.com",
    selector="article h2"
)
print(result.to_csv())
```

#### CLI Usage

```bash
# Basic scrape
ss -u https://example.com

# With description
ss -u https://example.com -d "extract all links"

# With CSS selector
ss -u https://example.com -s "h1" -o titles.json

# Batch scrape
ss batch https://site1.com https://site2.com -o ./output/

# Extract links
ss links https://example.com --max 20
```

### 📖 Detailed Guide

#### Natural Language Descriptions

SmartScraper understands these description patterns:

| Description | Extracts |
|-------------|----------|
| `"extract all links"` / `"链接"` | All `<a>` tags |
| `"get images"` / `"图片"` | All `<img>` tags |
| `"extract tables"` / `"表格"` | All `<table>` elements |
| `"extract articles"` / `"文章"` | Article blocks |
| `"get title"` / `"标题"` | Page title |
| `"get meta"` / `"元数据"` | Meta tags |

#### Advanced Configuration

```python
from smartscraper import SmartScraper

# Custom configuration
scraper = SmartScraper(
    timeout=30,      # Request timeout
    retries=3,       # Retry attempts
    delay=1.0,       # Delay between requests
    headers={        # Custom headers
        "Authorization": "Bearer token"
    }
)

# Batch scraping
urls = ["https://site1.com", "https://site2.com"]
results = scraper.scrape_batch(urls, description="extract titles")

# Link extraction with filtering
links = scraper.scrape_links(
    "https://example.com",
    pattern=r"\/blog\/",
    max_links=50
)
```

### 💡 Design & Roadmap

**Design Philosophy**:
- **Simplicity First**: One import, one command — no boilerplate
- **Intelligent Defaults**: Sensible retry, delay, and header strategies
- **Extensible**: Easy to add custom extractors and exporters

**Roadmap**:
- [ ] AI model integration for intelligent selector generation
- [ ] JavaScript rendering support (headless browser)
- [ ] Proxy rotation and session management
- [ ] Webhook and streaming output
- [ ] Plugin system for custom extractors

### 📦 Packaging & Deployment

```bash
# Run tests
make test

# Build package
make build

# Upload to PyPI
make upload
```

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

### 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

## 🇨🇳 简体中文

### 🎉 项目介绍

**SmartScraper** 是一款零配置智能网页抓取框架，让你通过自然语言描述或简单的 CSS 选择器从任何网页提取数据。无需编写复杂的 XPath 查询，无需处理反爬虫机制 —— 只需描述你想要什么，SmartScraper 会处理剩下的一切。

**灵感来源**：本项目受 [Scrapling](https://github.com/D4Vinci/Scrapling)（59K+ stars）启发，针对其配置复杂、学习曲线陡峭的问题，提供了真正零配置的体验，并支持 AI 驱动的选择器生成。

**自研差异化亮点**：
- 🧠 **AI 驱动选择器**：用中文或英文描述即可自动生成抓取规则
- ⚡ **零配置启动**：一个 URL，一条命令 —— 无需任何设置
- 🛡️ **内置反检测**：自动重试、User-Agent 轮换、礼貌请求间隔
- 📦 **多格式导出**：JSON、CSV、Markdown、TXT 开箱即用
- 🎯 **智能提取**：自动识别文章、链接、图片、表格和元数据

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🧠 **自然语言抓取** | `scrape(url, "提取所有文章标题")` —— 无需选择器 |
| 🎯 **CSS 选择器支持** | 完整支持 CSS3 选择器进行精确提取 |
| 🛡️ **智能重试与轮换** | 指数退避 + 抖动，自动轮换 User-Agent |
| 📦 **批量处理** | 一条命令抓取多个 URL |
| 🎨 **精美 CLI 输出** | 带进度指示器的漂亮终端输出 |
| 📤 **多格式导出** | 一行代码导出 JSON、CSV、Markdown、TXT |
| 🔗 **链接提取** | 支持正则过滤的链接提取 |
| ⚡ **零依赖核心** | 核心功能仅需 `requests` 和 `bs4` |

### 🚀 快速开始

#### 环境要求
- Python 3.8+
- pip

#### 安装

```bash
pip install smartscraper-cli
```

或从源码安装：

```bash
git clone https://github.com/gitstq/smartscraper.git
cd smartscraper
pip install -e ".[dev]"
```

#### 基础用法

```python
from smartscraper import SmartScraper

# 一行代码快速抓取
result = SmartScraper.quick_scrape("https://example.com")
print(result.to_json())

# 自然语言抓取
scraper = SmartScraper()
result = scraper.scrape(
    "https://news.ycombinator.com",
    description="提取所有文章标题和链接"
)
result.save("hackernews.json")

# CSS 选择器抓取
result = scraper.scrape(
    "https://example.com",
    selector="article h2"
)
print(result.to_csv())
```

#### CLI 用法

```bash
# 基础抓取
ss -u https://example.com

# 带描述
ss -u https://example.com -d "提取所有链接"

# 带 CSS 选择器
ss -u https://example.com -s "h1" -o titles.json

# 批量抓取
ss batch https://site1.com https://site2.com -o ./output/

# 提取链接
ss links https://example.com --max 20
```

### 📖 详细使用指南

#### 自然语言描述

SmartScraper 支持以下描述模式：

| 描述 | 提取内容 |
|------|----------|
| `"extract all links"` / `"链接"` | 所有 `<a>` 标签 |
| `"get images"` / `"图片"` | 所有 `<img>` 标签 |
| `"extract tables"` / `"表格"` | 所有 `<table>` 元素 |
| `"extract articles"` / `"文章"` | 文章区块 |
| `"get title"` / `"标题"` | 页面标题 |
| `"get meta"` / `"元数据"` | Meta 标签 |

#### 高级配置

```python
from smartscraper import SmartScraper

# 自定义配置
scraper = SmartScraper(
    timeout=30,      # 请求超时
    retries=3,       # 重试次数
    delay=1.0,       # 请求间隔
    headers={        # 自定义请求头
        "Authorization": "Bearer token"
    }
)

# 批量抓取
urls = ["https://site1.com", "https://site2.com"]
results = scraper.scrape_batch(urls, description="提取标题")

# 带过滤的链接提取
links = scraper.scrape_links(
    "https://example.com",
    pattern=r"\/blog\/",
    max_links=50
)
```

### 💡 设计思路与迭代规划

**设计理念**：
- **极简优先**：一个导入，一条命令 —— 无样板代码
- **智能默认**：合理的重试、延迟和请求头策略
- **可扩展**：轻松添加自定义提取器和导出器

**迭代计划**：
- [ ] AI 大模型集成，实现智能选择器生成
- [ ] JavaScript 渲染支持（无头浏览器）
- [ ] 代理轮换和会话管理
- [ ] Webhook 和流式输出
- [ ] 插件系统支持自定义提取器

### 📦 打包与部署

```bash
# 运行测试
make test

# 构建包
make build

# 上传 PyPI
make upload
```

### 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feat/新功能`)
3. 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 推送分支 (`git push origin feat/新功能`)
5. 发起 Pull Request

### 📄 开源协议

MIT 协议 —— 详见 [LICENSE](LICENSE) 文件。

---

## 🇹## 🇹🇬 繁體中文

### 🎉 專案介紹

**SmartScraper** 是一款零配置智慧網頁抓取框架，讓你可以透過自然語言描述或簡單的 CSS 選擇器從任何網頁提取數據。无需編寫複雜的 XPath 查詢，無需處理反爬蟲機制 —— 只需描述你想要什麼，SmartScraper 會處理剩下的一切。

**靈感來源**：本專案受 [Scrapling](https://github.com/D4Vinci/Scrapling)（59K+ stars）啟發，針對其配置複雜、學習曲線陡峭的問題，提供了真正零配置的體驗，並支援 AI 驅動的選擇器生成。

**自研差異化亮點**：
- 🧠 **AI 驅動選擇器**：用中文或英文描述即可自動生成抓取規則
- ⚡ **零配置啟動**：一個 URL，一條命令 —— 無需任何設置
- 🛡️ **內建反檢測**：自動重試、User-Agent 輪換、禮貌請求間隔
- 📦 **多格式導出**：JSON、CSV、Markdown、TXT 開箱即用
- 🎯 **智慧提取**：自動識別文章、連結、圖片、表格和元數據

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🧠 **自然語言抓取** | `scrape(url, "提取所有文章標題")` —— 無需選擇器 |
| 🎯 **CSS 選擇器支援** | 完整支援 CSS3 選擇器進行精確提取 |
| 🛡️ **智慧重試與輪換** | 指數退避 + 抖動，自動輪換 User-Agent |
| 📦 **批量處理** | 一條命令抓取多個 URL |
| 🎨 **精美 CLI 輸出** | 帶進度指示器的漂亮終端輸出 |
| 📤 **多格式導出** | 一行程式碼導出 JSON、CSV、Markdown、TXT |
| 🔗 **連結提取** | 支援正則過濾的連結提取 |
| ⚡ **零依賴核心** | 核心功能僅需 `requests` 和 `bs4` |

### 🚀 快速開始

#### 環境要求
- Python 3.8+
- pip

#### 安裝

```bash
pip install smartscraper-cli
```

或從原始碼安裝：

```bash
git clone https://github.com/gitstq/smartscraper.git
cd smartscraper
pip install -e ".[dev]"
```

#### 基礎用法

```python
from smartscraper import SmartScraper

# 一行程式碼快速抓取
result = SmartScraper.quick_scrape("https://example.com")
print(result.to_json())

# 自然語言抓取
scraper = SmartScraper()
result = scraper.scrape(
    "https://news.ycombinator.com",
    description="提取所有文章標題和連結"
)
result.save("hackernews.json")

# CSS 選擇器抓取
result = scraper.scrape(
    "https://example.com",
    selector="article h2"
)
print(result.to_csv())
```

#### CLI 用法

```bash
# 基礎抓取
ss -u https://example.com

# 帶描述
ss -u https://example.com -d "提取所有連結"

# 帶 CSS 選擇器
ss -u https://example.com -s "h1" -o titles.json

# 批量抓取
ss batch https://site1.com https://site2.com -o ./output/

# 提取連結
ss links https://example.com --max 20
```

### 📖 詳細使用指南

#### 自然語言描述

SmartScraper 支援以下描述模式：

| 描述 | 提取內容 |
|------|----------|
| `"extract all links"` / `"連結"` | 所有 `<a>` 標籤 |
| `"get images"` / `"圖片"` | 所有 `<img>` 標籤 |
| `"extract tables"` / `"表格"` | 所有 `<table>` 元素 |
| `"extract articles"` / `"文章"` | 文章區塊 |
| `"get title"` / `"標題"` | 頁面標題 |
| `"get meta"` / `"元數據"` | Meta 標籤 |

#### 進階配置

```python
from smartscraper import SmartScraper

# 自訂配置
scraper = SmartScraper(
    timeout=30,      # 請求超時
    retries=3,       # 重試次數
    delay=1.0,       # 請求間隔
    headers={        # 自訂請求頭
        "Authorization": "Bearer token"
    }
)

# 批量抓取
urls = ["https://site1.com", "https://site2.com"]
results = scraper.scrape_batch(urls, description="提取標題")

# 帶過濾的連結提取
links = scraper.scrape_links(
    "https://example.com",
    pattern=r"\/blog\/",
    max_links=50
)
```

### 💡 設計思路與迭代規劃

**設計理念**：
- **極簡優先**：一個導入，一條命令 —— 無樣板程式碼
- **智慧預設**：合理的重試、延遲和請求頭策略
- **可擴展**：輕鬆添加自訂提取器和導出器

**迭代計劃**：
- [ ] AI 大模型集成，實現智慧選擇器生成
- [ ] JavaScript 渲染支援（無頭瀏覽器）
- [ ] 代理輪換和會話管理
- [ ] Webhook 和串流輸出
- [ ] 插件系統支援自訂提取器

### 📦 打包與部署

```bash
# 運行測試
make test

# 建構包
make build

# 上傳 PyPI
make upload
```

### 🤝 貢獻指南

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feat/新功能`)
3. 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 推送分支 (`git push origin feat/新功能`)
5. 發起 Pull Request

### 📄 開源協議

MIT 協議 —— 詳見 [LICENSE](LICENSE) 文件。
