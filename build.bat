@RD /S /Q build
@RD /S /Q dist

pyinstaller BackSeatGamerReverseProxy.py --onefile --name "ReverseProxy" -i assets/logo.ico -y --clean --noconsole --hidden-import=pyttsx3.drivers --hidden-import=pyttsx3.drivers.sapi5 --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32"

cp assets dist -r

cd dist
zip -r "ReverseProxyWindows.zip" *

PAUSE