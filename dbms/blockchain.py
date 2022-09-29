from hashlib import sha256
import json
import time
from psycopg2 import Error
import psycopg2
from user import *
from psycopg2 import Error
import datetime

class vote:
    def __init__(self, voter_id, candidate_id, timestamp, previous_hash, difficulty, nonce=0):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True, default=str)
        return sha256(block_string.encode()).hexdigest()
    

class votechain:
    compromised = True
    mine=True
    def __init__(self, cursor, schema_name, election_id):
        self.cursor = cursor
        self.election_id = election_id
        self.table = election_id + "_votechain"

        try:
            cmd = """select EXISTS (
   SELECT FROM pg_tables
   WHERE  schemaname = '""" + schema_name + """'
   AND    tablename  = '""" + election_id + """_votechain'
   );
   """
            cursor.execute(cmd)
            r = cursor.fetchone()[0]
            if( r == False):
               self.create_table()

        except (Exception, Error) as error:
            print("Error while Executing Command(", cmd, ")\nError: ", error)

        
        self.query("select count(*) from " + self.table + ";")      
        self.count = cursor.fetchone()[0]
        self.query("select difficulty from " + self.table + " where id = " + str(self.count) + ";")
        
        r = cursor.fetchone()
        if(r and r!=0):
            self.difficulty = r[0]
        else:
            self.difficulty = 1 

        if(self.count == 0):
            self.genesis_block()
        
    def query(self, cmd):
        try:
            self.cursor.execute(cmd)
        except (Exception, Error) as error:
            print("Error while Executing Command(", cmd, ")\nError: ", error)

    def genesis_block(self):
        self.query("insert into " + self.table + """ values(DEFAULT, '0', '0', '""" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + """', '0', """ + str(0) + """, 0);""")
        self.count += 1

    def create_table(self):
        cmd = "create sequence srno_" + self.table + "; \ncreate table " + self.table + """(
            id int not null default nextval('srno_""" + self.table + """'),
            voter_id varchar(20) primary key, 
            candidate_id varchar(20) not null,
            times timestamp not null, 
            previous_hash varchar(100) not null, 
            difficulty int not null,
            nonce integer not null
        );
        alter sequence srno_""" + self.table + """ owned by """ + self.table + ".id;"
        self.query(cmd)

    def last_block(self):
        self.query("select * from " + self.table + " where id = " + str(self.count) + ";")
        r = self.cursor.fetchone()
        v = vote(r[1], r[2], r[3].strftime("%Y-%m-%d %H:%M:%S"), r[4], r[5], r[6])
        return v

    def add_block(self, block):
        self.query("insert into " + self.table + """ values(DEFAULT, '""" + block.voter_id + """', '""" + block.candidate_id + """', '""" + block.timestamp + """', '""" + block.previous_hash + """', """ + str(block.difficulty) + """, """ + str(block.nonce) + """);""")
        self.count += 1

    def proof_of_work(self, nonce, hash):
        self.query("""select * from """ + self.election_id + """_VotesCasted vta 
        where vta.voter_id = (select vt.voter_id from """ + self.election_id + """_VotesCasted as vt limit 1) 
        order by vote_time limit 1;""")
        r = self.cursor.fetchone()
        last_vote = self.last_block()
        current_vote = vote(r[0], r[2], r[1].strftime("%Y-%m-%d %H:%M:%S"), last_vote.compute_hash(), self.difficulty)
        current_vote.nonce = nonce
        print(current_vote.difficulty, current_vote.compute_hash(), current_vote.compute_hash().startswith('0' * current_vote.difficulty))
        if(current_vote.compute_hash() == hash and current_vote.compute_hash().startswith('0' * current_vote.difficulty)):
            if(self.mine):
                self.mine = False
            else:
                while(self.mine == False):
                    pass

            self.query("delete from " + self.election_id + "_VotesCasted where voter_id = \'" + r[0] + "\';")
            self.query("select from " + self.table +" where voter_id = \'" + r[0] + "\';")
            result = self.cursor.fetchall()
            if(len(result) > 1):
                self.compromised = True
                return False
            elif(len(result) == 0):
                self.add_block(current_vote)
                self.mine = True
                return True
            return False
        else:
            False

    def mine_block(self):
        self.query("""select * from """ + self.election_id + """_VotesCasted vta 
        where vta.voter_id = (select vt.voter_id from """ + self.election_id + """_VotesCasted as vt limit 1) 
        order by vote_time limit 1;""")
        r = self.cursor.fetchone()
        if(r):
            pass
        else:    
            return -1
        last_vote = self.last_block()
        current_vote = vote(r[0], r[2], r[1].strftime("%Y-%m-%d %H:%M:%S"), last_vote.compute_hash(), self.difficulty)
        while(current_vote.compute_hash().startswith('0' * current_vote.difficulty) == False):
            current_vote.nonce += 1

        print(current_vote.compute_hash().startswith('0' * current_vote.difficulty))
        if(self.proof_of_work(current_vote.nonce, current_vote.compute_hash())):
            return 1
        else:
            return -1

    def bc_is_valid(self):
        if(self.compromised):
            return False
        previous_hash = '0'
        for i in range(1, self.count+1):
            self.query("select * from " + self.table +" where id = " + str(i) + ";")
            result = self.cursor.fetchall()
            print(result[0])
            if(len(result) == 1):
                r = result[0]
                block = vote(r[1], r[2], r[3].strftime("%Y-%m-%d %H:%M:%S"), r[4], r[5], r[6])
                hash = block.compute_hash()
                print(hash)
                if(previous_hash == block.previous_hash and hash.startswith('0' * block.difficulty)):
                    previous_hash = hash
                else:
                    return False
            else:
                self.compromised = True
                return False
        return True

if __name__ == "__main__":
        #try:
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
        
        bc = votechain(cursor, "public", "p2pr230924")
        bc.compromised = False
        while(bc.mine_block()==1):
            pass
        print(bc.bc_is_valid())

        cursor.close()
        connection.close()


#   except (Exception, Error) as error:
#        print("Error while connecting to PostgreSQL", error)
