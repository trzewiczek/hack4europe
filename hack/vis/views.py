# Create your views here.
from django.http import HttpResponse
import urllib
import simplejson as json

def start( request ):
	result = json.loads( urllib.urlopen( 'http://cecyf.megivps.pl/api/json/' ).read() )
	html = '<ul>'
	for i in result['datasets']:
		html += '<li><a href="/load/'+str(i['idef'])+'/">'+ i['name']+ '</a> - ' + i['description'] + '</li>'

	html += '</ul>'

	return HttpResponse( html )

def load( request, idef ):
	result = json.loads( urllib.urlopen( 'http://cecyf.megivps.pl/api/json/dataset/'+idef+'/view/0/issue/2011/' ).read() )
	html = '<ul>'
	for i in result['data']:
		#html += '<li><a href="/load_views">'+ i['name']+ '</a> - ' + i['description'] + '</li>'
		html += '<li>'+ i['name'] + '<br />' +str(i['v_total'])+ '</li>'

	html += '</ul>'

	return HttpResponse( html )

