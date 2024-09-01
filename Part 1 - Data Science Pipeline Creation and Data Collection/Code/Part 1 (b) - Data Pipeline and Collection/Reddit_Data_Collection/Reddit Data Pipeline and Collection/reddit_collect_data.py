#Importing the Required Libraries 
import requests
import random
import string
import psycopg2
import json
import time
total_requests_count = 0

#Code to generate random User-Agent
def generate_user_agent():
    all_characters = string.ascii_letters + string.digits
    random_user_agent = ''.join(random.choice(all_characters) for i in range(10))
    return random_user_agent

#Code to generate bearer token to get the authorization
def bearer_token_generation(CLIENT_ID, CLIENT_SECRET, p_data):
    #Adding Client ID and Authorization
    #CLIENT_ID = 'tLXXkyhPEqaBerP9PV4pBQ'
    #CLIENT_SECRET = 'SHaShtpUxhCr-2YM3jZsoGI_StNNEg'

    #Authenticate the Reddit App
    c_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    user_agent = generate_user_agent()
    user_headers = {
        'User-Agent' : user_agent
    }

    #Getting Token and Access ID
    Get_Token_Endpoint = 'https://www.reddit.com/api/v1/access_token'

    #Getting Reponse based on the Authenticate and Token
    response = requests.post(Get_Token_Endpoint, data = p_data, headers = user_headers, auth = c_auth)

    #Getting Bearer Toekn from the Reddit Authentication
    if response.status_code == 200:
        bearer_token = response.json()['access_token']
    return bearer_token 

#Using Reddit REST APi's

#This function will return the Details about the Subreddit which we are passing
def get_subreddit(subreddit_name,bearer_token,connection,connection_cursor):
    request_headers = {
    'User-Agent' : generate_user_agent(),
    'Authorization': 'Bearer {}'.format(bearer_token)
    }
    search_url = 'https://oauth.reddit.com/r/'+subreddit_name+'/about.json'
    subreddit_url = 'https://www.reddit.com/r/'+subreddit_name+'/'
    search_parameters = {'q': subreddit_name, 'limit':10}
    subreddit_database_values = ()
    save_subreddit = 'INSERT INTO subreddits (subreddit_title, subreddit_name, subreddit_id, subreddit_url, subreddit_description, subreddit_subscribers, subreddit_data) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    check_subreddit = 'SELECT subreddit_id FROM subreddits' 
    try:
        search_response = requests.get(search_url, params = search_parameters, headers = request_headers)
        global total_requests_count #Counting the number of requests
        total_requests_count = total_requests_count + 1 #Counting the number of requests
        if search_response.status_code == 200:
            search_data = search_response.json()
            connection_cursor.execute(check_subreddit)
            existing_subreddits = [result[0] for result in connection_cursor.fetchall()]
            if search_data['data']['display_name_prefixed'] not in existing_subreddits:
                subreddit_database_values = (
                    search_data['data']['title'],
                    search_data['data']['display_name'],
                    search_data['data']['display_name_prefixed'],
                    subreddit_url,                    
                    search_data['data']['public_description'],
                    search_data['data']['subscribers'],
                    json.dumps(search_data['data'])
                    )
                connection_cursor.execute(save_subreddit, subreddit_database_values)
                connection.commit()
        else:
            print("Sorry!! No Subreddit Found with the name ["+subreddit_name+"] Try Again")
            print("Error ! : ",search_response.status_code)
    except requests.exceptions.RequestException as re:
        print("Got Exception : ",re)

