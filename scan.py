import os
import subprocess
import csv
import time

# ======================= CHANGABLE VARIABLES =======================
ip = '' # Ends in .0
authorized_devices_file = '' # Needs to be csv
ap_scan = True
fast_scan = False
extensive_scan = False





# Creates directory with date for all output files
date = str(subprocess.getoutput('date'))
date = date.replace(' ', '')
command = 'mkdir ' + date
os.system(command)

# Does an NMAP scan over the network
if ip != '':
	command = 'sudo nmap -sn -o nmap-results.txt ' + ip + '/24'
	os.system('cd ' + date + ' && ' + command)

# Create a file that alerts for device discrepancies
if authorized_devices_file != '':
	os.system('cd ' + date + ' && ' + 'touch nmap_device_alerts.txt')
	log = open(date + '/nmap_device_alerts.txt', 'a')
	authorized = open(authorized_devices_file, 'r')
	csvreader = csv.reader(authorized, delimiter = ',')

# Creates and defines needed variables
if authorized_devices_file != '':
	missing = []
	change = []
	authorizedKeys = []
	authorizedIPs = []
	authorizedManu = []
	y = 0
	for row in csvreader:
		if y == 0:
			y = y + 1
		else:
			authorizedKeys.append(row[0])
			authorizedIPs.append(row[1])
			authorizedManu.append(row[2])
	scan = open(date + '/nmap-results.txt', 'r')
	machistory = []
	iphistory = []
	manuhistory = []
	fs = '--top-ports 200 '
a = True
wlan_detected = False

# Loop that detects all discrepancies and writes them into the alert log
while a and ip != '' and authorized_devices_file != '':
#	Reads line of the scan
	line = scan.readline()
#	Checks if line contains the MAC Address and saves itself and the manufacturer
	if 'MAC Address' in line:
		mac = line[13:30]
		manu = line[31:]
#		Keeps MAC and Manufacturer history
		machistory.append(mac)
		manuhistory.append(manu)
#		If that said scanned MAC is not in the authorized MAC list, writes log and port scans
		if mac not in authorizedKeys:
			if fast_scan:
				fs = '--top-ports 50 '
			if extensive_scan:
				fs = ''
			log.write('Unidentified MAC Address at ' + iphistory[len(machistory)-1] + 'from ' + manu + mac + '\n')
			portscan = str(subprocess.getoutput('sudo nmap -Pn ' + fs + iphistory[machistory.index(mac)]))
			try:
				start = portscan.index('Not shown')
				end = portscan.index('MAC')
				port = portscan[start:end]
				if fs == '--top-ports 200 ' and '200 closed' in port:
					fs = '--top-ports 400 '
					portscan = str(subprocess.getoutput('sudo nmap -Pn ' + fs + iphistory[machistory.index(mac)]))
					start = portscan.index('Not shown')
					end = portscan.index('MAC')
					port = portscan[start:end]
				log.write(port + '\n\n')
			except ValueError:
				if not fast_scan:
					log.write('Port scan failed\n')
					log.write('Attempting bigger scan\n')
					portscan = str(subprocess.getoutput('sudo nmap -Pn --top-ports 800 ' + iphistory[machistory.index(mac)]))
					try:
						start = portscan.index('Not shown')
						end = portscan.index('MAC')
						port = portscan[start:end]
						log.write(port + '\n\n')
					except ValueError:
						log.write('Unable to do a port scan\n\n')
#	Checks if the line contains an ip and saves it
	elif 'scan report' in line:
		ip = line[21:]
		iphistory.append(ip)
#	Checks if there are no more filled lines in the scan results
	elif not line:
#		For all the authorized macs it checks....
		for x in authorizedKeys:
#			if that MAC was not scanned, it is written as missing
			if x not in machistory:
				missing.append('Missing MAC Address: ' + x + '\n\n')
#			if that MAC was scanned, compares its scanned IP and Manufacturer
#			to the authorized ip and manufacturer
			elif x in machistory:
				i = machistory.index(x)
				j = authorizedKeys.index(x)
				if iphistory[i] != authorizedIPs[j]:
					change.append('MAC Address ' + x + ' ip change: ' + authorizedIPs[j] +
						' --> ' + iphistory[i]+ '\n\n')
				if manuhistory[i] != authorizedManu[j]:
					change.append('MAC Address ' + x + ' detected manufacturer change: ' +
						 authorizedManu[j] + ' --> ' + manuhistory[i] + '\n\n')
#		Writes the logs in a neat way, missing MACs first, then the ip and Manufacturer changes
		for x in missing:
			log.write(x)
		for x in change:
			log.write(x)
#		Closes the used files and ends the loop
		authorized.close()
		log.close()
		scan.close()
		a = False

# Creates a buffer allowing the user to get ready before the AC scan
if ap_scan:
	input('\n\n\nPress enter to begin scan when ready.\nPress Control+C to stop scan when done')

# Sets up the AC scan
	os.system('sudo airmon-ng check kill')

# Check to see which wlan is capable of monitor mode (if any) and enters monitor mode (if able)
	output = str(subprocess.getoutput('iwconfig'))
	while (not wlan_detected):
		try:
			start = output.index('wlan')
			wlan = output[start:start+5]
			attempt = str(subprocess.getoutput('sudo airmon-ng start ' + wlan))
			if 'ERROR' in attempt:
				output = output.replace('wlan', '', 1)
			else:
				wlan_detected = True
		except ValueError:
			print('Could not find a wlan device that supports monitor mode')
			time.sleep(3)
			print('Exiting...')
			time.sleep(1)
			os.system('service NetworkManager restart')
			exit()
# Does Air-Crack network scan
	wlan = wlan + 'mon'
	os.system('cd ' + date + ' && sudo airodump-ng -w aircrackOutput ' + wlan)
	os.system('sudo airmon-ng stop ' + wlan)
	os.system('service NetworkManager restart')

# Combines and neatens files a bit
	os.system('cd ' + date + ' && sudo cat aircrackOutput-01.csv aircrackOutput-01.kismet.csv > aircrackOutput.csv')
	os.system('cd ' + date + ' && sudo rm aircrackOutput-01.csv aircrackOutput-01.kismet.csv')

