echo "Building executable..."
pyinstaller --noconfirm --onefile --windowed --name "MakeItShort_macos" --clean App.py

echo "Build complete. Mac OS executable is in dist/MakeItShort_macos.app"
