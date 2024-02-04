import time    # importing time ()
# import pandas as pd
import psycopg2
from sqlalchemy import create_engine 
# import matplotlib.pyplot as plt
# import seaborn as sns

class find_odd_even_char:  # creating a class.

    def __init__(self, dbname, user, password, host, port):       # declaring class variables
        self.dbname=dbname                                    #define constructors here
        self.user=user
        self.password=password
        self.host=host
        self.port=port
        self.conn=None
        self.cur=None
        self.table_name='odd_even'

    def connect_postgres(self): 
        try:
            self.conn = psycopg2.connect(
                user=self.user,
                host=self.host,
                password=self.password,
                port=self.port,
                dbname=self.dbname
            )
            self.cur = self.conn.cursor()
           
            print("postgress connected sucessfully!")
        except Exception as e:
            print(f"Error: Unable to connect to PostgreSQL. {e}")

    def connect_sqlalchemy(self):
        try:
            self.conn_pd = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')  # method to connect with postgres using sqlalchemy module
            
        except Exception as e:
            print(f"error execute query{e}")
            
    def create_table(self):  
       try:                                       # method for creating table
             self.cur.execute("drop table if exists odd_even")
             self.conn.commit()
             time.sleep(1)
             self.cur.execute('''create table odd_even(
                                name varchar(20),
                                odd_name varchar (20),
                                even_name varchar (20),
                                age int);
                              ''')
             self.conn.commit()
             print(f"create table successfully!")
       except Exception as e:
           print(f"error execute query:{e}")
          
           
    def insert_records(self):
        self.cur.execute('''insert into odd_even(name,age) values
                         ('priyansh',3),('manoj',25),('reyansh',5);''')
        self.conn.commit()
        self.cur.execute("select name from odd_even;")
        c=self.cur.fetchall()
        
            #print(char)
    def update_even(self,even_char,data):
        self.cur.execute("UPDATE odd_even SET even_name = %sWHERE name = %s;",
                (even_char,data[0]))
        self.conn.commit()
        print(f"update all the charecters")

    def update_odd(self,odd_char,data):
        self.cur.execute("update odd_even set odd_name= %s where name= %s",(odd_char,data[0]))
        self.conn.commit()
        print(f"update all the charectors")

    def print_odd_even(self):
        self.cur.execute("SELECT * FROM odd_even")
        for rows in self.cur.fetchall():
           print(rows)
           print(f"print odd even char successfully!")
    '''def pandas_graph(self):
        df=pd.read_sql_table('odd_even',self.conn_pd)
        sns.barplot(x='name',y='age',data=df)
        plt.ylabel('Count the age')
        plt.title('age')
        plt.show()'''
if __name__=="__main__":
    
               
    chars_find=find_odd_even_char(user='postgres',host='13.201.122.86',password='cloud11',port=5432,dbname='priyadb',)
    chars_find.connect_postgres()
    chars_find.connect_sqlalchemy()
    
    chars_find.create_table()
    chars_find.insert_records()
   

    cur=chars_find.cur     # create cursor obj
    cur.execute("select name from odd_even")
    chars_data=cur.fetchall()
 

    for data in chars_data:
           even_char = ''
           odd_char = ''

           for i, char in enumerate(data[0]):  
              if i % 2 == 0:
                  even_char = even_char+char
                  chars_find.update_even(even_char,data)
                  print(f"successfully all even charecters go to there charecters columns")
              else:
                  odd_char= odd_char + char
                  chars_find.update_odd(odd_char,data)
                  print(f"successfully all even charecters go to there charecters columns")
    # chars_find.pandas_graph()
    chars_find.print_odd_even()
    print(f"coding is done happy coding!")

