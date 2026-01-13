# GraphRecon 🔎

**GraphRecon** is a fast, asynchronous GraphQL endpoint discovery tool.  
It scans common and misconfigured API paths to identify exposed GraphQL endpoints.

Designed for:
- Security researchers
- Pentesters
- Bug hunters

---

## ✨ Features

- 🚀 Fully asynchronous (aiohttp + asyncio)
- 🔍 Detects GraphQL via real GraphQL queries
- 📍 Scans dozens of common GraphQL / API paths
- 🧠 Prevents duplicate endpoint results
- 🌐 Checks if the target is reachable
- 🧪 Uses safe GraphQL payloads (`__typename`)
- 📄 Optional GraphQL schema (introspection) fetching
- ❓ Prompts the user before fetching schemas
- 🧾 Lists discovered GraphQL types (Query / Mutation / Objects)
- 📂 Bulk scanning from a target list file
- ⚡ Parallel bulk scanning (scans multiple targets concurrently for speed)
- 🧹 Auto-normalizes list targets (supports plain domains per line, removes duplicates)
- 📊 Shows total loaded target count + scan progress (e.g. `3/120`)
- 🎯 Clean and simple CLI usage

---

## 📦 Installation

### pip (Windows, macOS, Linux)

```bash
pip install graphrecon