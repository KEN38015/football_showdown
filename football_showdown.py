import time
import random
import sys


has_ball = False
try:
	from ball import display_ball
except ModuleNotFoundError:
	pass
else:
	has_ball = True

class Player:
	def __init__(self, 
					name : str = "", 
					club : str = "", 
					max_hp : int = 0,
					attack_info : List[str | int] = ["", 0], 
					special_info : List[str | int] = ["", 0, 0],
					level_up_info : List[int | float] = [0, 0, 0, 0, 0],
				) -> None:
		self.name : str = name
		self.club : str = club
		self.hp : int = max_hp
		self.init_hp = max_hp
		self.attack_name, self.damage = attack_info
		self.attack_info = attack_info
		self.special_name, self.special_damage, self.special_uses = special_info
		self.init_special_uses = self.special_uses
		self.special_info = special_info
		self.level_up_info = level_up_info
		self.xp_threshold, self.thershold_mod, self.max_lvl, self.hp_mod, self.dmg_mod = level_up_info
		self._xp, self._lvl = 0, 0


		self.true_hp, self.true_dmg, self.true_special_dmg = self.hp, self.damage, self.special_damage
		self.init_dmg, self.init_special_dmg = self.damage, self.special_damage


	def is_alive(self) -> bool:
		return self.hp > 0


	def calc_stats(self, xp : int, lvl : int) -> Player:
		self._xp = xp
		self._lvl = lvl

		self.true_hp = self.init_hp * self.hp_mod ** self._lvl
		self.true_dmg = self.init_dmg * self.dmg_mod ** self._lvl
		self.true_special_dmg = self.init_special_dmg * self.dmg_mod ** self._lvl

		self.hp = round(self.true_hp)
		self.damage = round(self.true_dmg)
		self.special_damage = round(self.true_special_dmg)
		


	def take_damage(self, amount : int) -> None:
		self.hp = (self.hp - amount if self.hp >= amount else 0)


	def special_attack(self) -> int | bool:
		if self.special_uses:
			self.special_uses -= 1
			return self.special_damage
		return False


	def add_exp(self, xp : int) -> bool:
		if self._lvl == self.max_lvl:
			return
		self._xp += xp
		if self._xp >= self.xp_threshold:
			self._lvl += 1
			self.calc_stats(self._xp, self._lvl)


		return self._xp >= self.xp_threshold

	def get_xp(self) -> int:
		return self._xp

	def get_lvl(self) -> int:
		return self._lvl

	def get_xp_lvl(self) -> Tuple(int):
		return self._xp, self._lvl

	def load_data(self, ind : int, hp : int, special_uses : int, lvl : int) -> Player:
		p = players[ind]
		p.hp = hp
		p.special_uses = special_uses
		p._lvl = lvl
		return p

	# def refresh() -> None:
	# 	self.special_uses = self.init_special_uses

	def __str__(self) -> str:
		l = 30
		return f"\t{self.name}{" " * (l-len(self.name)-4)}| LVL: {self._lvl if self._lvl != self.max_lvl else "MAX LEVEL"}\n{" " * l}| HP: {self.hp}\n{" " * l}| {self.attack_name} : {self.damage}\n{" " * l}| {self.special_name}: {self.special_damage} (uses : {self.special_uses})"


	def __eq__(self, other) -> bool:
		return self.name == other.name


class Key:
	bit_max = 2**8-1
	def __init__(self, var_name : str):
		self._code : str
		self.name = var_name


	def to_binary(self) -> str:
		return ("".join(list(map(lambda x: f"{ord(x):08b}", self._code)))).replace("0b", "")

	def from_binary(self, s : str) -> None:
		subs = [int(s[i:i+8], 2) for i in range(0, len(s)-7, 8)]
		self._code = "".join(list(map(chr, subs)))




	def save_key(self) -> None:
		with open(self.name + ".bin", "w") as file:
			file.write(self.to_binary())


	def load_key(self, file_path : str) -> None:
		with open(self.name + ".bin", "r") as key_file:	
			# check if no exist contents
			with open(file_path, "r") as pf:
				if not len(contents := key_file.read()):
					self.generate_key(len(pf.read()))
					self.save_key()
				else:
					self.from_binary(contents)
		return

	def generate_key(self, length : int) -> None:
		# code format : (random character for each line)(the replacement character for a line)
		self._code = "".join(chr(random.randint(0, Key.bit_max)) for _ in range(length))

	def encrypted(self, text : str) -> str:
		encrypted = ""
		for ind, char in enumerate(text):
			# shift the ascii code of each character mod 256
			encrypted += chr((ord(char) + ord(self._code[-ind-1])) % Key.bit_max)
		return encrypted


	def decrypted(self, text : str) -> str:
		decrypted = ""
		for ind, char in enumerate(text):
			# shift the ascii code of each character mod 256
			decrypted += chr((ord(char) - ord(self._code[-ind-1])+Key.bit_max)%Key.bit_max)
		return decrypted





