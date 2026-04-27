import time
import random
import sys


class Player:
	def __init__(self, name : str, club : str, max_hp : int, attack_info : List[str | int], special_info : List[str | int]) -> None:
		self.name : str = name
		self.club : str = club
		self.hp : int = max_hp
		self.max_hp : int = max_hp
		self.attack_name, self.damage = attack_info
		self.special_name, self.special_damage, self.special_uses = special_info


	def is_alive(self) -> bool:
		return self.hp > 0

	def take_damage(self, amount : int) -> None:
		self.hp = (self.hp - amount if self.hp >= amount else 0)

	# there aint no encapsulation for ts
	# def normal_attack(self) -> int:
	# 	return self.damage

	def special_attack(self) -> int:
		if self.special_uses:
			self.special_uses -= 1
			return self.special_damage
		return -1


	def __str__(self) -> str:
		l = 25
		return f"\t{self.name}{" " * (l-len(self.name)-4)}| HP: {self.hp}\n{" " * l}| {self.attack_name} : {self.damage}\n{" " * l}| {self.special_name}: {self.special_damage} (uses : {self.special_uses})"


d = 0.8

# format {name : [club, max_hp, [attack_info, damage], [special name, special damage, special uses]]}

players = {
	"Nico O'Reilly" : [
		"Manchester City", 
		80, 
		["Nutmeg", 15], 
		["Header", 35, 2]
	],

	"Erling Haaland" : [
		"Manchester City", 
		130, 
		["Tap In", 20], 
		["Far Post Header", 45, 2]
	],

	"Rayan Cherki" : [
		"Manchester City",
		70, 
		["Rabona", 20], 
		["Juggling", 45, 1]
	],

	"Tijjani Reijnders" : [
		"Manchester City", 
		90, 
		["Shot", 15], 
		["Yellow Card", 70, 1]
	],

	"Kevin De Bruyne" : [
		"Manchester City", 
		105, 
		["Long-Distance Pass", 30], 
		["Curled Header", 35, 3]
	],

	"Dominik Szoboszlai" : [
		"Liverpool", 
		100, 
		["Curved Shot", 20], 
		["40-yard Banger", 60, 1]
	],

	# "Ryan Gravenberch" : ["Liverpool"],
	# "Mohamed Salah" : ["Liverpool"],
	# "Virgil Van Dijk" : ["Liverpool"],
	# "Slippy G" : ["Liverpool"],

	# "Cole Palmer" : ["Chelsea"],
	# "Alejandro Garnacho" : ["Chelsea"],
	# "Enzo Fernández" : ["Chelsea"],
	# "Marc Cucurella" : ["Chelsea"],
	# "Didier Drogba" : ["Chelsea"],

	# "Bruno Fernandes" : ["Manchester United"],
	# "Bryan Mbuemo" : ["Manchester United"],
	# "Matheus Cunha" : ["Manchester United"],
	# "Benjamin Šeško" : ["Manchester United"],
	# "Cristiano Ronaldo" : ["Manchester United"],
}


def delay(t : float = 0.8) -> None:
	time.sleep(t)


def create_teams() -> Tuple[List[Monster]]:
	print("choosing teams\n")
	player_team = []
	enemy_team = []
	for a in range(2):
		for i in range(3):
			# check no dupes
			while (chosen := random.choice(list(players.keys()))) in list(map(lambda x: x.name, player_team + enemy_team)):
				chosen = random.choice(list(players.keys()))
			if a-1: # is 0
				player_team.append(Player(chosen, *players[chosen]))
			else:
				enemy_team.append(Player(chosen, *players[chosen]))
			print(".", end="")
			delay()
		print()
	print("Done!")
	delay(1)
	return player_team, enemy_team


def display_team(team : List[Player], prompt : str = "", index : bool = False) -> None:
	print(prompt)
	for i in range(len(team)):
		print(f"\t{i+1}.\n" if index else "", team[i], end="\n\n", sep="")
		delay()



def choose_player(players : List[Player]) -> int:
	rge = list(range(1, len(players)+1))
	print(f"Type in a player's index between {rge[0]} and {rge[-1]} (inclusive)")
	delay()
	advice = ""
	while True:
		print(advice, end="\n" if advice else "", file=sys.stderr)
		delay(1)
		display_team(players, "Your team: ", True)
		choice = input("Choose: ")
		if not choice.isdigit():
			advice = "positive and digits only!"
			continue
		if int(choice) not in rge:
			advice = f"from {rge[0]} to {rge[-1]}!"
			continue
		break
	return players[int(choice)-1]


def enemy_choose(players : List[Player], selected, opposition) -> Player:
	if selected.hp <= 0:
		return random.choice(players)
	# check if 1-tap
	if opposition.damage >= selected.hp or (opposition.special_damage >= selected.hp and opposition.special_uses):
		# get another one thats healthy
		if (fir := list(filter(lambda p: p.hp > opposition.damage and (p.hp > opposition.special_damage and opposition.special_uses), players))):
			return random.choice(fir)

		if (sec := list(filter(lambda p: p.hp > opposition.damage,
				players))):
			return random.choice(sec)



		return max(players, key=lambda p: p.hp)
	return selected







def get_action(options : list, *, err_msg : str = None , prompt : str = "Select option:") -> int:
	if err_msg is not None:
		delay()
		print(err_msg, file=sys.stderr)
	delay()
	print(prompt)
	choice = input()
	return choice if choice in list(map(str, options)) else get_action(options, err_msg="Choose only from the given list!")




