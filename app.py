from flask import Flask, abort, jsonify, request
import json
import requests
import time
#from customException import ApplicationException
from cricket_parser_v2 import get_db_conn
import pandas as pd
app = Flask(__name__)
dbname = 'CRICKET_PERF'
@app.route('/')
def index():
    return "<h1>Cricket Parser :)</h1>"
   
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
    
@app.route('/api/v2/countries/all', methods=['GET'])
def get_all_countries():
  
    with get_db_conn(dbname) as sqlite_conn:
        cur = sqlite_conn.cursor()
    cur.execute('''select * from Countries; ''')
    
    s = "<table style='border:1px solid red'>"  
    col_name = [field[0] for field in cur.description]
    s = s + "<tr>" 
    for y in col_name:
        
        s = s + " <td>" + str(y) + "</td>" 
    s = s + "<tr>"    
    for row in cur:  
        s = s + "<tr>"  
        for x in row:  
            s = s + "<td>" + str(x) + "</td>"  
        s = s + "</tr>"  
    
    return "<html><body>" + s + "</body></html>"  

    
@app.route('/api/v2/countries', methods=['GET'])
def get_country_players():
    query_parameters = request.args
    #http://api.example.com/books?author=Ursula+K.+Le Guin&published=1969&output=xml

    country_name = query_parameters.get('name')
    match_type = query_parameters.get('match_type')
    
    query = "select a.country_id,b.country,a.player_id,a.player,a.odi_cap,a.t20_cap from Players a join Countries b on a.country_id=b.country_id where"
    to_filter = []

    if country_name:
        query += ' b.country=? AND'
        to_filter.append(country_name)
    if match_type:
        query += ' a.{}_cap=? AND'.format(match_type)
        to_filter.append('Y')
    if not (id or published or author):
        return page_not_found(404)
    
    query = query[:-4] + ';'
        
    with get_db_conn(dbname) as sqlite_conn:
        cur = sqlite_conn.cursor()
    cur.execute(query, to_filter)
    s = "<table style='border:1px solid red'>"  
    col_name = [field[0] for field in cur.description]
    s = s + "<tr>" 
    for y in col_name:
        
        s = s + " <td>" + str(y) + "</td>" 
    s = s + "<tr>"    
    for row in cur:  
        s = s + "<tr>"  
        for x in row:  
            s = s + "<td>" + str(x) + "</td>"  
        s = s + "</tr>"  
    
    return "<html><body>" + s + "</body></html>"  
    
@app.route('/api/v2/get_stats/countries', methods=['GET'])
def get_players_stats():
    query_parameters = request.args
    #http://api.example.com/books?author=Ursula+K.+Le Guin&published=1969&output=xml

    country_name = query_parameters.get('name')
    play_type = query_parameters.get('play_type')
    match_type = query_parameters.get('match_type')
    
    
    query = "select * from {}_Stats_{} where player in (select a.player from Players a join Countries b on a.country_id=b.country_id where".format(play_type,match_type)
    to_filter = []

    if country_name:
        query += ' b.country=? AND'
        to_filter.append(country_name)
    if match_type:
        query += ' a.{}_cap=? AND'.format(match_type)
        to_filter.append('Y')
    if not (id or published or author):
        return page_not_found(404)
    
    query = query[:-4] + ');'
        
    with get_db_conn(dbname) as sqlite_conn:
        cur = sqlite_conn.cursor()
    cur.execute(query, to_filter)
    s = "<table style='border:1px solid red'>"  
    col_name = [field[0] for field in cur.description]
    s = s + "<tr>" 
    for y in col_name:
        
        s = s + " <td>" + str(y) + "</td>" 
    s = s + "<tr>"    
    for row in cur:  
        s = s + "<tr>"  
        for x in row:  
            s = s + "<td>" + str(x) + "</td>"  
        s = s + "</tr>"  
    
    return "<html><body>" + s + "</body></html>"  
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)