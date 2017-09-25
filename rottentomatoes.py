# CMDA 3654 Project
# Brandon Ray & Krista McGuigan

# Imports
import requests
import pandas
import bs4
import itertools
from nltk import bigrams
from collections import Counter
import csv

# Table to store the reviews for each movie
table = pandas.DataFrame(columns=['Movie', 'Review', 'CleanReview'])

# Common words, as well as words commonly appearing in these reviews to ignore
stopWords = open('stop-word-list.txt').read().splitlines()
ignoreWords = ['ring', 'it', 'horror', 'movie', 'film', 'hollywood', 'exorcist', 'audience', 'halloween', 'insidious']
ignoreWords += ['movies', 'films', 'blair', 'witch', 'project', 'carrie', 'grudge', 'sinister']

# Positive and negative words for the Review Score
positiveData = pandas.read_csv('positive.txt')
positives = positiveData[positiveData.columns[0]].tolist()

negativeData = pandas.read_csv('negative.txt')
negatives = negativeData[negativeData.columns[0]].tolist()

# Note: for analysis, we can use graphs and get main sentiment for each movie and compare to critic scores

# Horror movies to analyze
movies = [('It', 'stephen_kings_it1990'), ('The Ring', 'ring'), ('The Exorcist', 'exorcist'), ('Halloween', '1009113_halloween'), ('Insidious', 'insidious'), ('Lights Out', 'lights_out_2016')]
movies += [('Scream', '1074316_scream'), ('The Blair Witch Project', 'blair_witch_project'), ('Carrie', 'carrie'), ('The Grudge', 'grudge'), ('Sinister', 'sinister_2012')]


meterRatings = list() # Stores the rotten tomatoes score
commonPairs = list() # Stores the top common pairs of words
commonWords = list() # Stores the top common words
totalScoreList = list()

# Loop through each movie
for movieName, m in movies:
	r = requests.get('https://www.rottentomatoes.com/m/' + m)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')

	# Gets the rotten tomatoes ratings
	meterValue = soup.find('span', {'class': 'meter-value'}).contents[0].contents[0]
	meterRatings.append(float(meterValue))
	audienceScore = soup.find('div', {'class': 'meter-value'}).contents[1].contents[0]

	# Gets the link to the page holding the critics reviews
	criticReviewsLink = soup.find('a', {'class': 'view_all_critic_reviews'}).attrs['href']
	criticReviewsLink = 'https://www.rottentomatoes.com' + str(criticReviewsLink)

	# Open a new request to that page
	r2 = requests.get(criticReviewsLink)
	soup2 = bs4.BeautifulSoup(r2.content, 'html.parser')

	# This is the number of pages of reviews to gather data from
	numberOfPages = soup2.find('span', {'class': 'pageInfo'}).contents[0].split()[3]

	reviews = list() # Stores all of the reviews

	# Loop through every page and add all of the [non-empty] reviews to the list as strings
	for i in range(1,int(numberOfPages)+1):
		url = criticReviewsLink + '?page=' + str(i) + '&sort='
		r3 = requests.get(url)
		soup3 = bs4.BeautifulSoup(r3.content, 'html.parser')
		pageReviews = soup3.find_all('div', {'class': 'the_review'}) #[0]
		reviews += [rev.contents[0] for rev in pageReviews if rev.contents[0] != '' and rev.contents[0] != ' ']

	# Clean up the reviews by filtering punctuation, capitalization, new lines and stop/common words
	cleanedReviews = [''.join([char for char in r.lower() if char not in ['.', ',', '!', '?', '"', "'", ':', ';', '|', '~', '-', '[', ']', '(', ')']]) for r in reviews]
	cleanedReviews = [r.lower() for r in cleanedReviews]
	cleanedReviews = [r.replace('\n', ' ') for r in cleanedReviews]
	cleanedReviews = [r.split() for r in cleanedReviews]
	cleanedReviews = [[word for word in rev if word not in stopWords and word not in ignoreWords] for rev in cleanedReviews]

	# Get the total score for each tweet based on the positive/negative words
	# Because these are horror movies, some "bad" words like "terrifying" may actually be good
	# This could be a source of error
	posScore = [float(len([w for w in rev if w in positives])) for rev in cleanedReviews]
	negScore = [float(len([w for w in rev if w in negatives])) for rev in cleanedReviews]
	totalScore = sum([x - y for x,y in zip(posScore, negScore)])
	totalScore = float(totalScore) / len(cleanedReviews)
	totalScoreList.append(totalScore)
     

	# Get the most common pairs of words appearing next to each other
	words = list()
	allWords = [[words.append(word) for word in wordArray] for wordArray in cleanedReviews]
	commonPairs.append(Counter(list(bigrams(words))).most_common(10))

	# For each movie, make a dataframe with the information and append it to the main pandas dataframe
	t = pandas.DataFrame(list(zip(itertools.repeat(movieName), reviews, cleanedReviews)), columns=['Movie', 'Review', 'CleanReview'])
	table = pandas.concat([table,t], axis=0, ignore_index=True)
     

