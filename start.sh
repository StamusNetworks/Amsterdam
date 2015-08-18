#!/bin/bash

for DIR in scirius suricata elasticsearch; do
	if [ ! -e "data/$DIR" ]; then
		mkdir -p "data/$DIR";
	fi
done

docker-compose up
