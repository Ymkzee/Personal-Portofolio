import uuid

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def add_user(self, nrp, Acc, email, Password):
        ## checking if user already exist or not
        
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM User
        WHERE Name = %s;
        """, (Acc,))
        for row in cursor.fetchall():
            result.append({
                'id_user': row['id_user'],
                'Acc': row['Name']
            })

        if result:
            cursor.close()
            return "User Exist !!"
        
        ## if user doesnt exist yet, create the account
        
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            print(generateUUID)
            cursor.execute("""
            INSERT INTO User (id_user, NRP, Name, Email,Password)
            VALUES (%s, %s, %s, %s, %s);
            """, ( generateUUID, nrp, Acc, email, Password))
            cursor.close()
            self.connection.commit()
            return "User Added !!"
        
    def add_file(self, Acc, file):
        # check if user already exist
        cursor = self.connection.cursor(dictionary=True)
       
        cursor.execute("""
        INSERT INTO File (id_user, file_name)
        VALUES (%s, %s);
        """, ( Acc, file))
        cursor.close()
        self.connection.commit()
        return "File uploaded !!"
    
    # get user for login
    def get_user(self, email, Password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM User 
        WHERE Email = %s AND Password = %s;
        """, (email, Password))
        for row in cursor.fetchall():
            result.append({
                'session_id':'',
                'id_user': row['id_user'],
                'email': row['Email']
            })
        cursor.close()
        return result

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='user_acc_file',
                user='root',
                password=''
            )
        except Error as e :
            print ("Connection Error !!", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())