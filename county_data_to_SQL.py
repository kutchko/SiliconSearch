#!/usr/bin/env python3


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


# read CSV files
county_data = pd.read_csv('national_county.csv',
    names = ['State', 'StateFIPS', 'CountyFIPS', 'CountyName', 'X'])
metro_counties = pd.read_csv('politan_areas.csv', encoding='latin-1')


# put into SQL tables
drop1_cmd = "drop table if exists county_data";
drop2_cmd = "drop table if exists metro_counties";

create1_cmd = "create table county_data (" +\
    "StateFIPS int(3), " +\
    "CountyFIPS int(4), " +\
    "State varchar(3), " +\
    "CountyName varchar(64), " +\
    "primary key (StateFIPS, CountyFIPS))"
create2_cmd = "create table metro_counties (" +\
    "StateFIPS int(3), " +\
    "CountyFIPS int(4), " +\
    "CBSA varchar(64), " +\
    "AreaType varchar(64), " +\
    "StateName varchar(64), " +\
    "CountyName varchar(64), " +\
    "primary key (StateFIPS, CountyFIPS))"

insert1_cmd = "insert into county_data " +\
    "(StateFIPS, CountyFIPS, State, CountyName) " +\
    "values (%s, %s, %s, %s)"

insert2_cmd = "insert into metro_counties " +\
    "(StateFIPS, CountyFIPS, CBSA, AreaType, StateName, CountyName) " +\
    "values (%s, %s, %s, %s, %s, %s)"

try:
    with connection.cursor() as cursor:
        cursor.execute(drop1_cmd)
        cursor.execute(drop2_cmd)
        cursor.execute(create1_cmd)
        cursor.execute(create2_cmd)

        for idx, line in county_data.iterrows():
            cursor.execute(insert1_cmd, (line['StateFIPS'], line['CountyFIPS'],
                line['State'], line['CountyName']))
        for idx, line in metro_counties.iterrows():
            cursor.execute(insert2_cmd, (line['FIPS State Code'], line['FIPS County Code'],
                line['CBSA Title'], line['Metropolitan/Micropolitan Statistical Area'],
                line['State Name'], line['County/County Equivalent']))

        # save city data to TSV
        data_query = "select t1.StateFIPS, t1.CountyFIPS, t1.CBSA, t2.* " +\
            "from metro_counties t1 left join metro_data t2 on t1.CBSA=t2.CBSA"
        cursor.execute(data_query)
        df = pd.DataFrame(cursor.fetchall())
        dfseries = df['StateFIPS'] * 1000 + df['CountyFIPS']
        df['id'] = dfseries.apply(lambda x: "%05d" % x)
        df.to_csv("flaskapp/flaskexample/static/county_data.tsv", sep="\t")

finally:
    connection.commit()
    connection.close()



