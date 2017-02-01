#!/bin/bash

#Functionnal Level
sudo python3 fl/os.py &
sleep 2
python3 fl/us.py &
sleep 0.1
#python3 fl/qe.py &
#sleep 0.1
python3 fl/pb.py &
sleep 0.1
python3 fl/mot.py &
sleep 0.1
python3 fl/led.py &
#Psleep 0.1

#Execution Control Level
python3 ecl/usc.py &
sleep 0.1
python3 ecl/vsc.py &
sleep 0.1
#python3 ecl/qec.py &
#sleep 0.1
python3 ecl/pbc.py &
sleep 0.1
python3 ecl/ledc.py &

#Decision Level
sleep 0.1
python3 dl/ve.py &
sleep 0.1
python3 dl/oa.py &
sleep 0.1
python3 dl/pfe.py &
sleep 0.1
python3 dl/vp.py &

#Waiting for a key to be pressed before quitting
read -rsp $'Press any key to quit...\n' -n1 key

killall python3
sleep 0.1
python3 abort.py