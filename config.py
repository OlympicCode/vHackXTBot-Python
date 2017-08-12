from random import uniform

user = "username"
password = "password"

# Enter Max Antivir to attack in normal mode
maxanti_normal = 3000

# Active or not the protection for cluster
active_cluster_protection = True

# Use booster
booster = False

# Finish all task by netcoins
Use_netcoins = True

# Enter Max Antivir to attack tournament
maxanti_tournament = 3000

# Enter Amount of Attacks normal
attacks_normal = 3

# Enter Amount of Attacks in tournament
attacks_tournament = 2

# define the initial mode
mode = "Secure"

BotNet_update = False

ddos_cluster = False

# change auto mode Potator for tournament
tournament_potator = True

AttackTournamentDB = False
Max_point_tournament = 1300
# Enter Updates (inet, hdd, cpu, ram, fw, av, sdk, ipsp, spam, scan, adw)
updates = ["ipsp", "adw", "fw", "scan", "sdk", "av"]
# updates = ["fw"]
# updates = ["ipsp",  "sdk"]
# Do you want to attack during tournament [True, False]
joinTournament = False
# Time to wait between each cycle in seconds
wait = round(uniform(0, 1), 2)
wait_load = round(uniform(1, 3), 2)
updatecount = 0
attackneeded = False
database = 'database.db'
anon = True