d = 0.8

''' format Player(
		name,
		club,
		health,
		[normal atck name, normal attack dmg],
		[special atck name, special atck dmg],
		[req xp, xp thresh modifier, max lvl, hp modifier, dmg modifier]
	)


1 match about 5-35 xp
'''


def randnum(choices : int) -> int:
	global seed_index, seed
	seed_index += 1
	return int(str(seed)[-seed_index]) % choices

def choose(options : list) -> int:
	return options[randnum(len(options))]



players = [

	# premier league
	Player(

		"Nico O'Reilly",
		"Manchester City", 
		75, 
		["Dribble", 15], 
		["Header", 25, 3],
		[80, 1.1, 15, 1.2, 1.2]
	),
	

	Player(
		"Erling Haaland",
		"Manchester City", 
		130,
		["Tap In", 17], 
		["Far Post Header", 42, 3],
		[120, 1.15, 9, 1.3, 1.3]
	),
	Player(
		"Rayan Cherki",
		"Manchester City",
		85,
		["Time Wasting", 20], 
		["Rabona", 50, 1],
		[60, 1.45, 20, 1.05, 1.2]
	),
	Player(
		"Tijjani Reijnders",
		"Manchester City", 
		95, 
		["Dribble", 17], 
		["Through Pass", 62, 1],
		[100, 1.2, 12, 1.2, 1.2]
	),
	Player(
		"Kevin De Bruyne",
		"Manchester City", 
		110, 
		["Whipped Cross", 26], 
		["Long Low-Driven Pass", 35, 4],
		[200, 1.5, 5, 1.3, 1.3]
	),



	Player(
		"Dominik Szoboszlai",
		"Liverpool",	
		105, 
		["Curved Shot", 20], 
		["40-yard Banger", 75, 1],
		[105, 1.25, 10, 1.1, 1.4]
	),
	Player(
		"Ryan Gravenberch",
		"Liverpool",
		95,
		["Rough Tackle", 20],
		["Yellow Card", 70, 1],
		[100, 1.3, 16, 1.3, 1.1]
	),
	Player(
		"Mohamed Salah",
		"Liverpool",
		85,
		["Sprint", 20],
		["Solo Dribble", 45, 2],
		[185, 1.5, 7, 1.3, 1.3]
	),
	Player(
		"Virgil Van Dijk",
		"Liverpool",
		142,
		["Tackle", 15],
		["Injury Time Header", 50, 1],
		[160, 1.6, 9, 1.2, 1.05]
	),
	Player(
		"Slippy G",
		"Liverpool",
		95,
		["Heavenly Pass", 25],
		["Half Field Volley", 80, 1],
		[250, 1.7, 5, 1.3, 1.67]
	),



	Player(
		"Cole Palmer",
		"Chelsea",
		80,
		["Dribble", 23],
		["Ice Cold Finish", 40, 3],
		[100, 1.25, 14, 1.05, 1.2]
	),


	Player(
	"Alejandro Garnacho",
		"Chelsea",
		98,
		["Pressing", 19],
		["Cut in", 40, 3],
		[60, 1.2, 13, 1.15, 1.2]
	),

	Player(
		"Enzo Fernández",
		"Chelsea",
		95,
		["Escape Pressure", 15],
		["Switch Play", 30, 4],
		[100, 1.3, 16, 1.3, 1.1]
	),

	Player(
		"Marc Cucurella",
		"Chelsea",
		75,
		["Hard Tackle", 20],
		["50/50 Challenge", 30, 4],
		[130, 1.2, 10, 1.35, 1.2]
	),

	Player(
		"Didier Drogba",
		"Chelsea",
		100,
		["The Flying Ivorian", 30],
		["Clutch Goal", 75, 1],
		[300, 1.3, 3, 1.3, 1.5]
	),



	Player(
		"Bruno Fernandes",
		"Manchester United",
		80,
		["Through Pass", 18],
		["Top Bins Free Kick", 45, 2],
		[140, 1.3, 8, 1.3, 1.1]

	),

	Player(
		"Bryan Mbuemo",
		"Manchester United",
		105,
		["Pressing", 15],
		["Low Bins Finish", 35, 7],
		[80, 1.3, 15, 1.05, 1.2]
	),
	Player(
		"Casemiro",
		"Manchester United",
		100,
		["Pass", 15],
		["Header", 67, 1],
		[140, 1.4, 7, 1.3, 1.1]
	),

	Player(
		"Benjamin Šeško",
		"Manchester United",
		100,
		["Run", 7],
		["The Flying Slovenian", 60, 2],
		[100, 1.2, 12, 1.3, 1.4]
	),

	Player(
		"Cristiano Ronaldo",
		"Manchester United",
		110,
		["Mr. Tap In", 25],
		["Bang Scorer- ahem Score Bangers", 90, 1],
		[200, 1.05, 10, 1.2, 1.2]
	),









	# la lig(m)a
	Player(
		"Jude Bellingham",
		"Real Madrid",
		110,
		["Elegant Pass", 28],
		["Composed Finish", 35, 2],
		[120, 1.2, 10, 1.1, 1.3]
	),

	Player(
		"Federico Valverde",
		"Real Madrid",
		80,
		["Full Field Sprint", 10],
		["Rocket Launcher", 90, 1],
		[200, 1.05, 10, 1.3, 1.1]
	),

	Player(
		"Antonio Rüdiger",
		"Real Madrid",
		130,
		["Aggresive Challenge", 23],
		["Crab Defending", 50, 2],
		[190, 1.1, 7, 1.5, 1.1]
	),

	Player(
		"Dictator Mbappé",
		"Real Madrid",
		100,
		["Explosive Sprint", 20],
		["Tap In", 40, 3],
		[130, 1.25, 10, 1.1, 1.2]
	),

	Player(
		"Sergio Ramos",
		"Real Madrid",
		120,
		["Tackle", 5],
		["Fatality", 200, 1],
		[250, 1.2, 4, 1.6, 1.1]
	),






	Player(
		"Lamine Yamal",
		"VARcelona",
		85,
		["Humiliation", 20],
		["Top Bins Curler", 45, 3],
		[50, 1.1, 20, 1.2, 1.3]
	),

	Player(
		"Pedri",
		"VARcelona",
		80,
		["La Croqueta", 12],
		["Ariel Through Pass", 40, 4],
		[70, 1.05, 16, 1.2, 1.2]
	),

	Player(
		"Robert Lewandoski",
		"VARcelona",
		118,
		["Dribble", 5],
		["The Flying Polish", 40, 4],
		[160, 1.2, 7, 1.3, 1.1]
	),
	
	Player(
		"Jules Koundé",
		"VARcelona",
		103,
		["Acceleration", 10],
		["Sliding Tackle", 60, 2],
		[95, 1.15, 10, 1.3, 1.2]
	),

	Player(
		"Lionel Messi",
		"VARcelona",
		60,
		["La Croqueta", 30],
		["Chip", 50, 6],
		[200, 1.05, 6, 1.01, 1.4]
	),




	Player(
		"Julián Álvarez",
		"Atlético de Madrid",
		65,
		["Sprint", 5],
		["Free Kick", 55, 3],
		[105, 1.2, 8, 1.2, 1.35]
	),

	Player(
		"Antoine Griezmann",
		"Atlético de Madrid",
		98,
		["Griddy", 23],
		["sIX SeVEn", 67, 2],
		[130, 1.3, 9, 1.3, 1.2]
	),

	Player(
		"Macros Llorente",
		"Atlético de Madrid",
		93,
		["Chase", 30],
		["Whipped Cross", 36, 2],
		[90, 1.15, 12, 1.3, 1.1]
	),

	Player(
		"Giuliano Simeone",
		"Atlético de Madrid",
		93,
		["Run Down", 30],
		["Whipped Cross", 36, 2],
		[80, 1.1, 10, 1.2, 1.2]
	),

	Player(
		"Fernando Torres",
		"Atlético de Madrid",
		115,
		["Low Bins", 20],
		["Towering Header", 52, 3],
		[300, 1.5, 3, 2, 2]
	),






	
	Player(
		"Ousmane Dembélé",
		"Paris Saint-Germain",
		99,
		["Sprint", 25],
		["High Press", 45, 4],
		[100, 1.05, 10, 1.2, 1.2]
	),

	Player(
		"Khvicha Kvaratskhelia",
		"Paris Saint-Germain",
		100,
		["Cut In", 10],
		["Blitz Curler", 55, 2],
		[50, 1.3, 18, 1.2, 1.2]
	),
	Player(
		"Désiré Doué",
		"Paris Saint-Germain",
		100,
		["Cut In", 10],
		["Blitz Curler", 55, 2],
		[40, 1.1, 23, 1.2, 1.2]
	),
	Player(
		"Vitinha",
		"Paris Saint-Germain",
		100,
		["Dribble", 15],
		["Long Pass", 40, 2],
		[70, 1.2, 13, 1.05, 1.2]
	),
	Player(
		"Thiago Silva",
		"Paris Saint-Germain",
		100,
		["Run", 10],
		["Hard Tackle", 40, 4],
		[40, 1.3, 21, 1.2, 1.2]
	),
]




