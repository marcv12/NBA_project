import pandas as pd
import mysql.connector as mysql

games = pd.read_csv("NBA_data/games.csv")
dfg = pd.DataFrame(games)
print(dfg)

games_details = pd.read_csv("NBA_data/games_details.csv")
dfgd = pd.DataFrame(games_details)
print(dfgd)

players = pd.read_csv("NBA_data/players.csv")
dfp = pd.DataFrame(players)
print(dfp)

teams = pd.read_csv("NBA_data/teams.csv")
dft = pd.DataFrame(teams)
print(dft)

ranking = pd.read_csv("NBA_data/ranking.csv")
dfr = pd.DataFrame(ranking)
print(dfr)

belongs = pd.read_csv("NBA_data/Belongs_to.csv")
dfb = pd.DataFrame(belongs)
print(dfb)

db = mysql.connect(
    host="localhost",
    user="root",
    # passwd= "Enter your password here"
)

mycursor = db.cursor()  # run this and the following line to create the database

mycursor.execute("CREATE DATABASE nba_dataset")

db = mysql.connect(
    host="localhost",
    user="root",
    # passwd= "Enter your password here",
    database="nba_dataset"
)

print(db)

if db:
    print("Connection successful")

cursor = db.cursor()

cursor.execute('''
		CREATE TABLE players (
			PLAYER_ID int,
			NAME varchar(50),
			primary key(PLAYER_ID)
			)
               ''');

cursor.execute('''
		CREATE TABLE Teams (
		    TEAM_ID int,
		    NICKNAME varchar(50),
		    YEARFOUNDED int,
		    CITY varchar(50),
		    ARENACAPACITY int,
		    primary key(TEAM_ID)
			)
               ''');

cursor.execute('''
		CREATE TABLE games (
		    GAME_ID int primary key,
		    HOME_TEAM_ID int,
		    VISITOR_TEAM_ID int,
		    SEASON int,
		    DATE date,
		    PTS_home int,
		    FG_PCT_home float,
		    FT_PCT_home float,
		    PTS_away int,
		    FG_PCT_away float,
		    FT_PCT_away float,
		    HOME_TEAM_WINS int check (HOME_TEAM_WINS=1 or HOME_TEAM_WINS=0),
		    FOREIGN KEY (HOME_TEAM_ID) REFERENCES Teams(TEAM_ID),
		    FOREIGN KEY (VISITOR_TEAM_ID) REFERENCES Teams(TEAM_ID)
			)
               ''');

cursor.execute('''
		CREATE TABLE Ranking (
          TEAM_ID int,
          SEASON_ID int,
          STANDINGSDATE date,
          CONFERENCE char(4),
          G int,
          W int,
          L int,
          W_PCT float,
          primary key(TEAM_ID, SEASON_ID),
          FOREIGN KEY (TEAM_ID) REFERENCES Teams(TEAM_ID)
 			)
                ''');

cursor.execute('''
    CREATE TABLE details(
      PLAYER_ID int,
      GAME_ID int,
      FGM int,
      FGA int,
      FG3M int,
      FG3A int,
      PTS int,
      PLUS_MINUS int,
      primary key(PLAYER_ID, GAME_ID),
      FOREIGN KEY (PLAYER_ID) REFERENCES players(PLAYER_ID),
      FOREIGN KEY (GAME_ID) REFERENCES games(GAME_ID)
      )
              ''');

cursor.execute('''
    CREATE TABLE belongs(
      TEAM_ID int,
      PLAYER_ID int,
      SEASON int,
      FOREIGN KEY (TEAM_ID) REFERENCES Teams(TEAM_ID),
      FOREIGN KEY (PLAYER_ID) REFERENCES players(PLAYER_ID),
      PRIMARY KEY (TEAM_ID, PLAYER_ID, SEASON)
      )
              ''')

