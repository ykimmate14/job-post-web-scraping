
import requests # for accesing web page
from bs4 import BeautifulSoup # for pulling data out of html
import pandas as pd # for general working with data
# from nltk import word_tokenize # text mining / analysis
from collections import Counter
from nltk.corpus import stopwords
import re #regex

# A function take jobtitle and location as arguments and return correct url for web scraping purpose
def searchquery(jobtitle, location):
    title = jobtitle.replace(' ', '+')
    loc = location.replace(' ', '+')
    url = 'http://www.indeed.com/jobs?q=%22'+ title +'%22&radius=50&limit=50&l='+loc
    return url

# A function to take job list's url as an input and return dataframe with job titles and url to job post
def collect_job_list(url):
    # create empty list
    jobtitle, hreflink = [], []
    
    # get contents from the web
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # find the page number
    x = soup.findAll('div', {'id': 'searchCount'})[0].text.replace(',', '')
    pageN = int(x[x.find('of ')+3:])
    
    # iterate over page number    
    for i in range(0, pageN, 50):
        joblisturl = url + '&start=' + str(i)
        r = requests.get(joblisturl)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # iterate over each listed job post on search result to obtain job title and link
        for data in soup.findAll('a', {'data-tn-element': 'jobTitle'}):
            if 'clk?jk=' in data.get('href'):
                hreflink.append(data.get('href'))
                jobtitle.append(data.text)
    df = pd.DataFrame({'title': jobtitle, 'link': hreflink})
    return df


# convert the href link data in dataframe to proper url
def properurl(link):
    joburl = 'http://www.indeed.com/viewjob?jk=' +\
            link[link.find('clk?jk=')+len('clk?jk='):link.find('&fccid')]
    return joburl
            

# A function to take job posting's url as an input, mine text data from selected job post. 
# and return the text from the post.
def collect_job_data(joblink_list):
    jobdesc = []
    #iterate over href link in data frame
    for i in range(0, len(joblink_list)):
        joburl = properurl(joblink_list[i])
        
        #extracting text data from selected job posting        
        r = requests.get(joburl)
        soup = BeautifulSoup(r.content, 'html.parser')
        desc = ''.join(soup.findAll('td', {'class': 'snip'})[0].text)
        desc = re.sub('[^A-Za-z0-9&]+', ' ', desc)
        jobdesc.append(desc[:desc.find('ago')].replace('\n', ' ').lower())
    return jobdesc

# A function to take str as input, split the str and count the words
def countword(text):
    #removing stopwords from the data
    stop = stopwords.words('english')
    #update stopwords as below
    stop.update(())
    
    
    nostopword = ' '.join([word for word in text.split() if word not in stop])
    #create word count list
    count = Counter(nostopword.split())
    return count

# A function to take words as input and return the list of counts for the words of interest.
def sortlist(words, countlist):
    result= []  
    for word in words.split():
        result.append([x for x in countlist if word in x])
    return result






    