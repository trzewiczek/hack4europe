from urllib import urlopen
from xml.dom import minidom

import sys
from time import time

search_result = ''
start = time()

for i in range( 2 ):
    search_result += urlopen( 'http://api.europeana.eu/api/opensearch.json?searchTerms=mozart&startPage='+str(i+1)+'&wskey=EPUGMNOLEH' ).read()

print time() - start

#print search_result

