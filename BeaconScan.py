#Uses beacontools library by citruz: https://github.com/citruz/beacontools
#and PyBluez: https://pypi.org/project/PyBluez/
#Code base from https://github.com/citruz/beacontools/blob/master/examples/scanner_ibeacon_example.py
#Last edited by ferrettt55: 2020-03-26

import time
from beacontools import BeaconScanner, BtAddrFilter

scanTime = 5; #time to scan (secs), may need to change based on beacon advertising period
runs = 5;     #number of times to run
count = 0;
n = 2;        #attenuation factor, 2 in free-space
mP = -64;     #measured power, factory-set value for beacons

#define beacon addresses
addrA0 = "18:04:ED:51:8E:9D";
addrA1 = "18:04:ED:51:7A:F1";

#lists for storing RSSI values, need one for each beacon
listA0 = [];
listA1 = [];

#define function "callback" which prints BT info
#need a copy for each beacon to scan
def callbackA0(bt_addr, rssi, packet, additional_info):
    if (rssi == 0):
        listA0.append(0);
    else:
        listA0.append(rssi);

def callbackA1(bt_addr, rssi, packet, additional_info):
    if (rssi == 0):
        listA1.append(0);
    else:
        listA1.append(rssi);

#scan for iBeacon advertisements from beacons with the specified address
scannerA0 = BeaconScanner(callbackA0,device_filter=BtAddrFilter(bt_addr=addrA0))
scannerA1 = BeaconScanner(callbackA1,device_filter=BtAddrFilter(bt_addr=addrA1))

#start scanning process
scannerA0.start()
scannerA1.start()

#run amount of scans equal to 'runs'
while (count < runs):
    time.sleep(scanTime) #wait for time period defined by 'scanTime'
    
    #average RSSI values
    avgA0 = int(sum(listA0) / len(listA0))
    avgA1 = int(sum(listA1) / len(listA1))
    
    #distance calculation, in cm
    dA0 = round((10**((mP - avgA0)/(10*n)))*100,2);
    dA1 = round((10**((mP - avgA1)/(10*n)))*100,2);
    
    #output averaged values "A0: -XX    d: XX cm"
    print("A0:",avgA0,"   d:",dA0,"cm")
    print("A1:",avgA1,"   d:",dA1,"cm")
    print(" ")
    
    # clear averaging lists
    listA0 = [];
    listA1 = [];
    
    count = count + 1; #increase 'count' value

#stop scanning
scannerA0.stop()
scannerA1.stop()
