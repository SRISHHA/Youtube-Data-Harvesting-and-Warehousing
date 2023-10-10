
import streamlit as st
import googleapiclient.discovery
import certifi
import pymongo
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
def get_channeldetails(channel_id):
    import googleapiclient.discovery
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCKOXMFc_ltyCvyTg1DO9VmSiGwIlS7DC4"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    request = youtube.channels().list(part="snippet,contentDetails,statistics",
        id=channel_id)
    response = request.execute()
    Channel_id=response["items"][0]["id"]
    Channel_name=response["items"][0]["snippet"]["title"]
    Channel_type=response["items"][0]["kind"]
    Channel_views=response["items"][0]["statistics"]["viewCount"]
    Channel_description=response["items"][0]["snippet"]["description"]
    Channel_Url=response["items"][0]["snippet"]["customUrl"]
    Channel_published=response["items"][0]["snippet"][ "publishedAt"]
    Channel_subscribers=response["items"][0]["statistics"]["subscriberCount"]
    Channel_videos=response["items"][0]["statistics"][ "videoCount"]
    Channel_upload=response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    Channel_details={"Channel_id":Channel_id,"Channel_name":Channel_name,
                "Channel_type":Channel_type,"Channel_views":Channel_views,
                "Channel_description":Channel_description,
                 "Channel_Url":Channel_Url,
                 "Channel_published":Channel_published,
                "Channel_subscribers":Channel_subscribers,
                "Channel_videos":Channel_videos,
                "Channel_upload":Channel_upload}
    return Channel_details

def get_playlist_info(channel_id):
    import googleapiclient.discovery
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCKOXMFc_ltyCvyTg1DO9VmSiGwIlS7DC4"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    playlists = []
    play_request = youtube.playlists().list(part='snippet',channelId=channel_id,maxResults=5,)
    response = play_request.execute()
    for item in response.get('items', []):
       playlist_id = item['id']
       playlist_name = item['snippet']['title']
       playlists.append({'id': playlist_id, 'name': playlist_name})
    Playlist_ID=[]
    Playlist_Name=[]
    Channel_ID=[]
    for playlist in playlists:
        Playlist_ID.append(playlist['id'])
        Channel_ID.append(channel_id)
        Playlist_Name.append(playlist['name'])

    Playlist_details={"Playlist_id":Playlist_ID,
                      "Channel_id":Channel_ID,
                      "Playlist_Name":Playlist_Name
                      }

    return  Playlist_details

def get_video_details(Total_Playlist_ID):
    try:
        import googleapiclient.discovery
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyCKOXMFc_ltyCvyTg1DO9VmSiGwIlS7DC4"
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
        Video_ID=[]
        Video_Title=[]
        Video_Description=[]
        Playlist_id=[]
        for playlist_id in Total_Playlist_ID:
            request = youtube.playlistItems().list(part='snippet',playlistId=playlist_id,maxResults=2,)
            response = request.execute()
            video_ids = [item['snippet']['resourceId']['videoId'] for item in response.get('items', [])]
            video_request = youtube.videos().list(
                        part='snippet',
                        id=','.join(video_ids),
                        maxResults=2,
                        )
            video_response = video_request.execute()
            video_details = []
            for item in video_response.get('items', []):
                video_id = item['id']
                video_title = item['snippet']['title']
                video_description = item['snippet']['description']
                video_details.append({'id': video_id, 'title': video_title, 'description': video_description})
                for video in video_details:
                    Video_ID.append(video['id'])
                    Video_Title.append(video['title'])
                    Video_Description.append(video['description'])
                    Playlist_id.append(playlist_id)

            Video_details1={"Video_ID": Video_ID,
                        "Playlist_id":Playlist_id,
                        "Video_Name":Video_Title,
                        "Video_Description":Video_Description}
            video_ids=Video_details1["Video_ID"]
            Published_At=[]
            Duration=[]
            View_count=[]
            Like_Count=[]
            Favourite_Count=[]
            Caption=[]
            def convert_time(duration_str):
                import pandas as pd
                x=pd.to_timedelta(duration_str)
                timedelta = pd.Timedelta(x)
                minutes = timedelta.total_seconds() / 60
                return minutes
            for video_id in video_ids:
                video_request = youtube.videos().list(
                part="snippet,statistics,contentDetails",id=video_id)
                video_response = video_request.execute()
                Published_At.append(video_response["items"][0]["snippet"]["publishedAt"])
                time=convert_time(video_response["items"][0]["contentDetails"]["duration"])
                Duration.append(time)
                Caption.append(video_response['items'][0]["contentDetails"]['caption'])
                View_count.append(video_response["items"][0]["statistics"]["viewCount"])
                Like_Count.append(video_response["items"][0]["statistics"]["likeCount"])
                Favourite_Count.append(video_response["items"][0]["statistics"]["favoriteCount"])
            Video_details2={"Published_at":Published_At,
               "Duration":Duration,
               "Caption":Caption,
               "View_count":View_count,
               "Like_Count":Like_Count,
               "Favourite_Count":Favourite_Count}
            Video_details1.update(Video_details2)
            Comment_count=[]
            Video_ID=[]
            for video_id in video_ids:
                try:
                    request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id)
                    response = request.execute()
                    total_comments = response.get('pageInfo', {}).get('totalResults', 0)
                    Comment_count.append(total_comments)
                    Video_ID.append(video_id)
                except Exception as e:
                    return " "
            cc={"Comment_count":Comment_count}
            Video_details1.update(cc)
        return Video_details1
    except Exception as e:
        return Video_details1

