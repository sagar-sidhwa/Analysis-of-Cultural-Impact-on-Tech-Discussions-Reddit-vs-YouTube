from django.shortcuts import render, HttpResponse, redirect
#Importing the Libraries
import numpy as np
import pandas as pd
import nltk
import json
import datetime
from io import BytesIO
import base64
nltk.download('punkt')
nltk.download('stopwords')
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt
import ast
from tabulate import tabulate
from django.db import connection
from django.conf import settings
from django.http import JsonResponse
import spacy
from itertools import cycle
from collections import Counter
from random import sample
#from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
import os

cache.clear()

def socialgoodhome(request):
    cache.clear()
    return render(request, 'index.html')

def demoanalysis(request):
    cache.clear()
    return render(request, 'demoanalysis.html')

def analysis(request):
    cache.clear()
    return render(request, 'analysis.html')

def fda_varying_analysis(request):
    if request.method == 'POST':
        date = request.POST.get('start')
        option = request.POST.get('option')
        if option == 'subreddit_posts':
            df_name = 'subreddit_posts'
            column_name = 'post_title'
            dt_column = 'post_date_time'
            title = 'Most Used Words in Subreddits Posts on ('+date+')'
        if option == 'subreddit_comments':
            df_name = 'subreddit_posts_comments'
            column_name = 'comment_body'
            dt_column = 'comment_date_time'
            title = 'Most Used Words in Subreddits Comments on ('+date+')'
        if option == 'youtube_videos':
            df_name = 'youtube_channel_videos'
            column_name = 'ycv_description'
            dt_column = 'ycv_date_time'
            title = 'Most Used Words in Youtube Videos on ('+date+')'
        if option == 'youtube_comments':
            df_name = 'youtube_videos_comments'
            column_name = 'ycvc_body'
            dt_column = 'ycvc_date_time'
            title = 'Most Used Words in Youtube Comments on ('+date+')'
        #content_query = "SELECT * FROM "+df_name+' WHERE to_char('+dt_column+', \'YYYY-MM-DD\') LIKE '+date+'%'
        content_query = "SELECT * FROM " + df_name + " WHERE to_char(" + dt_column + ", 'YYYY-MM-DD') LIKE '" + date + "%'"
        connection_cursor = connection.cursor()
        connection_cursor.execute(content_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df = pd.DataFrame(rows, columns=colnames)
        titles = df[column_name].tolist()  # Assuming 'post_title' is the column name
        print("Len :",len(titles))
        if len(titles) != 0:
            words = nltk.word_tokenize(' '.join(titles).lower())
            words = [word for word in words if word.isalpha() and word not in nltk.corpus.stopwords.words('english')]
            word_freq = Counter(words)
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(title)
            #plt.savefig(img_name+'.jpg')
            #plt.show()
            
            existing_image_path = os.path.join(settings.BASE_DIR, 'static/fda.jpg')  # Replace with your image path
            print(existing_image_path)
            # Check if the image exists and delete it
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)
            cache.clear()
            
            static_path = settings.BASE_DIR / 'static'
            figure_path = static_path / 'fda.jpg'

            plt.savefig(str(figure_path))
            
            image_stream = BytesIO()
            #plt.savefig(image_stream, format='png')
            plt.close()
        else:
            # Create an empty image with zeros (black pixels)
            width, height = 512, 512
            empty_image = np.ones((height, width, 3), dtype=np.uint8)*255

            # Display the empty image
            plt.imshow(empty_image)
            plt.axis('off')  # Turn off axis labels
            
            static_path = settings.BASE_DIR / 'static'
            figure_path = static_path / 'fda.jpg'

            plt.savefig(str(figure_path))
            
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()
    cache.clear()
    return render(request, 'analysis.html')
    #return redirect('analysis')

def return_table_column(option):
    if option == 'subreddit_posts':
        column_name = 'post_title'
        dt_column = 'post_date_time'
        return column_name,dt_column
    if option == 'subreddit_posts_comments':
        column_name = 'comment_body'
        dt_column = 'comment_date_time'
        return column_name,dt_column
    if option == 'youtube_channel_videos':
        column_name = 'ycv_name_title'
        dt_column = 'ycv_date_time'
        return column_name,dt_column
    if option == 'youtube_videos_comments':
        column_name = 'ycvc_body'
        dt_column = 'ycvc_date_time'
        return column_name,dt_column
    
nlp = spacy.load('en_core_web_sm')
def extract_keywords(text):
    # Load spaCy model
    # Function to extract keywords/topics from a text
    doc = nlp(text)
    print("Length of Text", len(text))
    print("Applying Data")
    return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    
