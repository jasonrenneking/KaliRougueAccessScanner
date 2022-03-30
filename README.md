# KaliRougueAccessScanner
This Repo leverages Kali Linux and AirCrack to scan Wireless Access Points

## Version History
### Python
Version coded in: 3.9.8

Version updated to: 3.9.8
### NMAP
Version used: 7.92
> liblua-5.3.6
> openssl-1.1.1l
> libssh2-1.10.0
> libz-1.2.11
> libpcre-8.39
> nmap-libpcap-1.7.3
> nmap-libdnet-1.12

https://nmap.org
### Aircrack-ng
Version used: 1.6

https://www.aircrack-ng.org

## Notes
When you download the scan python file, be mindful of its location. Its location is where the output files go, but is also the directory you will have to be under to run the file. Under our current configuration to make things easier, we created a python file in the default terminal directory that runs `os.system('cd <dir> && python3 scan.py')`. This just accesses its directory and runs.

The scan can also include devices, simply add the IP you want to scan its devices with under `ip = `. The IP must end in 0 as if does a full run through of the IPs (Ex: 192.168.3.0).

The scan file can also compare and contrasts to an authorized devices csv file if one is located in the same directory. This is used to generate alerts in the `nmap_device_alerts.txt` to show any unauthorized devices connected to the network and their open ports, any authorized devices that are missing, and any basic information change nmap can show. You can create this csv file, and add its name into the `authorized_devices_file = ` at the beginning of the scan file. Make sure the csv is typed with this format if typed in Excel or another spreadsheet software:

> First column will be the devices MAC Addresses

> Second Column will be the devices IP Address

> Third column is the nmap-detected manufacturer of the device

There are a couple device scan options if need be. The fast scan scans the devices top 50 most scanned ports at the most. The default scan scans the top 200 ports and if nothing shows, scans 400. The extensive scan scans the top 800 ports of the devices on the network. The scan times may vary depending on the devices connected to a network and the extense of the scan used. It is recommended to use smaller scans on networks with many devices, and vise versa an extensive scan would be more quick on a network with fewer devices. Also note with NMAP that in order to return a MAC Address from a network scan, you must be connected to that network, otherwise you will not get any MAC Addresses from the devices scanned. **NOTE: Extensive scan takes priority over the fast scan. If both enabled with True, you will always get an extensive scan!**


## Rogue Access Point Scanning Procedure

1. Plug in the Persistent Kali USB to a laptop
2. Reboot the laptop and boot from the USB
3. Plug wireless network adaptor that supports monitor mode
4. Open terminal in Kali and access directory the python script is in
5. Enter `python3 scan.py`

> The rest of the file includes a prompt before start a wireless access point scan

6. Once you are prepared to walk around the office, press enter to begin the wireless access point scan.
7. As you walk around, it constantly scans Wireless Access Points, and gives you information about them such as how close you are to them.All of this information is outputted to a number of files.
8. Once the scan is complete, some of the smaller files are combined and the network manager on the device is restarted.
> creates aircrackOutput.csv -> main Access Point information
> 
> creates aircrackOutput-01.log.csv -> logs all Access Point fluctuations
> 
> creates a wireshark file that shows broadcasts made to certain Access Points
> 
> creates an NMAP text file with all devices scanned and their MAC Addresses
9. Sorting the .csv files will help cut out all the things we don't need, and help focus out the stuff we do
