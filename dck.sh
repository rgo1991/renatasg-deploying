#!/bin/bash
get_cont(){

containers=`sudo docker ps -a -q`
}
get_cont


del_cont(){
for i in ${containers[@]};do
        sudo docker stop $i | echo Stopping "$i"
	wait
	echo -n deleting "$1"
	sudo docker rm $i 
	done
}
del_cont
