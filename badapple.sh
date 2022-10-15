PSD=$(pwd)"/"$(dirname $0)
while :; do
python3 $PSD/Dynascii.py \
    --log '$PSD/dynascii_badapple.log' \
    --log-level INFO \
    --host 127.0.0.1 \
    --port 6024 \
    --blocking-io \
    --blocking-timeout 0 \
    --no-blocking-delay 3 \
    --backlogs 4 \
    --poolsize 256 \
    --shell 'iplimitwrappershell' \
    --  --iplimit 8 \
        --shell_reject 'rejshell' \
        --shell_accept 'txtframeshell' \
            --txtframefile '$PSD/res/badapple.txt' \
            --interval 0.125
sleep 60
done