# Demo Notion Tasks

Dự án này dùng skill local `.agent/skills/notion-daily-tasks` để lấy danh sách nhiệm vụ hôm nay từ một Notion database và xuất ra màn hình kèm file `today_report.txt`.

## Cấu hình

Mở file `.env` và điền:

```env
NOTION_TOKEN=Nhap_API_Cua_Ban
NOTION_DATABASE_ID=Nhap_Gia_Tri_Cua_Ban
```

Các tên thuộc tính mặc định đang theo database hiện tại:

```env
NOTION_DATE_PROPERTY=Ngay_Bat_Dau
NOTION_STATUS_PROPERTY=Hoan_Thanh
NOTION_TITLE_PROPERTY=Nhiem_Vu
NOTION_DONE_STATUS=Đã Hoàn Thành
```

## Cài đặt

```powershell
pip install -r requirements.txt
```

## Chạy

```powershell
python get_todays_tasks.py
```

Hoặc chạy nhanh bằng file batch:

```powershell
.\Check_Notion_Tasks.bat
```

Muốn gọi thẳng script trong skill:

```powershell
python .\.agent\skills\notion-daily-tasks\scripts\check_today.py --project-root .
```
