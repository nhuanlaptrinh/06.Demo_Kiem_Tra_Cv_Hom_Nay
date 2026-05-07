@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Dang kiem tra nhiem vu hom nay tren Notion...
echo --------------------------------------------------------

python "%~dp0get_todays_tasks.py"

echo.
echo --------------------------------------------------------
if "%1"=="nopause" goto end

echo Nhan phim bat ky de dong cua so nay...
pause >nul

:end