def to_binary(string : str, digit_limit : int = 16) -> str:
	return ("".join(list(map(lambda x: f"{ord(x):0{digit_limit}b}", string)))).replace("0b", "")

def from_binary(string : str, bin_len : int = 16) -> None:
	subs = [int(string[i:i+bin_len], 2) for i in range(0, len(string)-bin_len+1, bin_len)]
	return "".join(list(map(chr, subs)))


def delay(t : float = 0.8) -> None:
	time.sleep(t)


def create_teams() -> Tuple[List[Monster]]:
	print("choosing teams\n")
	player_team = []
	enemy_team = []
	for a in range(2):
		for i in range(players_per_team):
			# check no dupes
			while (chosen := random.choice(players)).name in list(map(lambda x: x.name, player_team + enemy_team)):
				pass
			if a-1: # is 0
				player_team.append(chosen)
			else:
				enemy_team.append(chosen)
			print(".", end="")
			delay(.5)
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
		return players[seed % len(players)]
	# check if 1-tap
	if opposition.damage >= selected.hp or (opposition.special_damage >= selected.hp and opposition.special_uses):
		# get another one thats healthy
		if (fir := list(filter(lambda p: p.hp > opposition.damage and (p.hp > opposition.special_damage and opposition.special_uses), players))):
			return choose(fir)

		if (sec := list(filter(lambda p: p.hp > opposition.damage,
				players))):
			return choose(sec)



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
			print(f"{chosen_enemy.name} used {chosen_enemy.special_name} to deal {chosen_enemy.special_damage} DP to {chosen_player.name}!")
			delay()
			print(f"{chosen_player.name} is now on {chosen_player.hp} HP!")
			if chosen_player.hp <= 0:
				delay()
				print(f"{chosen_enemy.name} defeated {chosen_player.name}!")
				delay()
			break
		delay()
		print(f"{chosen_enemy.name} used {chosen_enemy.attack_name} to deal {chosen_enemy.damage} DP to {chosen_player.name}!")
		delay()
		chosen_player.take_damage(chosen_enemy.damage)
		print(f"{chosen_player.name} is now on {chosen_player.hp} HP!")
		if chosen_player.hp <= 0:
			delay()
			print(f"{chosen_enemy.name} defeated {chosen_player.name}!")
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
		if (e := choose_player(player_team)) != chosen_player:
			print(f"Substitution on the field for Home team, going off is {chosen_player.name}")
			delay()
			print(f"Replacing him, going on for Home team is, {e.name}!")
			chosen_player = e
		else:
			print(f"Continued using {chosen_player.name}!")

	delay(1)


