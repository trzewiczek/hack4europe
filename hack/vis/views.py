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

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    delta = (end - start).total_seconds()

    out = []
    for i in range(3):
        out.append('{title:"Item %d", start:"%s", point: {lat: %d, lon: %d}, options: { description: "opis", infoUrl: "info/id"}}' % (i, (start + timedelta(seconds = random.random() * delta)).isoformat(), latMin + random.random() * latDelta, lonMin + random.random() * lonDelta))

    return HttpResponse('%s([%s])' % (callback, ','.join(out)))

def info(request, id):
    out = '<div><h4>name</h4><p>detail description</p></div>'
    return HttpResponse(out)

def rights(request):
    colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'pink', 'brown', 'navy', 'orange', 'lightgray']
    out = []
    for i in range(10):
        out.append({'id':"right%d" % i, 'title': "title %d" % i, 'color': "%s" % colors[i]})
    return HttpResponse(json.dumps(out), mimetype="application/json")
