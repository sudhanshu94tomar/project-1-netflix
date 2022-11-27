#!/usr/bin/env python
# coding: utf-8

# # Netflix - Data Exploration and Visualisation
# performing Exploratry Data Analysis to understant the Dataset

# **Task**
# * Understand the Dataset, types and missing values
# * Clean the dataset and handle the missing values
# * Perform the data visulization
# * Create final summary report

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


df=pd.read_csv('netflix.csv')


# In[3]:


df.shape


# In[4]:


df.info()


# In[5]:


df.head()


# In[6]:


df.describe()


# # Correcting Data types and filling missing values

# In[7]:


df.isna().sum() #for missing values


# In[8]:


df.isnull().sum()/len(df)*100  #missing values in percentage


# **The following colums have missing values**
# * director
# * cast
# * country
# * date_added
# * rating
# * duration
# 
# **The data type of data_added must be datetime**
# 

# In[9]:


df['date_added']=pd.to_datetime(df['date_added'])


# In[10]:


df['date_added']


# In[11]:


df.head()


# In[12]:


pd.DataFrame(df['cast'].value_counts().sort_values(ascending=False))


# In[13]:


splitter = df['cast'].apply(lambda x: str(x).split(', ')).tolist()


# In[14]:


splitter


# In[15]:


df_cast = pd.DataFrame(splitter, index=df['title'])


# In[16]:


df_cast


# In[17]:


df_cast = pd.DataFrame(df_cast.stack()).reset_index()


# In[18]:


df_cast


# In[19]:


df_cast = df_cast[['title',0]]
df_cast.columns=['title','actor']
df_cast


# In[20]:


df = df.merge(df_cast, on='title',how='inner')


# # Seperating the genres

# In[21]:


splitter = df['listed_in'].apply(lambda x: str(x).split(', ')).tolist()


# In[22]:


splitter


# In[23]:


df_genre = pd.DataFrame(splitter, index=df['title'])


# In[24]:


df_genre


# In[25]:


df_genre = pd.DataFrame(df_genre.stack()).reset_index()


# In[26]:


df_genre=df_genre[['title',0]]


# In[27]:


df_genre.columns=['title','genre']


# In[28]:


df_genre


# In[29]:


df = df.merge(df_genre, on='title',how='inner')


# In[30]:


df.head()


# In[31]:


del df['listed_in']


# In[32]:


df.head()


# **Unit issue with time**
# * Time must be in integer
# * Removing min from time eg:- '90 min' to 90

# In[33]:


df['duration_new'] = df['duration'].apply(lambda x: str(x).split(' ')[0])


# In[34]:


df


# In[35]:


del df['cast']
del df['duration']


# # Filling missing values

# In[36]:


df.fillna({'rating':'Unavilable','actor':'Unavilable','country':'Unavilable','director':'Unavilable'},inplace=True)
df.isna().sum()


# For missing values of date can be subtitued by most recent date or we can drop the missing values.

# In[37]:


df[df.date_added.isnull()] #To check where date_added values has null value


# In[38]:


most_recent_entry_date=df['date_added'].max()
df.fillna({'date_added':most_recent_entry_date},inplace=True)


# In[39]:


df[df.show_id=='s8183'] #Checking if date_added has been filled or not


# checking null values in duration

# In[40]:


df[df['duration_new'].isnull()] #accessing the column where duration has null values


# * All movies which have null values in there duration has a common directior that is Louis C.K.
# * Here the important thing to note is that duration values are mistakenly placed in rating column.
# * So what we have to do is that we need to replace the rating values in duration column and then we have to make rating values as 'unavaliable'

# Checking to make sure therre is no other content with same director to avoid accidental overwriting

# In[41]:


df[df.director == 'Louis C.K.'].head()


# In[42]:


#loc helps us to easily access the columns by names
df.loc[df['director'] == 'Louis C.K.','duration_new'] = df['rating']
df[df.director == 'Louis C.K.'].head()


# In[43]:


#overwritting the values of rating as unavailable
df.loc[df['director'] == 'Louis C.K.','rating'] = 'Unavailable'
df[df.director == 'Louis C.K.'].head()


# In[44]:


#Checking if all null values are fixed
df.isna().sum()


# # Visualizations

# In[45]:


df.type.value_counts() #To find the number of movies and shows that are avaliable in netflix


# In[73]:


#count plot help us to plot counts of each category
plt.pie(df['type'].value_counts(),labels=set(df['type']),autopct='%0.1f%%',radius=2)
plt.pie([1],colors=['w'],radius=1)
#sns.countplot(x = 'type',data = df)
plt.title('Count vs Type of shows')


# On netflix there are more number of movies then tv shows

# # Country analysis

# In[47]:


df['country'].value_counts().head(10)


# In[78]:


plt.figure(figsize=(12,6))
sns.countplot(y = 'country', order = df['country'].value_counts().index[0:10],data=df)
plt.title('Country wise Content on Netflix')


# In[49]:


movie_countries = df[df.type == 'Movie']
tv_show_countries = df[df.type == 'TV Show']


# In[50]:


plt.figure(figsize = (12,6))
sns.countplot(y='country',order = df['country'].value_counts().index[0:10],data=movie_countries)
plt.title('Top 10 countries producing movies in netflix')


plt.figure(figsize = (12,6))
sns.countplot(y='country',order = df['country'].value_counts().index[0:10],data=tv_show_countries)
plt.title('Top 10 countries producing TV Shows in netflix')


# In[51]:


df.rating.value_counts()


# In[142]:


plt.figure(figsize = (9,6))
sns.countplot(x = 'rating', order = df['rating'].value_counts().index[0:10],data = df)
plt.title('Rating of shows on netflix')


# Most of the shows has rating TV-MA(mature adults) and TV-14(above 14) ratings.

# In[53]:


df.release_year.value_counts()[:20]


# In[54]:


plt.figure(figsize = (10,6))
sns.countplot(x='release_year',order=df['release_year'].value_counts().index[0:20],data=df)
plt.title('Content release in years on Netflix vs Counts')


# # Popular Genres

# In[55]:


plt.figure(figsize = (12,8))
sns.countplot(y='genre',order=df['genre'].value_counts().index[0:20],data=df)
plt.title('Top 20 Genres on Netflix')


# # Actor who has is in maximum movies

# In[56]:


plt.figure(figsize = (12,8))
sns.countplot(y='actor',order=df['actor'].value_counts().index[1:21],data=df)
plt.title('Actor who is featured in most movies')


# # Director with maximum movie

# In[57]:


plt.figure(figsize = (12,8))
sns.countplot(y='director',order=df['director'].value_counts().index[1:21],data=df)
plt.title('Top 20 director on Netflix')


# **Summary**
# So, far I have performed lots of operations over the dataset to dig out some very useful information form it. If, we have to conclude the dataset in few line, then we can say that:
# 
# * Netflix has more movies than TV shows.
# * Most number of movies and TV shows are produced by United States, followed by India who has produced the second most number of movies on Netflix.
# * Most content on Netflix(Movies and TV shows) are for Matured adults.
# * 2018 is the year in which Netflix released maximum content as compared to other years.
# * Dramas and International Movies are the most popular Genres on Netflix
# 

# In[121]:


df.head()


# In[ ]:




