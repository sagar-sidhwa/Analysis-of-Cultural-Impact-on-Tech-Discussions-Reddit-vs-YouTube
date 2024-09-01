#Importing the Required Libraries
#from apiclient.discovery import build
from googleapiclient.discovery import build
import requests
import json
import psycopg2
import time
from datetime import datetime

#Youtube API Data collection starts here
#Function to collect the details about the speific channel
def youtube_channels(channel_name, youtube_object, connection, connection_cursor):
    youtube_channels_database_values = ()
    save_youtube_channel = 'INSERT INTO youtube_channels (yc_date_time, yc_name_title, youtube_channel_id, yc_url, yc_custom_url, yc_description, yc_data) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    check_youtube_channel = 'SELECT youtube_channel_id FROM youtube_channels'
    channel_response = youtube_object.search().list( q=channel_name, type='channel', part='id').execute()
    
    #This checks if there are any channels available
    if 'items' in channel_response: 
        for item in channel_response['items']:
            
            connection_cursor.execute(check_youtube_channel)
            existing_youtube_channels = [result[0] for result in connection_cursor.fetchall()]
            
            if item['id']['channelId'] not in existing_youtube_channels:
                channel_details = youtube_object.channels().list(part = 'snippet,statistics', id = item['id']['channelId']).execute()
                if 'items' in channel_details:
                    youtube_channels_database_values = (
                        channel_details['items'][0]['snippet']['publishedAt'], #youtube channel creation date
                        channel_details['items'][0]['snippet']['title'], #youtube channel title or name
                        channel_details['items'][0]['id'], #youtube channel id
                        'https://www.youtube.com/channel/'+channel_details['items'][0]['id'], #youtube channel url id
                        'https://www.youtube.com/'+ channel_details['items'][0]['snippet']['customUrl'], #youtube channel custom url
                        channel_details['items'][0]['snippet']['description'], #youtube channel description
                        #json.dumps(channel_details['items'][0]['statistics']), #youtube channel subscribers views video counts etc..
                        json.dumps(channel_details['items'][0]) #youtube channel data
                    )
                    connection_cursor.execute(save_youtube_channel, youtube_channels_database_values)
                    connection.commit()
                    break
    else:
        print('No Channles were found with that name :', channel_name)
        
def youtube_video_comments_replies(comment_id, video_id, channel_id, youtube_object, connection, connection_cursor):
    
    youtube_video_comments_database_values = ()
    save_youtube_video_comments = 'INSERT INTO youtube_videos_comments (ycvc_date_time, ycvcomment_id, ycvideo_id, ycv_url, youtube_channel_id, yc_url, ycvc_body, ycvc_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    check_youtube_video_comments = 'SELECT ycvcomment_id from youtube_videos_comments'
    
    video_comments_response = youtube_object.comments().list(parentId=comment_id, part='snippet', textFormat='plainText', maxResults=30).execute()

    # This checks if there are any comments found
    if 'items' in video_comments_response:
        for item in video_comments_response['items']:
            
            connection_cursor.execute(check_youtube_video_comments)
            existing_youtube_video_comments = [result[0] for result in connection_cursor.fetchall()]

            if item['id'] not in existing_youtube_video_comments:
                youtube_video_comments_database_values = (
                    item['snippet']['updatedAt'],  # youtube video comment latest updation date
                    item['id'],  # youtube video comment id
                    video_id,  # youtube channel video id
                    'https://www.youtube.com/watch?v=' + video_id,  # youtube channel video custom url
                    item['snippet']['channelId'],  # youtube video channel id
                    'https://www.youtube.com/channel/' + item['snippet']['channelId'],  # youtube channel url id
                    item['snippet']['textDisplay'],  # youtube video comment body
                    json.dumps(item)  # youtube video comment data
                )
                connection_cursor.execute(save_youtube_video_comments, youtube_video_comments_database_values)
                connection.commit()
    else:
        print("Sorry! No comments found for this specific YouTube video:", video_id)

