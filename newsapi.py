import newspaper
import pandas as pd
import time

# function to print data table 
# def print_full(x):
#     pd.set_option('display.max_rows', len(x))
#     print(x)
#     pd.reset_option('display.max_rows')

cols = ['title', 'date', 'source']
df = pd.DataFrame(columns=cols)

#BBC, USA Today, Washington Post
bbc = newspaper.build('http://www.bbc.com/news')#, memoize_articles = False)
usa = newspaper.build('http://www.usatoday.com/news)')#, memoize_articles = False)
wapo = newspaper.build('https://www.washingtonpost.com')#, memoize_articles = False)

for article in bbc.articles:	
	article.download()
	try:
		article.parse()

		if '2017' in str(article.publish_date):
			x = [article.title, str(article.publish_date)[:10], 'BBC News']
			for val in x:
				if (val != None):
					if (val != ''):
						data_dict = dict(zip(cols, x))
						df = df.append(data_dict, ignore_index=True)
	except newspaper.article.ArticleException:
		pass				
	except UnicodeDecodeError:
		pass

for article in usa.articles:	
	article.download()
	try:
		article.parse()

		if '2017' in str(article.publish_date):
			x = [article.title, str(article.publish_date)[:10], 'USA Today']
			for val in x:
				if (val != None):
					if (val != ''):
						data_dict = dict(zip(cols, x))
						df = df.append(data_dict, ignore_index=True)

	except newspaper.article.ArticleException:
		pass				
	except UnicodeDecodeError:
		pass

for article in wapo.articles:	
	article.download()
	try:
		article.parse()

		if '2017' in str(article.publish_date):
			x = [article.title, str(article.publish_date)[:10], 'Washington Post']
			for val in x:
				if (val != None):
					if (val != ''):
						data_dict = dict(zip(cols, x))
						df = df.append(data_dict, ignore_index=True)

	except newspaper.article.ArticleException:
		pass				
	except UnicodeDecodeError:
		pass

df = df.drop_duplicates().sort_values('date')
#print_full(df)

#trending topics on Google
trending = pd.DataFrame({'topic': newspaper.hot()})
trending['date'] = time.strftime("%Y-%m-%d")
#print_full(trending)



