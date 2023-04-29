#!/usr/bin/env python3

import os, copy
import robomodules as rm
from operator import itemgetter
from variables import *
from grid import grid
from search import bfs
from messages import MsgType, message_buffers, LightState, PacmanCommand

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 30
PELLET_WEIGHT = 0.65
GHOST_WEIGHT = 0.35
FRIGHTENED_GHOST_WEIGHT = .3 * GHOST_WEIGHT
GHOST_CUTOFF = 10


class HighToLowTest(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        self.previous_loc = None
        self.direction = PacmanCommand.EAST
        self.grid = copy.deepcopy(grid)

    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            self._send_command_message_to_target(PacmanCommand.NORTH)
            self._send_command_message_to_target(PacmanCommand.NORTH)
            self._send_command_message_to_target(PacmanCommand.EAST)
            self._send_command_message_to_target(PacmanCommand.SOUTH)
            self._send_command_message_to_target(PacmanCommand.WEST)
            self._send_stop_command()

        self._send_stop_command()

    def _send_command_message_to_target(self, command):
        new_msg = PacmanCommand()
        new_msg.dir = command
        if new_msg.dir == PacmanCommand.NORTH:
            print("N")
        elif new_msg.dir == PacmanCommand.SOUTH:
            print("S")
        elif new_msg.dir == PacmanCommand.EAST:
            print("E")
        else:
            print("W")
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)



def main():
    module = HighToLowTest(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()