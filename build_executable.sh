echo "Building executable..."
pyinstaller --noconfirm --onefile --icon=makeitshort.ico --windowed --name "MakeItShort_win" --clean App.py

echo "Build complete. Executable is in /dist"
