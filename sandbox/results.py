from urllib import urlopen
from xml.dom import minidom
import simplejson as json

import sys
from time import time

search_result = ''
final_result = ''

start = time()

for i in range( 1 ):
    search_result = urlopen( 'http://api.europeana.eu/api/opensearch.rss?searchTerms=mozart&startPage='+str(i+1)+'&wskey=EPUGMNOLEH' ).read()
    search_result = minidom.parseString( search_result )
    links = search_result.getElementsByTagName("link")[1:]

    for link in links:
        item_result = urlopen( link.childNodes[0].data ).read()
        final_result += item_result


end = time() - start
print final_result
print end

