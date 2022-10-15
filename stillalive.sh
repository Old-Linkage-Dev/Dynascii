cd $(pwd)"/"$(dirname $0)
while :; do
python3 ./Dynascii.py \
    --log './dynascii_stillalive.log' \
    --log-level INFO \
    --host 127.0.0.1 \
    --port 6023 \
    --blocking-io \
    --blocking-timeout 0 \
    --no-blocking-delay 3 \
    --backlogs 4 \
    --poolsize 256 \
    --shell 'iplimitwrappershell' \
    --  --iplimit 8 \
        --shell_reject 'rejshell' \
        --shell_accept 'pipeshell' \
            --pipeshell 'python3 ./res/still_alive_credit_fortelnet.py'
sleep 60
done