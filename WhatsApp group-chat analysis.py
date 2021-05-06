# Import necessary modules
import pandas as pd
import numpy as np
import matplotlib
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML
from collections import Counter
from collections import OrderedDict
import re
import os
nltk.download('stopwords')
#Custom display function
def custom_display(txt):
    display(HTML("<h2>" + txt + "</h2>"))
print("_____"*23)
#function to sort
def sort_by_values(data, reverse=True):
    return OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))
#Defining functions for the barchart
def plot_bar_chart(total_items, y_values, x_values, title, xlabel, ylabel, rotation=0):
    plt.figure(figsize=(18,10))
    plt.bar(np.arange(total_items), y_values,color=['violet','indigo','blue','green', 'yellow', 'orange','red' ])
    plt.xticks(np.arange(total_items), x_values,rotation=rotation)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
#Get usernames with regex
def get_regex_user_name(name):
    return name.replace(' ', '\s').replace('|', '\|')
file_name = 'WhatsApp.txt'
fh = open(file_name,"r",encoding="utf8")
data = fh.read()
is_iphone = data[0] == '['
if is_iphone:
    data = data.replace('\xa0', ' ')
def create_date_time_user_name(time_and_names, is_24_hour_format):
    date_time_user_name = ['02/11/2019',  '19:17:00',  'Sorunke_Tomiwa']
    if is_24_hour_format:
        if is_iphone:
            for time_name in time_and_names:
                time_name = time_name.split(']')
                date_time = time_name[0][1:]
                date_ = date_time.split(',')[0].strip()
                time_ = date_time.split(',')[1].strip()
                time_ = time_.split(':')[0] + ':' + time_.split(':')[1]
                user_name = time_name[1][:-1].strip()
                date_time_user_name.append((date_, time_, user_name))
        else:
            for time_name in time_and_names:
                time_name = time_name.split(' - ')
                date_time = time_name[0]
                date_ = date_time.split(', ')[0].strip()
                time_ = date_time.split(', ')[1].strip()
                user_name = time_name[1][:-1].strip()
                date_time_user_name.append((date_, time_, user_name))
    else:
        if is_iphone:
            for time_name, meridian in time_and_names:
                date_time = time_name.split('] ')[0]
                name_ = time_name.split('] ')[1][:-1]
                date_ = date_time.split(', ')[0][1:]
                time_ = date_time.split(', ')[1].split(' ')[0]
                time_ = time_.split(':')[0] + ':' + time_.split(':')[1]
                hour_ = int(time_.split(':')[0])
                minute_ = time_.split(':')[1]
                if (meridian == 'PM') and (hour_ != 12):
                    hour_ += 12
                if (meridian == 'AM') and (hour_ == 12):
                    hour_ = 0
                if hour_ < 10:
                    hour_ = "0" + str(hour_)
                final_time = str(hour_) + ":" + str(minute_)
                date_time_user_name.append((date_, final_time, name_))
        else:
            for time_name, meridian in time_and_names:
                date_time = time_name.split(' - ')[0]
                name_ = time_name.split(' - ')[1][:-1]
                date_ = date_time.split(', ')[0]
                time_ = date_time.split(', ')[1].split(' ')[0]
                hour_ = int(time_.split(':')[0])
                minute_ = time_.split(':')[1]
                if (meridian == 'PM') and (hour_ != 12):
                    hour_ += 12
                if (meridian == 'AM') and (hour_ == 12):
                    hour_ = 0
                if hour_ < 10:
                    hour_ = "0"+str(hour_)
                final_time = str(hour_) + ":" + str(minute_)
                date_time_user_name.append((date_,final_time, name_ ))
    return date_time_user_name
def get_date_time_user_name_data():
    is_24_hour_format = False
    if is_iphone:
        # check for AM/PM
        time_and_names = re.findall(r'(\[\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\s(PM|AM)\]\s.*?:)', data)[1:]
        if len(time_and_names) == 0:
            is_24_hour_format = True
            time_and_names = re.findall(r'(\[\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}:\d{1,2}\]\s.*?:)', data)[1:]
    else:
        # check for AM/PM
        time_and_names = re.findall(r'(\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s(PM|AM)\s-\s.*?:)', data)
        if len(time_and_names) == 0:
            is_24_hour_format = True
            time_and_names = re.findall(r'(\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s-\s.*?:)', data)
    return create_date_time_user_name(time_and_names, is_24_hour_format)
def get_message_timings():
    users = {}
    message_timings = {}
    date_time_user_name = get_date_time_user_name_data()
    for date_, time_, name_ in date_time_user_name:
        name_ = name_.strip('\u202c').strip('\u202a')
        if name_ in users.keys():
            users[name_]+=1
        else:
            users[name_]=1
        hour = time_.split(':')[0]
        if hour not in message_timings.keys():
            message_timings[hour] = 0
        message_timings[hour] += 1
    return users, message_timings
    users,message_timings = get_message_timings()
    hours = sorted(message_timings.keys())
    message_counts = [message_timings[hour] for hour in hours]
    plot_bar_chart(len(hours), message_counts, hours, 'Number of Messages in a given hour', '24 hour format', 'Messages count')
    custom_display("Chats will be more during " + str(hours[np.argmax(message_counts)]) + ":00 hours")