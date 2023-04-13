# **April 13 log**

- [x] **Task:** configure RaspberryPi

**Reference:** 

- [Getting Started with the Raspberry Pi Zero Wireless](https://learn.sparkfun.com/tutorials/getting-started-with-the-raspberry-pi-zero-wireless/all)
- [setting up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3)



- [x] configure programming environment
  - [ ] ~~python 3? C++?~~
    - [ ] ~~refer to 2019 - 2020 branch for low-level code config, because PCB design refers also to 2019 - 2020 design.~~
  - [x] vscode
    - [x] [install vscode](https://code.visualstudio.com/docs/setup/raspberry-pi)
    - [x] [disable GPU](https://gist.github.com/andriyudatama/fe5d00deb36feeea30ef35a5ea0f7eff)



**Raspberry Pi code**

**Reference:**

- [raspberry pi GPIO](https://learn.sparkfun.com/tutorials/raspberry-gpio/all)
- [another raspberry pi GPIO tutorial](https://pimylifeup.com/raspberry-pi-gpio/)
- [official tutorial: going straight with PID](https://projects.raspberrypi.org/en/projects/robotPID/0)



- [ ] configuration
  - [ ] [add a repo branch `PiCode` and config the VSCode environment](https://pimylifeup.com/raspberry-pi-git-server/)
    - [ ] setup SSH on raspberrypi
      - [x] enable SSH on raspberry pi
      - [ ] [connect to raspberry pi using SSH](https://pimylifeup.com/raspberry-pi-ip-address/)
        - [ ] [how to find the IP address of raspberrypi](https://all3dp.com/2/find-raspberry-pi-on-network/#:~:text=Turn%20on%20your%20Raspberry%20Pi,periods%2C%20like%20so%3A%20192.)
        - [ ] connect using Putty
          - [ ] error: couldn't agree a key exchange algorithm
            - [ ] solution: upgrade [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
    - [x] clone the repo to local
      - [x] [generate a new ssh key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
      - [x] [adding a new ssh key to your github account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
      - [x] clone to local
      - [x] create a new branch `PiCode`
      - [x] test push
      - [x] connect to VSCode
- [ ] run a basic raspberry pi example using GPIO and PID
  - [ ] 
- [ ] run Harvard Public design code from 2019 - 2020 branch