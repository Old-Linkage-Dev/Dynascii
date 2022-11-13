cd $(pwd)"/"$(dirname $0)
while :; do
python3 -m dynascii \
    --log './dynascii_stillalive.log' \
    --log-level INFO \
    --host 127.0.0.1 \
    --port 6023 \
    --blocking-io \
    --blocking-timeout 0 \
    --no-blocking-delay 3 \
    --backlogs 4 \
    --poolsize 256 \
    --shell 'dynascii.shell.contrib.iplimitwrappershell' \
    --  --iplimit 8 \
        --shell_reject 'dynascii.shell.contrib.rejshell' \
        --shell_accept 'dynascii.shell.pipeshell' \
            --pipeshell 'python3 ./res/still_alive_credit_fortelnet.py'
sleep 60
done