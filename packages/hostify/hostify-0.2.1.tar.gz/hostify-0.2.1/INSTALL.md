# Hostify - Installation and Usage Guide

## 🎉 Success! Your Demo Site is Live!

**Live Demo:** https://hostify.yaspik.tech

![Hostify Demo Site](file:///C:/Users/yuvra/.gemini/antigravity/brain/b4502ffb-7d32-45cf-b880-27dd9c595f1b/hostify_demo_site_1768112998729.png)

---

## 📦 Installing Hostify as a Python Library

### Option 1: Install from Local Directory (Development)

```bash
cd d:\xamp\htdocs\hostify
pip install -e .
```

This installs hostify in "editable" mode, so you can make changes and they'll be reflected immediately.

### Option 2: Install from GitHub (After Publishing)

```bash
pip install git+https://github.com/yuvrajarora1805/hostify.git
```

### Option 3: Install from PyPI (After Publishing)

```bash
pip install hostify
```

---

## 🚀 Using Hostify in Your Projects

### Example 1: Host an Existing Server

```python
from hostify import Host

# Your Flask/Node/PHP app is already running on port 3000
Host(
    domain="app.example.com",
    port=3000
).serve()
```

### Example 2: Host Static Files

```python
from hostify import Host

# Serve static files from a directory
Host(
    domain="mysite.example.com",
    path="./public"
).serve()
```

### Example 3: With Custom API Token

```python
from hostify import Host

Host(
    domain="app.example.com",
    port=5000,
    api_token="your_cloudflare_api_token_here"
).serve()
```

---

## 🔧 Setup Requirements

### 1. Cloudflare API Token

Create a token at: https://dash.cloudflare.com/profile/api-tokens

**Required Permissions:**
- Account → Cloudflare Tunnel → Edit
- Zone → DNS → Edit
- Zone → Zone → Read

**Set the token:**
```powershell
# Windows PowerShell
$env:CF_API_TOKEN="your_token_here"

# Linux/Mac
export CF_API_TOKEN="your_token_here"
```

### 2. Domain in Cloudflare

Make sure your domain is added to Cloudflare and nameservers are configured.

---

## 📝 Complete Example: Flask App

**app.py:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from my old PC!</h1>"

if __name__ == '__main__':
    app.run(port=5000)
```

**host.py:**
```python
from hostify import Host

# Make sure app.py is running first!
Host(
    domain="flask.example.com",
    port=5000
).serve()
```

**Run:**
```bash
# Terminal 1
python app.py

# Terminal 2
python host.py
```

Your app is now live at `https://flask.example.com`! 🎉

---

## 🛠️ Publishing to PyPI (For Library Maintainers)

### 1. Build the Package

```bash
pip install build twine
python -m build
```

### 2. Upload to PyPI

```bash
twine upload dist/*
```

### 3. Install from PyPI

```bash
pip install hostify
```

---

## 📚 API Reference

### `Host` Class

```python
Host(
    domain: str,           # Required: Full domain (e.g., "app.example.com")
    port: int = None,      # Port of existing server (mutually exclusive with path)
    path: str = None,      # Path to static files (mutually exclusive with port)
    api_token: str = None  # Optional: Cloudflare API token
)
```

**Methods:**
- `.serve()` - Start hosting (blocks until Ctrl+C)
- `.cleanup()` - Clean up resources (called automatically)

---

## ✅ Features

- ✅ One-line API
- ✅ Automatic HTTPS via Cloudflare
- ✅ Auto-download cloudflared binary
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Automatic cleanup (no leaked resources)
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Static file hosting
- ✅ Existing server support

---

## 🎯 Use Cases

1. **Development**: Share local dev server with team
2. **Demos**: Show clients your work without deployment
3. **Old PCs**: Turn old hardware into production servers
4. **Home Labs**: Host personal projects from home
5. **Testing**: Test webhooks and integrations locally

---

## 🔍 Troubleshooting

### "No server found on port X"
Make sure your application is running before starting hostify.

### "Zone not found"
Ensure your domain is added to Cloudflare.

### "No Cloudflare accounts found"
Check your API token has the correct permissions.

### Site shows 404
Wait 30-60 seconds for tunnel to fully connect.

---

## 📄 License

MIT License - see [LICENSE](file:///d:/xamp/htdocs/hostify/LICENSE)

---

## 🙏 Credits

Built on [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

**Made with ❤️ for developers who want to host from anywhere**

**Created by Yuvraj Arora**

Uses Cloudflare Tunnel & Cloudflare APIs
