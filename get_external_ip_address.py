from urllib.request import Request, urlopen

def request(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read()

def ip_request():
    contents = request('https://www.whatismyip.com/')    
    lines = ip_request().decode("utf-8").split("\n")
    ip_v4_line = next(line for line in lines if line.startswith("My Public IPv4 is:"))
    href_attr = next(attr for attr in ip_v4_line.split() if attr.startswith("href="))
    return href_attr.split("/")[-2]

def ip_request2():
    contents = request("https://www.google.com/search?client=firefox-b-d&q=what+is+my+ip")