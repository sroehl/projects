import random
import collections

class Game:

	def get_max(self):
		max = 0
		for prize in self.odds:
			if self.odds[prize] > max:
				max = self.odds[prize]
		return max

	def get_jackpot(self):
		max = 0
		for prize in self.odds:
			if prize > max:
				max = prize
		return max

	def get_ordered_odds(self):
		ordered = collections.OrderedDict(sorted(self.odds.items()))
		temp_odds = {}
		prev_odd = 0
		for winning, odd in ordered.items():
			calc_odd = int(self.max_odd/odd)
			odd_index = prev_odd + calc_odd
			prev_odd = prev_odd + calc_odd
			temp_odds[odd_index] = winning
		return collections.OrderedDict(sorted(temp_odds.items()))

	def play_ticket(self):
		result = random.randint(0, self.max_odd)
		#print("random: {}".format(result))
		for odd, winning in self.ordered_odds.items():
			if result < odd:
				return winning
		return 0

	def print_odds(self):
		for odd, winning in self.ordered_odds.items():
			print("{} - {}".format(winning, odd))

	def __init__(self, name, cost, odds):
		self.name = name
		self.cost = cost
		self.odds = odds
		self.max_odd = self.get_max()
		self.jackpot = self.get_jackpot()
		self.ordered_odds = self.get_ordered_odds()
