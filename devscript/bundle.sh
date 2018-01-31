#!/bin/bash

if [ ! -d "design" ]
then
    echo "Please run this from the project root"
    exit
fi

cd ..
# Setting input folder and output folder
version=0.0.0
inbase=joytan
outbase=~/Desktop/$(date +"%m-%d_%H-%M-%S")_Joytan

mkdir ${outbase}
# Binary folder
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "darwin"* ]]; then
    binary=${outbase}
else
    binary=${outbase}/bin
    mkdir ${binary}
fi

# Freeze the application using Pyinstaller
if [[ "$OSTYPE" == "msys" ]]; then
    # On Windows, noconsole option conflicts with pydub's subprocess
    echo "Bundle for Windows"
    pyinstaller ${inbase}/runapp --onefile \
       --hidden-import='configparser' --specpath=${outbase} \
       --distpath=${binary} --workpath=${outbase}/build \
       --name='joytan' --icon=${inbase}/logo/joytan.ico

    cp ${inbase}/LICENSE.txt ${binary}
    cp ${inbase}/design/default_textbook.html ${binary}
    cp ${inbase}/logo/joytan.ico ${binary}
    cp ${inbase}/devscript/build_nsis.nsi ${binary}
    cp "C:\Program Files (x86)\Lame For Audacity\lame.exe" ${binary}
    cp "C:\Program Files\ffmpeg\bin\ffmpeg.exe" ${binary}
    makensis ${binary}/build_nsis.nsi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Bundle for Mac"
    pyinstaller ${inbase}/runapp --onefile --noconsole \
       --hidden-import='configparser' --specpath=${outbase} \
       --distpath=${binary} --workpath=${outbase}/build \
       --name='Joytan' --icon=${inbase}/logo/joytan.icns

    cp /usr/local/bin/ffmpeg ${binary}/Joytan.app/Contents/MacOS
    cp /usr/local/bin/lame ${binary}/Joytan.app/Contents/MacOS
    cp ${inbase}/design/default_textbook.html ${binary}/Joytan.app/Contents/MacOS
    dmgbuild -s ${inbase}/devscript/build_dmg.py \
        -D app=${binary}/Joytan.app "Joytan" ${binary}/joytan-${version}.dmg

else
    echo "Bundle for Linux"
    pyinstaller ${inbase}/runapp --onefile --noconsole \
       --hidden-import='configparser' --specpath=${outbase} \
       --distpath=${binary} --workpath=${outbase}/build \
       --name='joytan' --icon=${inbase}/logo/joytan.ico
fi

rm -rf ${outbase}/build ${outbase}/joytan.spec

# Move requirements for Linux installation
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    cp ${inbase}/joytan.desktop ${inbase}/joytan.xml \
    ${inbase}/joytan.xpm ${inbase}/Makefile ${outbase}
    cd ${outbase}
    tar -cvjSf joytan-${version}-amd64.tar.bz2 *
fi

