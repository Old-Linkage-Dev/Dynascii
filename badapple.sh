while :; do
python3 ./telnet_cast.py --log './dynascii_badapple.log' --host 127.0.0.1 --port 6024 --ipps 1 --shell txtframeshell --txtframefile './BadApple/badapple.txt' --interval 0.125
sleep 60
done