# KaliRougueAccessScanner
This Repo leverages Kali Linux and AirCrack to scan Wireless Access Points


## Rogue Access Point Scanning Procedure

1. Plug in the Persistent Kali USB to a laptop
2. Reboot the laptop and boot from the USB
3. Open terminal in Kali and enter `python3 scan.py`
> scan.py contains the following nmap scan:

`nmap -sn -o nmap-results.txt 172.22.130.0/24`

> The rest of the file includes a prompt before start a wireless access point scan

4. Once you are prepared to walk around the office, press enter to begin the wireless access point scan.
5. As you walk around, it constantly scans Wireless Access Points, and gives you information about them such as how close you are to them.All of this information is outputted to a number of files.
6. Once the scan is complete, some of the smaller files are combined and the network manager on the device is restarted.
> creates aircrackOutput.csv -> main Access Point information
> creates aircrackOutput-01.log.csv -> logs all Access Point fluctuations
> creates a wireshark file that shows broadcasts made to certain Access Points
> creates an NMAP text file with all devices scanned and their MAC Addresses
7. Sorting the .csv files will help cut out all the things we don't need, and help focus out the stuff we do