#This function will return the latest posts from the Subreddit passed
def get_subreddit_posts(subreddit_name, bearer_token, connection, connection_cursor):
    request_headers = {
    'User-Agent' : generate_user_agent(),
    'Authorization': 'Bearer {}'.format(bearer_token)
    }
    get_posts_url = 'https://oauth.reddit.com/r/'+subreddit_name+'/new.json' #For old /Hot Posts use get_posts_url = 'https://www.reddit.com/r/'+subreddit_name+'.json'
    subreddit_posts_database_values = ()
    posts_parameters = {'limit':20}
    save_subreddit_posts = 'INSERT INTO subreddit_posts (post_id, subreddit_id, subreddit_url, post_name, post_url, post_title, post_data) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    check_subreddit_posts = 'SELECT post_id FROM subreddit_posts'
    try:
        reddit_posts_response = requests.get(get_posts_url, params = posts_parameters, headers = request_headers)
        global total_requests_count #Counting the number of requests
        total_requests_count = total_requests_count + 1 #Counting the number of requests
        if reddit_posts_response.status_code == 200:
            reddit_posts_data = reddit_posts_response.json()
            if 'data' in reddit_posts_data and 'children' in reddit_posts_data['data']:
                for each_post in reddit_posts_data['data']['children']:
                    connection_cursor.execute(check_subreddit_posts)
                    existing_subreddits_posts = [result[0] for result in connection_cursor.fetchall()]
                    if each_post['data']['id'] not in existing_subreddits_posts:
                        subreddit_posts_database_values = (
                            each_post['data']['id'],
                            each_post['data']['subreddit_name_prefixed'],
                            'https://www.reddit.com/'+each_post['data']['subreddit_name_prefixed']+'/',
                            each_post['data']['name'],
                            'https://www.reddit.com'+each_post['data']['permalink'],
                            each_post['data']['title'],
                            json.dumps(each_post['data'])
                        )
                        connection_cursor.execute(save_subreddit_posts, subreddit_posts_database_values)
                        connection.commit()
                        #Executing the get_subreddit_post_comments which will save the data of the subreddit post latest comments
                        get_subreddit_post_comments(subreddit_name, each_post['data']['id'], bearer_token, connection, connection_cursor) #This function will call the comment function and collect the comments of that specific posts
                    else:
                        #Executing the get_subreddit_post_comments which will save the data of the subreddit post latest comments
                        #get_subreddit_post_comments(subreddit_name, each_post['data']['id'], bearer_token, connection, connection_cursor) #This function will call the comment function and collect the comments of that specific posts
                        pass
            else:
                print("Sorry!! No Posts Found Try Again")
        else:
            print("Error ! : ",reddit_posts_response.status_code)
        #Handle Any kind of Exception by printing it 
    except requests.exceptions.RequestException as pe:
        print("Got Exception : ",pe)

#This function will return the latest Comments Present in a specific subreddit post
def get_subreddit_post_comments(subreddit_name, subreddit_post_id, bearer_token, connection, connection_cursor):
    request_headers = {
    'User-Agent' : generate_user_agent(),
    'Authorization': 'Bearer {}'.format(bearer_token)
    }
    get_post_comments_url = 'https://oauth.reddit.com/r/'+subreddit_name+'/comments/'+subreddit_post_id+'.json'
    subreddit_post_comments_database_values = ()
    comments_parameters = {'limit':20}
    save_subreddit_post_comments = 'INSERT INTO subreddit_posts_comments (comment_id, post_id, post_name, post_url, subreddit_id, subreddit_name, subreddit_url, comment_body, comment_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    check_subreddit_post_comments = 'SELECT comment_id FROM subreddit_posts_comments'
    try:
        reddit_post_comments_response = requests.get(get_post_comments_url, params = comments_parameters, headers = request_headers)
        global total_requests_count #Counting the number of requests
        total_requests_count = total_requests_count + 1 #Counting the number of requests
        if reddit_post_comments_response.status_code == 200:
            reddit_post_comments_data = reddit_post_comments_response.json()
            if 'data' in reddit_post_comments_data[1] and 'children' in reddit_post_comments_data[1]['data']:
                reddit_post_all_comments_data = reddit_post_comments_data[1]['data']['children']
                for reddit_post_each_comments in reddit_post_all_comments_data:
                    connection_cursor.execute(check_subreddit_post_comments)
                    existing_subreddits_post_comments = [result[0] for result in connection_cursor.fetchall()]
                    if 'body' in reddit_post_each_comments['data']:
                        if reddit_post_each_comments['data']['id'] not in existing_subreddits_post_comments:
                            subreddit_post_comments_database_values = (
                                reddit_post_each_comments['data']['id'], #comment_id
                                reddit_post_comments_data[0]['data']['children'][0]['data']['id'], #post_id
                                reddit_post_comments_data[0]['data']['children'][0]['data']['name'], #post_name
                                'https://www.reddit.com'+reddit_post_comments_data[0]['data']['children'][0]['data']['permalink'], #post_url
                                reddit_post_comments_data[0]['data']['children'][0]['data']['subreddit_name_prefixed'], #subreddit_id
                                reddit_post_comments_data[0]['data']['children'][0]['data']['subreddit'], #subreddit_name
                                'https://www.reddit.com/'+reddit_post_comments_data[0]['data']['children'][0]['data']['subreddit_name_prefixed']+'/', #subreddit_url
                                reddit_post_each_comments['data']['body'], #comment_body
                                json.dumps(reddit_post_each_comments['data']) #comment_dict
                            )
                            connection_cursor.execute(save_subreddit_post_comments, subreddit_post_comments_database_values)
                            connection.commit()
                            get_subreddit_post_comments_replies(subreddit_name, subreddit_post_id,reddit_post_each_comments['data']['id'],reddit_post_comments_data[0]['data']['children'][0]['data']['name'], bearer_token, connection, connection_cursor)
                        else:
                            #get_subreddit_post_comments_replies(subreddit_name, subreddit_post_id,reddit_post_each_comments['data']['id'],reddit_post_comments_data[0]['data']['children'][0]['data']['name'], bearer_token, connection, connection_cursor)
                            pass     
    #Hanedle Any kind of Exception by printing it 
    except requests.exceptions.RequestException as pce:
        print("Got Exception : ",pce)

