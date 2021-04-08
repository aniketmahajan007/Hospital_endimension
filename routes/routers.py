from main import app
from flask import request
import psycopg2
import json
from datetime import datetime

POSTGRESQL_URI = "postgresql://uljbpurpmwvud4p69b9d:VyWZNAaoLnnuZI5VU3eq@b2hpkj8c9mjidilcresw-postgresql.services" \
                 ".clever-cloud.com:5432/b2hpkj8c9mjidilcresw"


@app.route('/')
def home():
    return "Bad Request"


@app.route('/Patient', methods=['GET'])
def Patient():
    connection = psycopg2.connect(POSTGRESQL_URI)
    user = request.args.get("user")
    password = request.args.get("pass")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM patient WHERE username::text = %s AND password = %s", (user, password))
            result = cursor.fetchall()
    connection.close()
    return json.dumps(result), 200, {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}


@app.route('/staff', methods=['GET'])
def Staff():
    connection = psycopg2.connect(POSTGRESQL_URI)
    user = request.args.get("user")
    password = request.args.get("pass")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hos_admin WHERE username::text = %s AND pass = %s", (user, password))
            result = cursor.fetchall()
    connection.close()
    return json.dumps(result), 200, {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}


@app.route('/all_appointment', methods=['GET'])
def all_appointment():
    connection = psycopg2.connect(POSTGRESQL_URI)
    date_n = str(datetime.today().strftime('%Y-%m-%d'))
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT fname,lname,city,state,mob_number,areason,slotstart,slotend FROM appointment WHERE appointdate::text = %s", [date_n])
            result = cursor.fetchall()
    connection.close()
    print(result)
    return json.dumps(result), 200, {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}


@app.route('/appointment', methods=['POST'])
def appointment():
    form_data = request.get_json()
    connection = psycopg2.connect(POSTGRESQL_URI)
    user = form_data["user"]
    fname = form_data["fname"]
    lname = form_data["lname"]
    areason = form_data["areason"]
    state = form_data["state"]
    city = form_data["city"]
    adate = form_data["adate"]
    anumber = form_data["anumber"]
    slotstart = "10:00"
    slotend = "10:30"
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pid FROM patient WHERE username::text = %s", [user])
            result = cursor.fetchall()
    pid = result[0][0]
    adate = adate[0:10]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pid FROM appointment WHERE appointdate::text = %s AND pid=%s", (adate, pid))
            result = cursor.fetchall()
    if len(result) > 0:
        connection.close()
        return json.dumps({"status": "already"}), 200, {'Access-Control-Allow-Origin': '*',
                                                        'Content-Type': 'application/json'}
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO appointment (pid,fname,lname,state,city,appointdate,mob_number,slotstart,slotend,areason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (pid, fname, lname, state, city, adate, anumber, slotstart, slotend, areason))
    connection.close()
    return json.dumps({"status": "success"}), 200, {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}

@app.route('/user_appointment', methods=['GET'])
def user_appointment():
    connection = psycopg2.connect(POSTGRESQL_URI)
    user = request.args.get("user")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pid FROM patient WHERE username::text = %s", [user])
            result = cursor.fetchall()
    pid = str(result[0][0])
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT fname,lname,city,state,mob_number,areason,appointdate FROM appointment WHERE pid::text = %s",
                [pid])
            result = cursor.fetchall()
    connection.close()
    print(result)
    return json.dumps(result), 200, {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}