
#import python file that contains functions for scraping job list data on indeed.com
from job_web_scraping import collect_job_data, collect_job_list, countword, searchquery, sortlist
from collections import Counter

# prompt a user to input job title and location of interest
jobtitle = input('Please enter the "job title" of interest:  ') 
location = input('Please enter the "location" of interest:  ')

# using the 'collect_job_list' funciton, assign data frame to a variable 'df' 
df = collect_job_list(searchquery(jobtitle, location))

# remove duplicated data
df = df[df.duplicated('link') == False]

# add column of text that contains job description to the dataframe
df['text'] = collect_job_data(list(df.link))

# Clean data with text whose length is less than 100
for index, row in df.iterrows():
    if(len(row.text) < 100):
        row.text = ''
df = df[df.text != '']

# iterate over the dataframe to split the texts into words
for index, row in df.iterrows():
    row.text = countword(row.text)

# count the occurence of words
totalcount = Counter()
for index, row in df.iterrows():
    totalcount += row.text

# reorder the list of count in descending order
result = totalcount.most_common()

# overview of the most frequent words
print("Number of open position: "+str(len(df)))
print("\nThe 100 most frequent words are as below:\n")
print(result[:100])

# prompt a user to sort the list with words of interest
intwords = input('Enter the words of interst separated by space\n')
sortlist(intwords, result)