#This function will return the latest Comments and their replies Present in a specific subreddit post
def get_subreddit_post_comments_replies(subreddit_name, subreddit_post_id, subreddit_comment_id, subreddit_post_name , bearer_token, connection, connection_cursor):
    request_headers = {
    'User-Agent' : generate_user_agent(),
    'Authorization': 'Bearer {}'.format(bearer_token)
    }
    get_post_comments_replies_url = 'https://oauth.reddit.com/r/'+subreddit_name+'/comments/'+subreddit_post_id+'/'+subreddit_comment_id+'.json'
    comments_replies_parameters = {'limit':5}
    try:
        reddit_post_comments_replies_response = requests.get(get_post_comments_replies_url, params = comments_replies_parameters, headers = request_headers)
        global total_requests_count #Counting the number of requests
        total_requests_count = total_requests_count + 1 #Counting the number of requests
        if reddit_post_comments_replies_response.status_code == 200:
            reddit_post_comments_replies_data = reddit_post_comments_replies_response.json()
            if 'data' in reddit_post_comments_replies_data[1] and 'children' in reddit_post_comments_replies_data[1]['data']:
                for each_reddit_post_comment_replies in reddit_post_comments_replies_data[1]['data']['children']:
                    get_all_comments_replies(each_reddit_post_comment_replies, subreddit_post_id, subreddit_comment_id, subreddit_post_name, connection, connection_cursor)
        else:
            print("Error ! : ",reddit_post_comments_replies_response.status_code)
    #Hanedle Any kind of Exception by printing it 
    except requests.exceptions.RequestException as pcre:
        print("Got Exception : ",pcre)

#This function will recursively return the latest Replies on the Comments Present in a specific subreddit post comment
def get_all_comments_replies(each_reddit_post_comment_replies, subreddit_post_id, subreddit_comment_id, subreddit_post_name, connection, connection_cursor):
    save_subreddit_post_comment_replies = 'INSERT INTO subreddit_posts_comments (comment_id, post_id, post_name, post_url, subreddit_id, subreddit_name, subreddit_url, comment_body, comment_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    check_subreddit_post_comments = 'SELECT comment_id FROM subreddit_posts_comments'
    subreddit_post_comments_replies_database_values = ()
    #Checking Existing Comments from comments table
    connection_cursor.execute(check_subreddit_post_comments)
    existing_subreddits_post_comments = [result[0] for result in connection_cursor.fetchall()]

    if 'body' in each_reddit_post_comment_replies['data']:
        if each_reddit_post_comment_replies['data']['id'] not in existing_subreddits_post_comments:
            subreddit_post_comments_replies_database_values = (
                each_reddit_post_comment_replies['data']['id'], #reply_id
                subreddit_post_id, #post_id
                subreddit_post_name, #post_name
                'https://www.reddit.com/'+each_reddit_post_comment_replies['data']['subreddit_name_prefixed']+'/', #post_comment_url
                each_reddit_post_comment_replies['data']['subreddit_name_prefixed'], #subreddit_id
                each_reddit_post_comment_replies['data']['subreddit'], #subreddit_name
                'https://www.reddit.com/'+each_reddit_post_comment_replies['data']['subreddit_name_prefixed']+'/', #subreddit_url
                each_reddit_post_comment_replies['data']['body'], #reply_body #comment_body
                json.dumps(each_reddit_post_comment_replies['data']) #reply_data #comment_data #comment_dict
            )
            connection_cursor.execute(save_subreddit_post_comment_replies, subreddit_post_comments_replies_database_values)
            connection.commit()

    #Checking if there are further replies on the given comment
    if 'replies' in each_reddit_post_comment_replies['data'] and 'data' in each_reddit_post_comment_replies['data']['replies']:
        reddit_post_each_comment_replies_data = each_reddit_post_comment_replies['data']['replies']['data']['children']
        for each_comment_replies_data in reddit_post_each_comment_replies_data:
            if 'data' in each_comment_replies_data and 'id' in each_comment_replies_data['data']: 
                get_all_comments_replies(each_comment_replies_data, subreddit_post_id, each_comment_replies_data['data']['id'], subreddit_post_name, connection, connection_cursor)
                
                
