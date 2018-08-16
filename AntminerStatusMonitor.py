#!/usr/bin/env python2.7
"""
Antminer Status Monitor
Author: Nicholas Fentekes

Basic tool to monitor antminers on the local network, and reboot if the hashrate
drops below the specified frequency

Edit the included iplist.csv file to specify local ipv4 addresses and the
targer frequency for each corresponding miner to be restarted when when it's
hashrate falls below
"""
import socket
import json
import sys
import time
import paramiko
import pandas as pd

def linesplit(socket):
	buffer = socket.recv(4096)
	done = False
	while not done:
		try:
			more = socket.recv(4096)
			if not more:
				done = True
			else:
				buffer = buffer+more
		except:
			print("ERROR: SOCKET ERROR!")
	if buffer:
		return buffer
freq = 530

def monitorAntminerStatus(api_ips,api_port=4028,restartFreqs):
	while(True):
		for i in range(len(api_ips)):
			try:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((api_ips[i],int(api_port)))
				response = linesplit(s)
				response = response.decode().replace('\x00','')
				response = json.loads(response)
				s.close()
			except:
				print("API ERROR")

			print("GH/s 5s: ",response['SUMMARY'][0]['GHS 5s'])
			print("Miner Down: ",response['SUMMARY'][0]['GHS 5s']=='0.00'or response['SUMMARY'][0]['GHS 5s']==0 or float(response['SUMMARY'][0]['GHS 5s'])<restartFreqs[i])
			if(response['SUMMARY'][0]['GHS 5s']=='0.00'or response['SUMMARY'][0]['GHS 5s']==0 or float(response['SUMMARY'][0]['GHS 5s'])<restartFreqs[i]):
				time.sleep(60)
				done = False
				while not done:
					try:
						s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						s.connect((api_ip,int(api_port)))
						s.send(json.dumps({"command":"summary"}).encode('utf-8'))
						response = linesplit(s)
						response = response.decode().replace('\x00','')
						response = json.loads(response)
						s.close()
						done=True
					except:
						print("socket error")
						time.sleep(10)
				if(response['SUMMARY'][0]['GHS 5s']=='0.00'or response['SUMMARY'][0]['GHS 5s']==0 or float(response['SUMMARY'][0]['GHS 5s'])<restartFreqs[i]):
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					done = False
					while not done:
						try:
							ssh.connect(api_ips[i], username='root', password='admin')
							done = True
						except:
							print('connect error')
							time.sleep(10)
					ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('/sbin/reboot')
					print("rebooting\n")
					time.sleep(360)
		time.sleep(30)

if __name__ == "__main__":
	ipFile = pd.read_csv("iplist.csv")
	monitorAntminerStatus(ipFile["IP"].tolist(),ipFile["RestartFrequency"].tolist())
