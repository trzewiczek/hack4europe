import sys, math, shutil
from urllib import urlopen
import xml.etree.ElementTree as et
import xml.dom.minidom as md
import simplejson as json

if len( sys.argv ) < 2:
    print "\n>> No keyword specified. Try:"
    print ">> $ python get_data.py <keyword>\n"
    sys.exit()

# namespaces
srw = '{http://www.loc.gov/zing/srw/}'
europeana = '{http://www.europeana.eu}'
enrichment = '{http://www.europeana.eu/schemas/ese/enrichment/}'
dc = '{http://purl.org/dc/elements/1.1/}'
opensearch = '{http://a9.com/-/spec/opensearch/1.1/}'

url  = 'http://api.europeana.eu/api/opensearch.rss?searchTerms='
url += sys.argv[1]
url += '+AND+enrichment_place_latitude:*+AND+enrichment_period_label:*+AND+(europeana_rights:*+OR+dc_rights:*)'
url += '&wskey=EPUGMNOLEH&startPage='


# check how many records there are for such a query
search_result = et.XML( urlopen( url + '1' ).read() )
records_number = int( search_result.find( 'channel/'+opensearch+'totalResults' ).text )
queries_number = int( math.ceil( records_number / 12.0 ))

print 'There is '+str(records_number)+' records for "'+sys.argv[1]+'"'
# ask if the user wants to download this data
if len( sys.argv ) == 3 and sys.argv[2] == 'ask':
    answer = raw_input( 'Do you want to continue? [y/n]: ' )
    if( answer == 'n' or answer == 'N' ):
        sys.exit()

# final result
result = None
count = 1

# go through the search results and grab the records
for i in range( queries_number ):
    search_result = md.parseString( urlopen( url + str(i+1) ).read() )
    # take all the links but the first that points to search result
    links = search_result.getElementsByTagName( 'link' )[1:]
  
    for link in links:
	# print links to see it works
	print '[%d/%d]: %s' % (count, records_number, link.childNodes[0].data )
	count += 1

        item = et.XML( urlopen( link.childNodes[0].data ).read() )
	if result == None:
	    result = item
	else:
	    result.find(srw+'records').append( item.find( srw+'records/'+srw+'record'))

print "Download loop done\nConverting to JSON"

#xml = et.XML( open(sys.argv[1]).read())

records = list( result.find(srw+'records').iter(srw+'record') )

json_records = []

for record in records:
    json_record = {}

    item = record.find( srw+'recordData/'+dc+'dc' )

    uri = item.find(europeana+'uri')
    title = item.find(dc+'title')

    rights = item.find(europeana+'rights')
    if rights == None:
        rights = item.find(dc+'rights')

    lon = item.find(enrichment+'place_longitude')
    lat = item.find(enrichment+'place_latitude')
    start = item.find(enrichment+'period_label')


    if uri != None:
        json_record['options'] = { 'infoUrl': uri.text.replace('resolve', 'portal').split('.srw')[0]+'.html' }

    if title != None:
        json_record['title'] = title.text

    if rights != None:
        json_record['rights'] = rights.text

    if lon != None:
        json_record['point'] = { 'lon': lon.text, 'lat': lat.text }

    if start != None:
        json_record['start'] = start.text

    json_records.append( json_record )

filename = sys.argv[1]+'.json'

output = open( '../data/'+filename, 'w' )
output.write( json.dumps( json_records, indent=4 ))
output.close()

shutil.copyfile( '../data/'+filename, '../hack/vis/static/json/'+filename )