def fdb_varying_analysis(request):
    if request.method == 'POST':
        date = request.POST.get('start2')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        column_name1, dt_column1 = return_table_column(option1)
        column_name2, dt_column2 = return_table_column(option2)
        
        content_query1 = "SELECT * FROM " + option1 + " WHERE to_char(" + dt_column1 + ", 'YYYY-MM-DD') LIKE '" + date + "%'"
        content_query2 = "SELECT * FROM " + option2 + " WHERE to_char(" + dt_column2 + ", 'YYYY-MM-DD') LIKE '" + date + "%'"
        
        connection_cursor = connection.cursor()
        
        connection_cursor.execute(content_query1)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df1 = pd.DataFrame(rows, columns=colnames)
        rows1_count = len(rows)
        
        print("Len Row 1: ",rows1_count)
        
        connection_cursor.execute(content_query2)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df2 = pd.DataFrame(rows, columns=colnames)
        rows2_count = len(rows)
        
        print("Len Row 2: ",rows2_count)
        
        print(column_name1,column_name2)
        # Assuming 'post_title' is the column name
        if (rows1_count != 0) and (rows2_count != 0):
            # Extract sets of keywords
            # Apply the function to each DataFrame
            print("Column Length",len(df1[column_name1]))
            df1['Keywords'] = df1[column_name1].apply(extract_keywords)
            print("Applied 1 Keyword")

            df2['Keywords'] = df2[column_name2].apply(extract_keywords)
            print("Applied 2 Keyword")
            
            keywords_set_df1 = set([keyword for keywords in df1['Keywords'] for keyword in keywords])
            print("Keyword Found One")
            
            keywords_set_df2 = set([keyword for keywords in df2['Keywords'] for keyword in keywords])
            print("Keyword Found Tow")
            
            # Find common keywords
            common_keywords = keywords_set_df1.intersection(keywords_set_df2)
            print("Intersection Done One")
            
            # Count occurrences of common words
            word_counts = {}
            for word in common_keywords:
                word_counts[word] = df1['Keywords'].apply(lambda x: word in x).sum() + df2['Keywords'].apply(lambda x: word in x).sum()

            plt.figure(figsize=(15, 10))
            top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:30]

            # Create a bar chart for the top 20 words
            top_words_dict = dict(top_words)
            
            # Get a set of distinct colors
            #colors = plt.cm.viridis_r.colors #old

            # Create a cycling iterator of colors
            #color_cycle = cycle(colors) #old
            
            # Get a list of distinct colors
            num_colors = len(top_words_dict)
            distinct_colors = sample(range(num_colors), num_colors)
            
            
            #plt.bar(top_words_dict.keys(), top_words_dict.values(),color=[next(color_cycle) for _ in range(len(top_words_dict))]) #Old
            plt.bar(top_words_dict.keys(), top_words_dict.values(),color=plt.cm.viridis(distinct_colors))
            plt.xlabel('Most Used Common Words')
            plt.ylabel('Frequency')
            plt.title('Top 30 Common Words on ({})'.format(date))
            plt.xticks(rotation=45, ha='right')
            #plt.show()
            #plt.title(title)
            #plt.savefig(img_name+'.jpg')
            #plt.show()
            
            existing_image_path = os.path.join(settings.BASE_DIR, 'static/fdb.jpg')  # Replace with your image path
            print(existing_image_path)
            # Check if the image exists and delete it
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)
            cache.clear()
            
            static_path = settings.BASE_DIR / 'static'
            figure_path = static_path / 'fdb.jpg'

            plt.savefig(str(figure_path))
            
            image_stream = BytesIO()
            #plt.savefig(image_stream, format='png')
            plt.close()
        else:
            # Create an empty image with zeros (black pixels)
            width, height = 512, 512
            empty_image = np.ones((height, width, 3), dtype=np.uint8)*255

            # Display the empty image
            plt.imshow(empty_image)
            plt.axis('off')  # Turn off axis labels
            
            static_path = settings.BASE_DIR / 'static'
            figure_path = static_path / 'fdb.jpg'

            plt.savefig(str(figure_path))
            
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()
    cache.clear()
    return render(request, 'analysis.html')
    #return redirect('analysis')

