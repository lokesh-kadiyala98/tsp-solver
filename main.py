import urllib.request

url = "https://raw.githubusercontent.com/pdrozdowski/TSPLib.Net/master/TSPLIB95/tsp/berlin52.tsp"
filename = "berlin52.tsp"

urllib.request.urlretrieve(url, filename)