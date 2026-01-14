# SQLite MCP Server

Last Updated January 13, 2026 - Production/Stable v2.6.5

[![GitHub](https://img.shields.io/badge/GitHub-neverinfamous/sqlite--mcp--server-blue?logo=github)](https://github.com/neverinfamous/sqlite-mcp-server)
[![Docker Pulls](https://img.shields.io/docker/pulls/writenotenow/sqlite-mcp-server)](https://hub.docker.com/r/writenotenow/sqlite-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-v2.6.5-green)
![Status](https://img.shields.io/badge/status-Production%2FStable-brightgreen)
[![PyPI](https://img.shields.io/pypi/v/sqlite-mcp-server-enhanced)](https://pypi.org/project/sqlite-mcp-server-enhanced/)
[![Security](https://img.shields.io/badge/Security-Enhanced-green.svg)](https://github.com/neverinfamous/sqlite-mcp-server/blob/master/SECURITY.md)
[![GitHub Stars](https://img.shields.io/github/stars/neverinfamous/sqlite-mcp-server?style=social)](https://github.com/neverinfamous/sqlite-mcp-server)
[![Type Safety](https://img.shields.io/badge/Pyright-Strict-blue.svg)](https://github.com/neverinfamous/sqlite-mcp-server)

Transform SQLite into an AI-ready database engine with **73 specialized tools** for analytics, JSON, text/vector search, geospatial, and workflow automation.

 **[Wiki](https://github.com/neverinfamous/sqlite-mcp-server/wiki)** • **[Changelog](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Changelog)** • **[Release Article](https://adamic.tech/articles/sqlite-mcp-server)**


## 🚀 Quick Start

```bash
docker run -i --rm -v $(pwd):/workspace writenotenow/sqlite-mcp-server:latest --db-path /workspace/database.db
```

**MCP Config (Claude Desktop / Cursor):**
```json
{
  "mcpServers": {
    "sqlite": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-v", "${workspaceFolder}:/workspace", "writenotenow/sqlite-mcp-server:latest", "--db-path", "/workspace/database.db"]
    }
  }
}
```

## 🎛️ Tool Filtering (v2.6.4)

Reduce tool count for clients with limits (Windsurf: 100, Cursor: ~80 warning):

```bash
docker run -i --rm \
  -e SQLITE_MCP_TOOL_FILTER="-vector,-stats,-spatial,-text" \
  -v $(pwd):/workspace writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/database.db
```

| Syntax | Description |
|--------|-------------|
| `-group` | Disable all tools in group |
| `-tool` | Disable specific tool |
| `+tool` | Re-enable after group disable |

**Groups:** core(5), fts(4), vector(11), json(9), virtual(8), spatial(7), text(7), stats(8), admin(14), misc(5)

**Common filters:**
- Windsurf: `-vector,-stats,-spatial,-text` (~50 tools)
- Read-only: `-write_query,-create_table`
- Minimal: `-fts,-vector,-virtual,-spatial,-text,-stats,-admin,-misc` (~14 tools)

[Full documentation →](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Tool-Filtering)

## 📦 Deployment Options

| Method | Command | Best For |
|--------|---------|----------|
| **Docker** | `docker pull writenotenow/sqlite-mcp-server:latest` | Production |
| **PyPI** | `pip install sqlite-mcp-server-enhanced` | Python devs |
| **Source** | `git clone` + `pip install -r requirements.txt` | Development |

## 🛡️ Supply Chain Security

Use SHA-pinned images for reproducible builds:
```bash
docker pull writenotenow/sqlite-mcp-server@sha256:<manifest-digest>
# Or: writenotenow/sqlite-mcp-server:sha-abc1234
```

## ✅ Testing

```bash
docker run -i --rm writenotenow/sqlite-mcp-server:v2.6.4 --test --quick    # 30 seconds
docker run -i --rm writenotenow/sqlite-mcp-server:v2.6.4 --test --standard # Full suite
```

## 🔑 Key Features

**v2.6.4:** Tool filtering via `SQLITE_MCP_TOOL_FILTER`

**v2.6.x:** JSON Helper Tools (6 tools), auto-normalization, parameter binding, enhanced diagnostics

**Core:** 73 tools across 14 categories:
- CRUD, schema management, transactions
- FTS5 search with BM25 ranking
- Vector/semantic search with embeddings
- Statistical analysis & time series
- SpatiaLite geospatial operations
- Advanced text processing (regex, fuzzy, phonetic)
- JSONB storage, validation, path operations
- Backup/restore, PRAGMA, virtual tables

## 🎯 JSON Helper Tools

```javascript
json_insert({ table: "products", column: "metadata", data: {name: "Product", price: 29.99} })
json_update({ table: "products", column: "metadata", path: "$.price", value: 39.99, where_clause: "id = 1" })
json_query({ table: "products", column: "metadata", filter_paths: {"$.category": "electronics"} })
```

## 📊 Container Options

```bash
# Database locations
-v /host/project:/workspace --db-path /workspace/database.db
-v sqlite-data:/data --db-path /data/database.db
--db-path :memory:

# Environment
-e SQLITE_DEBUG=true
-e SQLITE_LOG_DIR=/workspace/logs
-e SQLITE_MCP_TOOL_FILTER="-vector,-stats"

# Resource limits
--memory=512m --cpus=1.0
```

## 🏷️ Available Tags

| Tag | Description |
|-----|-------------|
| `latest` | Current stable (v2.6.5) |
| `v2.6.4` | Tool filtering feature |
| `sha-abc1234` | Commit-pinned builds |

## 🔍 Resources

- [AI-Powered Wiki Search](https://search.adamic.tech)
- [GitHub Wiki](https://github.com/neverinfamous/sqlite-mcp-server/wiki)
- [Changelog](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Changelog)
- [Practical Examples (Gists)](https://gist.github.com/neverinfamous/0c8ed77ddaff0edbe31df4f4e18c33ce)
- [v2.6.0 Release Article](https://adamic.tech/articles/2025-09-22-sqlite-mcp-server-v2-6-0)
- [Full README](https://github.com/neverinfamous/sqlite-mcp-server/blob/master/README.md)

## 👏 Contributors

**v2.6.4 Tool Filtering:** [@Insighttful](https://github.com/Insighttful) ([PR #50](https://github.com/neverinfamous/sqlite-mcp-server/pull/50))

See [Contributing Guide](https://github.com/neverinfamous/sqlite-mcp-server/blob/master/CONTRIBUTING.md)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied | Check volume mount permissions |
| Database not found | Verify volume path and --db-path |
| Too many tools warning | Use `SQLITE_MCP_TOOL_FILTER` |

**Architectures:** linux/amd64, linux/arm64
