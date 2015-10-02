ssh prod1 'bash -s' < proto_spawn_prod.sh 100000
ssh prod2 'bash -s' < proto_spawn_prod.sh 200000
ssh prod3 'bash -s' < proto_spawn_prod.sh 300000