for row in dfp.itertuples():
    cursor.execute('''
          INSERT INTO players (PLAYER_ID, NAME)
          VALUES (%s,%s)
          ''',
                   (row.PLAYER_ID,
                    row.NAME)
                   )

db.commit()

for row in dft.itertuples():
    cursor.execute('''
                INSERT INTO Teams (TEAM_ID,NICKNAME,YEARFOUNDED,CITY,ARENACAPACITY)
                VALUES (%s,%s,%s,%s,%s)
                ''',
                   (row.TEAM_ID,
                    row.NICKNAME,
                    row.YEARFOUNDED,
                    row.CITY,
                    row.ARENACAPACITY)
                   )

db.commit()

for row in dfg.itertuples():
    cursor.execute('''
                INSERT INTO games (GAME_ID,HOME_TEAM_ID,VISITOR_TEAM_ID,SEASON,DATE,PTS_home,
                                    FG_PCT_home,FT_PCT_home,PTS_away,FG_PCT_away,FT_PCT_away,HOME_TEAM_WINS)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',
                   (row.GAME_ID,
                    row.HOME_TEAM_ID,
                    row.VISITOR_TEAM_ID,
                    row.SEASON,
                    row.DATE,
                    row.PTS_home,
                    row.FG_PCT_home,
                    row.FT_PCT_home,
                    row.PTS_away,
                    row.FG_PCT_away,
                    row.FT_PCT_away,
                    row.HOME_TEAM_WINS)
                   )
db.commit()

cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
for row in dfgd.fillna(0).itertuples():
    cursor.execute('''
                INSERT INTO details (PLAYER_ID,GAME_ID,FGM,FGA,FG3M,
                                    FG3A,PTS,PLUS_MINUS)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ''',
                   (row.PLAYER_ID,
                    row.GAME_ID,
                    row.FGM,
                    row.FGA,
                    row.FG3M,
                    row.FG3A,
                    row.PTS,
                    row.PLUS_MINUS
                    )

                   )

db.commit()

cursor.execute('''DELETE FROM details WHERE PLAYER_ID NOT IN(SELECT PLAYER_ID FROM players)''')
cursor.execute('''DELETE FROM details WHERE GAME_ID NOT IN(SELECT GAME_ID FROM games)''')

for row in dfb.itertuples():
    cursor.execute('''
                INSERT INTO belongs (TEAM_ID, PLAYER_ID, SEASON)
                VALUES (%s,%s,%s)
                ''',
                   (row.TEAM_ID,
                    row.PLAYER_ID,
                    row.SEASON)
                   )

db.commit()

cursor.execute('''DELETE FROM belongs WHERE PLAYER_ID NOT IN(SELECT PLAYER_ID FROM players)''')
cursor.execute('''DELETE FROM belongs WHERE TEAM_ID NOT IN(SELECT TEAM_ID FROM teams)''')
# Deleting values of PLAYER_ID and TEAM_ID in "belongs" that don't respect their referential constraints to "players" and "teams", respectively

for row in dfr.itertuples():
    cursor.execute('''
                INSERT INTO ranking (TEAM_ID,SEASON_ID,STANDINGSDATE,CONFERENCE,G,W,
                                     L,W_PCT)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ''',
                   (row.TEAM_ID,
                    row.SEASON_ID,
                    row.STANDINGSDATE,
                    row.CONFERENCE,
                    row.G,
                    row.W,
                    row.L,
                    row.W_PCT
                    )

                   )

db.commit()

cursor.execute('''DELETE FROM ranking WHERE TEAM_ID NOT IN(SELECT TEAM_ID FROM teams)''')

cursor.execute('''use nba_dataset''')

# QUERIES

# Fans as the sixth player
fans = '''SELECT ((SELECT count(*) 
		                    FROM games 
		                    WHERE HOME_TEAM_WINS = 1) / count(*) * 100) as WIN_PCT_HOME
                    FROM games'''

cursor.execute(fans)
fan_result = cursor.fetchall()
print("Win percentage of teams playing home", fan_result, "\n")

# A geographical crack
conf = '''SELECT count(*)/20 *100 as east_win_percentage
            FROM (SELECT R.SEASON_ID, R.CONFERENCE, R.W 
                    FROM ranking as R JOIN (SELECT R2.SEASON_ID, max(R2.W) as wins
                                            FROM ranking as R2
                                            Group by R2.SEASON_ID) as M on M.SEASON_ID = R.SEASON_ID and M.wins = R.W) as P
            WHERE CONFERENCE = "East"
'''

cursor.execute(conf)
conf_result = cursor.fetchall()
print("Percentage of teams with most wins per season belonging to the East conference", conf_result, "\n")

# "The GOAT": Highest scoring player of the team with the most wins

goat = '''SELECT F2.NAME, F2.points_final
                  FROM (SELECT P.NAME, max(F.points) as points_final, 
			                        rank() over (order by max(F.points) desc) as rnk
	                    FROM (SELECT d.PLAYER_ID as PLAYER_ID, sum(d.PTS) as points
			                  FROM details as d
			                  WHERE d.GAME_ID in (SELECT gg.GAME_ID
								                  FROM games as gg
								                  WHERE gg.SEASON = 2020
										                and ((gg.HOME_TEAM_ID in (SELECT R.TEAM_ID
																                  FROM ranking as R
																                  WHERE R.SEASON_ID = 2020 and R.W = (SELECT max(R1.W)
																									                  FROM ranking as R1
																									                  WHERE R1.SEASON_ID = 2020)))
										                or (gg.VISITOR_TEAM_ID in (SELECT R0.TEAM_ID
																                   FROM ranking as R0
																                   WHERE R0.SEASON_ID = 2020 and R0.W = (SELECT max(R2.W)
																										                 FROM ranking as R2
																										                 WHERE R2.SEASON_ID = 2020))))
								                  )
			                  Group by d.PLAYER_ID
			                  ) as F, players as P
						WHERE P.PLAYER_ID = F.PLAYER_ID
	                    Group by P.NAME
	                    ) as F2
                  where F2.rnk = 1
'''

cursor.execute(goat)
goat_result = cursor.fetchall()
print("Highest scoring player of the team with the most wins", goat_result, "\n")

# Luck or skill ?
luck = '''SELECT distinct t1.NICKNAME, W_PCT
          FROM ranking as r1, teams as t1
          WHERE r1.TEAM_ID in (
				  SELECT distinct VISITOR_TEAM_ID
				  FROM games as g1
                  WHERE PTS_home > 150 and g1.SEASON = 2019
                  )
				and r1.SEASON_ID = 2019
                and r1.TEAM_ID = t1.TEAM_ID
          UNION
          SELECT t2.NICKNAME, W_PCT
          FROM ranking as r2, teams as t2
          WHERE  r2.TEAM_ID in (
				   SELECT distinct HOME_TEAM_ID
				   FROM games as g2
                   WHERE PTS_away > 150 and g2.SEASON = 2019
                   )
				and r2.SEASON_ID = 2019
                and r2.TEAM_ID = t2.TEAM_ID
'''

cursor.execute(luck)
luck_result = cursor.fetchall()
print("Win percentages of teams having scored more than 150 points in one game in the 2019 season", luck_result, "\n")

# Snakes
snakes = '''SELECT distinct b.PLAYER_ID, p.NAME, count(*) as Number_Of_Teams
                  FROM belongs as b, players as p
                  WHERE p.PLAYER_ID = b.PLAYER_ID
                  group by b.PLAYER_ID, p.NAME
                  order by Number_Of_Teams desc
                  limit 10
'''

cursor.execute(snakes)
snakes_result = cursor.fetchall()
print("Players who changed teams the most", snakes_result, "\n")

cursor.close()
db.close()
