# 本地 Agent 记忆库

一个强调隐私与项目隔离的本地长期记忆 Skill。它使用 SQLite 保存项目事实、技术决策和待办背景，不依赖云端数据库。

## 适合谁

- 需要让 Agent 记住项目约定的个人开发者。
- 同时维护多个项目，且不希望记忆互相污染的用户。
- 希望记忆数据完全保存在本机的小团队。

## 核心能力

- 按工作区隔离记忆。
- 新增、检索、查看、删除和导出记忆。
- 支持设置过期时间并清理过期记录。
- 写入前自动遮蔽常见 Token、密码和私钥格式。

## 安装

```bash
npx skills add https://github.com/dyc0616c-oss/local-agent-memory
```

安装后可对 Agent 说：

```text
使用 local-agent-memory 记住：这个项目统一使用 PostgreSQL。
```

## 命令示例

```bash
python3 scripts/memory_store.py --workspace demo add \
  --title "数据库选择" --content "统一使用 PostgreSQL"

python3 scripts/memory_store.py --workspace demo search "PostgreSQL"
python3 scripts/memory_store.py --workspace demo list
python3 scripts/memory_store.py --workspace demo delete 1
```

## 数据位置

默认保存在当前项目的 `.agent-memory/`。每个工作区会生成独立 SQLite 文件。

## 安全边界

- 默认不联网。
- 不会主动扫描 Claude、浏览器或整个用户目录。
- 自动脱敏只能降低误写风险，不能代替用户检查。
- 删除记忆时必须提供准确的记录 ID。

## 卸载

删除 Skill 安装目录。若不再需要历史记忆，再手动删除项目中的 `.agent-memory/`。

## 来源

本项目参考 AgentMemory 的产品思路重新实现，不直接分发原包代码。
