#!/bin/bash

python3 fl/us.py &
sleep 0.1
python3 fl/qe.py &
sleep 0.1
python3 fl/pb.py &
sleep 0.1
python3 fl/os.py &
sleep 0.1
python3 fl/mot.py &
sleep 0.1
python3 fl/led.py &
sleep 0.1
#python3 ecl/uc.py &
#sleep 0.5
python3 ecl/vsc.py &
sleep 0.1
#python3 ecl/qec.py &
#sleep 0.1
#python3 ecl/pbc.py &
#sleep 0.1
#python3 ecl/ledc.py &

sleep 0.1
python3 dl/ve.py &
sleep 0.1
python3 dl/oa.py
