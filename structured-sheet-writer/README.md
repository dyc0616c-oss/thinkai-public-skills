# 表格结构化写入工具

一个“先预览、再落盘”的结构化表格写入 Skill。支持将 JSON 或 CSV 数据安全地新增或更新到本地 CSV。

## 适合谁

- 需要批量整理结构化数据的运营人员。
- 希望根据唯一键更新表格的开发者。
- 担心批量导入时误覆盖数据的用户。

## 核心能力

- 支持 JSON 和 CSV 输入。
- 使用 Schema 限制允许的列。
- 使用一个或多个字段作为唯一键。
- 写入前显示新增与覆盖数量。
- 拒绝空键、重复键和未知列。

## 安装

```bash
npx skills add https://github.com/dyc0616c-oss/structured-sheet-writer
```

安装后可对 Agent 说：

```text
使用 structured-sheet-writer 预览这批 JSON 数据写入 CSV 后的变化。
```

## 使用示例

先预览：

```bash
python3 scripts/sheet_writer.py \
  --input records.json \
  --target table.csv \
  --schema references/schema.example.json \
  --key id
```

确认后写入：

```bash
python3 scripts/sheet_writer.py \
  --input records.json \
  --target table.csv \
  --schema references/schema.example.json \
  --key id \
  --apply
```

## 安全边界

- 默认 dry-run，不会修改目标文件。
- 仅访问用户明确提供的输入、Schema 和目标路径。
- 当前公共版不连接 Google Sheets，也不读取 Google 凭据。
- upsert 键冲突时不会静默覆盖。

## 卸载

删除 Skill 安装目录。用户生成的 CSV 文件不会被自动删除。

## 来源

本项目参考 sheets-io-toolkit 的结构化写入思路重新实现，不直接分发原包代码。
