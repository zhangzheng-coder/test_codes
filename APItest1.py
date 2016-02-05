import googlemaps
import datetime
import pprint
# Replace the API key below with a valid API key.
gmaps = googlemaps.Client(key='AIzaSyAh2PIcLDrPecSSR36z2UNubqphdHwIw7M')

#Automate to read from DB 
sources_file = open('sources.dat','r')
destinations_file = open('destinations.dat','r')
sources = sources_file.read().splitlines()
destinations = destinations_file.read().splitlines()
                                     
#read distance matrix from google API. Testing for more options pending. 
matrix_distance = gmaps.distance_matrix(sources, destinations, mode="driving")
#loop to generate the distance matrices. 

pprint.pprint(sources)

pprint.pprint(matrix_distance)

dtest={}

for n in sources:
	k=sources.index(n)
	for nn in destinations:
		kk=destinations.index(nn)
		dtest[n,nn]=matrix_distance['rows'][k]['elements'][kk]['distance']['value']

for s_idx, src in enumerate(sources):
	for dest_idx, dest in enumerate(destinations):
		dtest[src,dest]=matrix_distance['rows'][s_idx]['elements'][dest_idx]['distance']['value']

pprint.pprint(dtest)
		
