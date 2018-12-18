## Cricket Statistics WebScraping using Python 

The webscraping tool uses BeautifulSoup and requests module with best practice logging and argument parsing mechanism to efficiently scrap player batting and bowling statistics from  espncricinfo website for all players from different countries in their entire playing span ,a light-weight sqlite database is used to store the information fetched for further querying and analyis.

This tool provides user the flexibility to choose the countries of whose player statistics are to be scraped and stored in database along with either choosing ODI/T20 or both.

usage: cricket_parser_v2.py [-h] [-d DATABASENAME] [-t TYPEOFMATCH]
                            [-c [COUNTRIES [COUNTRIES ...]]]
                            
Valid entries:- 
-d : <any name without spaces>
-t : ODI/T20/ALL
-c [australia,bangladesh,england,india,new-zealand,pakistan,south-africa,sri-lanka,west-indies,zimbabwe,afghanistan] ##select based on requirement in list
                            
example: python cricket_parser_v2.py -d cricket_india_pakistan_stats -t ODI -c [india,pakistan]

The execution of above command would scrape the website for batting/bowling stats in ODI of all players from india and pakistan and parse and store results in 'cricket_india_pakistan_stats.sqlite' database which could be queried using below table structure.

The sqlite database would have the below table structure where the scraped data is parsed and stored in a normalized way:

Countries  > country_id INTEGER PRIMARY KEY,country TEXT

Players  > country_id INTEGER,player_id INTEGER UNIQUE,player TEXT,odi_cap TEXT,t20_cap TEXT

Batting_Stats_Odi  > player TEXT,playing_span TEXT,matches_played TEXT,
                    innings_batted TEXT,not_outs TEXT, runs_scored TEXT,highest_innings_score TEXT,batting_average TEXT,
                    balls_faced TEXT,batting_strike_rate TEXT,hundreds_scored TEXT,scores_between_50_and_99 TEXT,
                    ducks_scored TEXT,boundary_fours TEXT,boundary_sixes TEXT
       
Bowling_Stats_Odi > player TEXT,playing_span TEXT,matches_played TEXT,innings_bowled_in TEXT,
                    overs_bowled TEXT,balls_bowled TEXT,runs_conceded TEXT,maidens_earned TEXT,wickets_taken TEXT, 
                    best_bowling_in_an_innings TEXT,bowling_average TEXT,economy_rate TEXT,bowling_strike_rate TEXT,
                    four_wkts_exactly_in_an_inns TEXT,five_wickets_in_an_inns TEXT
                    
Batting_Stats_T20 > player TEXT,playing_span TEXT,matches_played TEXT,
                    innings_batted TEXT,not_outs TEXT, runs_scored TEXT,highest_innings_score TEXT,batting_average TEXT,
                    balls_faced TEXT,batting_strike_rate TEXT,hundreds_scored TEXT,scores_between_50_and_99 TEXT,ducks_scored TEXT,
                    boundary_fours TEXT,boundary_sixes TEXT
                    
Bowling_Stats_T20 > player TEXT, playing_span TEXT,matches_played TEXT,innings_bowled_in TEXT,
                    overs_bowled TEXT,balls_bowled TEXT,runs_conceded TEXT,maidens_earned TEXT,wickets_taken TEXT, 
                    best_bowling_in_an_innings TEXT,bowling_average TEXT,economy_rate TEXT,bowling_strike_rate TEXT,
                    four_wkts_exactly_in_an_inns TEXT,five_wickets_in_an_inns TEXT

                         
Once the parser completes execution we can query the required information for further analyis referring the table structure provided above.

Required modules:-
sqlite3
requests
BeautifulSoup
argparse
logging