import psycopg2
import datetime
from user import *
from psycopg2 import Error
from blockchain import *

def close_connection(cursor,connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

def query(cursor,cmd):
    try:
        cursor.execute(cmd)
    except (Exception, Error) as error:
        print("Error while Executing Command(", cmd, ")\nError: ", error)

def create_user(cursor, user):
    cmd = "insert into users(voter_id, credentials, name, dept, year) values ( \'" + user.vid + "\', \'" + user.credentials + "\', \'" 
    cmd += user.name + "\', \'" + user.dept + "\', " + str(user.year) + ");"
    try:
        query(cursor,cmd)
        return 1
    except (Exception, Error) as error:
        print("Error: ", error)
        return 0

def authenticate_user(cursor, vid, credentials):
    cmd = "select * from users where voter_id = \'" + vid + "\';" 
    try:
        print(cmd)
        query(cursor,cmd)
    except (Exception, Error) as error:
        print("Error: ", error)
        return 0
    result = cursor.fetchone()
    if(result):
        if(result[1] == credentials):
            return 1
        else:
            return -1 #Incorrect Password
    else:
        return -2 #User Does not Exist

def get_user(cursor, vid):
    cmd = "select * from users where voter_id = \'" + vid + "\';" 
    try:
        query(cursor,cmd)
    except (Exception, Error) as error:
        print("Error: ", error)
        return 0
    result = cursor.fetchone()
    if(result):
        user_data = {"name": result[2], "dept": result[3], "year": result[4]}
        print(user_data)
        return user_data
    else:
        return -1


def create_election(cursor, organisation, post, election_date, start_time, end_time, remark = ""):
    election_id = organisation[:2] + post[:2] + election_date[:2] + election_date[3:5] + election_date[8:] 
    election_id = election_id.lower()
    cmd = "insert into elections values(\'"+ election_id +"\', \'" + organisation + "\', \'" + post + "\', to_date( \'" + election_date + "\', \'DD/MM/YYYY \'), \'"
    cmd += start_time + "\', \'" + end_time + "\', \'" + remark + "\');"
    query(cursor,cmd)

    cmd = "create table " + election_id + """_electoralroll(
    voter_id varchar(15) not null primary key,
    vote_casted boolean default 'false',
    foreign key(voter_id) references users(voter_id)
);""" + "\ncreate table " + election_id + """_candidates(
	candidate_id varchar(15) not null primary key,
	name varchar(100) not null,
	dept varchar(10) not null,
	year int not null
);""" +"""\ncreate trigger """ + election_id + """_rolltrig 
before insert on """+ election_id + """_electoralroll
for each row
execute procedure add_to_active(\'"""+ election_id +"""\'); """ + "\ncreate table " + election_id + """_VotesCasted(
    voter_id varchar(15) not null,
    vote_time timestamp not null,
    candidate_id varchar(15) not null,
    foreign key(voter_id) references users(voter_id),
    foreign key(candidate_id) references """ + election_id + """_candidates(candidate_id)
);""" +"""\ncreate trigger """+ election_id + """_trigcast before insert on """+ election_id + """_votescasted
for each row
execute procedure delete_from_active(\'"""+ election_id +"""\'); """
    print(cmd)
    query(cursor,cmd)
    return election_id
    
def cast_vote(cursor,election_id,voter_id,candidate_id,vote_time):
    cmd= """insert into """ + election_id + """_VotesCasted
    values( '"""+ voter_id+"""','"""+vote_time+"""','"""+candidate_id+"""');
    """
    try:
        cursor.execute(cmd)
        return str(1)
    except (Exception, Error) as error:
        print(error)
        return "-1"

def create_candidate(cursor,election_id,candidate_id,name,dept,year):
    cmd= """insert into """ + election_id + """_candidates
    values( '"""+ candidate_id+"""','"""+name+"""','"""+dept+"""','"""+year+"""');
    """
    query(cursor,cmd)

def qs(cursor):
    '''
    create_user(cursor, user("37485", "123456", "abcd", "CSE", 2020))
    create_user(cursor, user("37486", "123456", "abcd", "CSE", 2020))
    create_user(cursor, user("37487", "123456", "abcd", "CSE", 2020))

    '''

    #print(authenticate_user(cursor, "37485", "123456"))
    eid=(create_election(cursor, "pehhc", "Presy", "20-09-2024", "09:00 AM", "05:00 PM", "Presy Election For the Term 2020-2021"))
    create_candidate(cursor, eid,'620','mantri','adm','2020')
    create_candidate(cursor, eid,'621','mantri2','adm2','2020')
    create_candidate(cursor, eid,'622','mantri3','adm1','2020')
    create_candidate(cursor, eid,'623','mantri3','adm1','2020')
    '''
    cast_vote(cursor, eid,'37485','620',str(datetime.datetime.now()))
    cast_vote(cursor, eid,'37485','621',str(datetime.datetime.now()))
    cast_vote(cursor, eid,'37485','622',str(datetime.datetime.now()))
    cast_vote(cursor, eid, '37486','622',str(datetime.datetime.now()))
    cast_vote(cursor, eid, '37485','621',str(datetime.datetime.now()))
    cast_vote(cursor, eid, '37485','623',str(datetime.datetime.now()))
    cast_vote(cursor, eid, '37487','622',str(datetime.datetime.now()))
    cast_vote(cursor, eid, '37486','623',str(datetime.datetime.now()))
    '''

    #try:

def active_elections(cursor, voter_id):
    cmd = "select distinct e.post, e.organisation, e.election_date, ae.election_id from active_elections ae, elections e where ae.voter_id =\'"+voter_id+"""\'  
    and ae.election_id = e.election_id ;"""
    query(cursor,cmd)
    result = cursor.fetchall()
    if(result):
        for i in range(len(result)):
            result[i] = {'post':result[i][0],'organisation':result[i][1],'election_date':result[i][2],'election_id':result[i][3]}
        
        return result
    else:
        return []

def list_candidates(cursor, election_id):
    query(cursor,  "select * from " + str(election_id) + "_candidates;")
    candidates = cursor.fetchall()
    if(candidates):
        for i in range(len(candidates)):
            candidates[i] = {'candidate_id': candidates[i][0], 'name':candidates[i][1], 'dept': candidates[i][2], 'year': candidates[i][3]}
        return candidates
    else:
        return []



if __name__ == "__main__":
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
    '''
    eid = "P2Pr230924"
    create_user(cursor, user("37488", "123456", "abcd", "CSE", 2020))
    cast_vote(cursor, eid,'37488','420',str(datetime.datetime.now()))
    
    qs(cursor)
    '''
    close_connection(cursor,connection)


    #except (Exception, Error) as error:
    #print("Error while connecting to PostgreSQL", error)