def player_turn() -> None:
	global player_team, enemy_team, chosen_player, chosen_enemy
		
	while True:
		print("Type your desired option:")
		s = {
				"normal" : f"{chosen_player.attack_name} - {chosen_player.damage}",
				"special" : f"{chosen_player.special_name} - {chosen_player.special_damage} ({chosen_player.special_uses} use{"s" if chosen_player.special_uses-1 else ""} left)",
				"check" : f"Check {chosen_enemy.name}'s health"
				}

		# if no special uses delete the option
		if not chosen_player.special_uses:
			del s["special"]


		# print options
		for k, v in s.items():
			print(f"\t{k}. {v}")
		match get_action(s.keys()):
			case "normal":
				print(f"You used {chosen_player.attack_name} to deal {chosen_player.damage} to {chosen_enemy.name}!")
				chosen_enemy.take_damage(chosen_player.damage)
				print(f"{chosen_enemy.name} is now on {chosen_enemy.hp} HP!")
				if chosen_enemy.hp <= 0:
					print(f"You defeated {chosen_enemy.name}!\n")
				break
			case "special":
				print(f"You used {chosen_player.special_name} to deal {chosen_player.special_damage} DP to {chosen_enemy.name}!")
				chosen_enemy.take_damage(chosen_player.special_attack())
				delay()
				print(f"{chosen_enemy.name} is now on {chosen_enemy.hp} HP!")
				if chosen_enemy.hp <= 0:
					delay()
					print(f"You defeated {chosen_enemy.name}!")
				break
			case "check":
				delay()
				print(f"{chosen_enemy.name} has {chosen_enemy.hp} HP remaining.\n\n")
				delay(1.4)
	print(end="\n\n")
	delay()



def enemy_turn() -> None:
	global player_team, enemy_team, chosen_player, chosen_enemy

	if chosen_enemy.hp <= 0:
		chosen_enemy = enemy_choose(enemy_team, chosen_player, chosen_enemy)
	

	while True:

		if (chosen_player.hp <= chosen_enemy.special_damage and chosen_enemy.special_uses) or chosen_enemy.special_uses >= 2:
			chosen_player.take_damage(chosen_enemy.special_attack())
			print(f"Enemy used {chosen_enemy.special_name} to deal DP {chosen_enemy.special_damage} to {chosen_player.name}!")
			delay()
			chosen_player.take_damage(chosen_enemy.damage)
			print(f"{chosen_player.name} is now on {chosen_player.hp} HP!")
			if chosen_player.hp <= 0:
				delay()
				print(f"Enemy defeated {chosen_player.name}!")
			break

		print(f"Enemy used {chosen_enemy.attack_name} to deal {chosen_enemy.damage} DP to {chosen_player.name}!")
		delay()
		chosen_player.take_damage(chosen_enemy.damage)
		print(f"{chosen_player.name} is now on {chosen_player.hp} HP!")
		if chosen_player.hp <= 0:
			delay()
			print(f"Enemy defeated {chosen_player.name}!")
		break



	print(end="\n\n")
	delay()


def player_substitution(player_team : List[Player], selected : Player) -> None:
	global chosen_player
	choice = None
	if selected.is_alive():
		while (choice := input("Substitution?\n").lower()) not in ["yes", "no"]:
			print("yes/no only!")

	if choice == "yes" or not selected.is_alive():
		e.name = choose_player(player_team).name
		if e != chosen_enemy:
			print(f"Substitution on the field for Home team, going off is {selected.name}")
			delay()
			print(f"Replacing him, going on for Home team is, {e.name}!")
			chosen_player = e
		else:
			print(f"Continued using {chosen_player}!")




def battle_loop(p_team : List[Player], e_team : List[Player]) -> bool:
	global player_team, enemy_team, chosen_player, chosen_enemy
	player_team = p_team[:]
	enemy_team = e_team[:]
	cycle = 0
	print("Choose your starting player!")
	delay()
	chosen_player = choose_player(player_team)
	chosen_enemy = random.choice(enemy_team)

	print(f"You're up against - {chosen_enemy.name} : {chosen_enemy.hp} HP!\n")
	delay(1)
	n = 60
	while player_team and enemy_team:
		if cycle:
			player_substitution(player_team, chosen_player)
			delay(1)
			if (tmp := enemy_choose(enemy_team, chosen_enemy, chosen_player)) != chosen_enemy:
				print(f"Substitution on the field for Away team, going off is {chosen_enemy.name}")
				delay()
				print(f"Replacing him, going on is, {tmp.name} with {tmp.hp} HP\n!")
				chosen_enemy = tmp
		delay()
		cycle += 1

		print("!"*n, f"\tROUND {cycle}    -    {chosen_player.name.upper()} VS. {chosen_enemy.name.upper()}", "!"*n, sep="\n", end="\n\n\n")
		delay(2)
		

		print(str("PLAYER" if (c := random.randint(0, 1)) else "ENEMY") + " GETS TO GO FIRST\n\n")
		delay(1)
		if c:
			player_turn()
			delay(1)
			if chosen_enemy.is_alive():
				enemy_turn()

		else:
			enemy_turn()
			delay(1)
			if chosen_player.is_alive():
				player_turn()


		player_team = list(filter(Player.is_alive, player_team))
		enemy_team = list(filter(Player.is_alive, enemy_team))

	delay(2)
	return bool(player_team)
		





player_team = None
enemy_team = None
chosen_player = None
chosen_enemy = None

def main() -> None:
	global player_team, enemy_team
	print("*"*40, "*"*40, "\n\t  WELCOME TO FOOTBALL SHOWDOWN\n", "*"*40, "*"*40, sep="\n")
	delay(2)
	print("\n\n")
	player_team, enemy_team = create_teams()
	player_won = battle_loop(player_team, enemy_team)
	print("&"*50, "\t\tYOU WIN!!!" if player_won else "\t\tYOU LOST", "&"*50, sep="\n")


	return


main()


