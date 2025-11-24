echo "Building executable..."
pyinstaller --noconfirm --onefile --windowed --name "MakeItShort_win" --clean App.py

echo "Build complete. Executable is in /dist"
