kill $(ps -ef | grep "python -m flask" | grep -v grep | awk '{print $2}')
