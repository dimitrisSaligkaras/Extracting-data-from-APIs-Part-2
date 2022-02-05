#as we are going to retrieve data from youtube we will need an authentication key
#the authentication key can be obtained in different ways. That depends on the website or platform
#for the youtube the way to take the key needed is described on the following link
#https://www.slickremix.com/docs/get-api-key-for-youtube/
#from the menu go to the api library and procceed according to the information provided from the link above
#following the steps described you should end up with an api key provided by google

#except from the api key we need the channel id
#the channel id can be obtained by copying the symbols which follow the last / of the particular channel url

import requests
import pandas as pd
from IPython.display import display


#keys
API_KEY = "PLACE YOUR KEY HERE"
CHANNEL_ID = "UCZqSxKHQmsEUwGuAIEMxTzQ"

#First, we add our API key that’s stored in the API_KEY variable in this key parameter.
#We specify the channel ID we want to collect information from.
#Next is the part parameter where we’re specifying that we want snippet and ID data.
#The snippet object contains basic details about a search result, such as its title or description. For example, if the search result is a video, then the title will be the video's title and the description will be the video's description.
#Order the data by date and then we want the maxResults of 10000 videos in our API call.
#Lastly, the pageToken is a token, which is a code, that is needed to get to the next page of the search results.
#for more about query properties that can be added check the https://developers.google.com/youtube/v3/docs/search
pageToken = ""
url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken
response = requests.get(url).json()
print(response)

#if we want to see the latest video of the channel
print(response['items'][0])

#The items key starts with a square brace and then basically is listing all the videos in the channel
#we can also see that the total results aka total videos are 134
#so we wish to add the information that we have retrieved from each video into variables

#Let’s save the video ID
video_id = response['items'][0]['id']['videoId']
print(video_id)
#Let’s do the same with the video title
#Here we're also replacing any & (ampersand) symbols with a blank
#Then let’s grab the upload date
video_title = response['items'][0]['snippet']['title']
print(video_title)
video_title = str(video_title).replace("&","")
video_title = str(video_title).replace("#","")
print(video_title)
upload_date = response['items'][0]['snippet']['publishedAt']
print(upload_date)
#if we want to only keep the date we are gonna trim the previous result
upload_date = str(upload_date).split("T")[0]
print(upload_date)

#we are going to create a loop to make the previous for all the videos
#also we want to collect some statistics for the videos such as likes etc.
#so we are going to add the statistics feature on the query parameter part
url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
response_video_stats = requests.get(url_video_stats).json()
print(response_video_stats)

#create a pandas DataFrame
df = pd.DataFrame(columns=["video_id","video_title","upload_date","view_count","like_count","dislike_count","comment_count"])

for video in response['items']:
    if video['id']['kind'] == "youtube#video":
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_title = str(video_title).replace("&amp;", "")
        upload_date = video['snippet']['publishedAt']
        upload_date = str(upload_date).split("T")[0]
        # colleccting view, like,  comment counts
        url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id + "&part=statistics&key=" + API_KEY
        response_video_stats = requests.get(url_video_stats).json()
        view_count = response_video_stats['items'][0]['statistics']['viewCount']
        like_count = response_video_stats['items'][0]['statistics']['likeCount']
        comment_count = response_video_stats['items'][0]['statistics']['commentCount']
        df = df.append({'video_id':video_id,'video_title':video_title,'upload_date':upload_date,'view_count':view_count,'like_count':like_count,'comment_count':comment_count},ignore_index=True)


df
pd.set_option("display.max_rows", 1000, "display.max_columns", 1000)
print(df)
styler = df.style.highlight_max(axis='index')
