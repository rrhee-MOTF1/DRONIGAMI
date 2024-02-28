@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_DRONIGAMI
conda install waitress -y --force-reinstall
conda deactivate