def battle_loop() -> bool:
	global player_team, enemy_team, chosen_player, chosen_enemy, continue_data

	if continue_data is None:
		cycle = 0
		print("Choose your starting player!")
		delay()
		chosen_player = choose_player(player_team)
		chosen_enemy = choose(enemy_team)
		print(f"You're up against - {chosen_enemy.name} : LVL {chosen_enemy.get_lvl()}!\n")
	
	else:
		player_team, enemy_team, chosen_player, chosen_enemy, cycle = continue_data
	
	delay(1)
	n = 80
	while player_team and enemy_team:
		if cycle and continue_data is None:
			player_substitution(player_team)
			delay(1)
			if (tmp := enemy_choose(enemy_team, chosen_enemy, chosen_player)) != chosen_enemy:
				print(f"Substitution on the field for Away team, going off is {chosen_enemy.name}")
				delay()
				print(f"Replacing him, going on is, {tmp.name} with {tmp.hp} HP!\n\n\n")
				chosen_enemy = tmp
			ask_save([player_team, enemy_team, chosen_player, chosen_enemy, int(cycle)])
			delay()
		cycle += 1
		delay(.4)
		continue_data = None




		print("\n\n\n"+"!"*n, f"\t\tROUND {cycle}    -    {chosen_player.name.upper()} VS. {chosen_enemy.name.upper()}", "!"*n, sep="\n", end="\n\n\n")
		delay(2)
		

		print(str("PLAYER" if (c := randnum(2)) else "ENEMY") + " GETS TO GO FIRST\n\n")
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
		





