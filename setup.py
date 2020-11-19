
from cx_Freeze import setup, Executable
setup(
    name="rename",
    version="1.0",
    description="rename_files",
    author="潇洒郎",
    executables=[Executable("main.py")])  