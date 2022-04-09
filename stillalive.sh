while :; do
python3 ./telnet_cast.py --log './dynascii_stillalive.log' --host 127.0.0.1 --port 6023 --ipps 1 --shell pipeshell --pipeshell 'python ./StillAlive/still_alive_credit_fortelnet.py'
sleep 60
done