"""socialgood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialgooddata import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.socialgoodhome, name = 'socialgoodhome'),
    path("analysis/", views.analysis, name = 'analysis'),
    path("demoanalysis/", views.demoanalysis, name = 'demoanalysis'),
    
    path("da", views.post_video_data_count, name = 'da'),
    path("db", views.reddit_vs_youtube_comment_count, name = 'db'), 
    path("dc", views.reddit_posts_ModerateHatespeech, name = 'dc'),
    path("dd", views.youtube_videos_ModerateHatespeech, name = 'dd'),
    path("de", views.reddit_comments_ModerateHatespeech, name = 'de'),
    path("df", views.youtube_comments_ModerateHatespeech, name = 'df'),
    path("dg", views.reddit_content_popularity_analysis, name = 'dg'), 
    path("dh", views.youtube_content_popularity_analysis, name = 'dh'),
    path("di", views.sentiment_analysis, name = 'di'),
    path("dj", views.subreddit_engagement_metrics_analysis, name = 'dj'),
    path("dk", views.youtube_engagement_metrics_analysis, name = 'dk'),
    
    path("fdaanalysis", views.fda_varying_analysis, name = 'fda'),
    path("fdbanalysis", views.fdb_varying_analysis, name = 'fdb'),
    path("fdcanalysis", views.fdc_varying_analysis, name = 'fdc'),
    
    #path("socialgoodhome", views.socialgoodhome, name = 'socialgoodhome'),
    #path("fdemoanalysis", views.fdemoanalysis, name = 'fdemoanalysis'),
    #path("details", views.details, name = 'details'),   
]
