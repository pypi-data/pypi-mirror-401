SQLite MCP Server -- Release Notes

Version 2.6.4 - New Tool Filtering Feature

## 🎛️ Tool Filtering Feature

This release introduces the **SQLITE_MCP_TOOL_FILTER** environment variable for selective tool enable/disable, addressing MCP client tool limits (e.g., Windsurf's 100-tool limit).

### ✨ New Features

- **Tool Filtering System** - Selectively enable/disable tools via environment variable
- **10 Tool Groups** - Logical grouping: core, fts, vector, json, virtual, spatial, text, stats, admin, misc
- **Flexible Filter Syntax**:
  - `-group` - Disable all tools in a group
  - `-tool` - Disable a specific tool  
  - `+tool` - Re-enable a tool after group disable
- **Left-to-Right Processing** - Rules processed in order for precise control
- **Universal Compatibility** - Works with all MCP clients (Cursor, Claude Desktop, Windsurf, etc.)

### 📖 Documentation

- Added [Tool Filtering](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Tool-Filtering) wiki page
- Added [Changelog](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Changelog) to wiki
- Added wiki sidebar navigation
- Updated all READMEs with tool filtering examples

### 🧪 Testing

- Comprehensive test suite with 410 lines of pytest tests
- Covers filter syntax, order of operations, edge cases, and real-world scenarios

### 📦 Example Configurations

```bash
# Reduce to ~40 tools (Windsurf-compatible)
SQLITE_MCP_TOOL_FILTER="-vector,-stats,-spatial,-text"

# Read-only mode
SQLITE_MCP_TOOL_FILTER="-write_query,-create_table"

# Core + JSON only (~14 tools)
SQLITE_MCP_TOOL_FILTER="-fts,-vector,-virtual,-spatial,-text,-stats,-admin,-misc"
```

### 👏 Contributors

- [@Insighttful](https://github.com/Insighttful) - Tool filtering feature ([PR #50](https://github.com/neverinfamous/sqlite-mcp-server/pull/50))

---

**Full Changelog**: https://github.com/neverinfamous/sqlite-mcp-server/wiki/Changelog

