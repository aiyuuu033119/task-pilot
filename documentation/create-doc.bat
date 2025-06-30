@echo off
REM Documentation Creation Script for Windows
REM Creates a new documentation file with current date and time

if "%~1"=="" (
    echo Usage: create-doc.bat ^<description^>
    echo Example: create-doc.bat feature-user-auth
    exit /b 1
)

REM Get current date and time
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set year=%datetime:~0,4%
set month=%datetime:~4,2%
set day=%datetime:~6,2%
set hour=%datetime:~8,2%
set minute=%datetime:~10,2%

REM Format date
set DATE=%year%-%month%-%day%
set TIME=%hour%%minute%
set DESCRIPTION=%1

REM Create filename
set FILENAME=%DATE%-%TIME%-%DESCRIPTION%.md

REM Get month name
if %month%==01 set MONTHNAME=January
if %month%==02 set MONTHNAME=February
if %month%==03 set MONTHNAME=March
if %month%==04 set MONTHNAME=April
if %month%==05 set MONTHNAME=May
if %month%==06 set MONTHNAME=June
if %month%==07 set MONTHNAME=July
if %month%==08 set MONTHNAME=August
if %month%==09 set MONTHNAME=September
if %month%==10 set MONTHNAME=October
if %month%==11 set MONTHNAME=November
if %month%==12 set MONTHNAME=December

REM Create file with template
(
echo # %DESCRIPTION%
echo **Date: %MONTHNAME% %day%, %year%**
echo **Type: [Feature/Bugfix/Refactor/Configuration/Other]**
echo.
echo ## Overview
echo [Brief description of what was accomplished]
echo.
echo ## Changes Made
echo.
echo ### 1. [Category of changes]
echo - [Specific change 1]
echo - [Specific change 2]
echo.
echo ## Files Modified
echo - `path/to/file1` - [What was changed]
echo - `path/to/file2` - [What was changed]
echo.
echo ## Notes
echo - [Any important considerations]
) > "%FILENAME%"

echo Created documentation file: %FILENAME%
echo Please edit the file to fill in the details.