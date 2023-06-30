# -*- coding: utf-8 -*-
"""
File to store all the constants used in the program

@author: bozzi
"""

### Product
# Product type
AA = 1
BB = 2
CC = 3
DD = 4
EE = 5
FF = 6
GG = 7
HH = 8
II = 9
JJ = 10

# Product weight
AA_WEIGHT = 20
BB_WEIGHT = 20
CC_WEIGHT = 20
DD_WEIGHT = 20
EE_WEIGHT = 20
FF_WEIGHT = 30
GG_WEIGHT = 30
HH_WEIGHT = 30
II_WEIGHT = 30
JJ_WEIGHT = 30

# Product state
TO_RELEASE = 0
RELEASING = 1
TRANSPORT = 2
BEING_PROCESSED = 3
EXITING = 4
FINISHED = 5


### Vehicles
# Vehicle type
TYPE1 = 1
TYPE2 = 2
TYPE3 = 3

# Vehicle state
WAITING_LOADING = 1
STANDBY = 2
MOVING = 3
WAITING_MACHINE = 4
GOING_CHARGER = 5
CHARGING = 6
WAITING_OUTSIDE = 7

# Battery Type
BATTERY_1 = 21
BATTERY_2 = 42
BATTERY_3 = 63

# Vehicle destination entity
DEST_MACHINE = 1
DEST_EXITINGVEHICLE = 2
DEST_CHARGINGSTATION = 3
DEST_LOADINGSTATION = 4


### Machines
# Machine state
IDLE = 0
BUSY = 1


### Recharging stations
RECH_IDLE = 0
RECH_BUSY = 1