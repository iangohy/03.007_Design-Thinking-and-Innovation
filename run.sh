#/usr/bin/env bash

COUNTER=1
while [ $COUNTER -lt 4 ]; do
    echo "-------------"
    echo "Check for internet (attempt $COUNTER)"

    if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
        echo "IPv4 is up"
	echo "IP Address: $(hostname -I)"
        git stash
        git pull git@github.com:iangohy/03.007_Design-Thinking-and-Innovation.git --rebase
        break
    else
        echo "IPv4 is down"
    fi


    if [ $COUNTER = 3 ]; then
        echo "Skipping update..."
        break
    fi

    ((COUNTER++))

    echo "Waiting for 5 seconds before retrying..."
    sleep 5
done

python3 recyclace_thread.py
