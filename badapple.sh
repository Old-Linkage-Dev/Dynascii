while :; do
python3 ./Dynascii.py \
    --log './dynascii_badapple.log' \
    --log-level INFO \
    --host 127.0.0.1 \
    --port 6024 \
    --backlogs 4 \
    --poolsize 256 \
    --shell 'iplimitwrappershell' \
    --  --iplimit 8 \
        --shell_reject 'rejshell' \
        --shell_accept 'txtframeshell' \
            --txtframefile './res/badapple.txt' \
            --interval 0.125
sleep 60
done