def fdc_varying_analysis(request):
    if request.method == 'POST':
        date = request.POST.get('cstart2')
        option1 = request.POST.get('coption1')
        option2 = request.POST.get('coption2')
        column_name1, dt_column1 = return_table_column(option1)
        column_name2, dt_column2 = return_table_column(option2)
        
        content_query1 = "SELECT * FROM " + option1 + " WHERE to_char(" + dt_column1 + ", 'YYYY-MM-DD') LIKE '" + date + "%'"
        content_query2 = "SELECT * FROM " + option2 + " WHERE to_char(" + dt_column2 + ", 'YYYY-MM-DD') LIKE '" + date + "%'"
        
        connection_cursor = connection.cursor()
        
        connection_cursor.execute(content_query1)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df1 = pd.DataFrame(rows, columns=colnames)
        rows1_count = len(rows)
        
        connection_cursor.execute(content_query2)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df2 = pd.DataFrame(rows, columns=colnames)
        rows2_count = len(rows)
        
        if (rows1_count != 0) and (rows2_count != 0):
            # Assuming you have dataframes df1 and df2
            total_rows_df1 = len(df1)
            total_rows_df2 = len(df2)
            plt.figure(figsize=(6, 10))
            # Create a bar graph
            plt.bar([option1+'\n('+column_name1+')',option2+'\n('+column_name2+')'], [total_rows_df1, total_rows_df2], color=['#6d05ff', '#e01631'])
            #plt.bar([option1, option2], [total_rows_df1, total_rows_df2], color=['#6d05ff', '#e01631'])

            for i, count in enumerate([total_rows_df1, total_rows_df2]):
                plt.text(i, count + 0.005 * max(total_rows_df1, total_rows_df2), str(count), ha='center', va='bottom')

            # Display percentages above the bars
            total_rows_sum = total_rows_df1 + total_rows_df2
            percent_df1 = (total_rows_df1 / total_rows_sum) * 100
            percent_df2 = (total_rows_df2 / total_rows_sum) * 100

            plt.text(0, total_rows_df1 + 0.025 * max(total_rows_df1, total_rows_df2), f'{percent_df1:.2f}%', ha='center', va='bottom')
            plt.text(1, total_rows_df2 + 0.025 * max(total_rows_df1, total_rows_df2), f'{percent_df2:.2f}%', ha='center', va='bottom')

            # Set labels and title
            plt.xlabel('Social Media Platform')
            plt.ylabel('Total Count of User Engagement across Platforms')
            plt.title('User Engagement Across Social Media Platforms On- ({})'.format(date))

            # Show the plot
            #plt.show()
            existing_image_path = os.path.join(settings.BASE_DIR, 'static/fdc.jpg')  # Replace with your image path
            print(existing_image_path)
            # Check if the image exists and delete it
            if os.path.exists(existing_image_path):
                os.remove(existing_image_path)
            cache.clear()
            
            static_path = settings.BASE_DIR / 'static'
            figure_path = static_path / 'fdc.jpg'

            plt.savefig(str(figure_path))
            
            image_stream = BytesIO()
            #plt.savefig(image_stream, format='png')
            plt.close()
        else:
            # Create an empty image with zeros (black pixels)
            width, height = 512, 512
            empty_image = np.ones((height, width, 3), dtype=np.uint8)*255

            # Display the empty image
            plt.imshow(empty_image)
            plt.axis('off')  # Turn off axis labels
            
            static_path = settings.BASE_DIR / 'static'
            figure_path = static_path / 'fdc.jpg'

            plt.savefig(str(figure_path))
            
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()  
    cache.clear()    
    return render(request, 'analysis.html')

def post_video_data_count(request):
    if request.method == 'GET':
        subreddit_posts_query = "SELECT * FROM subreddit_posts"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_posts_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit_posts = pd.DataFrame(rows, columns=colnames)
        
        youtube_channel_videos_query = "SELECT * FROM youtube_channel_videos"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_channel_videos_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_channel_videos = pd.DataFrame(rows, columns=colnames)
        
        # Assuming your DataFrame is named df and 'date_time' is the column containing date-time values
        subreddit_posts['post_date_time'] = pd.to_datetime(subreddit_posts['post_date_time'])
        youtube_channel_videos['ycv_date_time'] = pd.to_datetime(youtube_channel_videos['ycv_date_time'])
        subreddit_posts['post_date'] = subreddit_posts['post_date_time'].dt.date
        youtube_channel_videos['ycv_date'] = youtube_channel_videos['ycv_date_time'].dt.date
        dates_till_now =  subreddit_posts['post_date_time'].dt.date.unique()
        
        # Count the number of rows for each unique date present in 'dates_till_now'
        reddit_posts_daily_counts = subreddit_posts[subreddit_posts['post_date'].isin(dates_till_now)].groupby('post_date').size().reset_index(name='post_count')
        youtube_videos_daily_counts = youtube_channel_videos[youtube_channel_videos['ycv_date'].isin(dates_till_now)].groupby('ycv_date').size().reset_index(name='video_count')

        # Plotting
        plt.figure(figsize=(12, 6))
        #reddit_posts_daily_counts.plot(kind='line', marker='o', linestyle='-', color='blue', label='Reddit Posts Daily Counts')
        #youtube_videos_daily_counts.plot(kind='line', marker='o', linestyle='-', color='red', label='YouTube Videos Daily Counts')
        plt.plot(reddit_posts_daily_counts['post_date'], reddit_posts_daily_counts['post_count'], marker='o', linestyle='-', color='blue', label='Reddit Posts Daily Counts')
        plt.plot(youtube_videos_daily_counts['ycv_date'], youtube_videos_daily_counts['video_count'], marker='o', linestyle='-', color='red', label='YouTube Videos Daily Counts')
        plt.title('Reddit Posts Count vs Youtube Video Count (Number of New Entries per Day)')
        plt.xlabel('Date (Starting 1st November)')
        plt.ylabel('Count')
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.legend()
        #plt.savefig('Reddit Posts Count vs Youtube Video Count (Number of New Entries per Day).jpg')
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/da.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
            
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'da.jpg'
        #print(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg')
        #plt.savefig(str(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg'))
        plt.savefig(str(figure_path))
        # Convert the plot to an image and embed it in the response
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        
        plt.close()

        image_stream.seek(0)
        post_video_data_count_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return post_video_data_count_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})


