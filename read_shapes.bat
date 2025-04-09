@echo off
REM filepath: c:\Code\ELM-Python-Client\read_shapes.bat
echo Starting execution at: %time% on %date%
set start_time=%time%

set server=https://clm.celeris.se
set user=
set password=

echo Step 1: Getting available projects - Started at %time%
oslcquery -J %server% -U %user% -P %password% -p "X" > projects.txt
echo Step 1: Completed at %time%

echo Step 2: Extracting projects - Started at %time%
python read_projects.py | findstr "  '" > projs_components.txt
echo Step 2: Completed at %time%

echo Step 3: Preparing for configurations - Started at %time%
if exist projs_components_configs.txt del projs_components_configs.txt
echo Step 3: Completed at %time%

echo Step 4: Getting component information - Started at %time%
python read_components.py >>  projs_components_configs.txt
echo Step 4: Completed at %time%

echo Step 5: Reading configurations - Started at %time%
python read_configs.py
echo Step 5: Completed at %time%

echo Step 6: Generating CSV report - Started at %time%
python retreive_csv.py
echo Step 6: Completed at %time%

set end_time=%time%
echo.
echo Script execution complete
echo Started at: %start_time%
echo Ended at:   %end_time%
echo.
echo ---------- DONE ----------