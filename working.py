# Author : Rishabh Jain
# rishabhrjjain1997@gmail.com

# A simple program to recommend movies on the basis of what your friends like and as well as the similarity of your taste with them in the movie sector.

from math import sqrt
from recommendations import friend_ratings

class distance:

	def euclid_distance(prefs ,person1 ,person2): 

		shared_items = {}

		for item in prefs[person1]:
			if item in prefs[person2]:
				shared_items[item]=1

		if len(shared_items)==0:
			return 0  # Nothing was found common, no similarity at all

		dist =0

		for item in shared_items:
			dist = dist + pow(prefs[person2][item]-prefs[person1][item],2)

		return 1/(1+sqrt(dist))

	def pearson_distance(prefs, person1, person2):

		shared_items = {}

		for item in prefs[person1]:
			if item in prefs[person2]:
				shared_items[item]=1

		if len(shared_items)==0:
			return 0  # Nothing was found common, no similarity at all

		n = len(shared_items)

		sum1 = sum([prefs[person1][item] for item in shared_items])
		sum2 = sum([prefs[person2][item] for item in shared_items])

		sumsq1 = sum([pow(prefs[person1][item],2) for item in shared_items])
		sumsq2 = sum([pow(prefs[person2][item],2) for item in shared_items])

		psum = sum([prefs[person1][item]*prefs[person2][item] for item in shared_items])

		num = psum - (sum1*sum2)/n
		den = sqrt((sumsq1-pow(sum1,2)/n)*(sumsq2-pow(sum2,2)/n))

		if den==0:
			return 0 # To avoid divide by zero error

		return (num/den)

class Recommender:

	def top_matches(prefs,person,n): # The top n people you would like to consider while doing the analysis
		scores = [(distance.pearson_distance(prefs,person,other),other) for other in prefs if other!=person]
		scores.sort()
		scores.reverse()
		return scores[0:n]

	def get_recommendations(prefs,person):
		
		total = {}
		simsum = {}
		rankings = []
		for other in prefs:
			if other!=person:
				score = distance.pearson_distance(prefs,person,other) # Euclid Distance may also be used here, though the movie recommendations might change.
				for item in prefs[other]:
					if item not in prefs[person]:
						total.setdefault(item,0)
						simsum.setdefault(item,0)
						total[item]=total[item]+prefs[other][item]*score
						simsum[item]=simsum[item]+score
						rankings = [(val/simsum[item],item) for item,val in total.items()]
		rankings.sort()
		rankings.reverse()
		return rankings


print('Enter your username')
user = input()

if user in friend_ratings:
	print('Depending upon friend\'s interests, we recommend the following movies for you.')
	array = Recommender.get_recommendations(friend_ratings,user)
	if len(array)==0:
		print('Sorry, nothing for you')
	else:
		for rating,movie in array:
			print(movie)
else:
	print('May be you input the wrong username')
