# 安全 API 测试器

一个以安全默认值运行的 API 批量测试 Skill。通过 CSV 定义测试接口，执行后生成本地 HTML 报告。

## 适合谁

- 测试本地或开发环境接口的开发者。
- 需要批量检查 HTTP 状态码的小团队。
- 希望测试报告自动隐藏敏感字段的用户。

## 核心能力

- CSV 批量定义测试用例。
- 支持常见 HTTP 方法。
- 生成本地 HTML 测试报告。
- 自动遮蔽 Authorization、Cookie、Token、密码和密钥。
- 使用域名白名单限制请求目标。

## 安装

```bash
npx skills add https://github.com/dyc0616c-oss/safe-api-tester
```

安装后可对 Agent 说：

```text
使用 safe-api-tester 测试本地 API，并生成脱敏报告。
```

## CSV 格式

```csv
name,method,url,expected_status,body
health,GET,http://127.0.0.1:8000/health,200,
```

## 运行示例

```bash
python3 scripts/api_tester.py tests.csv \
  --allow-host 127.0.0.1 \
  --report report.html
```

## 写请求

默认仅允许 `GET` 和 `HEAD`。执行 POST、PUT、PATCH 或 DELETE 必须同时提供：

```bash
--allow-write --confirm-write I_UNDERSTAND
```

## 安全边界

- 默认只允许本机和用户明确加入的域名。
- 不提供自动 SQL 注入、XSS、撞库或攻击载荷。
- 不会通过邮件或聊天软件外发报告。
- 仅应测试用户拥有或已获授权的接口。

## 卸载

删除 Skill 安装目录以及用户自行生成的 HTML 报告。

## 来源

本项目参考 WebAPISkill 的批量测试思路重新实现，不直接分发原包代码。
