while :; do
python3 ./Dynascii.py --log './dynascii_badapple.log' --host 127.0.0.1 --port 6024 --backlogs 4 --poolsize 256 --pthread 'poolthread' --iplimit 8 --shell 'txtframeshell' --txtframefile './res/badapple.txt' --interval 0.125
sleep 60
done