# Create your views here.
from datetime import datetime, timedelta
import random
from django.http import HttpResponse
import urllib
import simplejson as json
from django.shortcuts import render_to_response

def main(request):
    try:
        cn = request.REQUEST['cn']
    except:
        cn = 'mozart'
    request.session['collection_name'] = cn
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
    rights_list = request.session['rights_list']
    ##q = request.REQUEST['q'] <- kwerenda (np. 'mozart beethoven')
    data = json.loads( open('/home/mikus/Projekty/hack4europe/statbrowser/hack/vis/static/json/'+request.session.get('collection_name', 'mozart')+'.json').read() )
#    data = json.loads( open('/home/mikus/Projekty/hack4europe/statbrowser/hack/vis/static/json/mozart.json').read() )
    data = [ d for d in data if d.has_key('start') and d['start'] > start.split('-')[0] and d['start'] < end.split('-')[0] ]
    data = [ d for d in data if d.has_key('rights') and d['rights'] == rights_list[int(id)] ]
    data += [ d for d in data if not d.has_key('rights') and rights_list[int(id)] == 'None']

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    delta = (end - start).total_seconds()


    out = []
    for i in data:
        out.append('{title:"%s", start:"%s", point: {lat: %d, lon: %d}, options: { description: "opis", infoUrl: "info/%s"}}' % (i['title'], i['start'], float(i['point']['lat']), float(i['point']['lon']), i['options']['infoUrl']))

    return HttpResponse('%s([%s])' % (callback, ','.join(out)))

import urllib

def info(request, id):
    out = ''
    filehandle = urllib.urlopen(id)
    for lines in filehandle.readlines():
        out += lines
    filehandle.close()
    return HttpResponse(out)


def rights(request):
    r_list = json.loads( open('/home/mikus/Projekty/hack4europe/statbrowser/hack/vis/static/json/'+request.session.get('collection_name', 'mozart')+'.json').read() )
    rights_set = set()
    rights_list = []

    for r in r_list:
        try:
            if r['rights'] == '' and r['rights'] == ' ':
                rights_set.add( 'None' )
            else:
                rights_set.add( r['rights'] )
        except:
            rights_set.add( 'None' )

    for r in rights_set:
        rights_list.append( r )
        
    request.session['rights_list'] = rights_list

    colors = ['red', 'blue', 'green', 'yellow', 'purple']
    out = []
    for i in range(len(rights_list)):
        out.append({'id':"%d" % i, 'title': "%s" % rights_list[i], 'color': "%s" % colors[i%len(colors)]})
    return HttpResponse(json.dumps(out), mimetype="application/json")
