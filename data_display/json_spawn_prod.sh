PRODSEED=$1
tmux new-session -s p1 -n bash -d
tmux new-window -t 1
tmux send-keys -t p1:1 'bash ~/SerIoTics/JSON_producer/spawn_kafka_streams.sh 3 p1 '"$PRODSEED"'' C-m