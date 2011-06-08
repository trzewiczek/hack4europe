# Create your views here.
from datetime import datetime, timedelta
import random
from django.http import HttpResponse
import urllib
import simplejson as json
from django.shortcuts import render_to_response


def main(request):
    return render_to_response('vis/main.html')

def data(request, id):

    latMin = 40
    latDelta = 20
    lonMin = -5
    lonDelta = 30

    start = request.REQUEST['start'].rjust(4,'0')
    if len(start) == 4:
        start += '-01-01'
    end = request.REQUEST['end'].rjust(4,'0')
    if len(end) == 4:
        end += '-01-01'
    callback = request.REQUEST['callback']
    ##q = request.REQUEST['q'] <- kwerenda (np. 'mozart beethoven')

    data = json.loads( open('/home/mikus/Projekty/hack4europe/statbrowser/hack/vis/static/json/mozart.json').read() )
    data = [ d for d in data if d.has_key('start') and d['start'] > start.split('-')[0] and d['start'] < end.split('-')[0] ]

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    delta = (end - start).total_seconds()


    out = []
    for i in data:
        out.append('{title:"%s", start:"%s", point: {lat: %d, lon: %d}, options: { description: "opis", infoUrl: "%s"}}' % (i['title'], i['start'], float(i['point']['lat']), float(i['point']['lon'], i['options']['infoUrl'])))

    return HttpResponse('%s([%s])' % (callback, ','.join(out)))

def info(request, id):
    out = '<div><h4>name</h4><p>detail description</p></div>'
    return HttpResponse(out)

def rights(request):
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'cyan', 'brown', 'navy']
    rights = [ "Th\u00fcringer Universit\u00e4ts- und Landesbibliothek, Jena",
                "ddrbildarchiv.de\u00ae",
                "Deutsches Dokumentationszentrum f\u00fcr Kunstgeschichte - Bildarchiv Foto Marburg [Resource]",
                "Th\u00fcringer Universit\u00e4ts- und Landesbibliothek, Jena"
                "Ok\u00e4nd",
                "Public Domain",
                "Deutsche Fotothek",
                "http://creativecommons.org/publicdomain/mark/1.0/"
    ]
    out = []
    for i in range(len(rights)):
        out.append({'id':"right%d" % i, 'title': "title %d" % i, 'color': "%s" % ( i, rights[i], color[i] )})
    return HttpResponse(json.dumps(out), mimetype="application/json")
