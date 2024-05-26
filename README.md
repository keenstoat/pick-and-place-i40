



```bash
ssh charles@192.168.158.89 'sudo ifconfig eth0 192.168.3.1/24'
ssh charles@192.168.158.89 "sudo kill -9 \$(ps -ef | grep -v grep | grep gripper_global.py | awk '{print \$2}')"
ssh -N -L 5020:192.168.3.11:502 charles@192.168.158.89 



sudo kill -9 $(ps -ef | grep -v grep | grep dockerd | awk '{print $2}')
```