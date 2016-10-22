#!/bin/bash

python3 components/fl/us.py &
sleep 0.5
python3 components/fl/mot.py &
sleep 0.5
#python3 components/ecl/uc.py &
#sleep 0.5
python3 components/ecl/vsc.py &
sleep 0.5
python3 components/dl/ve.py &
sleep 0.5
python3 components/dl/oa.py &
