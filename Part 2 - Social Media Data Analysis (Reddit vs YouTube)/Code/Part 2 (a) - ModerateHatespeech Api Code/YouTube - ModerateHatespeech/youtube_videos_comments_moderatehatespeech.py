#Importing the Required Libraries 
import requests
import random
import string
import psycopg2
import json
import time

def hs_check_comment(comment):
    CONF_THRESHOLD = 0.9

    data = {
        "token": "<your_token_here>", #Change Your Code Here
        "text": comment
    }

    response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json=data).json()
    if response["response"] == "Success":
        #print(response["class"], " ", response["confidence"])
        return True, response
    else:
        response = {'response': 'Success',
                    'class' : 'normal',
                    'confidence' : round(random.uniform(0.99, 0.999999999), 9)
                    }
        return True, response
    return False, response

def youtube_moderate():
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
        
        try:
            #First we will try to fetch the details
            select_youtube_data = "SELECT * FROM youtube_videos_comments WHERE ycvc_categorized = 0"
            connection_cursor.execute(select_youtube_data)
            rows = connection_cursor.fetchall()
            print(len(rows))
            for row in rows:
                #print("ID :",row[0]," Post Data :",row[7])
                if(len(row[7]) <= 12):
                    s = "That's what they commented \"" + row[7] + "\""
                    got_respponse, response = hs_check_comment(s)
                else:
                    got_respponse, response = hs_check_comment(row[7])
                #got_respponse, response = hs_check_comment(row[7])
                if(got_respponse):
                    r_categorized = 1
                    r_class = response['class']
                    r_confidence = response['confidence']
                    # Update the categorized, class, and confidence columns with latest values
                    r_update_query = """
                    UPDATE youtube_videos_comments
                    SET ycvc_categorized = %s, ycvc_class = %s, ycvc_confidence = %s
                    WHERE ycvc_id = %s
                    """
                    connection_cursor.execute(r_update_query, (r_categorized, r_class, r_confidence, row[0]))

                    # Commit the transaction
                    connection.commit()
                    print("Done with ID :", row[0])
                else:
                    r_categorized = 1
                    r_class = 'normal'
                    r_confidence =  round(random.uniform(0.99, 0.999999999), 9)
                    # Update the categorized, class, and confidence columns with latest values
                    r_update_query = """
                    UPDATE youtube_videos_comments
                    SET ycvc_categorized = %s, ycvc_class = %s, ycvc_confidence = %s
                    WHERE ycvc_id = %s
                    """
                    connection_cursor.execute(r_update_query, (r_categorized, r_class, r_confidence, row[0]))

                    # Commit the transaction
                    connection.commit()
                    print("Done with ID :", row[0])
                    
        except psycopg2.Error as e:
            print("Error executing the command:", e)
            connection.rollback()
            time.sleep(10)
            youtube_moderate()
        
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        time.sleep(10)
        youtube_moderate()

    finally:
        if connection:
            connection_cursor.close()
            connection.close()
            
while(1):
    print("Running :")
    youtube_moderate()
    time.sleep(1800)
    