# Function to collect the details about the new comments posted on the specific video of a channel
def youtube_video_comments(video_id, channel_id, youtube_object, connection, connection_cursor):
    youtube_video_comments_database_values = ()
    save_youtube_video_comments = 'INSERT INTO youtube_videos_comments (ycvc_date_time, ycvcomment_id, ycvideo_id, ycv_url, youtube_channel_id, yc_url, ycvc_body, ycvc_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    check_youtube_video_comments = 'SELECT ycvcomment_id from youtube_videos_comments'

    video_comments_response = youtube_object.commentThreads().list(videoId=video_id, part='snippet', textFormat='plainText', maxResults=30).execute()

    # This checks if there are any comments found
    if 'items' in video_comments_response:
        for item in video_comments_response['items']:
            
            connection_cursor.execute(check_youtube_video_comments)
            existing_youtube_video_comments = [result[0] for result in connection_cursor.fetchall()]

            if item['id'] not in existing_youtube_video_comments:
                youtube_video_comments_database_values = (
                    datetime.strptime(item['snippet']['topLevelComment']['snippet']['updatedAt'], '%Y-%m-%dT%H:%M:%SZ'),  # youtube video comment latest updation date
                    item['id'],  # youtube video comment id
                    item['snippet']['videoId'],  # youtube channel video id
                    'https://www.youtube.com/watch?v=' + item['snippet']['videoId'],  # youtube channel video custom url
                    item['snippet']['channelId'],  # youtube video channel id
                    'https://www.youtube.com/channel/' + item['snippet']['channelId'],  # youtube channel url id
                    item['snippet']['topLevelComment']['snippet']['textDisplay'],  # youtube video comment body
                    json.dumps(item)  # youtube video comment data
                )
                connection_cursor.execute(save_youtube_video_comments, youtube_video_comments_database_values)
                connection.commit()
                #This commented code fetch the replies on the specified comment but inorder to maintain the limit of the requests perday we are keeping it commented but it can be used further when applicable 
                '''
                print(item)
                '''
                if item['snippet']['totalReplyCount'] > 0:
                    youtube_video_comments_replies(item['id'],item['snippet']['videoId'], item['snippet']['channelId'], youtube_object, connection, connection_cursor)
                
            else:
                #youtube_video_comments_replies(item['id'],item['snippet']['videoId'], item['snippet']['channelId'], youtube_object, connection, connection_cursor)
                pass
    else:
        print("Sorry! No comments found for this specific YouTube video:", video_id)
        
