# implimenting this => https://youtube.com/shorts/LxJk4xVtH4Y?si=2xWf8w3Ew6VZ50ZU
import psycopg2
from sqlalchemy import create_engine     # importing lib's
import pandas as pd
import matplotlib.pyplot as plt
import time

class Animal_db_sorter:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password              # class variables
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None
        self.conn_pd = None
        self.table_name = 'sort_animal'

    def connect_postgres(self):             # method to connect with postgres using psycopg2 module
        self.conn = psycopg2.connect(
            user=self.user,
            host=self.host,
            password=self.password,
            port=self.port,
            database=self.dbname
        )
        self.cur = self.conn.cursor()    # creating cursor object
        print("PostgreSQL conn established successfully!")

    def connect_sqlalchemy(self):
        self.conn_pd = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')  # method to connect with postgres using sqlalchemy module
        print("SQLAlchemy conn established successfully!")

    def create_table(self):                                          # method for creating table
        self.cur.execute("drop table if exists sort_animal")
        self.conn.commit()
        time.sleep(1)

        self.cur.execute("""
            CREATE TABLE if not exists sort_animal (
                animal_name VARCHAR(20),
                animal_in_field VARCHAR(20),
                ewes_room VARCHAR(20),
                lambs_room VARCHAR(20)
            );
        """)
        self.conn.commit()

    def check_table_existence(self):
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")   # method for checking table created or not.
        if 'sort_animal' in self.cur.fetchone():
            print("Table created successfully")

    def insert_records(self):                       # method for inserting records
        self.cur.execute("""
            INSERT INTO sort_animal (animal_name) VALUES
            ('ewes1_red'), ('ewes2_red'), ('lamb1_green'), ('ewes_3_red'), ('lamb2_green'), ('ewes_4_red'),
            ('lamb3_green'), ('lamb4_green'), ('lamb5_green'), ('ewes_5_red'), ('ewes_6_red'), ('ewes_7_red'), ('ewes_8_red');
        """)
        self.conn.commit()
        self.cur.execute("UPDATE sort_animal SET animal_in_field = animal_name;")
        self.conn.commit()

    '''def update_records(self):
        self.cur.execute("UPDATE sort_animal SET animal_in_field = animal_name;")
        self.conn.commit()'''

    def update_ewes_room(self, animal):     # method for sorting and updating ewes_room column in db and also removing that animal from animal_in_field column
        self.cur.execute("UPDATE sort_animal SET ewes_room = %s WHERE animal_in_field = %s;", (animal, animal))
        self.conn.commit()
        self.cur.execute("UPDATE sort_animal SET animal_in_field = %s WHERE animal_in_field = %s;", ('-', animal))
        self.conn.commit()

    def update_lambs_room(self, animal):    # method for sorting and updating lambs_room column in db and also removing that animal from animal_in_field column
        self.cur.execute("UPDATE sort_animal SET lambs_room = %s WHERE animal_in_field = %s;", (animal, animal))
        self.conn.commit()
        self.cur.execute("UPDATE sort_animal SET animal_in_field = %s WHERE animal_in_field = %s;", ('-', animal))
        self.conn.commit()

    def close_conn(self):  # method for closing connection
        if self.conn:
            self.conn.close()
            print("conn closed.")

    def generate_pandas_graph(self):   # method for creating pandas graph.
        df = pd.read_sql_table(self.table_name, self.conn_pd)
        count_total_animal, count_ewes_room, count_lambs_room = df['animal_name'].count(), df['ewes_room'].count(), df['lambs_room'].count()
        counts = pd.Series([count_total_animal, count_ewes_room, count_lambs_room],
                           index=['Total Animals', 'Animals in ewes_room', 'Animals in lambs_room'])

        
        colors = ['skyblue', 'red', 'green']
        counts.plot(kind='bar', color=colors)
        plt.xlabel('Categories')
        plt.ylabel('Count')
        plt.title('Count of Animals in Different Categories')
        plt.show()

    def count_confirmation(self):    # method for counting confirmation.
        df = pd.read_sql_table(self.table_name, self.conn_pd)
        count_total_animal, count_ewes_room, count_lambs_room = df['animal_name'].count(), df['ewes_room'].count(), df['lambs_room'].count()
        if count_total_animal==count_ewes_room+count_lambs_room:
            print(f"ALL {count_ewes_room} EWES AND {count_lambs_room} LAMBS ARE SORTED/PLACED SUCCESSFULLY!")
            print("END")
        else:
            print(f"{count_total_animal}-({count_ewes_room}+{count_lambs_room}) ANIMALS ARE MISSING!")


if __name__ == "__main__":    # driver code
    # Instantiate the class
    sort_animal = Animal_db_sorter(dbname='youtube_sort', user='postgres', password='root11', host='localhost', port=5432) # creating class object.

    sort_animal.connect_postgres() # calling method for connect to postgresql and sqlacchemy
    sort_animal.connect_sqlalchemy()

    sort_animal.create_table()     # callin method for create and check the existnce of the table
    sort_animal.check_table_existence()

    sort_animal.insert_records()   # method calling for inserting records

    cur = sort_animal.cur # creating curson object
    cur.execute("SELECT animal_in_field FROM sort_animal;")  # getting all animal data
    animal_data = cur.fetchall()

    for animal in animal_data:  # loop over all animal one by one
        print(f"sending {animal[0]} to it's place")
        if animal[0][-3:] == 'red' and animal[0][0:4] == 'ewes': # condition for ewes
            time.sleep(1)
            sort_animal.update_ewes_room(animal[0])   # calling update_ewes_room method
            print(f"Successfully placed {animal[0]} in desired place | getting real time graph data from database: ==>")
            sort_animal.generate_pandas_graph()      # calling generate_pandas_graph method
            print('*'*40)

        elif animal[0][-5:] == 'green' and animal[0][0:4] == 'lamb':  # conditon for lambs
            time.sleep(1)
            sort_animal.update_lambs_room(animal[0])   # calling update_lambs_room method
            print(f"Successfully placed {animal[0]} in desired place | getting real time graph data from database: ==>")
            sort_animal.generate_pandas_graph()        # calling generate_pandas_graph method
            print('*'*40)

    sort_animal.count_confirmation()  # getting details...
    
    sort_animal.close_conn() # closing conn()........
