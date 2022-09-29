from flask import Flask, redirect, url_for, request, jsonify
from blockchain import *
from user import *
from main import *
import json

app = Flask(__name__)
votechains = {}
cursor = ''

@app.route('/mine',methods = ['POST'])
def mine():
    eid = request.json['election_id']
    result = votechains[eid].mine_block()
    return str(result)

@app.route('/registeruser', methods = ['POST'])
def register_user():
    voter_id = request.json['vid']
    credentials = request.json['password']
    name = request.json['name']
    dept = request.json['dept']
    year = request.json['year']
    return str(create_user(cursor, user(voter_id, credentials, name, dept, year)))

@app.route('/signin', methods = ['POST'])
def signin():
    voter_id = request.json['vid']
    credentials = request.json['password']
    return str(authenticate_user(cursor, voter_id, credentials))

@app.route('/castvote', methods = ['POST'])
def castvote():
    eid = request.json['election_id']
    voter_id = request.json['vid']
    credentials = request.json['credentials']
    candidate_id = request.json['candidate_id']
    if(authenticate_user(cursor, voter_id, credentials) == 1):
        return str(cast_vote(cursor, eid, voter_id, candidate_id,str(datetime.datetime.now())))
    else:
        return -1

@app.route('/profile', methods = ['POST'])
def get_user_profile():
    voter_id = request.json['vid']
    credentials = request.json['credentials']
    if(authenticate_user(cursor, voter_id, credentials) == 1):
        return jsonify(get_user(cursor, voter_id))
    else:
        return -1

@app.route('/registercandidate', methods = ['POST'])
def register_candidate():
    candidate_id = request.json['candidate_id']
    election_id = request.json['election_id']
    name = request.json['name']
    dept = request.json['dept']
    year = request.json['year']
    return str(create_candidate(cursor, election_id, candidate_id, name, dept, year))

@app.route('/createelection', methods = ['POST'])
def create_election():
    organisation = request.json['organisation']
    election_date = request.json['election_date']
    post = request.json['post']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    remark = request.json['remark']
    return str(create_election(cursor, organisation, post, election_date, start_time, end_time, remark))

@app.route('/getcandidates', methods = ['POST'])
def get_candidates():
    eid = request.json['election_id']
    print(eid)
    return jsonify({"result": list_candidates(cursor, eid)})
     
@app.route('/active',methods = ['POST'])
def active():
    voter_id = request.json['voter_id']
    return jsonify({"result":active_elections(cursor, voter_id)})


if __name__ == '__main__':
    f = open("db.key","r")
    usr = f.readline()[:-1]
    password = f.readline()[:-1]
    host = f.readline()[:-1]
    port = f.readline()[:-1]
    database = f.readline()
    connection = psycopg2.connect(user=usr,
                                password=password,
                                host=host,
                                port=port,
                                database=database)
    connection.autocommit = True

    cursor = connection.cursor()
    print(connection.get_dsn_parameters(), "\n")
    
    votechains["p2pr230924"] = votechain(cursor, "public", "p2pr230924")
    app.run()