# For each movie, get counts of the words in the CleanReview column. This only stores the top 20.
for movieName,m in movies:
	count = table[table.Movie == movieName].CleanReview.apply(pandas.value_counts)
	commonWords.append(list(count.loc[:, count.sum()>2].sum().sort_values(ascending=False)[:20].index))

# Write the table to a .csv file
table.to_csv('HorrorMovies.csv')

# At the end of the file (after all the reviews and such), write the movie name, along with the score,
# list of common words and list of common pairs of words.
for movie,score,words,pairs in list(zip(movies, meterRatings, commonWords, commonPairs)):
	temp = list()
	temp.append(score)
	csvFile = open('HorrorMovies.csv', 'a')
	writer = csv.writer(csvFile)
	writer.writerow([movie[0]])
	writer.writerow(['', 'Rating:'] + temp)
	writer.writerow(['', 'Common Words:'] + words)
	writer.writerow(['', 'Common Pairs:'] + pairs)



##################
#PART 2
##################
    
#the ring    
c = [x for x in table.CleanReview.loc[8:207]] 
ring = pandas.DataFrame({'reviews': c}, index=None)
ring = ring.reviews.apply(pandas.value_counts)
ringtop = list(ring.loc[:,ring.sum()>2].sum().sort_values(ascending=False)[:20].index) 

#lights out   
l = [x for x in table.CleanReview.loc[1010:1150]] 
lights = pandas.DataFrame({'reviews': l}, index=None)
lights = lights.reviews.apply(pandas.value_counts)
lightstop = list(lights.loc[:,lights.sum()>2].sum().sort_values(ascending=False)[:20].index)   

comp = list(set(ringtop + lightstop))

df = pandas.DataFrame(columns=['The Ring', 'The Grudge'], index=comp)
for i in comp:
    if i not in ringtop:
        x = 0
    else:
        x = ring[i].sum()
    if i not in lightstop:
        y = 0
    else:
        y = lights[i].sum()
        
    df.loc[i]['The Ring'] = x
    df.loc[i]['The Grudge'] = y

plot = df.plot.scatter(x='The Ring', y='The Grudge')

for i in range(len(df)):
    if df.get_value(comp[i], 'The Ring') != 0 and df.get_value(comp[i], 'The Grudge') != 0:
        plot.annotate(comp[i], xy=(df.get_value(comp[i], 'The Ring'), df.get_value(comp[i], 'The Grudge')))



import matplotlib.pyplot as plt
import numpy

# Linear regression
[m,b] = numpy.polyfit(totalScoreList, meterRatings, 1)

fig = plt.figure(figsize=(8,6))
plt.xlabel('Average Movie Sentiment Score', fontsize=8)
plt.ylabel('Rotten Tomatoes Meter Score', fontsize=8)

plot = plt.scatter(totalScoreList, meterRatings)
fig.suptitle('Comparing the Movie Review Sentiment Score to the Rotten Tomatoes Meter Score')

x = numpy.array([min(totalScoreList), max(totalScoreList)])
f = lambda x: m * x + b
labelText = 'Linear Regression: ' + str(round(m,3)) + 'x + ' + str(round(b,3)) 
line = plt.plot(x, f(x), c='orange', label=labelText)

for i,name in enumerate(movies):
    plt.annotate(name[0], (totalScoreList[i], meterRatings[i]), xytext=(-5,15), textcoords='offset points', ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='green', alpha=0.2), arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
plt.legend(loc=2) # 4: "lower right'
plt.show()