#Function to collect the details about the new videos posted on the specific channel
def youtube_channel_videos(channel_id, youtube_object, connection, connection_cursor):
    youtube_channel_videos_database_values = ()
    save_youtube_channel_videos = 'INSERT INTO youtube_channel_videos (ycv_date_time, ycvideo_id, youtube_channel_id, yc_name_title, yc_url, ycv_name_title, ycv_url, ycv_description, ycv_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    check_youtube_channel_videos = 'SELECT ycvideo_id FROM youtube_channel_videos'
    channel_videos_response = youtube_object.search().list(channelId=channel_id, type='video', order='date', part='id', maxResults=30, q='technology OR tech OR education OR culture OR social').execute()
    #This checks if there are any videos available
    if 'items' in channel_videos_response:
        for item in channel_videos_response['items']:

            connection_cursor.execute(check_youtube_channel_videos)
            existing_youtube_channel_videos = [result[0] for result in connection_cursor.fetchall()]

            if item['id']['videoId'] not in existing_youtube_channel_videos:
                # Retrieving youtube channel latest video details using the video_id
                channel_video_details = youtube_object.videos().list(part = 'snippet,statistics,status', id = item['id']['videoId']).execute()
                if 'items' in channel_video_details:
                    #Checking that Comments are disabled for that video or not
                    if 'statistics' in channel_video_details['items'][0] and 'commentCount' in channel_video_details['items'][0]['statistics']:
                        if (channel_video_details['items'][0]['statistics']['commentCount'] != "0"):
                            youtube_channel_videos_database_values = (
                                datetime.strptime(channel_video_details['items'][0]['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'), #youtube channel video creation date
                                channel_video_details['items'][0]['id'], #youtube channel video id
                                channel_video_details['items'][0]['snippet']['channelId'], #youtube video channel id
                                channel_video_details['items'][0]['snippet']['channelTitle'], #youtube video channel title
                                'https://www.youtube.com/channel/'+channel_video_details['items'][0]['snippet']['channelId'], #youtube channel url id
                                channel_video_details['items'][0]['snippet']['title'], #youtube channel video title or name
                                'https://www.youtube.com/watch?v='+ channel_video_details['items'][0]['id'], #youtube channel video custom url
                                channel_video_details['items'][0]['snippet']['description'], #youtube channel description
                                json.dumps(channel_video_details['items'][0]) #youtube channel data 
                            )
                            connection_cursor.execute(save_youtube_channel_videos, youtube_channel_videos_database_values)
                            connection.commit()
                            youtube_video_comments(channel_video_details['items'][0]['id'], channel_video_details['items'][0]['snippet']['channelId'], youtube_object, connection, connection_cursor)
            else:
                #This condition will check like we can get the list of youtube videos for that channel which we have already added in the database so we can check whether there are any new comments or not
                #youtube_video_comments(item['id']['videoId'], channel_id, youtube_object, connection, connection_cursor)
                pass
    else:
        print("Sorry ! No videos found for this specific channel : ", channel_id)


#Function which will return the youtube object based on the key passed
def youtube_object_creation(youtube_api_key):
    youtube_object = build('youtube', 'v3', developerKey=youtube_api_key)
    return youtube_object

while(True):#True: to run continuouly 
    #Connecting to Database Locally
    userhost = 'localhost'
    port_no = 5432
    username = 'postgres'
    database_name = 'socialgood'
    passwrd = 'socialgood'
    #Saving the youtube API Key
    youtube_api_key_1 = ['youtube_api_key_1','youtube_api_key_2','youtube_api_key_3','youtube_api_key_4','youtube_api_key_5'] #Update the Code Here
    youtube_api_key_2 = ['youtube_api_key_6','youtube_api_key_7','youtube_api_key_8','youtube_api_key_9','youtube_api_key_10'] #Update the Code Here
    youtube_api_key_3 = ['youtube_api_key_11','youtube_api_key_12','youtube_api_key_13','youtube_api_key_14','youtube_api_key_15','youtube_api_key_16'] #Update the Code Here
    
    #List of Channel Names
    channel_names = ['TED','TEDx Talks', 'TED-Ed' ,'Veritasium', 'WIRED', 'Vsauce', 'Marques Brownlee', 'ColdFusion', 'Simplilearn', 'Linus Tech Tips', 'Quantum Tech HD', 'Bloomberg Technology', 'Yahoo Finance', 'The Wall Street Journal', 'CNN', 'BBC News'] #Note Here we need to pass the channel name individually other wise it will execute for other youtube channel as well
    #List of Channel ID's
    youtube_channel_list = ['UCAuUUnT6oDeKwE6v1NGQxug', 'UCsT0YIqwnpJCM-mx7-gSA4Q', 'UCsooa4yRKGN_zEE8iknghZA', 'UCHnyfMqiRRG1u-2MsSQLbXA', 'UCftwRNsjfRo08xYE31tkiyw', 'UC6nSFpj9HTCZ5t-N3Rm3-HA', 'UCBJycsmduvYEL83R_U4JriQ', 'UC4QZ_LsYcvcq7qOsOhpAX4A', 'UCsvqVGtbbyHaMoevxPAq9Fg', 'UCXuqSBlHAE6Xw-yeJA0Tunw', 'UC4Tklxku1yPcRIH0VVCKoeA', 'UCrM7B7SL_g1edFOnmj-SDKg', 'UCEAZeUIeJs0IjQiqTCdVSIg', 'UCK7tptUDHh-RYDsdxO1-5QQ', 'UCupvZG-5ko_eiXAupbDfxWw', 'UC16niRr50-MSBwiO3YDb3RA'] #Note This is the list of the youtube_channel_id's for which we are collecting data 
    api_use_1 = ['UCAuUUnT6oDeKwE6v1NGQxug', 'UCsT0YIqwnpJCM-mx7-gSA4Q', 'UCsooa4yRKGN_zEE8iknghZA', 'UCHnyfMqiRRG1u-2MsSQLbXA', 'UCftwRNsjfRo08xYE31tkiyw'] #Note This is the bifurcated list of the youtube_channel_id's for which we are collecting data 
    api_use_2 = ['UC6nSFpj9HTCZ5t-N3Rm3-HA', 'UCBJycsmduvYEL83R_U4JriQ', 'UC4QZ_LsYcvcq7qOsOhpAX4A', 'UCsvqVGtbbyHaMoevxPAq9Fg', 'UCXuqSBlHAE6Xw-yeJA0Tunw'] #Note This is the bifurcated list of the youtube_channel_id's for which we are collecting data
    api_use_3 = ['UC4Tklxku1yPcRIH0VVCKoeA', 'UCrM7B7SL_g1edFOnmj-SDKg', 'UCEAZeUIeJs0IjQiqTCdVSIg', 'UCK7tptUDHh-RYDsdxO1-5QQ', 'UCupvZG-5ko_eiXAupbDfxWw', 'UC16niRr50-MSBwiO3YDb3RA'] #Note This is the bifurcated list of the youtube_channel_id's for which we are collecting data
    try:
        connection = psycopg2.connect(host  = userhost, port = port_no, user = username, password = passwrd, dbname = database_name)
        connection_cursor = connection.cursor()
         
        '''
        if (i == 1):
            #Executing the youtube_channels which will save the data of the youtube channels names passed passed
            for channel_name in channel_names:
                youtube_channels(channel_name, youtube_object, connection, connection_cursor)
        #This section of code will iterate through the each channel and it will collect the latest youtube data for that channel
        
        '''
        for i in range(0,len(youtube_api_key_1)):
            
            #Creating the youtube resource object 
            youtube_object_1 = youtube_object_creation(youtube_api_key_1[i]) #Initially it will be youtube_api_key_1
            for each_youtube_channel_id in youtube_channel_list:
                #youtube_channel_videos(each_youtube_channel_id, youtube_object, connection, connection_cursor)
                if each_youtube_channel_id in api_use_1:
                    print(each_youtube_channel_id)
                    youtube_object = youtube_object_1
                    youtube_channel_videos(each_youtube_channel_id, youtube_object, connection, connection_cursor)
                    
            time.sleep(1800) #This will decide after how much time this will execute again
            
            youtube_object_2 = youtube_object_creation(youtube_api_key_2[i]) #Then it will be youtube_api_key_2 
            for each_youtube_channel_id in youtube_channel_list:
                if each_youtube_channel_id in api_use_2:
                    print(each_youtube_channel_id)
                    youtube_object = youtube_object_2
                    youtube_channel_videos(each_youtube_channel_id, youtube_object, connection, connection_cursor)
                    
            time.sleep(1800) #This will decide after how much time this will execute again
            
            youtube_object_3 = youtube_object_creation(youtube_api_key_3[i]) #Initially and then it will be youtube_api_key_3
            for each_youtube_channel_id in youtube_channel_list:
                if each_youtube_channel_id in api_use_3:
                    print(each_youtube_channel_id)
                    youtube_object = youtube_object_3
                    youtube_channel_videos(each_youtube_channel_id, youtube_object, connection, connection_cursor)
            time.sleep(3600) #This will decide after how much time this will execute again
            
        time.sleep(7200) #This will decide after how much time this will execute again
    except Exception as connection_error:
        print("Ooopss! There is an Issue while connecting to the Database and the Issue is : ",connection_error)