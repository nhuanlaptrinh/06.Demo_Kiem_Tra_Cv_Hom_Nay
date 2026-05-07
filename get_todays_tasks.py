import runpy
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SKILL_SCRIPT = BASE_DIR / ".agent" / "skills" / "notion-daily-tasks" / "scripts" / "check_today.py"


def main() -> None:
    sys.argv = [
        str(SKILL_SCRIPT),
        "--project-root",
        str(BASE_DIR),
        *sys.argv[1:],
    ]
    runpy.run_path(str(SKILL_SCRIPT), run_name="__main__")


if __name__ == "__main__":
    main()
