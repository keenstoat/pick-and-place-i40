# Delta Robot 

Product page: https://www.igus.eu/product/20433?artNr=DLE-DR-0005

The [iRC User Manual](https://www.igus.eu/ContentData/Products/Downloads/iRC_R13_UserGuide_en.pdf) has the Modbus documentation. This manual can be found in the Downloads tab or the product page.

The [Robot Software](https://www.igus.eu/info/robot-software) page also has interesting documentation. Here one can find information on the [Modbus Server](https://wiki.cpr-robots.com/index.php/Modbus_Server)


## Connecting to the robot using Ethernet

The robot uses linux based system for its main computer with IP `192.168.3.11/24`

A PC connecting to the robot must have an IP address in the `192.168.3.0/24` network. 

> We use `192.168.3.1/24`
>
> Remember .0 and .255 cannot be used (they are the network and broadcast addresses)

The robot can be connected:
- Directly to a PC
- To a LAN

In the Technikum, two configurations work:
- Connect the robot to an ethernet port (usnig a network cable) and then connect the PC to the Technikum's WiFi.
- Connect the robot directly to the PC's ethernet port.

The robot linux system can be accessed through SSH with:
- username: `robot` 
- password: `robot`

Read more [here](https://cpr-robots.com/download/TinyCtrl/Filezilla_Putty_EmbCtrlAccess.pdf)


## Robot start Up sequence

Steps:
- connect
- reset
- activate
- reference all
- reset 
- activate

## ModbusTCP

The modbus server of the robot is implemented in the TinyCtrl robot control. Versions 12 and 13 of the modbus require license. Without a license the modbusTPC server can only be used for 30 mins. The robot must be restarted to get another 30 mins to play. Verion 14 and after can be used without a license. 

> NOTE: Check what version of the modbusTCP implementation the robot is using!!!!!

> Read more [here](https://wiki.cpr-robots.com/index.php/Modbus_Server) and also in the User Manual

### Test connection

To test whether the Modbus connection is successful the input registers on addresses 0-3 can be read: These contain the TinyCtrl version and mapping version, e.g. 980, 12, 20, 1.

### Moving the robot using modbusTCP

The approach for sending a position and starting a motion is the same for all types:

- Write the position values to the holding registers
- Write the motion velocity to holding register 180
- Write a rising edge (0 then 1) to the coil to start the motion

The register and coil addresses depend on the motion type, you will find them in the user manual.

> Read more [here](https://wiki.cpr-robots.com/index.php/Moving_Robots_via_Modbus)

#### Range of movement

The range of movement for the robot is depicted [here](https://www.igus.eu/ContentData/Products/Downloads/Delta%20Roboter%20DLE-DR-0050_DINA5_v2.pdf)
