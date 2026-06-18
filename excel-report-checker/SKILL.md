---
name: excel-report-checker
description: Check one Excel report for inconsistent totals or compare two Excel reports and produce a separate difference report. Use when users ask to check, validate, reconcile, compare, or find changes in .xlsx files while preserving the originals.
---

# Excel Report Checker

1. Confirm whether the task is a single-report check or a two-report comparison.
2. Inspect sheet names, headers, merged cells, formulas, dates, and the actual data range.
3. For a single report, check missing values, duplicates, inconsistent totals, invalid dates, and obvious outliers.
4. For two reports, use the first file as the baseline unless the user says otherwise. Match rows by a reliable key such as ID, date, order number, or name.
5. Never overwrite the source workbook. Create a new result workbook.
6. Include a summary sheet showing added, removed, changed, duplicate, and unresolved rows.
7. Mark uncertain matches as “需要确认”; do not force a match.
8. Preserve source formatting where practical and explain any formatting that could not be retained.

Read [references/result-format.md](references/result-format.md) before creating the output.
