@RD /S /Q build
@RD /S /Q dist

pyinstaller BackSeatGamerReverseProxy.py --onefile --name "ReverseProxy" -i assets/logo.ico -y --clean --noconsole

cp assets dist -r

cd dist
zip -r "ReverseProxyWindows.zip" *

PAUSE