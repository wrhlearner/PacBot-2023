from types import SimpleNamespace

'''pins = SimpleNamespace(**{
    "led" : 1,
    "motor_power_r": 26,
    "motor_power_l" : 13,
    "motor_direction_l" : 19,
    "motor_direction_r" : 6,
    "tof_front" : 0;
    "tof_left" : 0,
    "tof_left_diag" : 0,
    "tof_front" : 0,
    "tof_right_diag" : 0,
    "tof_right" : 0})
'''
pins = SimpleNamespace(**{ 
    "tof_front" : 21,  #Definitely correct. U3, IRB, pin 40, BCM21 for RPI 4B
    "tof_left" : 23,   #Definitely Incorrect. U6, IRD, pin 7, BCM17 for RPI 4B
    "tof_right" : 20,  #Maybe incorrect. U4, IRC, pin 38, BCM20 for RPI 4B
    "tof_rear" : 22,   #Definitely correct. U1, IRA, pin 15, BCM22 for RPI 4B
    # "tof_rleft" : 4,
    # "tof_rright" : 24,
    "motor_speed_r" : 18,     # U8, BEN, pin 12, BCM18 for RPI 4B
    "motor_direction_r" : 19, # U8, BPH, pin 35, BCM19 for RPI 4B
    "motor_speed_l" : 12,     # U8, AEN, pin 32, BCM12 for RPI 4B
    "motor_direction_l" : 6}) # U8, BPH, pin 31, BCM6 for RPI 4B
