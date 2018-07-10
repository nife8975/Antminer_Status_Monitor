# Antminer_Status_Monitor
Basic tool to monitor the hashrate of antminers via the cgminer API and reboot if the hashrate falls below a specified frequency

To use:
Edit "iplist.csv" and add the local IP address of each Antminer on your network along with the the hashrate at which you would like the miner rebooted if it's hashrate follow below (in the default units for your miner).
For Ex:

IP,RestartFrequency
10.0.0.23,780 

After editing "iplist.csv" simply run "AntminerStatusMonitor.py"
