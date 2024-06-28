from cx_Freeze import setup, Executable

setup(
    name="agent",
    version="1.0",
    description="agent",
    executables=[Executable("agent.py")],
)