def get_comment_details(video_ids):
    import googleapiclient.discovery
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCKOXMFc_ltyCvyTg1DO9VmSiGwIlS7DC4"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    Video_ID=[]
    Comment_ID=[]
    Comment_Text=[]
    Comment_Author=[]
    Published_Date=[]
    for video_id in video_ids:
        try:
            request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=2
            )
            response = request.execute()
            for item in response.get('items', []):
                Video_ID.append(video_id)
                Comment_ID.append(item['id'])
                Comment_Text.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                Comment_Author.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                Published_Date.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
        except Exception as e:
            return " "
    comment_details={"Video_ID":Video_ID,
                     "Comment_ID":Comment_ID,
                     "Comment_Text":Comment_Text,
                     "Comment_Author":Comment_Author,
                     "Published_Date":Published_Date

                        }
    return comment_details

def main(channel_id):
    channel_details=get_channeldetails(channel_id)
    playlist_details=get_playlist_info(channel_id)
    video_details=get_video_details(playlist_details['Playlist_id'])
    comment_details=get_comment_details(video_details["Video_ID"])

    data={
        "channel_details":channel_details,
        "playlist_details": playlist_details,
        "video_details": video_details,
        "comment_details":comment_details
    }
    return data



import certifi
ca = certifi.where()

def migrate_to_mongodb(channel_id):
    import certifi
    ca = certifi.where()
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://srishha:hello@cluster0.k1giiwc.mongodb.net/",tlsCAFile=ca)
    data=main(channel_id)
    db = client["channel"]
    channel_info=db["channel_details"]
    search_criteria = {"Channel_id":channel_id}
    existing_document = channel_info.find_one(search_criteria)
    if existing_document:
        print("Document exists")
    else:
        playlist_info=db["playlist_details"]
        video_info=db["video_details"]
        comment_info=db["comment_details"]
        channel_details=channel_info.insert_one(data['channel_details'])
        playlist_details=playlist_info.insert_one(data[ 'playlist_details'])
        video_details=video_info.insert_one(data['video_details'])
        comment_details=comment_info.insert_one(data['comment_details'])
        return channel_info["Channel_name"]








page = st.sidebar.radio("PAGES", ["HOME","UPLOAD TO MONGODB", "MIGRATING TO SQL", "DATA ANALYSIS"])

if page == "HOME":
    st.write('<h4 style="color: red;">YOUTUBE DATA HARVESTING AND WAREHOUSING</h1>', unsafe_allow_html=True)
  
    Channel_id=st.text_input("Enter your channel ID to fetch you the relevant details")
    if Channel_id:
        cd=get_channeldetails(Channel_id)
        st.write(cd)
    data = {
    "Channel_Name": ["DATAVECTOR 3099", "Curious Freaks", "Lukonde Mwila", "PENP_"],
    "Channel_ID": ["UCQOV6j0VbzRy9uCvlisk81w", "UCvhU9qF1xtUsFXdKrcJxbFA", "UCz98Ics0hXj0Lv1U2Y6BObQ", "UCTcTMIkKyv-kNq8bxUhOksw"],
    }
    df = pd.DataFrame(data)
    st.write("List Of Channels for Analysis related to tech")
    st.table(df)

elif page == "UPLOAD TO MONGODB":
    st.write('<h3 style="color: green;">MONGODB MIGRATION</h3>',unsafe_allow_html=True)
    Mongo_id = st.text_input("Enter your Channel ID to migrate to MongoDB")
    
    if st.button("Upload to MongoDB"):
        res=migrate_to_mongodb(Mongo_id)
        st.write('<h6 style="color: green;">UPLOADED!!</h6>',unsafe_allow_html=True)
    
