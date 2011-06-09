import sys
from urllib import urlopen
import xml.etree.ElementTree as et
import xml.minidom as md

result = None

url  = 'http://api.europeana.eu/api/opensearch.rss?searchTerms='
url += sys.argv[1]
url += '+AND+enrichment_place_latitude:*+AND+enrichment_period_label:*+AND+(europeana_rights:*+OR+dc_rights:*)'
url += '&wskey=EPUGMNOLEH&startPage='

# check how many records there are for such a query
search_result = et.XML( urlopen( url + '1' ).read() )
records_number = int( search_result.find( 'rss/chanel/totalSearch' ).text )

# go through the search results and grab the records
for i in range( records_number ):
    search_result = md.parseString( urlopen( url + str(i+1) ).read() )
    # take all the links but the first that points to search result
    links = search_result.getElementsByTagName( 'link' )[1:]

    for link in links:
        item = et.XML( urlopen( link.childNodes[0].data ).read() )
	if result == None:
	    result = item
	else:
	    result.find('path/to/records').append( item.find( 'path/to/record' ))

print et.tostring( result )
