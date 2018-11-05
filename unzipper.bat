@ECHO ON

setx path "C:\Program Files\7-Zip"

SET SourceDir=C:\Users\19190687\Downloads\
FOR /R %SourceDir% %%A IN ("*.gz") DO 7z x "%%~A" -o"%%~pA\"