def reddit_vs_youtube_comment_count(request):
    if request.method == 'GET':
        subreddit_posts_comments_query = "SELECT * FROM subreddit_posts_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_posts_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit_posts_comments = pd.DataFrame(rows, columns=colnames)
        
        youtube_videos_comments_query = "SELECT * FROM youtube_videos_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_videos_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_videos_comments = pd.DataFrame(rows, columns=colnames)
        
        # Assuming your DataFrame is named df and 'date_time' is the column containing date-time values
        subreddit_posts_comments['comment_date_time'] = pd.to_datetime(subreddit_posts_comments['comment_date_time'], errors='coerce')
        youtube_videos_comments['ycvc_date_time'] = pd.to_datetime(youtube_videos_comments['ycvc_date_time'])
        subreddit_posts_comments['comment_date']= subreddit_posts_comments['comment_date_time'].dt.date
        youtube_videos_comments['ycvc_date'] = youtube_videos_comments['ycvc_date_time'].dt.date
        comments_dates_till_now =  subreddit_posts_comments['comment_date_time'].dt.date.unique()
        
        # Count the number of rows for each unique date present in 'dates_till_now'
        reddit_comments_daily_counts = subreddit_posts_comments[subreddit_posts_comments['comment_date'].isin(comments_dates_till_now)].groupby('comment_date').size().reset_index(name='reddit_comment_count')
        youtube_comments_daily_counts = youtube_videos_comments[youtube_videos_comments['ycvc_date'].isin(comments_dates_till_now)].groupby('ycvc_date').size().reset_index(name='youtube_comment_count')

        # Plotting
        plt.figure(figsize=(12, 6))
        #reddit_posts_daily_counts.plot(kind='line', marker='o', linestyle='-', color='blue', label='Reddit Posts Daily Counts')
        #youtube_videos_daily_counts.plot(kind='line', marker='o', linestyle='-', color='red', label='YouTube Videos Daily Counts')
        plt.plot(reddit_comments_daily_counts['comment_date'], reddit_comments_daily_counts['reddit_comment_count'], marker='o', linestyle='-', color='darkblue', label='Reddit Comments Daily Counts')
        plt.plot(youtube_comments_daily_counts['ycvc_date'], youtube_comments_daily_counts['youtube_comment_count'], marker='o', linestyle='-', color='darkorange', label='YouTube Comments Daily Counts')
        plt.title('Reddit Comments Count vs Youtube Video Comments Count (Number of New Entries per Day)')
        plt.xlabel('Date (Starting 1st November)')
        plt.ylabel('Comments Count')
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.legend()
        #plt.savefig('Reddit Comments Count vs Youtube Video Comments Count (Number of New Entries per Day).jpg')
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/db.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'db.jpg'
        #print(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg')
        #plt.savefig(str(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg'))
        plt.savefig(str(figure_path))
        
        # Convert the plot to an image and embed it in the response
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        reddit_vs_youtube_comment_count_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return reddit_vs_youtube_comment_count_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})


def reddit_posts_ModerateHatespeech(request):
    if request.method == 'GET':
        subreddit_posts_query = "SELECT * FROM subreddit_posts"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_posts_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit_posts = pd.DataFrame(rows, columns=colnames)
        # Plotting the histogram
        plt.figure(figsize=(6, 10))
        
        # Count occurrences of 'yes' and 'no'
        subreddt_posts_flag_counts = subreddit_posts['post_class'].replace('', pd.NA).fillna('normal').value_counts()
        
        print(subreddt_posts_flag_counts)
        
        # Plotting the histogram
        bars = plt.bar(subreddt_posts_flag_counts.index, subreddt_posts_flag_counts.values, color=['green', 'red'])
        
        # Annotate each bar with count and ratio
        for bar, count in zip(bars, subreddt_posts_flag_counts.values):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{count}\n({count / len(subreddit_posts):.2%})', ha='center', va='bottom')
        # Customize the plot
        plt.title('Classification of Reddit Posts from ModerateHatespeech')
        plt.xlabel('ModerateHatespeech (Normal / Flag)')
        plt.ylabel('Total Count')
        #plt.legend()
        #plt.savefig('Classification of Reddit Posts from ModerateHatespeech.jpg')
        # Display the plot
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/dc.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'dc.jpg'
        plt.savefig(str(figure_path))
        # Convert the plot to an image and embed it in the response
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        reddit_posts_ModerateHatespeech_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return reddit_posts_ModerateHatespeech_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})

def youtube_videos_ModerateHatespeech(request):
    if request.method == 'GET':
        youtube_channel_videos_query = "SELECT * FROM youtube_channel_videos"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_channel_videos_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_channel_videos = pd.DataFrame(rows, columns=colnames)
        
        # Plotting the histogram
        plt.figure(figsize=(6, 10))
        
        # Count occurrences of 'yes' and 'no'
        youtube_videos_flag_counts = youtube_channel_videos['ycv_class'].replace('', pd.NA).fillna('normal').value_counts()
        
        # Plotting the histogram
        bars = plt.bar(youtube_videos_flag_counts.index, youtube_videos_flag_counts.values, color=['blue', 'red'])
        
        # Annotate each bar with count and ratio
        for bar, count in zip(bars, youtube_videos_flag_counts.values):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{count}\n({count / len(youtube_channel_videos):.2%})', ha='center', va='bottom')
        # Customize the plot
        plt.title('Classification of Youtube Videos from ModerateHatespeech')
        plt.xlabel('ModerateHatespeech (Normal / Flag)')
        plt.ylabel('Total Count')
        #plt.legend()
        #plt.savefig('Classification of Youtube Videos from ModerateHatespeech.jpg')
        # Display the plot
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/dd.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'dd.jpg'
        plt.savefig(str(figure_path))
        
        # Convert the plot to an image and embed it in the response
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        youtube_videos_ModerateHatespeech_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return youtube_videos_ModerateHatespeech_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})

