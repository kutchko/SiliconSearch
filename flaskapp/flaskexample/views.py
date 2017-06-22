from flask import render_template
from flask import request
from flask import Response
from flaskexample import app
import pymysql.cursors
import pandas as pd
import json

user = 'kkutchko'
passwd = 'password'
database = 'metro_areas'

connection = pymysql.connect(host='localhost',
        user=user,
        password=passwd,
        db=database,
        cursorclass=pymysql.cursors.DictCursor)




@app.route('/')
@app.route('/index')
@app.route('/input')
def cities_input():
    with connection.cursor() as cursor:
        cities_query = "select distinct(CBSA) from metro_data";
        cursor.execute(cities_query)
        rows = cursor.fetchall()
        
        cities = [r['CBSA'] for r in rows]

        return render_template('input.html', cities = cities, nomatch = False)


@app.route('/output')
def cities_output():
    recommended_city = ''
    city_data_json = ''
    city = request.args.get('city')

    t = request.args.get('good_for_tech')
    c = request.args.get('cheaper')
    d = request.args.get('diversity')

    query1 = "select * from metro_data where CBSA = %s"
    query2 = "select CBSA from metro_data" 
    with connection.cursor() as cursor:
        cursor.execute(query1, (city) )
    city1_row = cursor.fetchone()
    city2_row = None
    subqueries = []
    if c or d:
        row = []
        if c:
            subqueries.append("MedianRent < %s" % city1_row['MedianRent'])
        if d:
            subqueries.append("DiversityIndex > %s" % city1_row['DiversityIndex'])
    if t:
        subqueries.append("GoodForTech = 'Yes'")
    if subqueries:
        query2 += " where "
        query2 += " and ".join(subqueries)
    
    query3 = "select * from city_distance where CBSA1 = %s and CBSA2 in (" +\
        query2 + ") order by distance"
    with connection.cursor() as cursor:
        cursor.execute(query3, (city) )

        # if no city matches criteria
        if not cursor.rowcount:
            cities_query = "select distinct(CBSA) from metro_data";
            cursor.execute(cities_query)
            rows = cursor.fetchall()
            
            cities = [r['CBSA'] for r in rows]
            return render_template('input.html', cities = cities, nomatch=True)
        # if at least one city does match criteria
        else:
            df = pd.DataFrame(cursor.fetchall())

            row = df.iloc[0, ]
            recommended_city = row['CBSA2']

            cursor.execute(query1, recommended_city)
            city2_row = cursor.fetchone()
            city_data_json = df.to_json(orient='records')

    return render_template('output.html',
        reccity = recommended_city,
        city1_row = city1_row,
        city2_row = city2_row,
        city_data_json = city_data_json)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')






