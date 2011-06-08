from urllib import urlopen
from xml.dom import minidom
import simplejson as json

import sys
from time import time

host = 'http://api.europeana.eu/'
path = 'api/opensearch.rss?searchTerms=europeana_country:poland+AND+enrichment_place_label:*+AND+(europeana_rights:*+OR+dc_rights:*)&startPage='
key = '&wskey=EPUGMNOLEH'

search_result = ''
final_result = ''

c = open('resulty', 'w')

start = time()

for i in range( 65 ):
    search_result = urlopen( host + path + str(i+1) + key ).read()
    search_result = minidom.parseString( search_result )

    links = search_result.getElementsByTagName( 'link' )[1:]

    for link in links:
        item_result = urlopen( link.childNodes[0].data ).read()
   #     item_result = minidom.parseString( item_result )

        print item_result#.toprettyxml( encoding='utf-8' )

 #       titles = item_result.getElementsByTagName( 'dc:title' )[0]
 #       rights = item_result.getElementsByTagName( 'dc:rights' )[0]

  #      print x
#        print titles.toprettyxml()
   #     print rights.toprettyxml()
        #for title, right in zip( titles, rights ):
        #    final_result += title.childNodes[0].data + '\n'
        #    final_result += right.childNodes[0].data + '\n\n'


end = time() - start
#print final_result
print end
c.close()

