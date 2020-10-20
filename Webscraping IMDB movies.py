#!/usr/bin/env python
# coding: utf-8

# In[9]:


from requests import get
url='http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response=get(url)
print(response.text[:500])


# In[10]:


from bs4 import BeautifulSoup
html_soup=BeautifulSoup(response.text,'html.parser')
type(html_soup)


# In[12]:


movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
print(type(movie_containers))
print(len(movie_containers))


# In[13]:


first_movie=movie_containers[0]
first_movie


# In[14]:


first_movie.div


# In[15]:


first_movie.a


# In[16]:


first_movie.h3


# In[17]:


first_movie.h3.a


# In[18]:


first_movie.h3.a.text


# In[19]:


first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
first_year


# In[20]:


first_year=first_year.text
first_year


# In[21]:


first_movie.strong


# In[22]:


first_imdb=float(first_movie.strong.text)


# In[23]:


first_imdb


# In[24]:


first_mscore=first_movie.find('span',class_='metascore favorable')
first_mscore=int(first_mscore.text)
print(first_mscore)


# In[25]:


first_votes=first_movie.find('span',attrs={'name':'nv'})


# In[26]:


first_votes


# In[29]:


first_votes=int(first_votes['data-value'])


# In[30]:


first_votes


# In[31]:


twentytwo_movie_mscore = movie_containers[21].find('div', class_ = 'ratings-metascore')
type(twentytwo_movie_mscore)


# In[60]:


# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
# Extract data from individual movie container
for container in movie_containers:
# If the movie has Metascore, then extract:
    if container.find('div', class_ = 'ratings-metascore') is not None:
# The name
     name = container.h3.a.text
     names.append(name)
# The year
     year = container.h3.find('span', class_ = 'lister-item-year').text
     years.append(year)
# The IMDB rating
     imdb = float(container.strong.text)
     imdb_ratings.append(imdb)
# The Metascore
     m_score = container.find('span', class_ = 'metascore').text
     metascores.append(int(m_score))
# The number of votes
     vote = container.find('span', attrs = {'name':'nv'})['data-value']
     votes.append(int(vote))


# In[61]:


import pandas as pd
test_df = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes
})
print(test_df.info())
test_df                                                                       


# In[79]:




pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2018)]

from time import sleep
from random import randint
for i in range(0,5):
    print('blah')
    sleep(randint(1,4))


# In[81]:


from time import sleep
from random import randint


# In[86]:


import time
start_time=time.time()
requests = 0
for _ in range(5):
# A request would go here
    requests += 1
    sleep(randint(1,3))
    elapsed_time = time.time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))


# In[90]:


from IPython.core.display import clear_output
start_time = time.time()
requests = 0
for _ in range(5):
# A request would go here
    requests += 1
    sleep(randint(1,3))
    current_time = time.time()
    elapsed_time = current_time - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
clear_output(wait = True)


# In[97]:


from warnings import warn


# In[111]:


# Redeclaring the lists to store data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# Preparing the monitoring of the loop
start_time = time.time()
requests = 0

# For every year in the interval 2000-2017
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time.time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
                 warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_ = 'ratings-metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))
                 # Scrape the number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))


# In[112]:


movie_ratings = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes
})
print(movie_ratings.info())
movie_ratings.head(10)


# In[113]:


movie_ratings = movie_ratings[['movie', 'year', 'imdb', 'metascore', 'votes']]
movie_ratings.head()


# In[114]:


movie_ratings.to_csv('movie_ratings.csv')


# In[ ]:




