cd $(pwd)"/"$(dirname $0)
while :; do
python3 ./Dynascii.py \
    --log './dynascii_badapple.log' \
    --log-level INFO \
    --host 127.0.0.1 \
    --port 6024 \
    --blocking-io \
    --blocking-timeout 0 \
    --no-blocking-delay 3 \
    --backlogs 4 \
    --poolsize 256 \
    --shell 'dynascii.shell.contrib.iplimitwrappershell' \
    --  --iplimit 8 \
        --shell_reject 'dynascii.shell.contrib.rejshell' \
        --shell_accept 'dynascii.shell.txtframeshell' \
            --txtframefile './res/badapple.txt' \
            --interval 0.125
sleep 60
done