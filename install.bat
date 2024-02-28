@echo off
call C:\DRONIGAMI\setup_files\setup.bat
call C:\DRONIGAMI\setup_files\install_pandas.bat
call C:\DRONIGAMI\setup_files\install_flask.bat
call C:\DRONIGAMI\setup_files\install_waitress.bat
schtasks /create /sc onlogon /tn DRONIGAMI_RUN /tr C:\DRONIGAMI\Run_App - Shortcut.lnk