import psycopg2

# Function to fetch and display data from a table
def display_table_data(table_name, connection, cursor):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"Data in the '{table_name}' table:")
        print("Total Number of Rows or Data Count Present in Table : ",table_name, "is : ",len(rows))
        '''
        for row in rows:
            print(row)
        '''
        print("\n")
        
    except Exception as e:
        print(f"Error fetching data from the '{table_name}' table: {e}")

# Connect to your PostgreSQL database
try:
    #Connecting to Database Locally
    userhost = 'localhost'
    port_no = 5432
    username = 'postgres'
    database_name = 'socialgood'
    passwrd = 'socialgood'
    
    connection = psycopg2.connect(host  = userhost, port = port_no, user = username, password = passwrd, dbname = database_name)
    connection_cursor = connection.cursor()

    # List of your table names
    table_names = ["youtube_channels", "youtube_channel_videos", "youtube_videos_comments"]

    # Display data from each table
    for table_name in table_names:
        display_table_data(table_name, connection, connection_cursor)

except Exception as e:
    print(f"Error connecting to the database: {e}")

finally:
    if connection:
        connection_cursor.close()
        connection.close()
