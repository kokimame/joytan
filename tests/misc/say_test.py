from subprocess import call

call(["say", "Hello, this is test.", "-o", "greetings.aiff"])
call(["afplay", "greetings.aiff"])