elif page == "MIGRATING TO SQL":
    def options():
        import pymongo
        client = pymongo.MongoClient("mongodb+srv://srishha:hello@cluster0.k1giiwc.mongodb.net/",tlsCAFile=ca)
        db = client["channel"]
        collection = db["channel_details"]
        cursor = collection.find({})
        field_values = []
        for document in cursor:
            field_value = document.get("Channel_name")  
            if field_value is not None:
                field_values.append(field_value)
        return field_values  

    

   
    st.write('<h3 style="color: blue;">DATA MIGRATION TO SQL</h3>',unsafe_allow_html=True)
    ans=st.selectbox("Select the channel to migrate data to sql",[None] + options())
    
    if ans:
        sqlite_db_file ="youH.db"
        sqlite_conn = sqlite3.connect(sqlite_db_file)
        sqlite_cursor = sqlite_conn.cursor()
        channel_table = '''CREATE TABLE IF NOT EXISTS channel_details(
                        Channel_id TEXT PRIMARY KEY,
                        Channel_name TEXT,
                        Channel_type TEXT,
                        Channel_views INTEGER,
                        Channel_description TEXT,
                        Channel_Url TEXT,
                        Channel_published TEXT,
                        Channel_subscribers INTEGER,
                        Channel_videos INTEGER,
                        Channel_upload TEXT)'''
        playlist_table = '''CREATE TABLE IF NOT EXISTS playlist_details (
                           Playlist_id TEXT PRIMARY KEY,
                           Channel_id TEXT,
                           Playlist_Name TEXT)'''
        video_table = '''CREATE TABLE IF NOT EXISTS video_details (
                         Video_ID TEXT,
                         Playlist_id TEXT,
                         Video_Name TEXT,
                         Video_Description TEXT,
                         Published_at TEXT,
                         Duration INTEGER,
                         Caption TEXT,
                         View_count INTEGER,
                         Like_Count INTEGER,
                         Favourite_Count INTEGER,
                         Comment_count INTEGER)'''
        comment_table = '''CREATE TABLE IF NOT EXISTS comment_details (Video_ID TEXT,
                           Comment_ID TEXT,
                           Comment_Text TEXT,
                           Comment_Author TEXT,
                           Published_Date TEXT)'''
        sqlite_cursor.execute(channel_table)
        sqlite_cursor.execute(playlist_table)
        sqlite_cursor.execute(video_table)
        sqlite_cursor.execute(comment_table)
        sqlite_conn.commit()
        mongo_host ="mongodb+srv://srishha:hello@cluster0.k1giiwc.mongodb.net/"
        mongo_db_name ="channel"
        mongo_client = pymongo.MongoClient(mongo_host,tlsCAFile=ca)
        mongo_db = mongo_client[mongo_db_name]
        chan=mongo_db["channel_details"]
        cursor1 =chan.find({"Channel_name": ans})
        ID=""
        for document in cursor1:
            ID+=document.get("Channel_id")
        element_name = "Channel_id" 
        element_value =ID
        query = {element_name: element_value}
        chan_result = chan.find_one(query)
        values = (chan_result["Channel_id"],
        chan_result["Channel_name"],
        chan_result["Channel_type"],
        chan_result["Channel_views"],
        chan_result["Channel_description"],
        chan_result["Channel_Url"],
        chan_result["Channel_published"],
        chan_result["Channel_subscribers"],
        chan_result["Channel_videos"],
        chan_result["Channel_upload"])
        channel_insert ='''INSERT INTO channel_details(Channel_id,Channel_name,Channel_type,
            Channel_views,Channel_description,Channel_Url,Channel_published,
            Channel_subscribers,Channel_videos,Channel_upload)
            VALUES (?,?,?,?,?,?,?,?,?,?)'''
        sqlite_cursor.execute(channel_insert, values)
        sqlite_conn.commit()
       
            
        playlist_insert ='''INSERT INTO
            playlist_details(Playlist_id,Channel_id,Playlist_Name)
            VALUES (?,?,?)'''
        play=mongo_db["playlist_details"]
        ans=ID
        cursor2 = play.find({"Channel_id": ans})
        for document in cursor2:
            playid=document.get("Playlist_id")
        element_name = "Playlist_id" 
        element_value = playid
        query = {element_name: element_value}
        play_result = play.find_one(query)
        values=tuple(play_result.values())[1:]
        values1=tuple()
        values1=[]
        for i in values:
            values1.append(tuple(i))
        i=0
        count=len(values1[0])
        while i<count:
            values2=[]
            for h in range(len(values1)):
                values2.append(values1[h][i])
            values3=tuple(values2)
            i+=1
            sqlite_cursor.execute(playlist_insert,values3)
            sqlite_conn.commit()
        video_insert ="INSERT INTO video_details(Video_ID,Playlist_id,Video_Name,Video_Description,Published_at,Duration,Caption,View_count,Like_Count,Favourite_Count,Comment_count) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        vid =mongo_db["video_details"]
        cursor = vid.find({})
        element= playid[0]
        doc={}
        for document in cursor:
            find=document["Playlist_id"]
            if element in find:
                doc=document
                break
        values=tuple(doc.values())[1:]
        values1=[]
        for i in values:
            values1.append(tuple(i))
        i=0
        count=len(values1[0])
        while i<count:
            values2=[]
            for h in range(len(values1)):
                values2.append(values1[h][i])
            values3=tuple(values2)
            i+=1
            sqlite_cursor.execute(video_insert,values3)
            sqlite_conn.commit()
        comment_insert ="INSERT INTO comment_details(Video_ID,Comment_ID,Comment_Text,Comment_Author,Published_Date)VALUES (?,?,?,?,?)"
        cid=mongo_db["comment_details"]
        li=doc['Video_ID']
        cursor = cid.find({})
        element=li[0]
        dic={}
        for document in cursor:
            find=document["Video_ID"]
            if element in find:
                dic=document
                break
        values=tuple(dic.values())[1:]
        values1=[]
        for i in values:
            values1.append(tuple(i))
        i=0
        count=len(values1[0])
        while i<count:
            values2=[]
            for h in range(len(values1)):
                values2.append(values1[h][i])
            values3=tuple(values2)
            i+=1
            sqlite_cursor.execute(comment_insert,values3)
            sqlite_conn.commit()
        st.write('<h5 style="color: blue;">MIGRATION DONE!!</h5>',unsafe_allow_html=True)
