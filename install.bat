@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_PIIBlur
call C:\DRONIGAMI\setup_files\setup.bat
call C:\DRONIGAMI\setup_files\install_req.bat
schtasks /create /sc onlogon /tn DRONIGAMI_RUN /tr C:\DRONIGAMI\Run_App.bat