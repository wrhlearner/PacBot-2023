#!/usr/bin/env python3

import os, copy
import robomodules as rm
from variables import *
from grid import grid
from search import bfs, a_star, get_ghost_locations, grid_distance
from messages import MsgType, message_buffers, LightState, PacmanCommand
from time import sleep

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 60

class BasicHighLevelModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        self.grid = copy.deepcopy(grid)
        self.pathQueue = []
        self.currentpath = None
        self.east = False

    def _get_direction(self, p_loc, next_loc):
        if p_loc[0] == next_loc[0]:
            if p_loc[1] < next_loc[1]:
                return PacmanCommand.NORTH
            else:
                return PacmanCommand.SOUTH
        else:
            if p_loc[0] < next_loc[0]:
                return PacmanCommand.EAST
            else:
                return PacmanCommand.WEST

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        if self.state and self.state.mode == LightState.RUNNING:
            p_loc = (self.state.pacman.x, self.state.pacman.y)
            print(p_loc)

            # update game state
            if self.grid[p_loc[0]][p_loc[1]] in [o, O]:
                self.grid[p_loc[0]][p_loc[1]] = e
                self.eaten = (p_loc[0],p_loc[1])
            else:
                self.eaten = None


            # path = bfs(self.grid, p_loc, self.state, [o, O]) # ORIGINAL
            #path = bfs(self.grid, p_loc, [o, O]) # NEW
            path = a_star(self.state, self.grid, p_loc, self.currentpath, self.eaten) # NEW NEW

            self.currentpath = path

            # print("bfs", path_bfs)

            if path != None:
                next_loc = path[1]
                # next_loc_bfs = path_bfs[1]
                # Figure out position we need to move
                new_msg = PacmanCommand()
                # direction = self._get_direction(p_loc, next_loc)
                
                new_msg.dir = self._get_direction(p_loc, next_loc)
                self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
                sleep(1)

                return

        new_msg = PacmanCommand()
        new_msg.dir = PacmanCommand.STOP
        # self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
        # print(new_msg.SerializeToString())


def main():
    module = BasicHighLevelModule(ADDRESS, PORT)
    module.run()


if __name__ == "__main__":
    main()
