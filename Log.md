# **Log**

[toc]

## **1 Goal**

- understand game rules
- choose hardware parts
- choose development tool chain
- (*) codebase
- make time schedule

## **2 Tasks**

### **2.1 Game Rule**

- [Pacman game](https://freepacman.org/)

- **arena**

  - wall 4'' tall (10.16 cm)
  - [28 x 31 grid for location](https://github.com/HarvardURC/Pacbot/blob/master/src/gameEngine/pacbot/grid.py)
  - passage 7'' wide (17.78 cm)
  - the PacBots cannot exit the arena
  - given arena map
  - **Teams should be aware that due to design constraints the arena is built in three pieces, and may have small gaps or lips in the seams between the sections.** 

- **normal white dot**

  - 10 points/each
  - upon consumption, the dots vanish for the remainder of the game. 

- **4 special dots**

  > special scores: There will be 4 “special dots” that, upon collection by your PacBot, will enable the PacBot to “eat” the ghosts for extra points.

  - 50 points/each
  - 20 seconds for ghosts to avoid the PacBot
  - reach another special dot during the 20 second, 20 second avoiding time is reset
  - during the 20 seconds, PacBot can catch ghosts
    - To catch a ghost, your PacBot must enter the grid space currently occupied by the ghost.
    - scores
      - 200 points for the first ghost
      - 400 for second ghost
      - 800 for the third
      - 1600 for the fourth
    - the caught ghost will respawn in the ghost house

- **cherry**

  - 100 points
  - appear at (13, 13)
  - appear when the PacBot has eaten 70 pellets and again at 170 pellets eaten
  - disappear after 10 seconds

- **life**

  - 3 lives initially
  - start each life in its home position (position (14, 7) in arena grid).
  - At the end of each life, a “pause” signal will be sent out to your PacBot. Your PacBot **must** stop all autonomous movement at this time
  - for a ghost to catch your PacBot, it must also occupy the same grid space simultaneously.

- **Ghosts**

  - speed
    - 7''/sec or 2 grids/sec
    - <font color='red'>**may be sped up depending on the performance of the participating PacBots.**</font>
  - [action](http://gameinternals.com/understanding-pac-man-ghost-behavior)
    - 4 ghosts are independent
    - At the beginning of the game, Blinky will start just outside its home position, and approximately every 5 seconds, another ghost will exit the enclosure.
    - The ghosts are temporarily eliminated when they are caught, and will respawn at their home position.

- **end of game**

  - a team has lost all of their three lives
  - a team has collected all of the dots on the board
  - If it should be the case that the 20 second timer from a special dot still has remaining time when all the dots have been consumed, the game will end

- **win**

  1. number of points
  2. number of lives left
  3. the time taken

> **reference**
>
> - [understanding Pac-Man Ghost Behavior](http://gameinternals.com/understanding-pac-man-ghost-behavior)

### **2.2 Hardware Parts and Development Tool Chain**

past robot design: /Pacbot/docs

#### **2.3.1 Robot Design Requirements**

- **autonomous:** 
  - no human intervention in the robot’s functioning.
  - Off robot computation is allowed (i.e. your computer may run code that sends signals to your robot).
- <font color='red'>**size**</font>
  - <font color='red'>**7''x7'' grid**</font>
  - this is the minimum distance between walls, so you will likely want to build your robot smaller than this size.
  - <font color='red'>**$\le$4'' tall**</font>
- **top**
  - Each PacBot should have <font color='red'>**a flat area on top with room for a 3” diameter**</font> yellow acrylic computer vision target, which will be used for tracking the robot.
- **communication**
  - The field will have **an overhead camera** that the organizers will use **to detect the position of the PacBot** in the arena grid
  - Each robot will connect to **our server** via <font color='red'>**a socket over WiFi**</font> to receive the position of the ghosts, and other game state. A library to do this will be provided in <font color='red'>**Python**</font>. NOTE: We will <font color='red'>**not be supporting Xbee communication**</font> this year.
  - the robot must **read from the server multiple times a second** to execute "pause" movement and receive game states
  - **info from server**: an object/struct
    - The game state: paused or running
    - The position of the Pacbot in the arena grid according to the computer vision software
    - The position of each ghost in the arena grid
    - Whether each ghost is frightened
    - The Pacbot’s current score
    - The Pacbot’s remaining lives
- **movements**
  - must stay within the boundaries of the arena at all times
  -  cannot damage, adjust, move, or climb over any boundary of the arena

#### **2.3.2 Hardware and Dev Tool Chain**

- requirements

  - **size:** 7''x7''x4'' length x width x height
  - **network stacks:**
    - support WIFI
    - no Xbee communication
    - have Python API

- **default: Harvard sample hardware**

  - [electrical](https://docs.google.com/spreadsheets/d/1ZO9OBoGcNkOdx6GaBkAFo6AWodeVCOaCXKic-0er2z0/edit?usp=sharing)

  | components                            | quantity with spares | link                                                         |
  | ------------------------------------- | -------------------- | ------------------------------------------------------------ |
  | 3D Printed Materials                  | 1                    |                                                              |
  | Pololu 60mm Wheel set (yellow)        | 2                    | https://www.pololu.com/product/1422                          |
  | 1/2 in. Ball Caster (metal)           | 3                    | https://www.pololu.com/product/953                           |
  | IR Sensor                             | 8                    | https://www.pololu.com/product/2489                          |
  | Magnetic encoder pair                 | 2                    | https://www.pololu.com/product/3081                          |
  | DC Gear Motors                        | 4                    | https://www.pololu.com/product/2381                          |
  | Gearmotor Bracket                     | 2                    | https://www.pololu.com/product/989                           |
  | Li-Po Battery                         | 3                    | https://hobbyking.com/de_de/turnigy-1000mah-2s-20c-lipo-pack.html |
  | Motor Driver                          | 4                    | https://www.pololu.com/product/2135                          |
  | Voltage Regulator                     | 3                    | https://www.pololu.com/product/2851                          |
  | Diodes                                | 5                    | https://www.digikey.com/product-detail/en/MM3Z3V3B/MM3Z3V3BCT-ND/1626881 |
  | Power Transistors                     | 5                    | https://www.digikey.com/product-detail/en/MMBTA06LT1G/MMBTA06LT1GOSCT-ND/1139832 |
  | SMD LEDs                              | 25                   | https://www.digikey.com/product-detail/en/LTST-C190KSKT/160-1437-1-ND/386818 |
  | Slide Switch                          | 2                    |                                                              |
  | Assorted capacitors, resistors, wires | 1                    |                                                              |
  | IMU                                   | 1                    | https://www.adafruit.com/product/2472                        |
  | Raspberry Pi 0 W                      | 3                    | https://www.raspberrypi.org/products/raspberry-pi-zero-w/    |
  | Teensy 3.5                            | 2                    | https://www.pjrc.com/store/teensy32.html                     |
  | PCB: KiCAD                            | 3                    |                                                              |

  - Raspberry Pi Zero W
    - **802.11 b/g/n wireless LAN** WiFi
    - Bluetooth 4.1
    - Bluetooth Low Energy (BLE)
    - **1GHz, single-core CPU**
    - **512MB RAM**
    - Mini HDMI port and micro USB On-The-Go (OTG) port
    - Micro USB power
    - HAT-compatible 40-pin header
    - Composite video and reset headers
    - CSI camera connector

  - hierarchy
    - **3 PCB**: KiCAD, connecting all components
      - **microcontroller**
        - 3 raspberry Pi Zero W: run robot code using data from sensors (IR and Teensy); interface with the motors and IR sensors; receive instruction from host (high level code run on a remote computer, not on raspberry pi)

      - **power supply**
        - 3 Li-Po battery
        - 3 voltage regulator

      - **sensors**: PID control
        - 2 Teensy 3.5: receive magnetic encoder and IMU readings. Communicate these sensor data with raspberry pi via serial communication.
          - 2 magnetic encoder pair: track the amount of distance we travel.
          - 1 IMU: An IMU was intended to be used for general navigation of the robot (to ensure we don't hit walls and turn accurately - other uses are possible)
        - 8 IR sensors: IR sensors are used for detecting whether we are near walls. These are placed on the sides and the front/back of the bot

      - <font color='red'>**motors**</font>
        - 4 motor driver: A motor driver is necessary to communicate with the motors from the Raspberry Pi
          - 4 DC gear motors: 6V brushed DC gear motors

    - **Mechanical**: SolidWorks
      - 1 3D Printed Materials
      - 2 60mm wheel set
      - 1/2'' ball caster

    - **others**
      - 2 gearmotor bracket
      - 5 diodes
      - 5 power transistors
      - 25 SMD LEDs
      - 2 slide switch
      - 1 assorted caps, res, wires

- **UCLA micromouse sample**

> reference:

- components

  - development board

    | Board       | IDE                                                          | size | network stacks | Python API | RL   | power module | motor | sensor |
    | ----------- | ------------------------------------------------------------ | ---- | -------------- | ---------- | ---- | ------------ | ----- | ------ |
    | RaspberryPi |                                                              |      |                |            |      |              |       |        |
    | STM32       | STM32CubeIDE<br />STM32CubeMX<br />GCC<br />ST-LINK Debugger |      |                |            |      |              |       |        |
    | Arduino     |                                                              |      |                |            |      |              |       |        |

    Types of Microcontrollers

    | Microncontroller | RAM  | ROM  | clock rate | supply power | interfaces |
    | ---------------- | ---- | ---- | ---------- | ------------ | ---------- |
    |                  |      |      |            |              |            |
    |                  |      |      |            |              |            |
    |                  |      |      |            |              |            |

  - power supply

  - motor

  - sensors

  - reinforcement learning (RL) deployment

#### **2.3.3 Test env - Arena design**

refer to arena design in [Github public design](https://github.com/HarvardURC/Pacbot/tree/master/docs/Arena%20Documentation)

- design tools: SolidWorks

### **2.4 Software Code Base**

[Github Repo](https://github.com/HarvardURC/Pacbot)



#### **2.4.1 Pacman Game Code - host**

/Pacbot/src/gameEngine



#### **2.4.2 Bot Code - PacBot**

/Pacbot/src/botCode



#### **2.4.3 server**



#### **2.4.4 Communication**

/Pacbot/docs

[How to run the game and connect to your bot - A Guide](https://github.com/HarvardURC/Pacbot/blob/master/docs/A%20Guide%20to%20Connecting%20to%20the%20Game.md)

- 1 server, 1 host, 1 robot
- how does robot receive game status? server -> host -> robot via WIFI

### **2.5 Time Schedule**

