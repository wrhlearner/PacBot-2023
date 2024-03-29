from motor import Motor, MotorDirection
from pins import *
from sensors import Sensors
from GPIOhelpers import *
from PID import *
setGPIO()
import time
import signal, sys

from teensySensors import TeensySensors

from time import sleep


MOTOR_SPEED = 25 
TICKS_CELL = 510   # this is (encoder ticks per axis rev) * (motor gear ratio) * (ratio of cell width to circumference of wheel) - but I think we're missing ticks or something so I did it experimentally


TIME = 3000
KP = 0.4
KI = 0.01
KD = 0.05

class Direction():
    W = 0
    N = 1
    E = 2
    S = 3

class Motors:
    def __init__(self):
        # self.teensy_sensors = TeensySensors()
        # sleep(2)
        
        #self.ir_sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_fleft,pins.tof_fright,pins.tof_rleft,pins.tof_rright], ["front", "rear","fleft","fright","rleft","rright"], [0x30,0x31,0x32,0x33,0x34,0x35]) ORIGINAL (commented because we don't have all the sensors)
        # self.ir_sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_fleft,pins.tof_fright], ["front", "rear","fleft","fright"], [0x30,0x31,0x32,0x33])
        # self._frontIR = self.ir_sensors.sensors["front"]
        # self._fleftIR = self.ir_sensors.sensors["fleft"]
        # self._frightIR = self.ir_sensors.sensors["fright"]
        # self._rearIR = self.ir_sensors.sensors["rear"]

        # Sensors we don't have
        #self._rleftIR = self.ir_sensors.sensors["rleft"]
        #self._rrightIR = self.ir_sensors.sensors["rright"]
        # sleep(0.5)
        # # sometimes intial sensor readings are 0
        # self._frontIR.get_distance()
        # self._fleftIR.get_distance()
        # self._frightIR.get_distance()
        # self._rearIR.get_distance()

        # Sensors we don't have
        #self._rleftIR.get_distance()
        #self._rrightIR.get_distance()

        # self.heading = {Direction.W: 0, Direction.N: 90, Direction.E: 180, Direction.S: 270}
        # #sets default direction to be east
        # self.cur_dir = Direction.E

        self.left_motor = Motor("Left", pins.motor_speed_l, pins.motor_direction_l, 0)

        self.right_motor = Motor("Right", pins.motor_speed_r, pins.motor_direction_r, 0)

        # self.setpointHeading = 0
        # self.inputStraight = 0
        # self.PIDHeading = PID(self.inputStraight, self.setpointHeading, KP, KI, KD, DIRECT, Timer)
        # self.PIDHeading.set_output_limits(-1*(100 - MOTOR_SPEED), 100 - MOTOR_SPEED)
        # self.PIDHeading.set_mode(AUTOMATIC)

        # self.setpointTurnHeading = 0
        # self.inputTurn = 0
        # self.PIDTurn = PID(self.inputTurn, self.setpointHeading, 0.15, 0., 0.0, DIRECT, Timer)
        # self.PIDTurn.set_output_limits(-1*MOTOR_SPEED, MOTOR_SPEED)
        # self.PIDTurn.set_mode(AUTOMATIC)

        # self.reset_heading()

    def read_encoders(self):
        return self.teensy_sensors.get_left_encoder_ticks(), self.teensy_sensors.get_right_encoder_ticks()

    def reset_heading(self):
        current_heading = self.teensy_sensors.get_heading()

        for i in range(4):
            self.heading[(self.cur_dir + i) % 4] = (current_heading + (i * 90)) % 360



    def move_motors(self, left, right):
        if left >= 0:
            self.left_motor.move(MotorDirection.FORWARD, abs(left))
        else:
            self.left_motor.move(MotorDirection.BACKWARD, abs(left))
        if right >= 0:
            self.right_motor.move(MotorDirection.FORWARD, abs(right))
        else:
            self.right_motor.move(MotorDirection.BACKWARD, abs(right))

    def stop(self):
        #print("stopped")
        self.right_motor.stop()
        self.left_motor.stop()
    
    def move_cells(self, cells):
        self.drive_straight(self.heading[self.cur_dir], cells*TICKS_CELL)

    def move_cells_with_encoders(self, cells=1):
        #move x cells just using the encoders idk 
        #change the constant
        self.drive_straight_just_encoders(cells*0.5)


    def drive_straight_just_encoders(self, cells):
        self.move_motors(MOTOR_SPEED, MOTOR_SPEED)
        sleep(cells*1)
        self.stop()
    
    def turn_left(self, angle):
        self.move_motors(-MOTOR_SPEED, MOTOR_SPEED)
        sleep(0.01*angle)
        self.stop()

    def turn_right(self, angle):
        self.move_motors(MOTOR_SPEED, -MOTOR_SPEED)
        sleep(0.1*angle)
        self.stop()


    
    def drive_straight(self, heading, ticks):
        #print("drive straight")
        self.teensy_sensors.reset_encoders()
        self.setpointHeading = heading

        factor = ticks/TICKS_CELL
        distance_l, distance_r = 0, 0 
       
        # Cycle front IR  (this is weird and we don't know why)
        self._frontIR.get_distance()
        #print("    ", self._frontIR.get_distance())
        while min(distance_r, distance_l) < ticks:
        #while 1:
            # might wanna add logic to avoid hitting wall

            # logic to add distance for more time to straighten out
            # if abs(distance_l - distance_r) > 140:
            #     print('added: {}'.format(added))
            #     added += 4
            #     ticks += 4
            distance_l, distance_r = self.read_encoders()
            #print("Distance:", distance_l, distance_r)

            self.inputStraight = self.teensy_sensors.get_heading()
            
            # Only undergo PID ever 0.1 second
            last_set = time.time()
            # Compute error
            error = self.compute_heading_error(self.inputStraight, self.setpointHeading)
            self.PIDHeading.compute(error, 0)
            #print("Error:", error, " Pid heading:", self.PIDHeading.output())
            self.move_motors((MOTOR_SPEED + self.PIDHeading.output()), (MOTOR_SPEED - self.PIDHeading.output()))

            #print(self._rleftIR.get_distance(), " ", self._rrightIR.get_distance())

            sleep(0.1)
            if self._frontIR.detectWall(threshold = 60):
                break

        #print("    end drive_straight")

    def reverse(self, cells):
        self.reverse_direction()
        self.move_cells(cells)

    def back(self):
        # if(self._rearIR.get_distance() > 25 and self._rleftIR.get_distance()> 10 and self._rrightIR.get_distance() > 10): ORIGINAL (commented because we dont have rleftIR and rrightIR)
        if(self._rearIR.get_distance() > 25):
            print("back")
            self.move_ticks(-TICKS_CELL/4, -TICKS_CELL/4)
        else:
            print("not back")
 

    def turn_around(self):
        self.cur_dir = (self.cur_dir + 2) % 4
        self.turn_to_direction(self.heading[self.cur_dir])

    def compute_heading_error(self, cur, des):
        return (cur - des + 540) % 360 - 180

    def turn_to_direction(self, heading):
        self.inputTurn = self.compute_heading_error(self.teensy_sensors.get_heading(), heading)
        self.setpointTurnHeading = 0
        while abs(self.inputTurn) > 1:
            self.inputTurn = self.compute_heading_error(self.teensy_sensors.get_heading(), heading)
            self.PIDTurn.compute(self.inputTurn, self.setpointTurnHeading)
            self.move_motors(self.PIDTurn.output(), -self.PIDTurn.output())
        self.stop()
    
    def follow_heading_till_clear(self, irSensor, heading, direction=1):
        self.setpointHeading = heading
        
        # Cycle front and back IR  (this is weird and we don't know why)
        self._frontIR.get_distance()
        self._rearIR.get_distance()

        
        start_time = time.time()
        while (irSensor.detectWall() and ((time.time() - start_time < 1))):
            self.inputStraight = self.teensy_sensors.get_heading()
            error = self.compute_heading_error(self.inputStraight, self.setpointHeading)
            self.PIDHeading.compute(error, 0)
            self.move_motors(direction * (MOTOR_SPEED - 10 + self.PIDHeading.output()), direction * (MOTOR_SPEED - 10 - self.PIDHeading.output()))

            #print("Sensor reading:", irSensor.get_distance())
            #print(self._rleftIR.get_distance(), " ", self._rrightIR.get_distance())
            sleep(0.1)
            
            if direction == 1 and self._frontIR.detectWall(threshold = 60):
                break
            elif direction == -1 and self._rearIR.detectWall(threshold = 60):
                break

        sleep(0.05)
        self.stop()

    def reverse_direction(self):
        self.cur_dir = (self.cur_dir + 2) % 4
        self.turn_to_direction(self.heading[self.cur_dir])

    def straight(self):
        self.move_motors(MOTOR_SPEED/2, MOTOR_SPEED/2)

    def escape(self):
        pass


    # function for driving in actual direction
    def drive_in_direction(self, direction, cells, old_direction):
        turning = self.how_far_off(old_direction, direction)
        if turning < 0:
            self.turn_right(abs(turning))
        elif turning > 0:
            self.turn_left(turning)
        self.drive_straight_just_encoders(cells)

        return direction



    def how_far_off(self, old_direction, direction):
        one = 0
        two = 0
        if (old_direction) == Direction.N:
            one = 0
        elif (old_direction) == Direction.S:
            one = 180
        elif (old_direction == Direction.E):
            one = 90
        else:
            one = 270
        
        if (direction) == Direction.N:
            two = 0
        elif (direction) == Direction.S:
            two = 180
        elif (direction == Direction.E):
            two = 90
        else:
            two = 270


        how_far_off = one - two

        #negative is right
        #positive is left

        return(how_far_off)




        # desired_heading = self.heading[direction]
        # heading_error = self.compute_heading_error(self.teensy_sensors.get_heading(), desired_heading)
        
        # # Make directional adjustment if greater than 20 degrees
        # if abs(heading_error) > 20:
        #     # Do appropriate corrections with IR sensors (when turning about 90 degrees left or right)
        #     if heading_error < -70 and heading_error > -110:
        #         curr_heading = self.heading[(direction - 1) % 4]
        #         #self.follow_heading_till_clear(self._rrightIR, curr_heading) # Commented out because we don't have this sensor
        #         self.follow_heading_till_clear(self._frightIR, curr_heading, direction=-1)
        #     elif heading_error > 70 and heading_error < 110:
        #         curr_heading = self.heading[(direction + 1) % 4]
        #         #self.follow_heading_till_clear(self._rleftIR, curr_heading) # Commented out because we don't have this sensor
        #         self.follow_heading_till_clear(self._frightIR, curr_heading, direction=-1)

        #     self.turn_to_direction(desired_heading)

        # # Drive forward
        # self.drive_straight(desired_heading, cells*TICKS_CELL)
