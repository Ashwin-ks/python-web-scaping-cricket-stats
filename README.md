# Build Webscraper to scrape Cricket Statistics and Create/deploy WebApp

## Description
Create a webscraping tool which allows us to scrape a website, parse that data, and create a webapp that anyone with a browser can visit to view data in formatted manner. We have created this tool to scrape Cricket Players Statistics from espncricinfo website along with information of players from all leading nations playing and store the data in Sqlite database with necessary schema created

Utilized Python for webscraping and parsing with various modules including BeautifulSoup,requests,regex,sqlite3,argparse etc. and used microservices web framework Flask for creating and deployinh Webapp.

The functions defined within "cricket_parser_v2.py" performs the following functions:-

- get_db_conn : Get sqlite database connection object
- get_country_details : Extract countries details and respective Id for each country by parsing Url of respective countries selected and insert the details into sqlite "Countries" table.
- get_player_details : For each of the extracted countries dynamically create Url for extracting all players to have capped in ODI/T20 matches and parse for player names and player id's and odi_cap,t20_cap for appearance in match types.
- get_player_statistics: For selected match type(ODI/T20) and type of action(Bowling/Batting) dynamically create url for extracting statistics for each players referring the previously extracted and saved countries,player id's from database tables.Use this to parse the data from website and save it in respective tables.


Used BeautifulSoup and requests module with best practice logging and argument parsing mechanism to efficiently scrape player batting and bowling statistics from  espncricinfo website for all players from different countries in their entire playing span ,a light-weight sqlite database is used to store the information fetched for further querying and analyis. Create and deploy webapp for easier access via browser with url endpoints.    

## Usage
This tool provides user the flexibility to choose the countries of whose player statistics are to be scraped and stored in database along with either choosing ODI/T20 or both.     

> **usage**:  cricket_parser_v2.py [-h] [-d DATABASENAME] [-t TYPEOFMATCH]
                            [-c [COUNTRIES [COUNTRIES ...]]]    

> Usage with Default values:- Scrapes all players statistics(bowling and fielding) from major 11 playing nations in both ODI and T20 format        
example: python cricket_parser_v2.py       
-d :'CRICKET_PERF'   (default) 
-t :'ALL'            (default)
-c :'ALL'            (default)

> Usage with Custom entries:- Scrapes all players statistics(bowling and fielding) from selected countries and selected playing format   
example: python cricket_parser_v2.py -d cricket_india_pakistan_stats -t ODI -c [india,pakistan]    
-d : <any name without spaces>    
-t : ODI/T20/ALL    
-c [australia,bangladesh,england,india,new-zealand,pakistan,south-africa,sri-lanka,west-indies,zimbabwe,afghanistan] ##select based on requirement in list    
                         
The execution of above command would scrape the website for batting/bowling stats in ODI of all players from india and pakistan and parse and store results in 'cricket_india_pakistan_stats.sqlite' database which could be queried using below table structure.

The sqlite database would have the below table structure where the scraped data is parsed and stored in a normalized way:

> **Countries**  > country_id PRIMARY KEY,country     

> **Players**  > country_id ,player_id  UNIQUE,player ,odi_cap ,t20_cap     

> **Batting_Stats_Odi**  > player ,playing_span ,matches_played ,
                    innings_batted ,not_outs , runs_scored ,highest_innings_score ,batting_average ,
                    balls_faced ,batting_strike_rate ,hundreds_scored ,scores_between_50_and_99 ,
                    ducks_scored ,boundary_fours ,boundary_sixes     

> **Bowling_Stats_Odi** > player ,playing_span ,matches_played ,innings_bowled_in ,
                    overs_bowled ,balls_bowled ,runs_conceded ,maidens_earned ,wickets_taken , 
                    best_bowling_in_an_innings ,bowling_average ,economy_rate ,bowling_strike_rate ,
                    four_wkts_exactly_in_an_inns ,five_wickets_in_an_inns     

> **Batting_Stats_T20** > player ,playing_span ,matches_played ,
                    innings_batted ,not_outs , runs_scored ,highest_innings_score ,batting_average ,
                    balls_faced ,batting_strike_rate ,hundreds_scored ,scores_between_50_and_99 ,ducks_scored ,
                    boundary_fours ,boundary_sixes     

> **Bowling_Stats_T20** > player , playing_span ,matches_played ,innings_bowled_in ,
                    overs_bowled ,balls_bowled ,runs_conceded ,maidens_earned ,wickets_taken , 
                    best_bowling_in_an_innings ,bowling_average ,economy_rate ,bowling_strike_rate ,
                    four_wkts_exactly_in_an_inns ,five_wickets_in_an_inns     

                         
Once the parser completes execution we can query the required information for further analyis referring the table structure provided above.    


## Web App

Run: python app.py 

Once it is deployed we can access the details via webbrowser, few examples given below:
- Get all the Countries 
> http://localhost:5000/api/v2/countries/all
- Get all players information from selected country and match type
> http://localhost:5000/api/v2/countries?name=india&match_type=t20
- Get all statistics based on selected parameters
> http://localhost:5000/api/v2/get_stats/countries?name=india&play_type=Batting&match_type=t20


## Required modules 
sqlite3    
requests    
BeautifulSoup    
argparse    
logging    
Flask    
Pandas    