def reddit_comments_ModerateHatespeech(request):
    if request.method == 'GET':
        subreddit_posts_comments_query = "SELECT * FROM subreddit_posts_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_posts_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit_posts_comments = pd.DataFrame(rows, columns=colnames)
        # Plotting the histogram
        plt.figure(figsize=(6, 10))
        
        # Count occurrences of 'yes' and 'no'
        subreddt_comment_flag_counts = subreddit_posts_comments['comment_class'].replace('', pd.NA).fillna('normal').value_counts()
        
        # Plotting the histogram
        bars = plt.bar(subreddt_comment_flag_counts.index, subreddt_comment_flag_counts.values, color=['green', 'red'])
        
        # Annotate each bar with count and ratio
        for bar, count in zip(bars, subreddt_comment_flag_counts.values):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{count}\n({count / len(subreddit_posts_comments):.2%})', ha='center', va='bottom')
        # Customize the plot
        plt.title('Classification of Reddit Comments from ModerateHatespeech')
        plt.xlabel('ModerateHatespeech (Normal / Flag)')
        plt.ylabel('Total Count')
        #plt.legend()
        #plt.savefig('Classification of Reddit Comments from ModerateHatespeech.jpg')
        # Display the plot
        #plt.show()
        # Convert the plot to an image and embed it in the response
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/de.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'de.jpg'

        plt.savefig(str(figure_path))
        
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        reddit_comments_ModerateHatespeech_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return reddit_comments_ModerateHatespeech_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})

def youtube_comments_ModerateHatespeech(request):
    if request.method == 'GET':
        youtube_videos_comments_query = "SELECT * FROM youtube_videos_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_videos_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_videos_comments = pd.DataFrame(rows, columns=colnames)
        #Plotting the histogram
        plt.figure(figsize=(6, 10))
        
        # Count occurrences of 'yes' and 'no'
        youtube_comment_flag_counts = youtube_videos_comments['ycvc_class'].replace('', pd.NA).fillna('normal').value_counts()
        
        # Plotting the histogram
        bars = plt.bar(youtube_comment_flag_counts.index, youtube_comment_flag_counts.values, color=['darkcyan', 'red'])
        
        # Annotate each bar with count and ratio
        for bar, count in zip(bars, youtube_comment_flag_counts.values):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{count}\n({count / len(youtube_videos_comments):.2%})', ha='center', va='bottom')
        # Customize the plot
        plt.title('Classification of Youtube Comments from ModerateHatespeech')
        plt.xlabel('ModerateHatespeech (Normal / Flag)')
        plt.ylabel('Total Count')
        #plt.legend()
        #plt.savefig('Classification of Youtube Comments from ModerateHatespeech.jpg')
        # Display the plot
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/df.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'df.jpg'
        plt.savefig(str(figure_path))
        
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        youtube_comments_ModerateHatespeech_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return youtube_comments_ModerateHatespeech_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})
    

def reddit_content_popularity_analysis(request):
    if request.method == 'GET':
        df_name = 'subreddit_posts'
        column_name = 'post_title'
        title = 'Reddit Posts Content Popularity Analysis'
        content_query = "SELECT * FROM "+df_name
        connection_cursor = connection.cursor()
        connection_cursor.execute(content_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df = pd.DataFrame(rows, columns=colnames)
        titles = df[column_name].tolist()  # Assuming 'post_title' is the column name
        words = nltk.word_tokenize(' '.join(titles).lower())
        words = [word for word in words if word.isalpha() and word not in nltk.corpus.stopwords.words('english')]
        word_freq = Counter(words)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        #plt.savefig(img_name+'.jpg')
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/dg.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'dg.jpg'

        plt.savefig(str(figure_path))
        
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        content_popularity_analysis_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return content_popularity_analysis_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})

def youtube_content_popularity_analysis(request):
    if request.method == 'GET':
        df_name = 'youtube_channel_videos'
        column_name = 'ycv_name_title'
        title = 'Youtube Videos Content Popularity Analysis'
        content_query = "SELECT * FROM "+df_name
        connection_cursor = connection.cursor()
        connection_cursor.execute(content_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        df = pd.DataFrame(rows, columns=colnames)
        titles = df[column_name].tolist()  # Assuming 'post_title' is the column name
        words = nltk.word_tokenize(' '.join(titles).lower())
        words = [word for word in words if word.isalpha() and word not in nltk.corpus.stopwords.words('english')]
        word_freq = Counter(words)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        #plt.savefig(img_name+'.jpg')
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/dh.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'dh.jpg'

        plt.savefig(str(figure_path))
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        content_popularity_analysis_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return content_popularity_analysis_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})


