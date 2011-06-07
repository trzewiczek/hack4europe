# Create your views here.
from datetime import datetime, timedelta
import random
from django.http import HttpResponse
import urllib
import simplejson as json
from django.shortcuts import render_to_response

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

def main(request):
    return render_to_response('vis/main.html')

def data(request):
    latMin = 40
    latDelta = 20
    lonMin = -5
    lonDelta = 30

    start = request.REQUEST['start']
    end = request.REQUEST['end']
    callback = request.REQUEST['callback']
    ##q = request.REQUEST['q'] <- kwerenda (np. 'mozart beethoven')

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    delta = (end - start).total_seconds()

    out = []
    for i in range(10):
        out.append('{title:"Item %d", start:"%s", point: {lat: %d, lon: %d}, options: { description: "opis", infoUrl: "info/id"}}' % (i, (start + timedelta(seconds = random.random() * delta)).isoformat(), latMin + random.random() * latDelta, lonMin + random.random() * lonDelta))

    return HttpResponse('%s([%s])' % (callback, ','.join(out)))

def info(request, id):
    out = '<div><h4>name</h4><p>detail description</p></div>'
    return HttpResponse(out)
