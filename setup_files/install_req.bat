@echo off
call C:\ProgramData\miniconda3\Scripts\activate.bat C:\ProgramData\miniconda3\envs\USaR_DRONIGAMI
conda install anaconda::pandas -y --force-reinstall
conda install conda-forge::flask -y --force-reinstall
conda install conda-forge::waitress -y --force-reinstall
conda deactivate