def sentiment_analysis(request):
    if request.method == 'GET':
        # Categorize sentiments
        print("Pass sentiment_analysis")
        subreddit_posts_comments_query = "SELECT * FROM subreddit_posts_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_posts_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit_posts_comments = pd.DataFrame(rows, columns=colnames)
            
        youtube_videos_comments_query = "SELECT * FROM youtube_videos_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_videos_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_videos_comments = pd.DataFrame(rows, columns=colnames)

        comments = subreddit_posts_comments['comment_body'].tolist() + youtube_videos_comments['ycvc_body'].tolist()
        positive, negative, neutral = 0, 0, 0
        for comment in comments:
            analysis = TextBlob(str(comment))
            if analysis.sentiment.polarity > 0:
                positive += 1
            elif analysis.sentiment.polarity < 0:
                negative += 1
            else:
                neutral += 1

        # Data to plot
        categories = ['Positive', 'Negative', 'Neutral']
        counts = [positive, negative, neutral]
        colors = ['green', 'red', 'blue']

        # Plot
        plt.bar(categories, counts, color=colors)
        plt.title('Sentiment Analysis of Reddit Comments and Youtube Comments')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Sentiment Polarity Count')
        plt.savefig('Sentiment Analysis of Reddit Comments and Youtube Comments.jpg')
        # Display the plot
        #plt.show()
        #return counts
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/di.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'di.jpg'
        plt.savefig(str(figure_path))
        
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        sentiment_analysis_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return sentiment_analysis_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})

def subreddit_engagement_metrics_analysis(request):
    if request.method == 'GET':
        print("Pass subreddit_engagement_metrics_analysis")
        
        subreddit_query = "SELECT * FROM subreddits"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit = pd.DataFrame(rows, columns=colnames)

        subreddit_posts_comments_query = "SELECT * FROM subreddit_posts_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(subreddit_posts_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        subreddit_posts_comments = pd.DataFrame(rows, columns=colnames)
        # Assuming 'subreddit_id', 'subreddit_subscribers', and 'comment_id' columns exist in your DataFrame
        # Merge the dataframes on 'subreddit_id'
        plt.figure(figsize=(10,20))
        subreddit_merged_df = pd.merge(subreddit_posts_comments, subreddit, on='subreddit_id', how='inner')
        grouped_data = subreddit_merged_df.groupby('subreddit_id').agg({'subreddit_subscribers': 'first', 'comment_id': 'count'}).reset_index()
        grouped_data.columns = ['subreddit_id', 'subscribers', 'comment_count']
        sns.pairplot(grouped_data[['subscribers', 'comment_count']])
        plt.xlabel('Subreddit Engagement Metrics Analysis (Engagement of Subscribers with respect to Comments)')
        #plt.savefig('Subreddit Engagement Metrics Analysis.jpg')
        plt.suptitle('Subreddit Engagement Metrics Analysis (Engagement of Subscribers with respect to Comments)', y=-0.05, va='bottom')  # Adjust the y parameter for positioning
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/dj.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'dj.jpg'
        plt.savefig(str(figure_path))
        
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        subreddit_engagement_metrics_analysis_image = base64.b64encode(image_stream.read()).decode('utf-8')
        #return subreddit_engagement_metrics_analysis_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})

def youtube_engagement_metrics_analysis(request):
    if request.method == 'GET':
        print("Pass youtube_engagement_metrics_analysis")
        
        youtube_channels_query = "SELECT * FROM youtube_channels"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_channels_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_channels = pd.DataFrame(rows, columns=colnames)

        youtube_videos_comments_query = "SELECT * FROM youtube_videos_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_videos_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_videos_comments = pd.DataFrame(rows, columns=colnames)

        # Merge the dataframes on 'youtube_channel_id'
        yc = youtube_channels.copy()
        # Extract 'subscribers' from 'yc_data'
        print(type(yc['yc_data'][0]))
        subscribers = yc['yc_data'].apply(lambda x: int(x['statistics']['subscriberCount']))

        # Update the DataFrame with 'subscribers'
        yc['subscribers'] = subscribers
        youtube_merged_df = pd.merge(youtube_videos_comments, yc, on='youtube_channel_id', how='inner')
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Group data and plot
        grouped_data = youtube_merged_df.groupby('youtube_channel_id').agg({'subscribers': 'first', 'ycvcomment_id': 'count'}).reset_index()
        grouped_data.columns = ['youtube_channel_id', 'subscribers', 'comment_count']
        sns.pairplot(grouped_data[['subscribers', 'comment_count']])
        plt.xlabel('Subreddit Engagement Metrics Analysis (Engagement of Subscribers with respect to Comments)')
        # Save the figure to the static folder
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'Youtube_Engagement_Metrics_Analysis.jpg'
        #print(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg')
        #plt.savefig(str(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg'))
        plt.savefig(str(figure_path))
        plt.suptitle('Youtube Engagement Metrics Analysis (Engagement of Subscribers with respect to Comments)', y=-0.05, va='bottom')
        #plt.show()
        existing_image_path = os.path.join(settings.BASE_DIR, 'static/dk.jpg')  # Replace with your image path
        print(existing_image_path)
            # Check if the image exists and delete it
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
        cache.clear()
        
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'dk.jpg'

        plt.savefig(str(figure_path))
        image_stream = BytesIO()
        #plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        youtube_engagement_metrics_analysis_image = base64.b64encode(image_stream.read()).decode('utf-8')
        print("Pass")
        #return youtube_engagement_metrics_analysis_image
    cache.clear()
    return JsonResponse({'Success': 'Success request method'})
    


