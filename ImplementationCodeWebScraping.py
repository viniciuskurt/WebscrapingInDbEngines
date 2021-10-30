#!/usr/bin/env python
# coding: utf-8

# ## Loading the NumPy, Pandas, BeautifulSoup, MatPlotLib, Requests, JSON and Seaborn libraries:

# In[146]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import json


# ##  Accessing website https://db-engines.com/en/ranking for scraping:

# In[147]:


site = requests.get("https://db-engines.com/en/ranking").content
soup = BeautifulSoup(site,'html5lib')


# ## Generating Table with Ranking Database list:

# In[158]:


table = soup.find('table',{'class':'dbi'}).find('tbody')
table


# ## Creating lists Base and Spots to store values obtained from the site:

# In[159]:


lines = table.find_all('tr')
counterLines = 0
base = []
spots = []

for line in lines:
    counterLines += 1
    if counterLines > 3:
        data = line.find_all('td')
        data2 = line.find('a')
        spots.append(float(data[3].text))
        base.append(data2.contents[0])


# ## Generating dataframe DataBases

# In[161]:


data = pd.DataFrame(base,columns=['DataBases'])
data['Spots'] = spots

data


# ## Viewing Top 4 Databases

# In[151]:


data.head()


# ## Generating column chart with amount of points for a current month bank with Seaborn

# In[162]:


sns.barplot(data = data.head(4), x = 'DataBases', y = 'Spots')


# **We can see that Oracle is in first place, closely followed by MySql.**

# ## Generating Top 10 dataframe with relevance percentage

# In[163]:


dataTop10 = data.head(10)

total = dataTop10['Spots'].sum()
dataTop10['Share'] = dataTop10['Spots'] / total * 100

dataTop10


# **Oracle has 24,034805 share in the top 10. These data were collected in October 2021.**

# ### Chart with MatPlotLib based on how each database is shared against the other 9 in the generated list:

# In[164]:


plt.pie(dataTop10['Share'],labels=dataTop10['DataBases'])
plt.show


# **As we can see in the graph, the 3 databases Oracle, MySql and SqlServer have more than half of shares**

# ## Percentage of relevance of each database in relation to the others:

# In[155]:


percentageRelevance = data['Spots'].sum()
data['% Relevance'] = data['Spots'] / percentageRelevance * 100

data


# ## Creating a csv file to store the generated information: 

# In[156]:


data.to_csv("db-rankink.csv")

