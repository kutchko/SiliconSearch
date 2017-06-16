from flask import render_template
from flask import request
from flaskexample import app
import pymysql.cursors
import pandas as pd

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
    with connection.cursor() as cursor:  # TODO move this block to another file
        data_query = "select t1.StateFIPS, t1.CountyFIPS, t1.CBSA, t2.* " +\
            "from metro_counties t1 left join metro_data t2 on t1.CBSA=t2.CBSA"
        cursor.execute(data_query)
        df = pd.DataFrame(cursor.fetchall())
        dfseries = df['StateFIPS'] * 1000 + df['CountyFIPS']
        df['id'] = dfseries.apply(lambda x: "%05d" % x)
        df.to_csv("flaskexample/static/county_data.tsv", sep="\t")

    with connection.cursor() as cursor:
        cities_query = "select distinct(CBSA) from metro_data";
        cursor.execute(cities_query)
        rows = cursor.fetchall()
        
        cities = [r['CBSA'] for r in rows]

        return render_template('input.html', cities = cities)

@app.route('/map')
def mappage():
    return render_template('map.html')

@app.route('/output')
def cities_output():
    recommended_city = ''
    city = request.args.get('city')

    t = request.args.get('good_for_tech')
    c = request.args.get('cheaper')
    d = request.args.get('diversity')

    query2 = "select CBSA from metro_data" 
    subqueries = []
    if c or d:
        query1 = "select * from metro_data where CBSA = %s"
        row = []
        with connection.cursor() as cursor:
            cursor.execute(query1, (city) )
            row = cursor.fetchone()

            if c:
                subqueries.append("MedianRent < %s" % row['MedianRent'])
            if d:
                subqueries.append("DiversityIndex > %s" % row['DiversityIndex'])
    if t:
        subqueries.append("GoodForTech = 'Yes'")
    if subqueries:
        query2 += " where "
        query2 += " and ".join(subqueries)
    
    query3 = "select * from city_distance where CBSA1 = %s and CBSA2 in (" +\
        query2 + ") order by distance limit 1"
    with connection.cursor() as cursor:
        cursor.execute(query3, (city) )
        if not cursor.rowcount:
            recommended_city = 'No cities found!'
        else:
            row = cursor.fetchone()
            recommended_city = row['CBSA2']


    return render_template('output.html',
        reccity = recommended_city)



@app.route('/db')
def birth_page():
    sql_query = """
                select * from city_distance where CBSA1 like '%St. George, UT%';
                """
    query_results = pd.read_sql_query(sql_query, connection)
    results = ""
    for i in range(0, 10):
        results += query_results.iloc[i]['CBSA2']
        results += "<br>"
    return results

@app.route('/db_fancy')
def birth_page_fancy():
    sql_query = """
                select * from city_distance where CBSA1 like '%St. George, UT%';
                """
    query_results = pd.read_sql_query(sql_query, connection)
    res = []
    for i in range(0, query_results.shape[0]):
        res.append(dict(index = i,
                        attendant = query_results.iloc[i]['CBSA2'],
                        birth_month = query_results.iloc[i]['distance']))
    return render_template('starter-template.html', births = res)






