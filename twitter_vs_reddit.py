import pandas as pd
import matplotlib.pyplot as plt

# twitter trends
twitter = pd.read_csv('twitter.csv')
trends = twitter['Trend'].tolist()

# filter out junk trends
trends.remove('es')
trends.remove('b')
trends.remove('est')

# subreddit titles
r1 = list(set([str(x).lower() for x in pd.read_csv('sports.csv')['Title'].tolist()]))
r2 = list(set([x.lower() for x in pd.read_csv('television.csv')['Title'].tolist()]))
r3 = list(set([x.lower() for x in pd.read_csv('worldnews.csv')['Title'].tolist()]))
r4 = list(set([x.lower() for x in pd.read_csv('politics.csv')['Title'].tolist()]))
r5 = list(set([x.lower() for x in pd.read_csv('uplifting_news.csv')['Title'].tolist()]))
r6 = list(set([x.lower() for x in pd.read_csv('news.csv')['Title'].tolist()]))
reddits = r1 + r2 + r3 + r4 + r5 + r6

toAdd = list()
for trend in trends:
    temp = [post for post in reddits if trend in post]
    if len(temp) == 0:
        temp = "None"
    toAdd.append('Trend: ' + str(trend) + ', Article Matches: ' + str(temp))

t = pd.DataFrame(list(toAdd), columns=['Matches'])
pd.set_option('display.max_colwidth', 1000)

toAdd2 = list()
for trend in trends:
    count = [post for post in reddits if trend in post]
    toAdd2.append((trend, len(count)))

t2 = pd.DataFrame(toAdd2, columns=['Trend', 'ArticleMatchCount'])

# plot
fig = plt.figure()
plt.ylim([0, 100])
plt.xlabel('Twitter Trend ID', fontsize=8)
plt.ylabel('# Subreddit Post Title Matches', fontsize=8)

plt.bar(range(len(t2.Trend)), t2.ArticleMatchCount)
fig.suptitle('Twitter Trends vs. Subreddit Post Titles')

# top and bottom matches
topTrends = t2[t2.ArticleMatchCount >= 20]
bottomTrends = t2[t2.ArticleMatchCount < 3]

zeroMatches= t2[t2.ArticleMatchCount == 0]
oneMatch = t2[t2.ArticleMatchCount >= 1]
fiveMatches = t2[t2.ArticleMatchCount >= 5]
tenMatches = t2[t2.ArticleMatchCount >= 10]
twMatches = t2[t2.ArticleMatchCount >= 20]


# top correlated trends
plt.text(1, 70, '#election', fontsize=12)
plt.text(186, 82, '#season', fontsize=12)
plt.text(82, 64, '#law', fontsize=12)
plt.text(148, 54, '#right', fontsize=12)
plt.text(109, 51, '#game', fontsize=12)
plt.text(211, 230, '#new', fontsize=12)
plt.text(40, 96, '#ca', fontsize=12)
plt.text(76, 96, '#nc', fontsize=12)

plt.show()

