import re
import pandas as pd

def preprocess(data): 
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    #Convert message_date type
    df["message_date"] = pd.to_datetime(df['message_date'], format = '%d/%m/%Y, %H:%M - ')

    df.rename(columns = {'message_date': 'date'}, inplace = True)
    # users = []
    # messages = []

    # for message in df['user_message']:
    #     entry = re.split('([\W\W]+?):\s', message)
    #     if entry[1:]: #user name
    #         users.append(entry[1])
    #         messages.append(entry[2])
    #     else:
    #         users.append('group_notification')
    #         messages.append(entry[0])

    # df["user"] = users
    # df['message'] = messages
    # df.drop(columns = ['user_message'], inplace = True)
    # df["year"] = df['date'].dt.year
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    # df['hour'] = df['date'].dt.hour
    # df['minute']  = df['date'].dt.minute
    
    df["year"] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute']  = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    
    #Separate users and messages...

    # Create empty lists to store usernames and messages
    usernames = []
    messages = []

    # Split each message in the chat data
    for message in df['user_message']:
        parts = message.split(": ", 1)  # Split at the first colon and space
        if len(parts) == 2:
            username, message_text = parts
            usernames.append(username)
            messages.append(message_text)
        else:
            # Handle cases where a message doesn't follow the expected format
            usernames.append('group notification')
            messages.append(message)

    # Create a DataFrame
    #df = pd.DataFrame({'Username': usernames, 'Message': messages})
    df['Username'] = usernames
    df['Message'] = messages
    df.drop(columns = ['user_message'], inplace = True, axis = 1)

    return df