#Global Variables
'''
subreddit_query = "SELECT * FROM subreddits"
connection_cursor = connection.cursor()
connection_cursor.execute(subreddit_query)
rows = connection_cursor.fetchall()
colnames = [column[0] for column in connection_cursor.description]
subreddit = pd.DataFrame(rows, columns=colnames)

youtube_channels_query = "SELECT * FROM youtube_channels"
connection_cursor = connection.cursor()
connection_cursor.execute(youtube_channels_query)
rows = connection_cursor.fetchall()
colnames = [column[0] for column in connection_cursor.description]
youtube_channels = pd.DataFrame(rows, columns=colnames)

subreddit_posts_query = "SELECT * FROM subreddit_posts"
connection_cursor = connection.cursor()
connection_cursor.execute(subreddit_posts_query)
rows = connection_cursor.fetchall()
colnames = [column[0] for column in connection_cursor.description]
subreddit_posts = pd.DataFrame(rows, columns=colnames)
    
youtube_channel_videos_query = "SELECT * FROM youtube_channel_videos"
connection_cursor = connection.cursor()
connection_cursor.execute(youtube_channel_videos_query)
rows = connection_cursor.fetchall()
colnames = [column[0] for column in connection_cursor.description]
youtube_channel_videos = pd.DataFrame(rows, columns=colnames)

subreddit_posts_comments_query = "SELECT * FROM subreddit_posts_comments"
connection_cursor = connection.cursor()
connection_cursor.execute(subreddit_posts_comments_query)
rows = connection_cursor.fetchall()
colnames = [column[0] for column in connection_cursor.description]
subreddit_posts_comments = pd.DataFrame(rows, columns=colnames)
    
youtube_videos_comments_query = "SELECT * FROM youtube_videos_comments"
connection_cursor = connection.cursor()
connection_cursor.execute(youtube_videos_comments_query)
rows = connection_cursor.fetchall()
colnames = [column[0] for column in connection_cursor.description]
youtube_videos_comments = pd.DataFrame(rows, columns=colnames)
'''
# Create your views here.
'''
def index(request):
    #return HttpResponse("This is Index Page")
    return render(request, 'index.html')
    
    
def fdemoanalysis(request):
    post_video_data_count_image = post_video_data_count()
    reddit_vs_youtube_comment_count_image = reddit_vs_youtube_comment_count()
    reddit_posts_ModerateHatespeech_image = reddit_posts_ModerateHatespeech()
    youtube_videos_ModerateHatespeech_image = youtube_videos_ModerateHatespeech()
    reddit_comments_ModerateHatespeech_image = reddit_comments_ModerateHatespeech()
    youtube_comments_ModerateHatespeech_image = youtube_comments_ModerateHatespeech()
    reddit_content_popularity_analysis_image = content_popularity_analysis('subreddit_posts', 'post_title', 'Reddit Posts Content Popularity Analysis')
    youtube_content_popularity_analysis_image = content_popularity_analysis('youtube_channel_videos', 'ycv_name_title', 'Youtube Videos Content Popularity Analysis')

    #sentiment_analysis_image = sentiment_analysis()
    #subreddit_engagement_metrics_analysis_image = subreddit_engagement_metrics_analysis()
    youtube_engagement_metrics_analysis_image = youtube_engagement_metrics_analysis()

    images = [
        #post_video_data_count_image,
        #reddit_vs_youtube_comment_count_image,
        #reddit_posts_ModerateHatespeech_image,
        #youtube_videos_ModerateHatespeech_image,
        #reddit_comments_ModerateHatespeech_image,
        #youtube_comments_ModerateHatespeech_image,
        #reddit_content_popularity_analysis_image,
        #youtube_content_popularity_analysis_image,
        #sentiment_analysis_image,
        #subreddit_engagement_metrics_analysis_image,
        youtube_engagement_metrics_analysis_image
    ]

    # Pass the graph data to the template
    #context = {'graph_data_list': graph_data_list}
    
    # Render the template
    demoanalysis_images = {'images':images}
    return render(request, 'test.html', demoanalysis_images)




def details(request):
    if request.method == 'GET':
        print("Pass youtube_engagement_metrics_analysis")
        
        youtube_channels_query = "SELECT * FROM youtube_channels"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_channels_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_channels = pd.DataFrame(rows, columns=colnames)

        youtube_videos_comments_query = "SELECT * FROM youtube_videos_comments"
        connection_cursor = connection.cursor()
        connection_cursor.execute(youtube_videos_comments_query)
        rows = connection_cursor.fetchall()
        colnames = [column[0] for column in connection_cursor.description]
        youtube_videos_comments = pd.DataFrame(rows, columns=colnames)

        # Merge the dataframes on 'youtube_channel_id'
        yc = youtube_channels.copy()
        # Extract 'subscribers' from 'yc_data'
        print(type(yc['yc_data'][0]))
        subscribers = yc['yc_data'].apply(lambda x: int(x['statistics']['subscriberCount']))

        # Update the DataFrame with 'subscribers'
        yc['subscribers'] = subscribers
        youtube_merged_df = pd.merge(youtube_videos_comments, yc, on='youtube_channel_id', how='inner')
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Group data and plot
        grouped_data = youtube_merged_df.groupby('youtube_channel_id').agg({'subscribers': 'first', 'ycvcomment_id': 'count'}).reset_index()
        grouped_data.columns = ['youtube_channel_id', 'subscribers', 'comment_count']
        sns.pairplot(grouped_data[['subscribers', 'comment_count']])
        plt.xlabel('Subreddit Engagement Metrics Analysis (Engagement of Subscribers with respect to Comments)')
        # Save the figure to the static folder
        static_path = settings.BASE_DIR / 'static'
        figure_path = static_path / 'c.jpg'
        #print(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg')
        #plt.savefig(str(settings.BASE_DIR+'/static/Youtube Engagement Metrics Analysis.jpg'))
        plt.savefig(str(figure_path))
        plt.suptitle('Youtube Engagement Metrics Analysis (Engagement of Subscribers with respect to Comments)', y=-0.05, va='bottom')
        #plt.show()
        
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        image_stream.seek(0)
        youtube_engagement_metrics_analysis_image = base64.b64encode(image_stream.read()).decode('utf-8')
        print("Pass")
        #return youtube_engagement_metrics_analysis_image


        return JsonResponse({'Success': 'Success request method'})

'''






































