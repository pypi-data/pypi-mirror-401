import torch
import torch.nn.functional as F
import numpy as np
from PepperPepper.RL.models.DQN.Qnet import Qnet


class DQN:
    '''
    DQN 算法模型
    '''
    def __init__(self,  
                 state_dim, 
                 hidden_dim, 
                 action_dim, 
                 learning_rate, 
                 gamma,
                 epsilon, 
                 target_update, 
                 device,
                 dqn_type='VanillaDQN'):
        self.action_dim = action_dim
        self.q_net = Qnet(state_dim, hidden_dim, action_dim).to(device) # 当前 Q 网络

        self.target_q_net = Qnet(state_dim, hidden_dim, action_dim).to(device) # 目标 Q 网络


        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=learning_rate) # Adam 优化器
        self.gamma = gamma # 折扣因子
        self.epsilon = epsilon # ε-贪婪策略的 ε
        self.target_update = target_update # 目标网络更新频率
        self.count = 0 # 用于记录学习次数，从而决定何时更新目标网络
        self.device = device # 设备（CPU 或 GPU）

        self.dqn_type = dqn_type # DQN 类型

    

    def take_action(self, state): # epsilon-贪婪策略采取动作
        '''
        选择动作
        '''
        if np.random.random() < self.epsilon:
            action = np.random.randint(self.action_dim) # 随机选择动作
        else:
            state = torch.tensor([state], dtype=torch.float).to(self.device)
            action = self.q_net(state).argmax().item() # 选择 Q 值最大的动作
        return action
    
    def max_q_value(self, state):
        '''
        计算状态的最大 Q 值
        '''
        state = torch.tensor([state], dtype=torch.float).to(self.device)
        max_q_value = self.q_net(state).max().item()
        return max_q_value
    

    def update(self, transition_dict):
        '''
        更新 DQN 模型
        '''
        states = torch.tensor(transition_dict['states'], dtype=torch.float).to(self.device)
        actions = torch.tensor(transition_dict['actions']).view(-1, 1).to(self.device)
        rewards = torch.tensor(transition_dict['rewards'], dtype=torch.float).view(-1, 1).to(self.device)
        next_states = torch.tensor(transition_dict['next_states'], dtype=torch.float).to(self.device)
        dones = torch.tensor(transition_dict['dones'], dtype=torch.float).view(-1, 1).to(self.device)

        # 计算当前 Q 值
        q_values = self.q_net(states).gather(1, actions)

        if self.dqn_type == 'DoubleDQN':
            max_action = self.q_net(next_states).max(1)[1].view(-1, 1)
            max_next_q_values = self.target_q_net(next_states).gather(1, max_action)
        else:  # Vanilla DQN
            max_next_q_values = self.target_q_net(next_states).max(1)[0].view(-1, 1)
        
        q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)  # TD误差目标
        dqn_loss = torch.mean(F.mse_loss(q_values, q_targets))  # 均方误差损失函数
        # # 计算目标 Q 值
        # with torch.no_grad():
        #     next_q_values = self.target_q_net(next_states).max(1)[0].view(-1, 1)
        #     target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        # # 计算损失函数
        # loss = torch.mean((q_values - target_q_values) ** 2)

        # 优化模型

        q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)  # TD误差目标
        dqn_loss = torch.mean(F.mse_loss(q_values, q_targets))  # 均方误差损失函数
        self.optimizer.zero_grad()
        dqn_loss.backward()
        self.optimizer.step()

        # 更新目标网络
        if self.count % self.target_update == 0:
            self.target_q_net.load_state_dict(
                self.q_net.state_dict())  # 更新目标网络
        self.count += 1

