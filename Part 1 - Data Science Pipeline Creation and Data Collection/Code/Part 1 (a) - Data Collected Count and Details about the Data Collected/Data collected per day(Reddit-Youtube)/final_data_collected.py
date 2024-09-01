import psycopg2
from datetime import datetime
import time

def insert_data_to_table(connection, cursor, subreddits_count, subreddit_posts_count, subreddit_comments_count, youtube_channels_count, youtube_videos_count, youtube_comments_count):
    # SQL query to insert data into the table
    insert_query = """
        INSERT INTO data_collected_count (
            subreddits_count, subreddit_posts_count, subreddit_comments_count,
            youtube_channels_count, youtube_videos_count, youtube_comments_count
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        )
    """
    
    # Get the current date and time
    #current_datetime = datetime.now()

    # Execute the insert query
    cursor.execute(insert_query, (
        subreddits_count, subreddit_posts_count, subreddit_comments_count,
        youtube_channels_count, youtube_videos_count, youtube_comments_count
    ))
        
    # Commit the transaction
    connection.commit()

    print("Data inserted successfully!")
    
    

# Connect to your PostgreSQL database
while(True):
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
        table_names = ["subreddits", "subreddit_posts", "subreddit_posts_comments", "youtube_channels", "youtube_channel_videos", "youtube_videos_comments"]
        table_column_names = ["subreddit_date_time", "post_date_time", "comment_date_time", "yc_date_time", "ycv_date_time", "ycvc_date_time"]
        
        subreddits_count = []
        subreddit_posts_count = []
        subreddit_comments_count = []
        youtube_channels_count = []
        youtube_videos_count = []
        youtube_comments_count = []
        # Display data from each table
        for i in range(0,len(table_names)):
            get_count_query = "SELECT DATE_TRUNC('day', {column_name}) AS day, COUNT(*) AS count_table1 FROM {table_name} GROUP BY 1 ORDER BY 1".format(column_name=table_column_names[i], table_name=table_names[i])
            connection_cursor.execute(get_count_query)
            rows = connection_cursor.fetchall()
            for row in rows:
                if i == 0:
                    subreddits_count.append(row[1]) 
                if i == 1:
                    latest_date = row[0]
                    subreddit_posts_count.append(row[1]) 
                if i == 2:
                    subreddit_comments_count.append(row[1]) 
                if i == 3:
                    youtube_channels_count.append(row[1]) 
                if i == 4:
                    youtube_videos_count.append(row[1]) 
                if i == 5:
                    youtube_comments_count.append(row[1]) 
            
        get_date_query = "SELECT DATE_TRUNC('day', dcc_date_time) AS day FROM data_collected_count GROUP BY 1 ORDER BY 1"
        connection_cursor.execute(get_date_query)
        date_rows = [str(result[0])[0:10] for result in connection_cursor.fetchall()]
        
        # Get the current date and time
        current_datetime = datetime.now()
        
        if str(current_datetime)[0:10] in date_rows:
            print("Date Match")
        else:
            insert_data_to_table(connection, connection_cursor, subreddits_count[0], sum(subreddit_posts_count), sum(subreddit_comments_count), sum(youtube_channels_count), sum(youtube_videos_count), sum(youtube_comments_count))
        print(str(current_datetime)[0:10] == str(latest_date)[0:10])
        print("The Datais for the table : ", table_names[i])
        print(subreddits_count[0])
        print(sum(subreddit_posts_count))
        print(sum(subreddit_comments_count))
        print(sum(youtube_channels_count))
        print(sum(youtube_videos_count))
        print(sum(youtube_comments_count))
    
        time.sleep(86400)
        #break 
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    finally:
        if connection:
            connection_cursor.close()
            connection.close()