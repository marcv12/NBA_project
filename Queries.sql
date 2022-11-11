USE nba_dataset;

# FANS AS THE SIXTH PLAYER

SELECT ((SELECT count(*) 
	FROM games 
	WHERE HOME_TEAM_WINS = 1) / count(*) * 100) as WIN_PCT_HOME
FROM games;


# Geographical crack

SELECT count(*)/20 *100 as east_win_percentage
FROM (SELECT R.SEASON_ID, R.CONFERENCE, R.W 
      FROM ranking as R JOIN (SELECT R2.SEASON_ID, max(R2.W) as wins
                              FROM ranking as R2
                              Group by R2.SEASON_ID) as M on M.SEASON_ID = R.SEASON_ID and M.wins = R.W) as P
WHERE CONFERENCE = "East";


# THE GOAT

SELECT F2.NAME, F2.points_final
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
where F2.rnk = 1;


#Luck or skill
select distinct t1.NICKNAME, W_PCT
from ranking as r1, teams as t1
where r1.TEAM_ID in (
				  select distinct VISITOR_TEAM_ID
				  from games as g1
                  where PTS_home > 150 and g1.SEASON = 2019
                  )
				and r1.SEASON_ID = 2019
                and r1.TEAM_ID = t1.TEAM_ID
union
select t2.NICKNAME, W_PCT
from ranking as r2, teams as t2
where  r2.TEAM_ID in (
				   select distinct HOME_TEAM_ID
				   from games as g2
                   where PTS_away > 150 and g2.SEASON = 2019
                   )
				and r2.SEASON_ID = 2019
                and r2.TEAM_ID = t2.TEAM_ID;


#snakes
select distinct b.PLAYER_ID, p.NAME, count(*) as Number_Of_Teams
from belongs as b, players as p
where p.PLAYER_ID = b.PLAYER_ID
group by b.PLAYER_ID, p.NAME
order by Number_Of_Teams desc
limit 10;
