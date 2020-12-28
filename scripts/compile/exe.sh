# python -O -m PyInstaller "src/graphical_interface/graphical_interface.py" --noconsole --windowed --onefile --specpath "scripts/compile/"
# pyinstaller "scripts/compile/graphical_interface.spec"
pyinstaller --windowed --onefile "graphical_interface.spec"
# pyinstaller "src/graphical_interface/graphical_interface.py"
# pyinstaller "scripts/compile/graphical_interface.spec"
# --noconsole --onefile --windowed 