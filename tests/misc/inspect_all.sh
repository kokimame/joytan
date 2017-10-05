
for i in ./song/*.mp3
do
    echo $i
    ffmpeg -i $i 2>&1 | awk '/Duration/,/Stream/'
done

