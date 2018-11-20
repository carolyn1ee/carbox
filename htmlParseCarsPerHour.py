import urllib.request
#https://data.wprdc.org/dataset/allegheny-county-traffic-counts/resource/8edd8a76-8607-4ed3-960f-dcae914fd937?view_id=a9051235-807c-43e3-afb7-7743a80a9d01
#here is the data website
url = "https://data.wprdc.org/datastore/odata3.0/8edd8a76-8607-4ed3-960f-dcae914fd937"

with urllib.request.urlopen(url) as response:
   html = response.read()
   

#use html parser to get the html code from the website.

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/#tag 
#documentation on html parsing

text = soup.getText()


def convertSoupToList(text):
    l = text.split("\n\n\n\n\n")
    i = 0
    while i < len (l):
        l[i] = l[i].splitlines()
        if len (l[i]) == 0 or not l[i][0].isdigit():
            l.pop(i)
        else:
            i += 1
    return l
#turns a list into a dictionary with the keys as the location (lat,long)
#and the valuse as the list of the number of cars at each hour.
def convertListToDict(l):
    d = {}
    for elem in l:
        lat = elem[3]
        long = elem[2]
        data = elem [4:]
        d[(lat, long)] = data 
    return d
    
#returns the number of cars that are at the location(lat, long) and 
#time (on a 24 hour clock)
def getCarsAtLocationAndTimeFromDict(location, dict, time):
    return dict[location][time - 1]

def main():
    l = convertSoupToList (text)
    d = convertListToDict (l)
    print (getCarsAtLocationAndTimeFromDict(('40.58620733','-79.82843807'), d, 2))
main()













#print (l)

#print (soup.getText())

#for line in (soup.prettify().splitlines()[:60]):
#    print (line)



#fileobj = urllib.urlopen(url)
def capTrue (s):
    return s.replace ("true", "True")
    
html = capTrue (html.decode())
#dik = eval (html)
#print (dik["success"])

