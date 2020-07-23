@ECHO OFF
python --version
echo Let us pretend that this is building something ... and takes 20 seconds

FOR /l %%A in (1, 1, 20) DO (
  ECHO Building [[01;31m %%A of 20 [00m]
  PING 8.8.8.8 -n 1 -w 1000 >NUL
)
