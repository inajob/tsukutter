import urllib2
import re

def get(url):
  print "get " +url
  try:
    r = urllib2.urlopen(url);
    url = r.geturl();
    return url;
  except:
    print "failed" + url;
    return url;

def getrepl(m):
  return get(m.group(0));

def conv(s):
  rurl = re.compile(r'http://[/a-zA-Z.\-#%&?0-9_]+');
  return rurl.sub(getrepl, s);

if __name__=='__main__':
  print "hello test"
  print conv('aaa http://yahoo.jp/ hogehoge http://google.com/ ');
