#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $DIR

#Functionnal Level
sudo python3 $DIR/fl/os.py &
sleep 2
python3 $DIR/fl/us.py &
sleep 0.1
#python3 $DIR/fl/qe.py &
#sleep 0.1
python3 $DIR/fl/pb.py &
sleep 0.1
python3 $DIR/fl/mot.py &
sleep 0.1
python3 $DIR/fl/led.py &
#Psleep 0.1

#Execution Control Level
python3 $DIR/ecl/usc.py &
sleep 0.1
python3 $DIR/ecl/vsc.py &
sleep 0.1
#python3 $DIR/ecl/qec.py &
#sleep 0.1
python3 $DIR/ecl/pbc.py &
sleep 0.1
python3 $DIR/ecl/ledc.py &

#Decision Level
sleep 0.1
python3 $DIR/dl/ve.py &
sleep 0.1
python3 $DIR/dl/oa.py &
sleep 0.1
python3 $DIR/dl/pfe.py &
sleep 0.1
python3 $DIR/dl/vp.py &

sleep 0.1
python3 $DIR/turnStatusLedOn.py &