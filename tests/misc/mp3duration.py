from bavl.cmder.mp3cmder import hhmmss2secCmd, mp3Duration

mp3len = mp3Duration("/home/kokimame/Emotan/Some-song/anthem/anthem-jp.mp3")
print("Mp3len: ", mp3len, type(mp3len))

mp3sec = hhmmss2secCmd(mp3len)
print("Mp3sec: ", mp3sec)