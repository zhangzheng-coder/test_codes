import googlemaps
import datetime
# Replace the API key below with a valid API key.
gmaps = googlemaps.Client(key='AIzaSyAh2PIcLDrPecSSR36z2UNubqphdHwIw7M')

#Automate to read from DB 
sources_file = open('sources.dat','r')
destinations_file = open('sources.dat','r')
sources = sources_file.read().splitlines()
destinations = destinations_file.read().splitlines()
                                     
#read distance matrix from google API. Testing for more options pending. 
matrix_distance = gmaps.distance_matrix(sources, destinations, mode="driving")

#loop to generate the distance matrices. 
for n in sources:
	k=sources.index(n)
	for nn in destinations:
		kk=destinations.index(nn)
		val= matrix_distance['rows'][k]['elements'][kk]['distance']['value']
		print val
		