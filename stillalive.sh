while :; do
python3 ./Dynascii.py \
    --log './dynascii_stillalive.log' \
    --host 127.0.0.1 \
    --port 6023 \
    --backlogs 4 \
    --poolsize 256 \
    --pthread 'poolthread' \
        --iplimit 8 \
    --shell 'pipeshell' \
        --pipeshell 'python3 ./res/still_alive_credit_fortelnet.py'
sleep 60
done