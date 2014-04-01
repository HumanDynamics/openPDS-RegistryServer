#-*- coding: utf-8 -*-


from django.shortcuts import render_to_response
from django.template import RequestContext
from oauth2app.models import Client, AccessToken, Code
from base64 import b64encode
#from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import pdb

def client(request, client_id):
    client = Client.objects.get(key=client_id)
    template = {
        "client":client,
        "basic_auth":"Basic %s" % b64encode(client.key + ":" + client.secret),
        "codes":Code.objects.filter(client=client).select_related(),
        "access_tokens":AccessToken.objects.filter(client=client).select_related()}
    template["error_description"] = request.GET.get("error_description")
    return render_to_response(
        'client/client.html', 
        template, 
        RequestContext(request))

#def targeting(request):
#    template = {}
#    healthMetricValues = [ { "name": "", "value": None }, { "name": "Low", "value": "lpd:low" }, { "name": "Average", "value": "lpd:average" } , { "name": "High", "value": "lpd:high" } ]
#    template["healthMetricValues"] = healthMetricValues
#    socialHealthMetrics = [{"title": "Activity Level", "id": "activityLevel"},{"title": "Social Level", "id": "socialLevel"},{"title": "Focus Level", "id": "focusLevel"}]
#    template["socialHealthMetrics"] = socialHealthMetrics
#    sparql = SPARQLWrapper("http://linkedpersonaldata.org:3030/sparql")
#    sparql.setReturnFormat(JSON)   #pdb.set_trace()
#    genresQuery = "prefix lpd: <http://linkedpersonaldata.org/ontology#> prefix foaf: <http://xmlns.com/foaf/0.1/> prefix like: <http://ontologi.es/like#> select distinct ?genre from <http://linkedpersonaldata.org/members> where { ?member a foaf:Person . ?member foaf:account ?account . ?account lpd:sparqlEndpoint ?uri . service ?uri { ?member like:likes ?genre }}"
#    sparql.setQuery(genresQuery)
#    results = sparql.query().convert()
#    genres = [result["genre"]["value"] for result in results["results"]["bindings"]]
#    genres = [{ "name": "Doesn't matter", "uri": "" }] + [{ "name": genre[genre.rindex("/")+1:].replace("_", " "), "uri": genre } for genre in genres]
#    template["genres"] = genres
#    if request.method == "POST":
#        template["sent"] = "Offer sent"
##        try:
#        if "offerUri" in request.POST:
#            placeUri = request.POST["offerUri"]
#            title= request.POST["offerTitle"]
#            query = """
#                prefix lpd: <http://linkedpersonaldata.org/ontology#> 
#                prefix foaf: <http://xmlns.com/foaf/0.1/> 
#                prefix like: <http://ontologi.es/like#> 
#                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#                prefix spatial: <http://geovocab.org/spatial#>\n 
#                select distinct ?member ?reason 
#                from <http://linkedpersonaldata.org/members> 
#                from <http://linkedpersonaldata.org/ontology>
#                where { 
#                  ?member a foaf:Person . 
#                  ?member foaf:account ?account . 
#                  ?account  lpd:sparqlEndpoint ?uri . 
#                  service ?uri {\n """
#            #Remove all the silly whitespace added above solely for making the query look nice...
#            query = query.replace("        ", "")
#            if request.POST.get("activityLevel", "") != "":
#                query += "    ?member lpd:recentActivityLevel %s .\n " % request.POST.get("activityLevel", "")
#            if request.POST.get("socialLevel", "") != "":
#                query += "    ?member lpd:recentSocialLevel %s .\n " % request.POST.get("socialLevel", "")
#            if request.POST.get("focusLevel", "") != "":
#                query += "    ?member lpd:recentFocusLevel %s .\n " % request.POST.get("focusLevel", "")
#            if request.POST.get("genre", "") != "":
#               query += "    ?member like:likes <%s> .\n " % request.POST.get("genre", "")
#            query += "    ?member lpd:hasSuggestion ?suggestion .\n "
#            query += "    ?suggestion spatial:Feature <%s> .\n " % placeUri
#            query += "    ?suggestion lpd:reason ?reasonUri .\n "
#            query += "}\n "
#            query += "  ?reasonUri rdfs:label ?reason .\n "
#            query += "}"
#            template["query"] = query
#            sparql.setQuery(query.replace("\n", ""))
#            results = sparql.query().convert()
#            offers = [{ "reason": result["reason"]["value"], "uri": placeUri , "member": result["member"]["value"] } for result in results["results"]["bindings"]]
#            token="fe501324f7"
#
#            for offer in offers:
#                uuid = offer["member"][-39:-3] 
#                reason=offer["reason"]
#                nodeUri = "lpd://assistant%s" % placeUri[placeUri.rindex("/"):]
#                path = "http://pds.linkedpersonaldata.org/api/personal_data/notification/?format=json&bearer_token=%s&datastore_owner__uuid=%s"%(token, uuid)
#                data = '{ "datastore_owner" : { "uuid": "%s" }, "title": "%s", "content": "%s", "type": 1, "uri": "%s" }' % (uuid, title, reason, nodeUri)
#                r = requests.post(path, data=data, headers={"content-type":"application/json"})
#                template["response"] = r.text
##                print r.text
##        except Exception as e:
##            raise Exception(e)
#            
#
#    return render_to_response(
#        "client/targeting.html",
#        template, 
#        RequestContext(request)) 
