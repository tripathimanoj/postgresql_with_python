# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import psycopg2

class DatabaseConnector:     # class for only connection to database
    def __init__(self, user, host, password, port, database):              # constructor function
        self.user = user
        self.host = host
        self.password = password
        self.port = port
        self.database = database

    def connect_with_psycopg2(self):    # function for connecting to db using psycopg2 lib
        try:
            conn = psycopg2.connect(
                user=self.user,
                host=self.host,
                password=self.password,
                port=self.port,
                database=self.database
            )
            print("Connection with psycopg2 successful")
            return conn
        except psycopg2.Error as e:
            print("Error connecting with psycopg2:", e)
            return None

    def connect_with_sqlalchemy(self):       # function for connecting to db using sqlalchemy lib
        try:
            engine = create_engine(
                f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
            )
            print("Connection with SQLAlchemy successful")
            return engine
        except Exception as e:
            print("Error connecting with SQLAlchemy:", e)
            return None

class DataOperations:                 # class for other data related operations
    def __init__(self, connection,connection1):   # constructor here the previous class instance will be passed as a connection parameter ok.
        self.connection = connection
        self.connection1 = connection1

    def create_table_and_insert_data(self):  # function for creating table and inserting data into it, here psycopg2 lib wll be called
        if self.connection is not None:
            try:
                cur = self.connection.cursor()
                cur.execute("DROP TABLE IF EXISTS raw_data")
                self.connection.commit()

                cur.execute("""
                    CREATE TABLE raw_data (
                        department_name VARCHAR(50),
                        sales VARCHAR(50),
                        country VARCHAR(50)
                    )
                """)
                self.connection.commit()

                cur.execute("""
                    INSERT INTO raw_data VALUES
                    ('@#h*&#R&','nine 7','+91'),
                    ('s@a#le&S','nine foUr','+91'),
                    ('maNage*&#ment&','one 0 Zero','iNdia'),
                    ('Da@@ta_te@m*','17','inDIA'),
                    ('M*&^%$l','five five','+99'),
                    ('W#eB*DeveL0Opm#en@!t','onE siX','ruSSIA')
                """)
                self.connection.commit()

                print("Table created and data inserted successfully")
            except psycopg2.Error as e:
                print("Error creating table or inserting data:", e)
        else:
            print("Connection is not established")

    def convert_table_to_dataframe(self):                # function for reading a sql table and converting it to a df here sqlalchemy lib will be called ok.
        try:
            df = pd.read_sql_table('raw_data', self.connection1)
            return df
        except Exception as e:
            print("Error converting table to DataFrame:", e)
            return None

def main():   # all done here is the driver function which will call above classes and it's functions.
    # Database connection parameters
    user = "postgres"
    host = "localhost"
    password = "root11"
    port = 5432
    database = "eda_ops"

    # Creating DatabaseConnector class object
    db_connector = DatabaseConnector(user, host, password, port, database)

    # Connect to database using psycopg2
    conn_psycopg2 = db_connector.connect_with_psycopg2()
    conn_sqlalchemy = db_connector.connect_with_sqlalchemy()

    # Creating DataOperations class object
    data_ops = DataOperations(conn_psycopg2,conn_sqlalchemy)
    data_ops.create_table_and_insert_data()

    # Convert table to DataFrame using SQLAlchemy
    df = data_ops.convert_table_to_dataframe()

    # function 1 for department_name
    def department_name(name):
        flag = ''
        for ele in name:
            if ele.isalpha():
                flag += ele
        return flag.lower()
    
    # function 2 for sales_data
    def sales(sales_data):
        dict_num = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
        result = ''
        for word in sales_data.split():
            if word.isnumeric():
                result += word
            elif word.lower() in dict_num:
                result += str(dict_num.get(word.lower()))
        return int(result)

    # function 3 for country_code
    def country(country_code):
        return str(country_code).lower().replace('+91', 'india')

    # applying above 3 data cleaning function to it's respective cols.
    if df is not None:
        df['department_name'] = df['department_name'].apply(department_name) # function1
        df['sales'] = df['sales'].apply(sales) # function2
        df['country'] = df['country'].apply(country) # function3
        
        # filtering only india records.
        cleandata = df[df['country'] == 'india']

        # creating new table with cleaned data.
        if conn_sqlalchemy is not None:
            table_name = 'clean_data'
            cleandata.to_sql(table_name, conn_sqlalchemy, if_exists='replace', index=False)
            print(f"DataFrame updated to PostgreSQL table: {table_name}")

            # reading cleaned data table for creating graph.
            df_clean = pd.read_sql_table(table_name, conn_sqlalchemy)

            # Plot graph
            df_sorted = df_clean.sort_values(by='sales')
            plt.bar(df_sorted['department_name'], df_sorted['sales'])
            plt.xlabel('Department Name')
            plt.ylabel('Sales')
            plt.title('Sales by Department in Increasing Order')
            plt.show()
        else:
            print("Error: SQLAlchemy connection not established")
    else:
        print("Error: DataFrame is None")


if __name__ == "__main__": # calling driver function.
    main()