player_team : Player = None
enemy_team : Player = None
chosen_player : Player = None
chosen_enemy : Player = None

continue_data : str = None


players_per_team = 5

seed : int = 0
seed_index : int = 0





data_key = Key("data_key")
data_key.load_key("player_data.bin")

save_file_key = Key("save_file_key")
save_file_key.load_key("save_file.bin")

seed_key = Key("seed_key")


# save data looks like:
'''			 
	save_data = [
		player_team
		enemy_team
		chosen_player
		chosen_enemy
		cycle
	]
'''

def generate_seed() -> None:
	global seed
	# creates like a number from 0 to 2**128-1, process with modulo
	seed = random.randint(0, 2**128-1)


def ask_save(save_data : list) -> None:
	delay(1)
	while (choice := input("\n\nSave progress up to this point?\nAgreement would override the previous save file\n")) not in ("yes", "no"):
		print("yes/no only!")
		delay(.3)

	p_team, e_team, c_player, c_enemy, cycle = save_data
	if choice == "yes":
		save_progress(save_data)



	delay(.2)
	print("All set!")
	delay(.9)


def save_progress(save_data : List) -> None:
	global save_file_key, players, seed, seed_key, seed_index
	with open("save_file.bin", "w") as player_file:
		# formats into *index_of_team_players (seperator ,) applies for both teams
		p_team = ",".join([f"{str(tuple(map(lambda x: x.name, players)).index(p.name))} {p.hp} {p.special_uses} {p._lvl}" for p in save_data[0]])
		e_team = ",".join([f"{str(tuple(map(lambda x: x.name, players)).index(p.name))} {p.hp} {p.special_uses} {p._lvl}" for p in save_data[1]])
		c_player = tuple(map(lambda x: x.name, save_data[0])).index(save_data[2].name)
		c_enemy = tuple(map(lambda x: x.name, save_data[1])).index(save_data[3].name)
		cycle = str(save_data[-1])


		save_file_key.generate_key(len(save := "\n".join(tuple(map(str, [p_team, e_team, c_player, c_enemy, cycle])))))
		player_file.write(to_binary(save_file_key.encrypted(save)))
		save_file_key.save_key()


		with open("seed.bin", "w") as seed_file:
			seed_key.generate_key(257)
			seed_file.write(to_binary(seed_key.encrypted(f"{seed:0128}\n{seed_index-1:0128}")))
		with open("seed_key.bin", "w") as seed_key_file:
			seed_key_file.write(seed_key.to_binary())


	delay(1)
	print("Saved!")
	delay(1)




