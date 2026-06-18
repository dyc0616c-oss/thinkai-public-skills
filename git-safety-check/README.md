# Git 工作流安全检查

一个完全只读的 Git 仓库检查 Skill，用于提交或推送前发现常见风险。

## 适合谁

- 经常忘记检查当前分支和工作区状态的开发者。
- 希望统一分支命名规则的小团队。
- 担心误提交 `.env`、私钥和凭据文件的用户。

## 核心能力

- 检查当前分支和受保护分支。
- 检查 Git 用户名与邮箱是否配置。
- 检查未提交文件数量。
- 识别常见敏感文件名。
- 支持项目级 `.skill-git-policy.json` 规则。

## 安装

```bash
npx skills add https://github.com/dyc0616c-oss/git-safety-check
```

安装后可对 Agent 说：

```text
提交代码前使用 git-safety-check 检查当前仓库。
```

## 运行示例

```bash
python3 scripts/git_safety_check.py --repo /path/to/repository
```

## 自定义规则

复制 `references/policy.example.json` 到仓库根目录并命名为：

```text
.skill-git-policy.json
```

可以配置保护分支、允许的分支命名规则以及是否要求 Git 身份。

## 安全边界

- 只执行读取类 Git 命令。
- 不会提交、推送、合并、切换分支或修改 Git 配置。
- 不连接员工目录、内部 GitLab 或其他远程身份服务。
- 默认只报告问题，不强制阻断工作流。

## 卸载

删除 Skill 安装目录。项目中的 `.skill-git-policy.json` 可按需保留。

## 来源

本项目参考 bdgit-governance 的治理思路重新实现，并移除了组织内部规则与服务。
