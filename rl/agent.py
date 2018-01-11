import numpy as np 
import json
import sys

class Agent(object):
	"""
	Agent is the reinforcement learning agent that learns optimal state action pairs
	"""
	def __init__(self, game, qtable=dict(), player='X', learning_rate=5e-1, discount=1, epsilon=5e-1):
		"""
		Initialize agent with properties 
		- qtable is json table with Q values Q(s,a)
		- game is reference to game being played
		- player is what player the agent is 'X' or 'O'
		- learning_rate is alpha value for gradient update
		- discount is discount factor for future expected rewards
		- epsilon is probability of exploration in epsilon greedy strategy
		"""
		self.game = game
		self.qtable = qtable
		self.player = player
		self.learning_rate = learning_rate
		self.discount = discount
		self.epsilon = epsilon

	def qvalue(self, state):
		"""
		Retrieve value from qtable or initialize if not found
		"""
		if state not in self.qtable:
			# Initialize Q-value at 0
			self.qtable[state] = 0.0
		return self.qtable[state]

	def argmax(self, values):
		vmax = np.max(values)
		max_indices = []
		for i, v in enumerate(values):
			if v == vmax:
				max_indices.append(i)
		return np.random.choice(max_indices)

	def argmin(self, values):
		vmin = np.min(values)
		min_indices = []
		for i, v in enumerate(values):
			if v == vmin:
				min_indices.append(i)
		return np.random.choice(min_indices)

	def step(self, verbose=False):
		"""
		Agent makes one step which involves
		- Deciding optimal or random action following e-greedy strategy given current state
		- Taking selected action and observing next state
		- Calculating immediate reward of taking action, current state, and next state
		- Updating q table values using GD with derivative of MSE of Q-value
		- Returns game status
		"""
		state = self.game.get_state(self.game.board)
		action = self.next_move()
		winner = self.game.make_move(action)
		reward = self.reward(winner)
		self.update(reward, winner)
		if verbose:
			print "========="
			print state
			print action
			print winner
			self.game.print_board()
			print reward
		return winner

	def next_move(self):
		"""
		Select next move in MDP following e-greedy strategy
		"""
		states, actions = self.game.available_moves()
		# Exploit
		i = self.optimal_next(states)
		if np.random.random_sample() < self.epsilon:
			# Explore
			i = np.random.randint(0, len(states))
		return actions[i]

	def optimal_next(self, states):
		"""
		Input 
		- states list of possible next states
		Output
		- index of next state that produces maximum value
		"""
		values = [self.qvalue(s) for s in states]
		# Exploit
		if self.game.player == self.player:
			# Optimal move is max
			return self.argmax(values)
		else: 
			# Optimal move is min
			return self.argmin(values)

	def reward(self, winner):
		"""
		Calculates reward for different end game conditions
		- win is 1.0
		- loss is -1.0
		- draw and unfinished is 0.0
		"""
		opponent = 'O' if self.player == 'X' else 'X'
		if (winner == self.player):
			return 1.0
		elif (winner == opponent):
			return -1.0
		else:
			return 0

	def update(self, reward, winner):
		"""
		Updates q-value using recorded observations of performing a certain action in a certain state and continuing optimally from there
		"""
		state = self.game.get_state(self.game.board)
		# Finding estimated future value by finding max(Q(s', a'))
		# If terminal condition is reached, future reward is 0
		future_val = 0
		fs = None
		if not winner:
			future_states, _ = self.game.available_moves()
			i = self.optimal_next(future_states)
			fs= future_states[i]
			future_val = self.qvalue(future_states[i])
		# Q-value update
		self.qtable[state] = ((1 - self.learning_rate) * self.qvalue(state)) + (self.learning_rate * (reward + self.discount * future_val))

	def train(self, episodes):
		"""
		Trains by playing against self for however many episodes
		Each episode is a full game
		"""
		for i in range(episodes):
			game_active = True
			while(game_active):
				winner = self.step()
				if winner:
					game_active = False
					self.game.reset()
			if (i%(episodes/10) == 0) and (i >= (episodes/10)):
				print '.'
		# self.save_values()

	def stats(self):
		"""
		Agent plays optimally against self with no exploration
		"""
		x_wins = 0
		o_wins = 0
		draws = 0
		episodes = 10000
		for i in range(episodes):
			game_active = True
			while(game_active):
				states, actions = self.game.available_moves()
				i = self.optimal_next(states)
				winner = self.game.make_move(actions[i])
				if winner:
					if (winner == 'X'):
						x_wins += 1
					elif (winner == 'O'):
						o_wins += 1
					else:
						draws += 1
					game_active = False
					self.game.reset()
		print '	X: {} Draw: {} O: {}'.format((x_wins*1.0)/episodes, (draws*1.0)/episodes, (o_wins*1.0)/episodes)

	def save_values(self): 
		"""
		Save Q values as json file
		"""
		with open('data/qtable.json', 'w') as out:
			json.dump(self.qtable, out)

	def demo(self):
		"""
		Demo so users can play against trained agent
		"""
		# Agent goes first
		game_active = True
		turn = 0
		while game_active:
			winner = None
			if turn == 0:
				states, actions = self.game.available_moves()
				i = self.optimal_next(states)
				winner = self.game.make_move(actions[i])
				self.game.print_board()
				turn = 1
			elif turn == 1:
				p = int(sys.stdin.readline()[:-1])
				if self.game.is_valid_move(p):
					winner = self.game.make_move(p)
					self.game.print_board()
					turn = 0
				else:
					print 'Invalid move.'
			if winner:
				print 'Winner: {}'.format(winner)
				game_active = False
		self.game.reset()
