import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests


PLACEHOLDERS = {"Nhap_API_Cua_Ban", "Nhap_Gia_Tri_Cua_Ban"}


def configure_output_encoding() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def load_env(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value in PLACEHOLDERS:
        raise RuntimeError(f"Thiếu cấu hình {name} trong file .env")
    return value


def get_plain_title(properties: dict, title_property: str) -> str:
    title = properties.get(title_property, {}).get("title", [])
    if not title:
        return "Không có tên"
    return title[0].get("plain_text") or "Không có tên"


def get_select_name(properties: dict, status_property: str) -> str:
    select_data = properties.get(status_property, {}).get("select")
    if not select_data:
        return "Chưa rõ"
    return select_data.get("name") or "Chưa rõ"


def fetch_todays_tasks(project_root: Path) -> tuple[str, list[str], list[str]]:
    load_env(project_root / ".env")

    token = require_env("NOTION_TOKEN")
    database_id = require_env("NOTION_DATABASE_ID")

    timezone_name = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")
    date_property = os.getenv("NOTION_DATE_PROPERTY", "Ngay_Bat_Dau")
    status_property = os.getenv("NOTION_STATUS_PROPERTY", "Hoan_Thanh")
    title_property = os.getenv("NOTION_TITLE_PROPERTY", "Nhiem_Vu")
    done_status = os.getenv("NOTION_DONE_STATUS", "Đã Hoàn Thành")

    today = datetime.now(ZoneInfo(timezone_name)).strftime("%Y-%m-%d")
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    payload = {
        "filter": {
            "property": date_property,
            "date": {"equals": today},
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    tasks_done: list[str] = []
    tasks_pending: list[str] = []

    for page in response.json().get("results", []):
        properties = page.get("properties", {})
        task_name = get_plain_title(properties, title_property)
        status = get_select_name(properties, status_property)
        task_line = f"- {task_name}"

        if status == done_status:
            tasks_done.append(task_line)
        else:
            tasks_pending.append(task_line)

    return today, tasks_done, tasks_pending


def build_report(today: str, tasks_done: list[str], tasks_pending: list[str]) -> str:
    lines = [
        f"NHIỆM VỤ HÔM NAY ({today})",
        "",
        "ĐÃ HOÀN THÀNH:",
        *(tasks_done or ["- Không có"]),
        "",
        "CHƯA HOÀN THÀNH:",
        *(tasks_pending or ["- Không có"]),
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check today's tasks from Notion.")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project folder that contains .env and receives the report file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    try:
        today, tasks_done, tasks_pending = fetch_todays_tasks(project_root)
        report = build_report(today, tasks_done, tasks_pending)

        report_file = project_root / os.getenv("REPORT_FILE", "today_report.txt")
        report_file.write_text(report, encoding="utf-8")
        print(report)
        return 0
    except requests.HTTPError as exc:
        print(f"Lỗi Notion API: {exc.response.status_code}", file=sys.stderr)
        print(exc.response.text, file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    configure_output_encoding()
    raise SystemExit(main())
