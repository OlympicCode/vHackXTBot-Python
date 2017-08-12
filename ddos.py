import config
import json
import sqlite3
import re
import operator
import os
import time
import console


class Ddos:

    def __init__(self, uhash):
        self.ddos_cluster = config.ddos_cluster
        self.database = config.database
        self.Max_point_tournament = config.Max_point_tournament
        self.username = config.user
        self.password = config.password
        self.uhash = uhash
        self.c = console.Console(self.username, self.password, self.uhash)

    def run_ddos(self):
        if self.ddos_cluster:
            checkcluster = json.loads(self.c.check_Cluster())
            TournamentPosition = json.loads(self.c.GetTournamentPosition())
            try:
                # determine and attack cluster tournament
                db = sqlite3.connect(self.database)
                cursor = db.cursor()

                try:
                    cursor.execute("""CREATE TABLE Cluster (ID TEXT, cluster_name TEXT, cluster_point TEXT) """)
                except sqlite3.OperationalError:
                    pass

                tournament_left = re.findall('\d+', TournamentPosition["tleft"])
                print "Tournament star finish in " + str(TournamentPosition["tleft"])
                try:
                    tournament_hour = tournament_left[0]
                    tournament_minute = tournament_left[1]
                except IndexError:
                    tournament_hour = 0
                    try:
                        tournament_minute = tournament_left[0]
                    except IndexError:
                        tournament_minute = 0

                if int(tournament_hour) == 0 and int(tournament_minute) < 60:

                    cluster_name = {}
                    for row in cursor.execute(
                            "SELECT * FROM (SELECT cluster_point, cluster_name FROM Cluster ORDER BY cluster_point ASC)"):
                        cluster_name[row[0]] = row[1]

                    newA = sorted(cluster_name.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(cluster_name)]

                    for i in range(0, len(newA)):
                        Cluster_name = newA[i][1]
                        Cluster_point = newA[i][0]

                        checkcluster = json.loads(self.c.check_Cluster())
                        if "DDoS not ready" in checkcluster["ddosready"]:
                            print checkcluster["ddosready"]
                            break
                        else:
                            try:
                                scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                            except UnicodeEncodeError:
                                scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))

                            if scan_cluster["result"] == "0":
                                scan_cluster["ddoschance"] = scan_cluster["ddoschance"].split("%")
                                ddoschance = re.findall('\d+', scan_cluster["ddoschance"][0])
                                if int(ddoschance[0]) > 50:
                                    print "attack " + Cluster_name + "(" + str(Cluster_point) + ")" + " Your chance is " + \
                                          scan_cluster["ddoschance"][0] + "%"
                                    result = json.loads(self.c.AttackCluster(Cluster_name))
                                    os.remove(self.database)
                                    if result['result'] == 6:
                                        pass
                                    else:
                                        break
                else:
                    # Analyse Cluster in tournament
                    db = sqlite3.connect(self.database)
                    cursor = db.cursor()

                    try:
                        cursor.execute("""CREATE TABLE Cluster (ID TEXT, cluster_name TEXT, cluster_point TEXT) """)
                    except sqlite3.OperationalError:
                        pass

                    count = 0
                    data = []
                    point = {}
                    nb = len(TournamentPosition['data'])
                    for i in range(1, nb):
                        getCluster = TournamentPosition['data'][i]['user'].split("|")
                        data.append(getCluster[0])
                        point[getCluster[0].strip()] = point.get(getCluster[0].strip(), 0) + i

                    data2 = {}
                    for i in data:
                        data2[str(i.encode("utf-8")).strip()] = int(data.count(i))
                    newA = sorted(data2.iteritems(), key=operator.itemgetter(1), reverse=True)[0:nb]

                    print "best list for tournament :"
                    final_data = {}
                    for i in range(0, len(newA)):
                        Cluster_name = newA[i][0]
                        Cluster_pepole = newA[i][1]
                        print " cluster : " + Cluster_name.decode("utf-8") + " | people on cluster : " + str(
                            Cluster_pepole) + " | Points in clusters = " + str(
                            point[Cluster_name.decode("utf-8")] / Cluster_pepole)
                        final_data[Cluster_name.decode("utf-8")] = int(point[Cluster_name.decode("utf-8")] * Cluster_pepole)

                    newA = sorted(final_data.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(newA)]
                    for i in range(0, len(newA)):
                        Cluster_name = newA[i][0]
                        Cluster_point = newA[i][1]
                        if Cluster_point < self.Max_point_tournament:
                            # try:
                            #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                            # except UnicodeEncodeError:
                            #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))

                            count = count + 1
                            print "if attack " + Cluster_name + "(" + str(Cluster_point) + ")"
                            Cluster = [(0, Cluster_name, str(Cluster_point))]
                            cursor.executemany("INSERT INTO Cluster VALUES (?,?,?)", Cluster)
                            db.commit()
                    else:
                        count = 0
                        for i in range(0, len(newA)):
                            Cluster_name = newA[i][0]
                            Cluster_point = newA[i][1]
                            if Cluster_point < self.Max_point_tournament and count < 5:
                                # try:
                                #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                                # except UnicodeEncodeError:
                                #	scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))

                                count = count + 1
                                print "if attack " + Cluster_name + "(" + str(Cluster_point) + ")"
                                Cluster = [(0, Cluster_name, str(Cluster_point))]
                                cursor.executemany("INSERT INTO Cluster VALUES (?,?,?)", Cluster)
                                db.commit()
                        time.sleep(5)


            except KeyError:
                # attack cluster for not in tournament
                tournament_next = re.findall('\d+', TournamentPosition['nexttournament'])
                try:
                    tournament_hour = tournament_next[0]
                    tournament_minute = tournament_next[1]
                except IndexError:
                    tournament_hour = 0
                    try:
                        tournament_minute = tournament_next[0]
                    except:
                        tournament_minute = 0

                if int(tournament_hour) > 4:
                    data = []
                    point = {}
                    nb = len(TournamentPosition['data'])
                    for i in range(1, nb):
                        getCluster = TournamentPosition['data'][i]['user'].split("|")
                        data.append(getCluster[0])
                        point[getCluster[0].strip()] = point.get(getCluster[0].strip(), 0) + i

                    data2 = {}
                    for i in data:
                        data2[str(i.encode("utf-8")).strip()] = int(data.count(i))
                    newA = sorted(data2.iteritems(), key=operator.itemgetter(1), reverse=True)[0:nb]

                    print "best list for tournament :"
                    final_data = {}
                    for i in range(0, len(newA)):
                        Cluster_name = newA[i][0]
                        Cluster_pepole = newA[i][1]
                        # print " cluster : "+ Cluster_name.decode("utf-8") + " people on cluster : " + str(Cluster_pepole)  + " Points in clusters = " + str(point[Cluster_name.decode("utf-8")]/Cluster_pepole)
                        final_data[Cluster_name.decode("utf-8")] = int(point[Cluster_name.decode("utf-8")] * Cluster_pepole)

                    newA = sorted(final_data.iteritems(), key=operator.itemgetter(1), reverse=True)[0:len(newA)]
                    for i in range(0, len(newA)):
                        Cluster_name = newA[i][0]
                        Cluster_point = newA[i][1]
                        if Cluster_point < self.Max_point_tournament:
                            checkcluster = json.loads(self.c.check_Cluster())
                            test = "no"
                            if "DDoS not ready" in checkcluster["ddosready"] and test == "no":
                                print checkcluster["ddosready"]
                                break
                            else:
                                try:
                                    scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.decode("utf-8")))
                                except UnicodeEncodeError:
                                    scan_cluster = json.loads(self.c.ScanCluster(Cluster_name.encode("utf-8")))
                                if scan_cluster["result"] == "0":
                                    scan_cluster["ddoschance"] = scan_cluster["ddoschance"].split("%")
                                    ddoschance = re.findall('\d+', scan_cluster["ddoschance"][0])
                                    if int(ddoschance[0]) > 50:
                                        print "attack " + Cluster_name + "(" + str(
                                            Cluster_point) + ")" + " Your chance is " + scan_cluster["ddoschance"][0] + "%"
                                        result = json.loads(self.c.AttackCluster(Cluster_name))
                                        if result['result'] == 6:
                                            pass
                                        else:
                                            break
                                    else:
                                        print "no attack possible to " + Cluster_name + " (" + str(
                                            Cluster_point) + ")" + " Your chance is " + scan_cluster["ddoschance"][0] + "%"
                else:
                    print "next tournament in " + TournamentPosition['nexttournament']