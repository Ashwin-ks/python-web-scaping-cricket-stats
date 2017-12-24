# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 16:03:22 2017

@author: Ashwin
"""

import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import csv
import logging
import datetime

def get_db_conn():
    '''Returns sqlite db connection'''
    conn=sqlite3.connect('Cricket.sqlite')
    return conn

# def db_execute(conn,query):
    # '''executes provided query and commits the connection'''
    # cur=conn.cursor()
    # cur.execute(query)
    # conn.commit()

def get_country_details(country_links):
    
    for country_link in country_links:
        country = country_link.text
        country_id=country_link.get('href').split('/')[-1].split('.')[0]
        cur.execute('INSERT OR IGNORE INTO Countries (country_id,country) VALUES (?,?)',(country_id,country))
    conn.commit()
    
def get_player_details(country_ids):
    
    for cid in country_ids:
        squad_url='http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/squad/'+str(cid)+'.html'
        squad_page=requests.get(squad_url)
        soup1=BeautifulSoup(squad_page.text,"html.parser")
        player_links=soup1.findAll('a', href=re.compile('/icc-cricket-world-cup-2015/content/player/'))
        for i in player_links:
            if i.text:
                player_id=player_id=i.get('href').split('/')[-1].split('.')[0]
                player=i.text.strip()
                cur.execute('INSERT OR IGNORE INTO Players (country_id,player_id,player) VALUES (?,?,?)',(cid,player_id,player))
    conn.commit()

def get_player_statistics(action,play_list):

    for play in play_list:
        pid=play[2]
        country_name=play[1]
        player_name=play[3]
        stats_url='http://stats.espncricinfo.com/ci/engine/player/'+str(pid)+'.html?class=2;template=results;type='+str(action)+';view=innings;year='+str(year)
        stats_page=requests.get(stats_url)
        soup2=BeautifulSoup(stats_page.text,"html.parser")
        stats=soup2.findAll(text='filtered')[0].findParents('tr')[0].findAll("td")
        if action=="bowling":
            check=[3,4,6,5,7,12,13]
        else:
            check=[4,13,12,11,10,9,7,2]
        results=[]
        for i in check:
            try:
                results.append(float(stats[i].get_text()))
            except:
                results.append(0)
        if action=="batting":
            cur.execute('INSERT OR IGNORE INTO Batting_Stats (player,runs,sixes,fours,ducks,fifties,hundreds,balls_faced,innings)VALUES(?,?,?,?,?,?,?,?,?)',(player_name,results[0],results[1],results[2],results[3],results[4],results[5],results[6],results[7]))
        elif action=="bowling":
            cur.execute('INSERT OR IGNORE INTO Bowling_Stats (player,bowlinnings,overs,runsgiven,maidens,wickets,fourw,fivew)VALUES(?,?,?,?,?,?,?,?)',(player_name,results[0],results[1],results[2],results[3],results[4],results[5],results[6]))
    conn.commit()
        
if __name__ == "__main__":
    
    
    ##Setup logger
    
    logger=logging.getLogger(__name__)
    
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(config.log_format)
    
    file_handler = RotatingFileHandler(config.log_file,maxBytes=10485760,backupCount=20
    file_handler.setFormatter(formatter)
    
    logger.info("Process Start at {}".format(str(datetime.datetime.now())))
    print("Process Start at {}".format(str(datetime.datetime.now()))")
    
    ##main cricket series web page url
    url='http://www.espncricinfo.com/icc-cricket-world-cup-2015/content/current/series/509587.html'
    
    page=requests.get(url)
    
    ##Check if webpage is active
    if page.status_code == 200:
        print('Url status code indicates active status,proceeding with webscraping')
        logger.info('Url status code indicates active status,proceeding with webscraping')
    elif page.status_code == 404:
        print("Url provided doesn't exist,exiting with error code 404")
        logger.error("Url provided doesn't exist,exiting with error code 404")
        sys.exit(-1)
    
    ##Create sqlite db connection and create cursor object
    try:
        sqlite_conn = get_db_conn()
        print('Database connection established')
        logger.info('Database connection established')
    except Exception as e:
        print('Error obtaining database connection',e)
        logger.error('Error obtaining database connection',e)
        sys.exit(-1)
    
    cur = sqlite_conn.cursor()
    
    ##creating BeautifulSoup Object
    soup=BeautifulSoup(page.text,"html.parser")
    
    #print(soup.prettify())
    #display(HTML(page.text))
    
    country_links=soup.find_all('a',href=re.compile('/icc-cricket-world-cup-2015/content/squad/'))
    print(country_links)
    
    ##Create necessary tables in database for insertion of stats data
    cur.execute('''CREATE TABLE IF NOT EXISTS Countries
            (country_id INTEGER PRIMARY KEY,country TEXT)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Players
            (country_id INTEGER,player_id INTEGER UNIQUE,player TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Batting_Stats
                        (player TEXT,runs INTEGER,sixes INTEGER,fours INTEGER,ducks INTEGER,fifties INTEGER,hundreds INTEGER,balls_faced INTEGER,innings INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Bowling_Stats
                        (player TEXT,bowlinnings INTEGER ,overs INTEGER ,runsgiven INTEGER,maidens INTEGER,wickets INTEGER,fourw INTEGER,fivew INTEGER)''')
    
    logger.info('Created necessary tables in database')
    print('Database tables created')
    
    ##Fetch all participating countires name and id and store in database
    get_country_details(country_links)
    logger.info('Inserted data into Countries table')
    print('Inserted data into Countries table')
    
    
    ##Fetch countries id from database and store in list
    cur.execute('SELECT country_id FROM Countries')
    countryid_list=list()
    for row in cur:
        countryid_list.append(row[0])
    
    ##Fetch player details and insert into database
    get_player_details(countryid_list)
    logger.info('Inserted data into Players table')
    print('Inserted data into Players table')
    
    ##select country id,name and player id,name from database
    cur.execute('select a.country_id,a.country,b.player_id,b.player from Countries a,Players b where a.country_id=b.country_id')
    play_list=list()
    for row in cur:
        play_list.append(row)
        
    #play_action=['batting','bowling']
    
    year=2015 ##2015 worldcup
    
    ##get batting and bowling statistics for each player in each country and store in database for further querying
    for action in ('batting','bowling'):
        get_player_statistics(action,play_list)
    
    logger.info('Successfully collected Player bowling and batting statistics and stored in database')
    print('Successfully collected Player bowling and batting statistics and stored in database')
    
    




