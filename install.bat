
set currentpath=%~dp0
echo Installation path: %currentpath%

cd C:\Python27

echo Installing caster dependencies
python -m pip install -r "%currentpath%requirements.txt"

echo Activating natlink user directory
python C:\NatLink\NatLink\confignatlinkvocolaunimacro\natlinkconfigfunctions.py -e

echo Setting natlink user directory
python C:\NatLink\NatLink\confignatlinkvocolaunimacro\natlinkconfigfunctions.py -n "%currentpath:~0,-1%"

echo Caster installed at %currentpath%

pause 1
