# ThinkAI 首批公共安全版 Skills

本目录是基于 XSkillHub 原包思路进行的 clean-room 重构，不直接转载原代码。

| Skill | 状态 | 默认权限 | 核心能力 |
|---|---|---|---|
| local-agent-memory | 可候选上架 | 本地文件 | 工作区隔离的记忆增删查导出 |
| safe-api-tester | 限制通过候选 | 白名单网络 | GET/HEAD 默认的 API 测试与脱敏报告 |
| git-safety-check | 可候选上架 | 只读 Git | 分支、身份、改动和敏感文件检查 |
| structured-sheet-writer | 可候选上架 | 本地文件 | dry-run 后 upsert CSV |
| team-blocker-tracker | 可候选上架 | 本地文件 | 卡点、SLA、去重、解决和导出 |

## 当前边界

- `structured-sheet-writer` 首版只提供本地 CSV 核心。Google Sheets 远程适配器需单独审核后增加。
- `team-blocker-tracker` 首版不发送 Telegram/飞书消息，也不调用 AI。
- 五个包仍需确认公共版维护主体和正式许可证文本后再公开发布。

## 验证

五个 Skill 已通过：

- Python 语法编译。
- `skill-creator/quick_validate.py`。
- 真实 CLI 冒烟测试。
- 内部域名和常见硬编码凭据扫描。

发布 ZIP 位于 `dist/`，校验和见 `dist/SHA256SUMS`。

## 一键安装

```bash
npx skills add https://github.com/dyc0616c-oss/thinkai-public-skills --skill local-agent-memory
npx skills add https://github.com/dyc0616c-oss/thinkai-public-skills --skill safe-api-tester
npx skills add https://github.com/dyc0616c-oss/thinkai-public-skills --skill git-safety-check
npx skills add https://github.com/dyc0616c-oss/thinkai-public-skills --skill structured-sheet-writer
npx skills add https://github.com/dyc0616c-oss/thinkai-public-skills --skill team-blocker-tracker
```
