# 小团队卡点助手

一个离线的小团队阻塞事项管理 Skill，用于记录卡点、负责人、优先级、SLA 和解决结果。

## 适合谁

- 需要追踪项目阻塞事项的项目经理。
- 不想部署完整任务管理平台的小团队。
- 希望月底导出卡点数据进行复盘的负责人。

## 核心能力

- 创建 P0～P3 卡点。
- 根据 SLA 自动计算截止时间。
- 使用去重键避免重复建卡。
- 查看进行中、已解决和超时状态。
- 解决卡点并记录结果。
- 导出 CSV 复盘数据。

## 安装

```bash
npx skills add https://github.com/dyc0616c-oss/team-blocker-tracker
```

安装后可对 Agent 说：

```text
使用 team-blocker-tracker 记录一个 P1 卡点：测试环境无法访问，负责人 Alice，24 小时内处理。
```

## 使用示例

```bash
python3 scripts/blocker_tracker.py --db blockers.sqlite3 add \
  --title "测试环境无法访问" \
  --owner Alice \
  --priority P1 \
  --sla-hours 24 \
  --dedup-key test-env-access

python3 scripts/blocker_tracker.py --db blockers.sqlite3 list
python3 scripts/blocker_tracker.py --db blockers.sqlite3 resolve 1 --note "权限已开通"
python3 scripts/blocker_tracker.py --db blockers.sqlite3 export --output blockers.csv
```

## 安全边界

- 默认不联网。
- 不发送 Telegram、飞书或邮件消息。
- 不调用任何 AI 模型润色催办文案。
- 不包含聊天平台 Token、群 ID 或账号凭据。

## 卸载

删除 Skill 安装目录。若不再保留数据，再手动删除指定的 SQLite 数据库和 CSV 导出文件。

## 来源

本项目参考 checkpoint-arbiter 的卡点追踪思路重新实现，移除了常驻 Bot 和外部集成。