def save_player_data() -> None:
	global players, data_key

	with open("player_data.bin", "w") as player_file:
		save = "\n".join([f"{xp} {lvl}" for xp, lvl in list(map(Player.get_xp_lvl, players))])
		data_key.generate_key(len(save))
		data_key.save_key()
		save = to_binary(data_key.encrypted(save))
		player_file.write(save)


def process_save_file(content : str) -> Tuple:
	content = save_file_key.decrypted(from_binary(content)).split("\n")
	content[0] = [Player().load_data(int(i.split()[0]), *list(map(int, i.split()[1:]))) for i in content[0].split(",")]
	content[1] = [Player().load_data(int(i.split()[0]), *list(map(int, i.split()[1:]))) for i in content[1].split(",")]
	
	
	content[2] = content[0][int(content[2])]
	content[3] = content[1][int(content[3])]

	content[-1] = int(content[-1])
	return content





def load_data() -> None:
	global players, data_key, save_file_key, continue_data, seed_key, seed
	# unpack file to variables
	with open("player_data.bin", "r") as player_file:
		

		# check if data aint there
		if not len(player_data := player_file.read()):
			save_player_data()
			return


		

		# decrypt to readable

		player_data = (data_key.decrypted(from_binary(player_data))).split("\n")

		
		for player, data in zip(players, player_data):
			player.calc_stats(*list(map(int, data.split())))




		with open("save_file.bin", "r+") as file:
			contents = file.read()
			if contents:
				print("You have a save file!")
				delay()
				while (cont := input("Would you like to load it?\nAny action would delete the file contents after usage\n")) not in ("yes", "no"):
					print("yes/no only!")
					delay()
				if cont == "no":
					file.truncate(0)
					return

				data_key.load_key("player_data.bin")
				continue_data = process_save_file(contents)
				delay()
				print("loading...")
				delay()
				seed_key.load_key("seed.bin")
				with open("seed.bin", "r") as seed_file:
					seed, seed_index = seed_key.decrypted(from_binary(seed_file.read())).split("\n")

			file.truncate(0)










def award(win : bool) -> None:
	xp_reward_range = (10, 60) if win else (0, 35)
	print("The following players would be awarded the following amount of XP:")
	for player in player_team + enemy_team:
		prev_xp_thresh = player.xp_threshold
		player.add_exp(amount := choose(list(range(*xp_reward_range))) * 10) # debugging
		print(f"{player.name} - {amount} / {prev_xp_thresh}")
		if (amount := choose(list(range(*xp_reward_range))) * 10) >= player.xp_threshold:
			delay()
			
			print(f"{player.name} leveled up to level {player.get_lvl()}!")
			delay()
		delay()




def main() -> None:
	global player_team, enemy_team, continue_data, players

	load_data()
	generate_seed()

	print("\n\n\n"+"*"*40, "*"*40, "\n\t  WELCOME TO FOOTBALL SHOWDOWN\n", "*"*40, "*"*40, sep="\n", end="\n"*5)
	delay(2)
	print("\n\n")

	if continue_data is None:
		player_team, enemy_team = create_teams()

	player_won = battle_loop()

	delay(2)
	print("&"*40, "\t\t\t\tYOU WIN!!!" if player_won else "\t\t\t\tYOU LOSE", "&"*40, sep="\n", end="\n"*5)
	delay(3)

	print("deleting save file", end="")
	for _ in range(3):
		print(".", end="")
		delay(.3)

	# deletes file
	with open("save_file.bin", "w") as save_file:
		save_file.write(str())


	print("\nDone!")
	delay()

	


	award(player_won)

	save_player_data()

	while (again := input("Play again? (yes/no)\n").lower()) not in ("yes", "no"):
		print("yes/no only!")

	map(Player.refresh(), players)

	if again == "yes":
		print("\n\n\n\n\n"*10)
		delay(1)
		main()

	print("\n\n\nGoodbye!")
	save_player_data()
	return

if __name__ == "__main__":
	if has_ball:
		while (see_ball := input("wanna see ballz?\n")) not in ["yes", "no"]:
			delay(.3)
		if see_ball == "yes":
			display_ball()
			delay()
			print("Look at this!")
			delay(5)
		print("\n\n\n\n\n")
	
	main()


