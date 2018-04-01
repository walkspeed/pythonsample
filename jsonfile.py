import json

jsonfile = "jsontest.json"

def loadJsonFile():
    jf = open( jsonfile, 'r' )
    return json.load( jf )

def saveJsonFile( pyobject, filename ):
    #str = json.dumps( pyobject )
    json.dump( pyobject, open( filename, 'w+' ) )

jsobject = loadJsonFile()

print '[url] : ', jsobject['url']

jsobject['url'] = "http://127.0.0.1/mytest.html"

saveJsonFile( jsobject, jsonfile )

jsobject = loadJsonFile()
print '[url] : ', jsobject['url']
