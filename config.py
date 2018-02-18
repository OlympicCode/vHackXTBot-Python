from random import uniform

user = ""
password = ""


# define number task update
number_task = 30

# Enter Max Antivir to attack in normal mode
maxanti_normal = 3000

# Active or not the protection for cluster ( don't attack if you are ddos your cluster)
active_cluster_protection = True

# Use booster
booster = True

# Finish all task by netcoins
Use_netcoins = False

# Enter Max Antivir to attack tournament
maxanti_tournament = 3000

# Enter the minimal energy for update botnet
minimal_energy_botnet_upgrade = 10

# Enter Amount of Attacks normal
attacks_normal = 2

# Enter Amount of Attacks in tournament
attacks_tournament = 30

# define the initial mode
mode = "Secure"

# update botnet auto
BotNet_update = True

# check list of more player in tournament and ddos the cluster.
ddos_cluster = False

# change auto mode Potator for tournament
tournament_potator = False

AttackTournamentDB = False
Max_point_tournament = 1300
# Enter Updates (inet, hdd, cpu, ram, fw, av, sdk, ipsp, spam, scan, adw)
updates = ["ipsp", "fw", "scan", "sdk", "av"]
# updates = ["fw"]
# updates = ["ipsp",  "sdk"]

# Do you want to attack during tournament [True, False]
joinTournament = True

# Time to wait between each cycle in seconds
wait = round(uniform(0, 1), 2)
wait_load = round(uniform(0, 3), 2)
updatecount = 0
attackneeded = False
database = 'database.db'

# check attack anonymous
anon = True
