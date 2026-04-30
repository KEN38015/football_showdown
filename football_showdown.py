import time
import random
import sys
from ball import display_ball


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





players = (

	# premier league
	Player(
		"Nico O'Reilly",
		"Manchester City", 
		75, 
		["Dribble", 15], 
		["Header", 25, 3]
	),
	

	"Erling Haaland" : [
		"Manchester City", 
		130,
		["Tap In", 17], 
		["Far Post Header", 42, 3]
	],

	"Rayan Cherki" : [
		"Manchester City",
		85,
		["Time Wasting", 20], 
		["Rabona", 50, 1]
	],

	"Tijjani Reijnders" : [
		"Manchester City", 
		95, 
		["Dribble", 17], 
		["Through Pass", 62, 1]
	],

	"Kevin De Bruyne" : [
		"Manchester City", 
		110, 
		["Whipped Cross", 30], 
		["Long Low-Driven Pass", 35, 3]
	],




	"Dominik Szoboszlai" : [
		"Liverpool",	
		105, 
		["Curved Shot", 20], 
		["40-yard Banger", 75, 1]
	],

	"Ryan Gravenberch" : [
		"Liverpool",
		95,
		["Rough Tackle", 20],
		["Yellow Card", 70, 1]
	],

	"Mohamed Salah" : [
		"Liverpool",
		85,
		["Sprint", 20],
		["Solo Dribble", 45, 2]
	],

	"Virgil Van Dijk" : [
		"Liverpool",
		142,
		["Tackle", 15],
		["Injury Time Header", 50, 1]
	],

	"Slippy G" : [
		"Liverpool",
		95,
		["Heavenly Pass", 25],
		["Half Field Volley", 80, 1]
	],




	"Cole Palmer" : [
		"Chelsea",
		80,
		["Assist", 23],
		["Ice Cold Finish", 30, 2]
	],

	"Alejandro Garnacho" : [
		"Chelsea",
		98,
		["Pressing", 19],
		["Cut in", 40, 3]
	],

	"Enzo Fernández" : [
		"Chelsea",
		95,
		["Escape Pressure", 15],
		["Switch Play", 30, 4],
	],


	"Marc Cucurella" : [
		"Chelsea",
		65,
		["Hard Tackle", 20],
		["50/50 Challenge", (lambda: random.randint(0, 50))(), 4]
	],

	"Didier Drogba" : [
		"Chelsea",
		100,
		["The Flying Ivorian", 30],
		["Clutch Goal", 75, 1]
	],




	"Bruno Fernandes" : [
		"Manchester United",
		80,
		["Through Pass", 18],
		["Top Bins Free Kick", 45, 2]

	],

	"Bryan Mbuemo" : [
		"Manchester United",
		105,
		["Pressing", 15],
		["Low Bins Finish", 35, 7]
	],

	"Casemiro" : [
		"Manchester United",
		100,
		["Pass", 15],
		["Header", 67, 1]
	],

	"Benjamin Šeško" : [
		"Manchester United",
		100,
		["Pace Abuse", 5],
		["The Flying Slovenian", 60, 2]
	],

	"Cristiano Ronaldo" : [
		"Manchester United",
		100,
		["Mr. Tap In", 25],
		["Bang Scorer- ahem Score Bangers", 90, 1]
	],









	# la lig(m)a
	"Jude Bellingham" : [
		"Real Madrid",
		110,
		["Elegant Pass", 28],
		["Composed Finish", 30, 1]
	],

	"Federico Valverde" : [
		"Real Madrid",
		80,
		["Full Field Sprint", 10],
		["Rocket Launcher", 90, 1]
	],

	"Antonio Rüdiger" : [
		"Real Madrid",
		130,
		["Aggresive Challenge", 23],
		["Crab Defending", 50, 2]
	],

	"Dictator Mbappé" : [
		"Real Madrid",
		100,
		["Explosive Sprint", 20],
		["Tap In", 40, 3]
	],

	"Sergio Ramos" : [
		"Real Madrid",
		120,
		["Powerful Header", 25],
		["Fatality", 200, 1]
	],







	"Lamine Yamal" : [
		"VARcelona",
		85,
		["Humiliation", 20],
		["Top Bins Curler", 45, 3]
	],

	"Pedri" : [
		"VARcelona",
		80,
		["La Croqueta", 12],
		["Ariel Through Pass", 40, 4]
	],

	"Robert Lewandoski" : [
		"VARcelona",
		118,
		["Dribble", 5],
		["The Flying Polish", 40, 4]
	],
	
	"Joules Koundé" : [
		"VARcelona",
		103,
		["Acceleration", 10],
		["Sliding Tackle", 60, 2]
	],

	"Lionel Messi" : [
		"VARcelona",
		60,
		["La Croqueta", 30],
		["Chip", 50, 6]
	],





	"Julián Álvarez" : [
		"Atlético de Madrid",
		65,
		["Sprint", 5],
		["Free Kick", 55, 3]
	],


	"Antoine Griezmann" : [
		"Atlético de Madrid",
		98,
		["Griddy", 23],
		["sIX SeVEn", 67, 2]
	],

	"Macros Llorente" : [
		"Atlético de Madrid",
		93,
		["Chase", 30],
		["Whipped Cross", 36, 2]
	],

	"Giuliano Simeone" : [
		"Atlético de Madrid",
		93,
		["Run Down", 30],
		["Whipped Cross", 36, 2]
	],

	"Fernando Torres" : [
		"Atlético de Madrid",
		115,
		["Low Bins", 20],
		["Towering Header", 50, 2],
	],







	"Gerard Moreno" : [
		"Villarreal",
		99,
		["Curled Shot", 15],
		["Lethal Assist", 45, 3],
	],
	
)










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
	delay()
	return choice if choice in list(map(str, options)) else get_action(options, err_msg="Choose only from the given options!")




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
				print(f"\nYou used {chosen_player.attack_name} to deal {chosen_player.damage} to {chosen_enemy.name}!")
				chosen_enemy.take_damage(chosen_player.damage)
				print(f"{chosen_enemy.name} is now on {chosen_enemy.hp} HP!")
				if chosen_enemy.hp <= 0:
					delay()
					print(f"\nYou defeated {chosen_enemy.name}!\n")
					delay()
				break
			case "special":
				print(f"\nYou used {chosen_player.special_name} to deal {chosen_player.special_damage} DP to {chosen_enemy.name}!")
				chosen_enemy.take_damage(chosen_player.special_attack())
				delay()
				print(f"{chosen_enemy.name} is now on {chosen_enemy.hp} HP!")
				if chosen_enemy.hp <= 0:
					delay()
					print(f"\nYou defeated {chosen_enemy.name}!")
				break
			case "check":
				delay()
				print(f"\n{chosen_enemy.name} has {chosen_enemy.hp} HP remaining.\n\n")
				delay(1.1)
	print(end="\n\n")
	delay()



