import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
 
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #st.dataframe(df)

    #Fetch unique users...
    user_list = df['Username'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user =  st.sidebar.selectbox("Show Analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
       st.title('Top Statistics')
       num_messages, words, num_media_messages, num_links =  helper.fetch_stats(selected_user, df)
       col1, col2, col3, col4 =   st.columns(4)

       with col1: 
            st.header("Total Messages")
            st.title(num_messages)

       with col2:
            st.header("Total Words")
            st.title(words)

       with col3: 
            st.header("Media Shared")
            st.title(num_media_messages)

       with col4: 
            st.header("links Shared")
            st.title(num_links)
            
        
        # Monthly timeline

       st.title('Monthly Timeline')
       timeline = helper.monthly_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(timeline['time'], timeline['Message'])
       plt.xticks(rotation = 'vertical')
       st.pyplot(fig)
        
        # Daily timeline 
       st.title('Daily Timeline')
       daily_timeline = helper.daily_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['Message'])
       plt.xticks(rotation = 'vertical')
       st.pyplot(fig)
       
       # activity map
       st.title('Activity Map')
       col1, col2 = st.columns(2)
       
       with col1:
           st.header("Most Active Days")
           busy_day = helper.week_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_day.index, busy_day.values)
           plt.xticks(rotation = 'vertical')
           st.pyplot(fig)
           
       with col2: 
            
           st.header("Most Active Months")
           busy_month = helper.month_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_month.index, busy_month.values, color = 'orange')
           plt.xticks(rotation = 'vertical')
           st.pyplot(fig)
             

        #finding the busiest users in the group(Group level)
       if selected_user == 'Overall': 
            st.title("Most Active Users")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1: 
                ax.bar(x.index, x.values)
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)   
            
            with col2: 
                st.dataframe(new_df) 

        # Wordcloud
       st.title("WordCloud")
       df_wc = helper.create_wordcloud(selected_user, df)
       fig, ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)
       
       #most common words
       most_common_df = helper.most_common_words(selected_user, df)
       
       fig, ax = plt.subplots()
       
       ax.barh(most_common_df[0], most_common_df[1])
       
       plt.xticks(rotation = 'vertical')
       
       st.title('Most common words')
       st.pyplot(fig)
       
       #emoji analysis
       
       emoji_df = helper.emoji_helper(selected_user, df)
       st.title("Emoji Analysis")
       col1, col2 = st.columns(2)
       
       with col1:
            st.dataframe(emoji_df)
            
       with col2: 
           fig, ax = plt.subplots()
           ax.pie(emoji_df[1].head(), labels =  emoji_df[0].head(), autopct = "%0.2f")
           st.pyplot(fig)
           
        
       
        
