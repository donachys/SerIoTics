ssh prod1 'bash -s' < json_spawn_prod.sh 100000
ssh prod2 'bash -s' < json_spawn_prod.sh 200000
ssh prod3 'bash -s' < json_spawn_prod.sh 200000