'''
# views.py
 
def new_post_video_data_count(request):
    # Your existing function logic
    subreddit_posts = ...  # Assuming you have your DataFrame
    youtube_channel_videos = ...  # Assuming you have your DataFrame

    subreddit_posts['post_date_time'] = pd.to_datetime(subreddit_posts['post_date_time'])
    youtube_channel_videos['ycv_date_time'] = pd.to_datetime(youtube_channel_videos['ycv_date_time'])
    subreddit_posts['post_date'] = subreddit_posts['post_date_time'].dt.date
    youtube_channel_videos['ycv_date'] = youtube_channel_videos['ycv_date_time'].dt.date
    dates_till_now = subreddit_posts['post_date_time'].dt.date.unique()

    reddit_posts_daily_counts = subreddit_posts[subreddit_posts['post_date'].isin(dates_till_now)].groupby('post_date').size().reset_index(name='post_count')
    youtube_videos_daily_counts = youtube_channel_videos[youtube_channel_videos['ycv_date'].isin(dates_till_now)].groupby('ycv_date').size().reset_index(name='video_count')

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(reddit_posts_daily_counts['post_date'], reddit_posts_daily_counts['post_count'], marker='o', linestyle='-', color='blue', label='Reddit Posts Daily Counts')
    plt.plot(youtube_videos_daily_counts['ycv_date'], youtube_videos_daily_counts['video_count'], marker='o', linestyle='-', color='red', label='YouTube Videos Daily Counts')
    plt.title('Reddit Posts Count vs Youtube Video Count (Number of New Entries per Day)')
    plt.xlabel('Date (Starting 1st November)')
    plt.ylabel('Count')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.legend()

    # Convert the plot to an image and embed it in the response
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    context = {'image_base64': image_base64}
    return render(request, 'your_app/demoanalysis.html', context)

    
    
def post_video_data_count(subreddit_posts,youtube_channel_videos):
    
    sql_query = "SELECT Count(*) FROM subreddit_posts"
    cursor = connection.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    print(results)
    # Assuming your DataFrame is named df and 'date_time' is the column containing date-time values
    subreddit_posts['post_date_time'] = pd.to_datetime(subreddit_posts['post_date_time'])
    youtube_channel_videos['ycv_date_time'] = pd.to_datetime(youtube_channel_videos['ycv_date_time'])
    subreddit_posts['post_date'] = subreddit_posts['post_date_time'].dt.date
    youtube_channel_videos['ycv_date'] = youtube_channel_videos['ycv_date_time'].dt.date
    dates_till_now =  subreddit_posts['post_date_time'].dt.date.unique()
    
    # Count the number of rows for each unique date present in 'dates_till_now'
    reddit_posts_daily_counts = subreddit_posts[subreddit_posts['post_date'].isin(dates_till_now)].groupby('post_date').size().reset_index(name='post_count')
    youtube_videos_daily_counts = youtube_channel_videos[youtube_channel_videos['ycv_date'].isin(dates_till_now)].groupby('ycv_date').size().reset_index(name='video_count')

    # Plotting
    #plt.figure(figsize=(12, 6))
    #reddit_posts_daily_counts.plot(kind='line', marker='o', linestyle='-', color='blue', label='Reddit Posts Daily Counts')
    #youtube_videos_daily_counts.plot(kind='line', marker='o', linestyle='-', color='red', label='YouTube Videos Daily Counts')
    plt.plot(reddit_posts_daily_counts['post_date'], reddit_posts_daily_counts['post_count'], marker='o', linestyle='-', color='blue', label='Reddit Posts Daily Counts')
    plt.plot(youtube_videos_daily_counts['ycv_date'], youtube_videos_daily_counts['video_count'], marker='o', linestyle='-', color='red', label='YouTube Videos Daily Counts')
    plt.title('Reddit Posts Count vs Youtube Video Count (Number of New Entries per Day)')
    plt.xlabel('Date (Starting 1st November)')
    plt.ylabel('Count')
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.legend()
    #plt.savefig('Reddit Posts Count vs Youtube Video Count (Number of New Entries per Day).jpg')
    #plt.show()
    
    # Convert the plot to an image and embed it in the response
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_stream.seek(0)
    post_video_data_count_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return post_video_data_count_image


'''