import os, copy
import robomodules as rm
from variables import *
from grid import grid
import numpy as np
from messages import MsgType, message_buffers, LightState, PacmanCommand

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 60

#to do with enviorment
#see what the path returns

class HighLevelMarkov(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.state = None
        self.grid = copy.deepcopy(grid)

        self.policy = np.zeros((grid.shape, 4))
        self.lr = 0.01
        self.min_lr = 0.001
        self.lr_decay = 0.99
        self.gamma = 1
        self.eps = 0.1
        self.eps_decay = 0.999
        self.min_eps = 0.001


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
    
    def action_to_command(action):
        if action == 0:
            return PacmanCommand.NORTH
        if action == 1:
            return PacmanCommand.SOUTH
        if action == 2:
            return PacmanCommand.EAST
        if action == 3:
            return PacmanCommand.WEST
        else:
            return None
    
    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg


    def get_action(self, state, train: bool) -> int:
        #Given a state, get action()
        # returns an action as an index value between 0 and the number of actions.
        # 0 is N, 1 is S, 2 is E, 3 is W
        #  If train is true, selection should be done following ε-greedy; otherwise, it should be done in a purely greedy manner. Both
        # methods should reference policy, a |S| × |A| NumPy array holding the Q-values
        if train:
            int = np.random.rand() 
            if int <= self.eps:
                #pick a random value between 0 and 3
                value = np.random.randint(0,4)
                return value  
        #else we return the best policy
        actionstates = self.policy[state]
        best_state = np.argmax(actionstates)
        return best_state
    
    def learn(self,state, action: int, reward: float, next_state):
        Q = self.policy[state, action] #pociy w/ e greedy
        Q_prime = np.max(self.policy[next_state]) #policy with greedy

        #apply algorithum
        TD = (reward + self.gamma*(Q_prime) - Q)
        new_Q = Q + self.lr*TD

        #update Q value for the policy
        self.policy[state, action] = new_Q
        # print(new_Q, "not equal", Q, "equal",  self.policy[state, action])

        return TD


    def value_iteration(self, gamma, eps, grid, max_episodes, max_steps, train):
        if self.state and self.state.mode == LightState.RUNNING:
            map = {}
            for i in range(max_episodes):
                curr_state = (self.state.pacman.x, self.state.pacman.y)
                done = False #init done
                total_reward = 0 #init reward

                for j in range(max_steps): #loop
                    action = self.get_action(curr_state, train)
                    next_state, reward, done, dead = self.step(action) #generate S', r
                    total_reward += reward
                
                if train:
                    self.learn(state, action, reward, next_state) #update Q

                if done or dead:
                    break

                state = next_state #s = s'
            
                map[i] = total_reward
                print(f"episode {i}: {total_reward}")
                self.eps = self.eps * self.eps_decay
                self.eps = max(self.eps, self.min_eps)
                self.lr = self.lr * self.lr_decay
                self.lr = max(self.lr, self.min_lr)

            return map

        #never update the walls

    
    def get_reward(self, action:int, state, done, past_action:int, eat_pellet, is_dead, past_state):
        #time penalty + coin rewards + finishing reards + eatghost reward + euclidian dist from ghosts when not in power up mode
        reward = -1 #time penalty
        if done: #finish reward
            reward += 500
        if eat_pellet:
            reward +=10
        if is_dead:
            reward-=500

        #penalty for turning
        if past_action != action:
            reward -= 2
        
        if (past_state == state):
            reward -= 30

        #later = penatly for being close to ghosts

    def is_done(self):
        done = True
        for i in self.grid.shape[0]:
            for j in self.grid.shape[1]:
                if self.grid[i][j] in [o, O]:
                    done = False
        return done
    
    def is_dead(self, state):
        self.grid[state[0]][state[1]]
        
        

    def step(self, past_state, past_action):
        # e is empty
        # O has the big yums
        #o has the little yums
        # I is wall
        # n is ghost??
        state = past_state
        eat_pellet = False
        if self.state and self.state.mode == LightState.RUNNING:
            state = (self.state.pacman.x, self.state.pacman.y)

        # update game state, we have eaten the little thing good for us
        if self.grid[state[0]][state[1]] in [o, O]:
            self.grid[state[0]][state[1]] = e
            eat_pellet = True
        
        action = self.get_action(state, False)
        print(action) #action is equivilant of path[1], it should be of the form,
        command = self.action_to_command(action)
        print(command)

        done = self.is_done() #return true if eaten all coins
        dead = self.is_dead()
        reward = self.get_reward(action, state, done, past_action, eat_pellet, dead, past_state)
       
        if action != None:
            # Figure out position we need to move
            new_msg = PacmanCommand()
            new_msg.dir = self._get_direction(state, action)
            self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)
            return

        new_msg = PacmanCommand()
        new_msg.dir = PacmanCommand.STOP
        self.write(new_msg.SerializeToString(), MsgType.PACMAN_COMMAND)


        return self.get_next_state(action), reward, done, dead

    def get_next_state(self, state, action):
        #this is like the slippery probablem, there is a pronbablity we will slip and stay at a certain state
        #maybe adding more slippage to the simulation will help
        next_state = state 
        if (action == 0):
            #go up
            y = next_state[1]
            if y > 0:
                y-=1
            next_state[1] = y
            

        if action == 1:
            #go down
            y = next_state[1]
            if y < self.grid.shape[1]:
                y+=1
            next_state[1] = y
        if action == 2:
            #go left
            x = next_state[0]
            if y < self.grid.shape[0]:
                x+=1
            next_state[0] = x
        if action == 3:
            #go left
            x = next_state[0]
            if y > 0:
                x-=1
            next_state[0] = x

        if self.is_wall(next_state):
            return state
        return next_state

    def is_wall(state):
        #returns true is the next state is a wall
        return False




            




 