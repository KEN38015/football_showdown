import time
import random


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

	def take_damage(self, amount) -> None:
		self.hp -= amount

	def normal_attack(self) -> int:
		return self.damage

	def special_attack(self) -> int:
		if self.special_uses:
			self.special_uses -= 1
			return special_damage
		return -1

	def __str__(self) -> str:
		l = 25
		return f"{self.name}{" " * (l-len(self.name))}| HP: {self.hp}\n{" " * l}| {self.attack_name} : {self.damage}\n{" " * l}|{self.special_name}: {self.special_damage} (uses : {self.special_uses})"


d = 0.8

# format {name : [club, max_hp, [attack_info, damage], [special name, special damage, special uses]]}

players = {
	"Kevin De Bruyne" : ["Manchester City", 105, ["Long-Distance Pass" ,30], ["Curled Header", 35, 3]],
	"Erling Haaland" : ["Manchester City", 130, ["Tap In", 20], ["Far Post Header", 45, 2]],
	"Rayan Cherki" : ["Manchester City", 70, ["Rabona", 20], ["Juggling", 45, 1]],
	"Tijjani Reijnders" : ["Manchester City", 90, ["Shot", 15], ["Yellow Card", 70, 1]],
	"Riyad Mahrez" : ["Manchester City", 80, ["Shot", 25], ["Lobbed Pass", 35, 2]],

	"Dominik Szoboszlai" : ["Liverpool", 100, ["Curved Shot", 20], ["40-yard Banger", 60, 1]],
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
	print("done!")
	delay(1)
	return player_team, enemy_team


def display_team(team : List[Player], prompt : str = "") -> None:
	print(prompt)
	for player in team:
		print(player, end="\n\n")
	delay()



def choose_player(selection_range : range) -> int:
	pass


def player_turn() -> None:
	pass


def enemy_turn() -> None:
	pass


def battle_loop(p_team : List[Player], e_team : List[Player]) -> None:
	player_team = p_team[:]
	enemy_team = e_team[:]
	cycle = 0
	while all(list(map(lambda x: x.hp > 0, player_team))) or all(list(map(lambda x: x.hp > 0, enemy_team))):
		cycle += 1
		print("!"*40, f"\t\tROUND {cycle}", "!"*40, sep="\n")
		





def main() -> None:
	print("*"*40, "*"*40, "\n\t  WELCOME TO FOOTBALL SHOWDOWN\n", "*"*40, "*"*40, sep="\n")
	delay()
	player_team, enemy_team = create_teams()
	display_team(player_team, "Your team:\n")
	battle_loop()
	


	return


main()


