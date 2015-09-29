#!/bin/bash
NUM_SPAWNS=$1
SESSION=$2
SEED=$3
tmux new-session -s $SESSION -n bash -d
for ID in `seq 1 $NUM_SPAWNS`;
do
	sleep $[ ( $RANDOM % 4 )  + 1 ]s
    echo $ID
    TEMPSEED=$((($ID*1000)+$SEED))
    tmux new-window -t $ID
    tmux send-keys -t $SESSION:$ID 'java -jar ~/SerIoTics/JSON_producer/target/SerIoTics_data_generation-1.0.jar '"$TEMPSEED"' 5 60' C-m
done
