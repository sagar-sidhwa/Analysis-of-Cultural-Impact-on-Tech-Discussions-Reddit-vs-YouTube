# Analysis of Cultural Impact on Tech Discussions: Reddit vs YouTube
[![Python](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-blue.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue.svg)](https://www.postgresql.org/)
[![Python Libraries](https://img.shields.io/badge/Python%20Libraries-Various-green.svg)](https://pypi.org/)
[![NLP](https://img.shields.io/badge/NLP-Various-blue.svg)](https://www.nltk.org/)
[![Data Collection](https://img.shields.io/badge/Data%20Collection-Various-orange.svg)](https://beautiful-soup-4.readthedocs.io/en/latest/)
[![Data Analysis](https://img.shields.io/badge/Data%20Analysis-Various-purple.svg)](https://pandas.pydata.org/)
[![Linux](https://img.shields.io/badge/Linux-Various-black.svg)](https://www.linux.org/)

## Overview

This project involves developing an automated system designed to collect and analyze data from Reddit and YouTube. The system leverages Python, PostgreSQL, and machine learning models. It utilizes NLP techniques to provide comprehensive insights into online discussions, sentiment, and cultural trends, while also identifying toxic behaviors and assessing cultural influences. Additionally, it automates data processing for efficiency and accuracy.

### Key Features
- **Automated Data Collection**: Utilizes Python to automate the gathering of data from Reddit and YouTube, ensuring a continuous flow of up-to-date information.
- **Data Storage**: Employs PostgreSQL for robust and scalable storage of collected data, enabling efficient querying and management.
- **Machine Learning Models**: Integrates machine learning algorithms to perform advanced analyses such as trend predictions and sentiment analysis.
- **NLP Techniques**: Applies Natural Language Processing (NLP) methods to assess sentiment, identify toxic behaviors, and analyze cultural influences within the data.
- **Data Processing and Visualization**: Automates the processing of data and presents insights using Flask and Django for web interfaces, and Power BI for interactive visualizations.

### Technologies Used
- **Python**: Core language for scripting and implementing data processing and machine learning models.
- **PostgreSQL**: Database system for storing and managing large volumes of collected data.
- **Machine Learning**: For predictive analytics and advanced data analysis.
- **NLP**: Techniques for analyzing text data, sentiment, and trends.
- **Flask & Django**: Web frameworks used to build the application’s interface and functionality.
- **Analysis**: Used multiple Python and NLP Libraries & Tools for visualizing data and generating insightful reports.

### Goals
- Provide actionable insights from large datasets on social media platforms.
- Enhance understanding of public sentiment and cultural trends through automated and scalable methods.
- Offer a comprehensive tool for analyzing and visualizing complex data in a user-friendly manner.


## Step - 1 : Getting Started

1. **Installation**: Make sure you have Python and Django and other necessary libraries installed. If not, you can install them using:

   ```bash
   pip install numpy
   pip install pandas
   pip install django
   pip install nltk
   pip install wordcloud
   pip install matplotlib
   pip install textblob
   pip install seaborn
   pip install spacy
   pip install tabulate

## Step - 2 : Setting Up Database (PostgreSQL)

This project uses PostgreSQL as the database management system to store and manage the collected data. PostgreSQL is a powerful, open-source object-relational database system known for its robustness, scalability, and support for advanced data types.

### Documentation

For more information about PostgreSQL, including installation, configuration, and usage, refer to the official [PostgreSQL Documentation](https://www.postgresql.org/docs/).

### Database Setup

You will need to set up a PostgreSQL database for this project. Below are the details for configuring your database (For my Project):

- **Database Name**: socialgood
- **User Name**: postgres
- **Database Name**: socialgood
- **PASSWORD**: socialgood
- **HOST Name**: localhost
- **PORT**: 5432

Names and the details about database and tables will be provided in the `Reddit vs YouTube Database Setup.txt` file.

### Installation

Ensure that you have PostgreSQL installed and running on your system. You can follow the installation guide in the PostgreSQL documentation linked above.

To connect to your PostgreSQL database from your application, make sure to configure the database settings in your Django settings file (typically `<Your Path to Django Project>\Part 3 - Analysis of Cultural Impact on Tech Discussions Reddit vs YouTube (Django-Website)\Code (Django-Website)\socialgood\socialgood\settings.py`):

1. **Setting up the Database**: Make sure to change this based on your settings:

   ```bash
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'Your_Database_Name_Here',
            'USER': 'Your_Username_Here',
            'PASSWORD': 'Your_Password_Here',
            'HOST': 'localhost',
            'PORT': '5432',
        }
   }
## Step - 3 : Configuring the Data Collection Files - (Part 1 - Data Science Pipeline Creation and Data Collection)

### Configuring `reddit_collect_data.py`

To collect data from Reddit using the `reddit_collect_data.py` (typically `<Your Path to Project>\Analysis of Cultural Impact on Tech Discussions Reddit vs YouTube\Part 1 - Data Science Pipeline Creation and Data Collection\Code\Part 1 (b) - Data Pipeline and Collection\Reddit_Data_Collection\Reddit Data Pipeline and Collection\reddit_collect_data.py`) script, follow these steps:

1. **Create Reddit API Accounts:**
   - Visit the [Reddit API Collection Page](https://www.reddit.com/prefs/apps) or [Reddit API Documentation](https://www.reddit.com/dev/api/).
   - Create multiple Reddit API accounts. You will need to do this to obtain different `CLIENT_ID` and `CLIENT_SECRET` values. Each account will provide unique credentials.

2. **Obtain Your Credentials:**
   - After creating Reddit API accounts, you will receive `CLIENT_ID` and `CLIENT_SECRET` values for each account. You should have a list of these credentials like so:
     - `CLIENT_ID = ['sjkfdekrjkegjt', 'qjebwfkrf', ...]`
     - `CLIENT_SECRET = ['kjasnfkjnvgkjf', 'kjsdfnvjgkrtj', ...]`

3. **Set Up User Data:**
   - You will also need to set up user credentials for authentication. Prepare a list of dictionaries containing user information:
     - `p_data = [{'grant_type': 'password', 'username': '<username1>', 'password': 'password1'}, {'grant_type': 'password', 'username': '<username2>', 'password': 'password2'}, ...]`

4. **Update `reddit_collect_data.py`:**
   - Open the `reddit_collect_data.py` file in your code editor.
   - Locate the section where you need to input your `CLIENT_ID`, `CLIENT_SECRET`, and `p_data`.
   - Replace the placeholder values in the script with the credentials and user data you obtained.

   Example snippet to update in `reddit_collect_data.py`:

   ```python
   CLIENT_ID = ['sjkfdekrjkegjt', 'qjebwfkrf', ...]
   CLIENT_SECRET = ['kjasnfkjnvgkjf', 'kjsdfnvjgkrtj', ...]
   p_data = [
       {'grant_type': 'password', 'username': '<username1>', 'password': 'password1'},
       {'grant_type': 'password', 'username': '<username2>', 'password': 'password2'},
       ...
   ]

### Configuring `youtube_data_collection.py`

To collect data from YouTube using the `youtube_data_collection.py` (typically `<Your Path to Project>\Analysis of Cultural Impact on Tech Discussions Reddit vs YouTube\Part 1 - Data Science Pipeline Creation and Data Collection\Code\Part 1 (b) - Data Pipeline and Collection\YouTube_Data_Collection\YouTube Data Pipeline and Collection\youtube_data_collection.py`) script, follow these steps:

1. **Create Google API Accounts:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project if you don’t have one.
   - Navigate to the [API & Services Dashboard](https://console.cloud.google.com/apis/dashboard) and enable the YouTube Data API v3.
   - Create credentials for your project to obtain API keys.

2. **Obtain Your YouTube API Keys:**
   - You will receive API keys for your project. You should have a list of these keys like so:
     - `youtube_api_key_1 = ['asjfvhkshdfvkh', ...]`
     - `youtube_api_key_2 = ['alkjfnlejgnlkt', ...]`
     - `youtube_api_key_3 = ['sdckjkvjbj', ...]`

3. **Set Up Channel Data:**
   - You need to specify the list of YouTube channel names you want to collect data from. For example:
     - `channel_names = ['TED', 'TEDx Talks', 'TED-Ed', 'Veritasium', 'WIRED', 'Vsauce', 'Marques Brownlee', 'ColdFusion', 'Simplilearn', 'Linus Tech Tips', 'Quantum Tech HD', 'Bloomberg Technology', 'Yahoo Finance', 'The Wall Street Journal', 'CNN', 'BBC News']`
   - You should also provide the associated YouTube channel IDs:
     - `youtube_channel_list = ['UCAuUUnT6oDeKwE6v1NGQxug', 'UCsT0YIqwnpJCM-mx7-gSA4Q', 'UCsooa4yRKGN_zEE8iknghZA', 'UCHnyfMqiRRG1u-2MsSQLbXA', 'UCftwRNsjfRo08xYE31tkiyw', 'UC6nSFpj9HTCZ5t-N3Rm3-HA', 'UCBJycsmduvYEL83R_U4JriQ', 'UC4QZ_LsYcvcq7qOsOhpAX4A', 'UCsvqVGtbbyHaMoevxPAq9Fg', 'UCXuqSBlHAE6Xw-yeJA0Tunw', 'UC4Tklxku1yPcRIH0VVCKoeA', 'UCrM7B7SL_g1edFOnmj-SDKg', 'UCEAZeUIeJs0IjQiqTCdVSIg', 'UCK7tptUDHh-RYDsdxO1-5QQ', 'UCupvZG-5ko_eiXAupbDfxWw', 'UC16niRr50-MSBwiO3YDb3RA']`

4. **Update `youtube_data_collection.py`:**
   - Open the `youtube_data_collection.py` file in your code editor.
   - Locate the section where you need to input your `youtube_api_key` values, 'channel names', and 'channel IDs' etc..
   - Replace the placeholder values in the script with the API keys and channel data you obtained.

   Example snippet to update in `youtube_data_collection.py`:

   ```python
   youtube_api_key_1 = ['asjfvhkshdfvkh', ...]
   youtube_api_key_2 = ['alkjfnlejgnlkt', ...]
   youtube_api_key_3 = ['sdckjkvjbj', ...]

   # List of Channel Names
   channel_names = ['TED', 'TEDx Talks', 'TED-Ed', 'Veritasium', 'WIRED', 'Vsauce', 'Marques Brownlee', 'ColdFusion', 'Simplilearn', 'Linus Tech Tips', 'Quantum Tech HD', 'Bloomberg Technology', 'Yahoo Finance', 'The Wall Street Journal', 'CNN', 'BBC News']

   # List of Channel IDs
   youtube_channel_list = ['UCAuUUnT6oDeKwE6v1NGQxug', 'UCsT0YIqwnpJCM-mx7-gSA4Q', 'UCsooa4yRKGN_zEE8iknghZA', 'UCHnyfMqiRRG1u-2MsSQLbXA', 'UCftwRNsjfRo08xYE31tkiyw', 'UC6nSFpj9HTCZ5t-N3Rm3-HA', 'UCBJycsmduvYEL83R_U4JriQ', 'UC4QZ_LsYcvcq7qOsOhpAX4A', 'UCsvqVGtbbyHaMoevxPAq9Fg', 'UCXuqSBlHAE6Xw-yeJA0Tunw', 'UC4Tklxku1yPcRIH0VVCKoeA', 'UCrM7B7SL_g1edFOnmj-SDKg', 'UCEAZeUIeJs0IjQiqTCdVSIg', 'UCK7tptUDHh-RYDsdxO1-5QQ', 'UCupvZG-5ko_eiXAupbDfxWw', 'UC16niRr50-MSBwiO3YDb3RA']

   # Bifurcate channel list for faster access
   api_use_1 = ['UCAuUUnT6oDeKwE6v1NGQxug', 'UCsT0YIqwnpJCM-mx7-gSA4Q', 'UCsooa4yRKGN_zEE8iknghZA', 'UCHnyfMqiRRG1u-2MsSQLbXA', 'UCftwRNsjfRo08xYE31tkiyw']
   api_use_2 = ['UC6nSFpj9HTCZ5t-N3Rm3-HA', 'UCBJycsmduvYEL83R_U4JriQ', 'UC4QZ_LsYcvcq7qOsOhpAX4A', 'UCsvqVGtbbyHaMoevxPAq9Fg', 'UCXuqSBlHAE6Xw-yeJA0Tunw']
   api_use_3 = ['UC4Tklxku1yPcRIH0VVCKoeA', 'UCrM7B7SL_g1edFOnmj-SDKg', 'UCEAZeUIeJs0IjQiqTCdVSIg', 'UCK7tptUDHh-RYDsdxO1-5QQ', 'UCupvZG-5ko_eiXAupbDfxWw', 'UC16niRr50-MSBwiO3YDb3RA']

## Step - 4 : Part 2 - Social Media Data Analysis (Reddit vs YouTube)

### Part 2 (a) - ModerateHatespeech Api Code
In this part of the project 'Part 2 (a) - ModerateHatespeech Api Code', we will perform an analysis of the collected social media data from Reddit and YouTube. Specifically, we will use the following Python scripts to process and analyze the data:

- `subreddit_posts_comments_moderatehatespeech.py`
- `subreddit_posts_moderatehatespeech.py`
- `youtube_channel_videos_moderatehatespeech.py`
- `youtube_videos_comments_moderatehatespeech.py`

### Overview

For this analysis, we will use the [Moderate Hate Speech](https://moderatehatespeech.com/) API to classify and assess the data collected from Reddit and YouTube. This involves the following steps:

1. **Sign Up and Obtain API Key:**
   - Visit the [Moderate Hate Speech](https://moderatehatespeech.com/) website.
   - Sign up for an account and obtain an API key.

2. **Configure API Keys:**
   - You need to update the API keys in the Python scripts mentioned above.
   - The API key will be used to authenticate requests to the Moderate Hate Speech service.

3. **Update Python Scripts:**
   - Open each of the following scripts in your code editor and replace the placeholder API key with the one you obtained:
     - `subreddit_posts_comments_moderatehatespeech.py`
     - `subreddit_posts_moderatehatespeech.py`
     - `youtube_channel_videos_moderatehatespeech.py`
     - `youtube_videos_comments_moderatehatespeech.py`

   Example of what to update in the Python scripts:

   ```python
   # Replace 'your_api_key_here' with your actual API key (token)
   'token': 'your_api_key_here'

## Step 5: Optional Data Analysis

In this step, you have two optional processes for analyzing the collected social media data from Reddit and YouTube. These processes are designed to help you convert the PostgreSQL data into a more accessible format (CSV) and then perform in-depth analysis using IPython notebooks.

### Part 2(b): Convert Data from PostgreSQL to CSV

To facilitate static data visualization and ease of analysis, you can convert the data from your PostgreSQL database into CSV files. Follow these instructions to create CSV files for each table:

1. **Run the Data Conversion Script:**
   - Use the `postgresql_to_csv.ipynb` Jupyter notebook to export data from PostgreSQL to CSV files.
   - This script will extract data from all relevant tables (Reddit and YouTube) and save them as CSV files.

   Example usage:
   ```bash
   jupyter notebook postgresql_to_csv.ipynb

### Part 2(c): Performing Social Media Data Analysis (Reddit vs YouTube) in an IPython Notebook

After converting your PostgreSQL data into CSV files in Part 2(b), you can proceed with analyzing this data using an IPython notebook. This step involves using the CSV files created earlier to perform a comprehensive analysis of social media data from Reddit and YouTube.

#### Overview

The goal of this part is to use the CSV files for detailed data analysis, including examining trends, sentiments, and comparisons between Reddit and YouTube data. The analysis will help you gain insights into the cultural impact and behavioral patterns observed in the data collected.

#### Instructions

1. **Open the Analysis Notebook:**
   - Use the `Social_Media_Data_Analysis.ipynb` Jupyter notebook for your data analysis.
   - This notebook contains code and instructions for analyzing the data from the CSV files generated in Part 2(b).

   Example usage:
   ```bash
   jupyter notebook Social_Media_Data_Analysis.ipynb

## Step - 6 : Part 3 - Analysis of Cultural Impact on Tech Discussions Reddit vs YouTube (Django-Website)

### Part 3 - Django Project Setup

In this final step, you will set up and run a Django project that provides dynamic analysis and visualization of the collected data from Reddit and YouTube. Follow these instructions to configure and launch the Django application. first you should open your Visual Studio Code with this path (typically `<Your Path to Project>\Analysis of Cultural Impact on Tech Discussions Reddit vs YouTube\Part 3 - Analysis of Cultural Impact on Tech Discussions Reddit vs YouTube (Django-Website)\Code (Django-Website)\socialgood`), and follow these steps:

### 1. **Prepare Your Django Environment**

Ensure that you have completed all previous steps, including updating your `settings.py` file and installing all necessary dependencies.

### 2. **Run the Server**
1. **Run the Server**: Execute the following command to run the Django development server:

   ```bash
   python manage.py runserver

- Access the project at http://<your_localhost>/.

### Documentation

#### Django Documentation
Comprehensive documentation for Django framework.
[Read the Docs](https://docs.djangoproject.com/en/stable/)

#### Python and Its Libraries
Documentation for Python programming and its libraries.
[Python Official Documentation](https://docs.python.org/3/)

#### PostgreSQL Documentation
Official documentation for PostgreSQL database management.
[PostgreSQL Documentation](https://www.postgresql.org/docs/)

#### VS Code Documentation
Guides and documentation for Visual Studio Code.
[VS Code Documentation](https://code.visualstudio.com/docs)

#### NLP Libraries Documentation
Information on Natural Language Processing libraries.
[NLTK Documentation](https://www.nltk.org/)
[TextBlob Documentation](https://textblob.readthedocs.io/en/dev/)

#### Jupyter Notebook Documentation
Documentation for Jupyter Notebooks.
[Jupyter Documentation](https://jupyter.org/documentation)

#### Reddit API Documentation
Official documentation for Reddit's API.
[Reddit API Documentation](https://www.reddit.com/dev/api/)

#### YouTube API Documentation
Official documentation for YouTube's API.
[YouTube API Documentation](https://developers.google.com/youtube/v3)

#### Moderate Hate Speech API Documentation
Documentation for the Moderate Hate Speech API used for text classification.
[Moderate Hate Speech API](https://moderatehatespeech.com/)