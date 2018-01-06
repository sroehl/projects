import Game
import sys

class Lotto:
VERBOSE=False

def get_game(file=None):
	if file is None:
		return Game.Game("21", 1, {1:11, 2:14, 4:42, 8:101, 10:201, 20:301, 25:201, 50:1695, 100:180000, 1800:540000})
	else:
		name = None
		cost = None
		odds = {}
		with open(file, "r") as fh:
			for line in fh:
				try:
					if "name" in line:
						name = line.split(":")[1].rstrip()
					elif "cost" in line:
						cost = int(line.split(":")[1])
					else:
						vals = line.split(" ")
						prize = vals[0][1:].rstrip().replace(',','')
						odd = vals[1].split(":")[1].rstrip().replace(',','')
						odds[int(prize)] = int(odd)
				except IndexError:
					print("Failed to parse: {}".format(line))
		if name is not None and cost is not None and len(odds) > 0:
			return Game.Game(name, cost, odds)
		else:
			print("Unable to read file")
			sys.exit(-1)
					

def sim_year(game, tickets_per_week):
	won = 0
	cost = 0
	for i in range(0,52*tickets_per_week):
		cost += game.cost
		game_won = game.play_ticket()
		if game_won == game.jackpot:
			print_verbose("Won jackpot!")
		won += game_won
	#print("Total earnings for {}: {}".format(ticket.name, won-cost))	
	return won-cost
	

def print_verbose(msg):
	if VERBOSE:
		print(msg)


if __name__ == '__main__':
	avg = 0
	sims = 100000
	max_won = -10000000
	max_lost = 10000000
	num_of_pos = 0
	num_of_neg = 0
	if len(sys.argv) > 1:
		game = get_game(sys.argv[1])
	else:
		game = get_game()
	if len(sys.argv) > 2:
		tickets_per_week = int(sys.argv[2])
	else:
		tickets_per_week = 1

	if len(sys.argv) > 3:
		if sys.argv[3] == '-v':
			VERBOSE = True
	
	for i in range(0, sims):
		if i % (sims/4) == 0:
			print("Completed {}%".format(int((i/sims)*100)))
		amount = sim_year(game, tickets_per_week)
		avg += amount
		if amount > max_won:
			max_won = amount
		if amount < max_lost:
			max_lost = amount
		if amount > 0:
			num_of_pos += 1
		else:
			num_of_neg +=1
	
	print("{},{},{},{},{}".format(game.name,tickets_per_week,avg/sims,num_of_pos,num_of_neg}
	print("Total earnings over {} sims for {} was: {}".format(sims, game.name, avg/sims))
	print("Max won for year was {}".format(max_won))
	print("Max lost for year was {}".format(max_lost))
	print("There were {} positive years and {} negative years".format(num_of_pos, num_of_neg))
