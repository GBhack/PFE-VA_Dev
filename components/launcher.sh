#!/bin/bash

python3 fl/us.py &
sleep 0.5
python3 fl/mot.py &
sleep 0.5
#python3 ecl/uc.py &
#sleep 0.5
python3 ecl/vsc.py &
sleep 0.5
python3 dl/ve.py &
sleep 0.5
python3 dl/oa.py &
