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

- [Pacman game](https://pacman-30thanniversary.com/)

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

- **default: Harvard sample tool chain**

- **UCLA micromouse sample**

- 

- components

  - development board

    | Board       | IDE                                                          | size | network stacks | Python API | RL   | power module | motor | sensor |
    | ----------- | ------------------------------------------------------------ | ---- | -------------- | ---------- | ---- | ------------ | ----- | ------ |
    | RaspberryPi |                                                              |      |                |            |      |              |       |        |
    | STM32       | STM32CubeIDE<br />STM32CubeMX<br />GCC<br />ST-LINK Debugger |      |                |            |      |              |       |        |
    | Arduino     |                                                              |      |                |            |      |              |       |        |

  - power supply

  - motor

  - sensors

  - reinforcement learning (RL) deployment

### **2.4 Software Code Base**

[Github Repo](https://github.com/HarvardURC/Pacbot)



#### **2.4.1 Pacman Game Code**

/Pacbot/src/gameEngine



#### **2.4.2 Bot Code**

/Pacbot/src/botCode



#### **2.4.3 Communication**

/Pacbot/docs



### **2.5 Time Schedule**

