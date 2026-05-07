---
name: notion-daily-tasks
description: Kiểm tra nhiệm vụ hôm nay từ Notion database bằng cấu hình .env của dự án. Use when Codex needs to run, maintain, or explain this project's Notion daily task checker, including updating Notion property names, task status mapping, or the local workflow that reads project-level inputs.
---

# Notion Daily Tasks

## Workflow

Use this skill for the local project workflow that checks today's Notion tasks.

1. Keep secrets and runtime inputs in the project root `.env`.
2. Run `scripts/check_today.py` with `--project-root <project-root>`.
3. Do not hard-code `NOTION_TOKEN` or `NOTION_DATABASE_ID` in code, docs, workflows, or examples.
4. Keep generated output outside the skill. The default output file is `<project-root>/today_report.txt`.

## Project Inputs

The script reads these values from the project root `.env`:

```env
NOTION_TOKEN=Nhap_API_Cua_Ban
NOTION_DATABASE_ID=Nhap_Gia_Tri_Cua_Ban
TIMEZONE=Asia/Ho_Chi_Minh
NOTION_DATE_PROPERTY=Ngay_Bat_Dau
NOTION_STATUS_PROPERTY=Hoan_Thanh
NOTION_TITLE_PROPERTY=Nhiem_Vu
NOTION_DONE_STATUS=Đã Hoàn Thành
REPORT_FILE=today_report.txt
```

`NOTION_TOKEN` and `NOTION_DATABASE_ID` are required. Other values have defaults.

## Script

Run from the project root:

```powershell
python .\.agent\skills\notion-daily-tasks\scripts\check_today.py --project-root .
```

The script prints the report and writes it to `REPORT_FILE`.
