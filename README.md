## Cricket Statistics WebScraping using Python 

The webscraping tool uses BeautifulSoup and requests module with best practice logging and argument parsing mechanism to efficiently scrape player batting and bowling statistics from  espncricinfo website for all players from different countries in their entire playing span ,a light-weight sqlite database is used to store the information fetched for further querying and analyis.    

This tool provides user the flexibility to choose the countries of whose player statistics are to be scraped and stored in database along with either choosing ODI/T20 or both.     

usage: cricket_parser_v2.py [-h] [-d DATABASENAME] [-t TYPEOFMATCH]
                            [-c [COUNTRIES [COUNTRIES ...]]]    

Usage with Default values:- Scrapes all players statistics(bowling and fielding) from major 11 playing nations in both ODI and T20 format        
example: python cricket_parser_v2.py       
-d :'CRICKET_PERF'    
-t :'ALL'    
-c :'ALL'     

Usage with Custom entries:- Scrapes all players statistics(bowling and fielding) from selected countries and selected playing format    
example: python cricket_parser_v2.py -d cricket_india_pakistan_stats -t ODI -c [india,pakistan]    
-d : <any name without spaces>    
-t : ODI/T20/ALL    
-c [australia,bangladesh,england,india,new-zealand,pakistan,south-africa,sri-lanka,west-indies,zimbabwe,afghanistan] ##select based on requirement in list    
                            


The execution of above command would scrape the website for batting/bowling stats in ODI of all players from india and pakistan and parse and store results in 'cricket_india_pakistan_stats.sqlite' database which could be queried using below table structure.

The sqlite database would have the below table structure where the scraped data is parsed and stored in a normalized way:

Countries  > country_id PRIMARY KEY,country     

Players  > country_id ,player_id  UNIQUE,player ,odi_cap ,t20_cap     

Batting_Stats_Odi  > player ,playing_span ,matches_played ,
                    innings_batted ,not_outs , runs_scored ,highest_innings_score ,batting_average ,
                    balls_faced ,batting_strike_rate ,hundreds_scored ,scores_between_50_and_99 ,
                    ducks_scored ,boundary_fours ,boundary_sixes     
       
Bowling_Stats_Odi > player ,playing_span ,matches_played ,innings_bowled_in ,
                    overs_bowled ,balls_bowled ,runs_conceded ,maidens_earned ,wickets_taken , 
                    best_bowling_in_an_innings ,bowling_average ,economy_rate ,bowling_strike_rate ,
                    four_wkts_exactly_in_an_inns ,five_wickets_in_an_inns     
                    
Batting_Stats_T20 > player ,playing_span ,matches_played ,
                    innings_batted ,not_outs , runs_scored ,highest_innings_score ,batting_average ,
                    balls_faced ,batting_strike_rate ,hundreds_scored ,scores_between_50_and_99 ,ducks_scored ,
                    boundary_fours ,boundary_sixes     
                    
Bowling_Stats_T20 > player , playing_span ,matches_played ,innings_bowled_in ,
                    overs_bowled ,balls_bowled ,runs_conceded ,maidens_earned ,wickets_taken , 
                    best_bowling_in_an_innings ,bowling_average ,economy_rate ,bowling_strike_rate ,
                    four_wkts_exactly_in_an_inns ,five_wickets_in_an_inns     

                         
Once the parser completes execution we can query the required information for further analyis referring the table structure provided above.    

Required modules:-    
sqlite3
requests
BeautifulSoup
argparse
logging