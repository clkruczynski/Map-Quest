import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
orig = "Mabalacat City, Pampanga"
dest = "Angeles City, Pampanga"
key = "wMz7DsbJzW5VjP5iOmrXqKMrOISKfgaY"

url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})

json_data = requests.get(url).json()
print(json_data)