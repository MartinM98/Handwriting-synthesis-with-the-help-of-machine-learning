# rm -rf build dist
python3 "scripts/compile/macOS/macos_setup.py" py2app
cp -r data dist/Scripturam.app/Contents/Resources
cp -r resources dist/Scripturam.app/Contents/Resources