@RD /S /Q build
@RD /S /Q dist

pyinstaller BackSeatGamerReverseProxy.py --onefile --name "ReverseProxy" -i assets/logo.ico -y --clean --noconsole --hidden-import=pyttsx3.drivers

cp assets dist -r

cd dist
zip -r "ReverseProxyWindows.zip" *

PAUSE