@echo off
@REM @REM 隐藏bat窗口
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin

@REM 启动主程序
start cmd /c .\BackgroundMuter\BackgroundMuter.exe

set /a timer=0

@REM 等待主程序启动
:waiting
tasklist | findstr BackgroundMuter.exe > nul
if %errorlevel% neq 0 (
    echo BackgroundMuter.exe is not running
    set /a timer+=1
    if %timer% geq 30 goto end
) else (
    echo BackgroundMuter.exe is running
    goto start
)
goto waiting

@REM 等待主程序退出
:start
tasklist | findstr BackgroundMuter.exe > nul
if %errorlevel% neq 0 (
    echo BackgroundMuter.exe is not running
    @REM 启动主程序带任意参数恢复静音
    start cmd /c .\BackgroundMuter\BackgroundMuter.exe reset
    exit /b 1
) else (
    echo BackgroundMuter.exe is running
)
@REM sleep 1
ping 127.0.0.1 -n 1 > nul
goto start

:end