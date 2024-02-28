@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_DRONIGAMI
conda install pandas -y --force-reinstall
conda deactivate