#i = 1
subreddits = ['politics', 'technology', 'tech', 'ScienceAndTechnology', 'compsci', 'bad_science_culture', 'SocietyAndCulture', 'CultureAndGenerations', 'Futurology', 'gadgets', 'Apple', 'Android', 'AskTechnology', 'AskReddit', 'programming', 'pcgaming', 'worldnews', 'science', 'cyberpunk', 'AskScience', 'dataisbeautiful']
while(True):#True: to run continuouly 
    
    #Connecting to Database Locally
    userhost = 'localhost'
    port_no = 5432
    username = 'postgres'
    database_name = 'socialgood'
    passwrd = 'socialgood'
    try:
        #connection = psycopg2.connect(host  = userhost, port = port_no, user = username, password = passwrd, dbname = database_name)
        #connection_cursor = connection.cursor()
        
        '''
        #Generating bearer token
        bearer_token = bearer_token_generation()
        #Existing this condition in order to save the new subreddits if not present in database and it will execute for only one time
        if(i == 1):
            for subreddit in subreddits:
                print(subreddit)
                #Executing the get_subreddit which will save the data of the subreddits passed
                get_subreddit(subreddit, bearer_token, connection, connection_cursor)
        ''' 
        
        
        #Adding Client ID and Authorization
        CLIENT_ID = ['client_id_1', 'client_id_2', 'client_id_3','client_id_4', 'client_id_5' ] #Update the Code Here
        CLIENT_SECRET = ['client_secret_1', 'client_secret_2','client_secret_3','client_secret_4','client_secret_5'] #Update the Code Here
        p_data = [{'grant_type' : 'password', 'username': 'reddit_user_name_1','password' : 'reddit_user_name_1_password'}, {'grant_type' : 'password', 'username': 'reddit_user_name_2','password' : 'reddit_user_name_2_password'}, {'grant_type' : 'password', 'username': 'reddit_user_name_3','password' : 'reddit_user_name_3_password'}, {'grant_type' : 'password', 'username': 'reddit_user_name_4','password' : 'reddit_user_name_4_password'}, {'grant_type' : 'password', 'username': 'reddit_user_name_5','password' : 'reddit_user_name_5_password'}] #Update the Code Here
        
        for i in range(0,len(p_data)):
            #Generating bearer token
            connection = psycopg2.connect(host  = userhost, port = port_no, user = username, password = passwrd, dbname = database_name)
            connection_cursor = connection.cursor()
            bearer_token = bearer_token_generation(CLIENT_ID[i], CLIENT_SECRET[i], p_data[i])
            for subreddit in subreddits:
                print(subreddit)
                #Executing the get_subreddit_posts which will save the data of the subreddit posts and comments and their replies passed
                get_subreddit_posts(subreddit, bearer_token, connection, connection_cursor)
                time.sleep(241) #This will decide after 121 seconds of previous execution time this will execute again for another subreddits
                #Generating bearer token
                bearer_token = bearer_token_generation(CLIENT_ID[i], CLIENT_SECRET[i], p_data[i])
        #time.sleep(14400) #7200
    except Exception as connection_error:
        print("Ooopss! There is an Issue while connecting to the Database and the Issue is : ",connection_error)
        
        