def enemy_turn() -> None:
	global player_team, enemy_team, chosen_player, chosen_enemy

	if chosen_enemy.hp <= 0:
		chosen_enemy = enemy_choose(enemy_team, chosen_player, chosen_enemy)
	

	while True:

		if (chosen_player.hp <= chosen_enemy.special_damage and chosen_enemy.special_uses) or chosen_enemy.special_uses >= 2:
			chosen_player.take_damage(chosen_enemy.special_attack())
			delay()
			print(f"Enemy used {chosen_enemy.special_name} to deal DP {chosen_enemy.special_damage} to {chosen_player.name}!")
			delay()
			print(f"{chosen_player.name} is now on {chosen_player.hp} HP!")
			if chosen_player.hp <= 0:
				delay()
				print(f"Enemy defeated {chosen_player.name}!")
				delay()
			break
		delay()
		print(f"Enemy used {chosen_enemy.attack_name} to deal {chosen_enemy.damage} DP to {chosen_player.name}!")
		delay()
		chosen_player.take_damage(chosen_enemy.damage)
		print(f"{chosen_player.name} is now on {chosen_player.hp} HP!")
		if chosen_player.hp <= 0:
			delay()
			print(f"Enemy defeated {chosen_player.name}!")
			delay()
		break



	print(end="\n\n")
	delay()


def player_substitution(player_team : List[Player]) -> None:
	delay(1)
	global chosen_player
	choice = None
	if chosen_player.is_alive():
		while (choice := input(f"Substitution?\n{chosen_player.name} has {chosen_player.hp} HP remaining.\n").lower()) not in ["yes", "no"]:
			print("yes/no only!")

	if choice == "yes" or not chosen_player.is_alive():
		if (e := choose_player(player_team)).name != chosen_player.name:
			print(f"Substitution on the field for Home team, going off is {chosen_player.name}")
			delay()
			print(f"Replacing him, going on for Home team is, {e.name}!")
			chosen_player = e
		else:
			print(f"Continued using {chosen_player.name}!")

	delay(1)


def battle_loop(p_team : List[Player], e_team : List[Player]) -> bool:
	global player_team, enemy_team, chosen_player, chosen_enemy
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
			player_substitution(player_team)
			delay(1)
			if (tmp := enemy_choose(enemy_team, chosen_enemy, chosen_player)) != chosen_enemy:
				print(f"Substitution on the field for Away team, going off is {chosen_enemy.name}")
				delay()
				print(f"Replacing him, going on is, {tmp.name} with {tmp.hp} HP\n!")
				chosen_enemy = tmp
		delay()
		cycle += 1

		print("\n\n\n"+"!"*n, f"\tROUND {cycle}    -    {chosen_player.name.upper()} VS. {chosen_enemy.name.upper()}", "!"*n, sep="\n", end="\n\n\n")
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
	print("\n\n\n"+"*"*40, "*"*40, "\n\t  WELCOME TO FOOTBALL SHOWDOWN\n", "*"*40, "*"*40, sep="\n")
	delay(2)
	print("\n\n")
	player_team, enemy_team = create_teams()
	player_won = battle_loop(player_team, enemy_team)
	delay(2)
	print("&"*50, "\t\t\t\tYOU WIN!!!" if player_won else "\t\tYOU LOSE", "&"*50, sep="\n")
	delay(3)
	while (again := input("Play again? (yes/no)\n").lower()) not in ("yes", "no"):
		print("yes/no only!")

	if again == "yes":
		print("\n\n\n\n\n"*10)
		delay(1)
		main()

	print("\n\n\nGoodbye!")

	return

if __name__ == "__main__":
	display_ball()
	delay()
	print("Look at this!")
	delay(5)
	print("\n\n\n\n\n"*5)
	main()


