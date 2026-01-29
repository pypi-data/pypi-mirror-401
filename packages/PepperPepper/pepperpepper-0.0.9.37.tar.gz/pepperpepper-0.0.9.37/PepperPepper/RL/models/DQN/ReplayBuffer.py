import collections
import numpy as np
import random

class ReplayBuffer:
    '''经验回访池'''
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = collections.deque(maxlen=capacity)

    

    def add(self, state, action, reward, next_state, done):
        '''添加经验,包括状态，动作，奖励，下一个状态，是否终止'''
        self.buffer.append((state, action, reward, next_state, done))


    
    def sample(self, batch_size):
        '''随机采样一批经验'''
        transitions = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*transitions)
        return np.array(state), action, reward, np.array(next_state), done
    

    def size(self):
        '''当前经验池大小'''
        return len(self.buffer)
    