elif page == "DATA ANALYSIS":
    sqlite_db_file ="youH.db"
    sqlite_conn = sqlite3.connect(sqlite_db_file)
    res=st.selectbox("Select the question to hunt the data",[None]+["What are the names of all the videos and their corresponding channels?",
                    "List of channels having the most number of videos?","What are the top 10 most viewed videos and their respective channels?",
                    "How many comments were made on each video along with video names?",
                    "Which videos have the highest number of likes, and their channel names?",
                    "What is the total number of likes and their video names?",
                    "What is the total number of views for each channel, and their channel names?",
                    "What are the names of channels that have published videos in the year 2022?",
                    "What is the average duration of all videos in a channel,and channel names?",
                    "Which video have the highest number of comments, and channel names?"])
    if res=="What are the names of all the videos and their corresponding channels?":
       
        query1='''SELECT video_details.Video_Name,channel_details.Channel_name FROM video_details
        JOIN playlist_details ON  video_details.Playlist_id= playlist_details.Playlist_id
        JOIN channel_details ON  channel_details.Channel_id=playlist_details.Channel_id'''
        df_query1= pd.read_sql_query(query1,sqlite_conn)
        st.write(df_query1)
    if res=="List of channels having the most number of videos?":
        query2='''SELECT  COUNT( vd.Video_ID) AS number_of_count , cd.Channel_name
            FROM  video_details  vd JOIN    playlist_details  pd ON  vd.Playlist_id= pd.Playlist_id
            JOIN channel_details cd  ON  cd.Channel_id=pd.Channel_id
            GROUP BY  Channel_name ORDER BY   number_of_count  DESC'''
        df_query2= pd.read_sql_query(query2,sqlite_conn)
        st.write(df_query2)
        fig, ax = plt.subplots()
        ax.bar(df_query2['Channel_name'], df_query2['number_of_count'],color="pink", width=0.3)
        ax.set_xlabel('Category')
        ax.set_ylabel('number_of_count')
        st.pyplot(fig)
    if res=="What are the top 10 most viewed videos and their respective channels?": 
  
        query3='''SELECT   vd.View_count ,vd.Video_Name, cd.Channel_name
            FROM  video_details  vd JOIN    playlist_details  pd ON  vd.Playlist_id= pd.Playlist_id JOIN channel_details cd  ON  cd.Channel_id=pd.Channel_id
            ORDER BY   vd.View_count  DESC LIMIT 10'''
        df_query3= pd.read_sql_query(query3,sqlite_conn)
        st.write(df_query3)
        scatterplot = sns.scatterplot(x="Video_Name", y="View_count", hue="Channel_name", data=df_query3)
        plt.xticks(rotation=90) 
        st.pyplot(scatterplot.figure)
    if res=="How many comments were made on each video along with video names?":
        query4='''SELECT   COUNT(cd.Comment_ID) AS Comment_Count,video_details.Video_Name FROM  comment_details  cd JOIN    video_details
                ON  video_details .Video_ID = cd.Video_ID GROUP BY  video_details.Video_ID'''
        df_query4= pd.read_sql_query(query4,sqlite_conn)
        st.write(df_query4)
        scatterplot=sns.barplot(x="Video_Name", y="Comment_Count",color="green",data=df_query4)
        plt.xlabel("Video_Name")
        plt.ylabel("Comment_Count")
        plt.xticks(rotation=90) 
        st.pyplot(scatterplot.figure)
    if res=="Which videos have the highest number of likes, and their channel names?":
        query5='''SELECT   vd.Like_Count , cd.Channel_name,vd.Video_Name  FROM  video_details  vd
               JOIN    playlist_details  pd ON  vd.Playlist_id= pd.Playlist_id
               JOIN channel_details cd  ON  cd.Channel_id=pd.Channel_id ORDER BY   vd.Like_Count  DESC'''
        df_query5= pd.read_sql_query(query5,sqlite_conn)
        st.write(df_query5)
        scatterplot = sns.scatterplot(x="Video_Name", y="Like_Count", hue="Channel_name", data=df_query5)
        plt.xticks(rotation=90) 
        st.pyplot(scatterplot.figure)
    if res=="What is the total number of likes and their video names?":
        query6='''SELECT   vd.Like_Count , vd.Video_Name FROM  video_details  vd
        JOIN    playlist_details  pd ON  vd.Playlist_id= pd.Playlist_id
        JOIN channel_details cd  ON  cd.Channel_id=pd.Channel_id'''
        df_query6= pd.read_sql_query(query6,sqlite_conn)
        st.write(df_query6)
        barplot = sns.barplot(x="Video_Name", y="Like_Count",color="red",data=df_query6)
        plt.xticks(rotation=90) 
        st.pyplot(barplot.figure)
    if res=="What is the total number of views for each channel, and their channel names?":
        query7='''SELECT Channel_views,Channel_name FROM  channel_details ORDER BY Channel_views DESC'''
        df_query7 = pd.read_sql_query(query7,sqlite_conn)
        st.write(df_query7)
        barplot = sns.barplot(x="Channel_name", y="Channel_views",color="blue",data=df_query7,width=0.3)
        plt.xticks(rotation=90) 
        st.pyplot(barplot.figure)
    if res=="What are the names of channels that have published videos in the year 2022?":
        query8='''SELECT vd.Published_at,  cd.Channel_name FROM video_details vd
                JOIN    playlist_details  pd ON  vd.Playlist_id= pd.Playlist_id
                JOIN channel_details cd  ON  cd.Channel_id=pd.Channel_id
                WHERE vd.Published_at  LIKE  "2022%" '''
        df_query8 = pd.read_sql_query(query8,sqlite_conn)
        st.write(df_query8)
    if res=="What is the average duration of all videos in a channel,and channel names?":
        query9='''SELECT   AVG(vd.Duration) AS AVERAGE_DURATION_IN_MINS,cd.Channel_name FROM  video_details vd
            JOIN    playlist_details pd ON   vd.Playlist_id= pd.Playlist_id JOIN channel_details cd
            ON  cd.Channel_id=pd.Channel_id GROUP BY cd.Channel_name'''
        df_query9 = pd.read_sql_query(query9,sqlite_conn)
        st.write(df_query9)
    if res=="Which video have the highest number of comments, and channel names?":
        query10='''SELECT   vd.Comment_count,cd.Channel_name,vd.Video_Name
        FROM  video_details vd JOIN    playlist_details pd ON   vd.Playlist_id= pd.Playlist_id
        JOIN channel_details cd ON   cd.Channel_id=pd.Channel_id ORDER BY vd.Comment_count DESC'''
        df_query10 = pd.read_sql_query(query10,sqlite_conn)
        st.write(df_query10)
        scatterplot = sns.scatterplot(x="Video_Name", y="Comment_count", hue="Channel_name", data=df_query10)
        plt.xticks(rotation=90) 
        st.pyplot(scatterplot.figure)



    



