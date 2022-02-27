@echo Start
@echo on
set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib

@echo Creating log14109.html

echo ^<head^> > .\release\log14109.html
echo ^<link rel="stylesheet" href="style.css"^> >> .\release\log14109.html
echo ^<title^>Logik - NINA API (14109)^</title^> >> .\release\log14109.html
echo ^<style^> >> .\release\log14109.html
echo body { background: none; } >> .\release\log14109.html
echo ^</style^> >> .\release\log14109.html
echo ^<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"^> >> .\release\log14109.html
echo ^</head^> >> .\release\log14109.html

type .\README.md | C:\Python27\python -m markdown -x tables >> .\release\log14109.html

@echo Generate code
cd ..\..
C:\Python27\python generator.pyc "14109_NINA_API" UTF-8

@echo Copying files
xcopy .\projects\14109_NINA_API\src .\projects\14109_NINA_API\release /exclude:.\projects\14109_NINA_API\src\exclude.txt

@echo Fertig.

@pause