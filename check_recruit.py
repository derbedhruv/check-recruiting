# cache local copies of websites of companies and keep checking if something was posted by them
# will only look at the difference between the <html> portion
# if something is found, send an email to me
import sys, requests
from bs4 import BeautifulSoup
from smtplib import SMTP

# get username and password from the login.txt file
try:
  with open('login.txt', 'r') as f:
    smptpserver, username, password, from_addr, to_addr = f.read().split()
except IOError:
  print "File login.txt not found!"
  sys.exit(0)
except:
  print "something's wrong with the login.txt file.. please check!"
  sys.exit(0)

def sendmessage(SUBJECT, TEXT):
  # REFERENCES:
  # * https://community.webfaction.com/questions/8989/sending-mail-with-python
  msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
  s = SMTP()
  s.connect(smptpserve)
  s.login(username, password)
  s.sendmail(from_addr, [to_addr], msg)
  s.quit()

# check if the websites have any differences
def checksite(SITE):
  # will check given site for whether there hvae been any changes from the cached copy
  # if there has been any then will return the difference, else None
  # if there is no cached copy, then will cache the local one and do nothing
  FILENAME = re.search('\.[a-z]+\.', SITE).group(0)[1:-1]   # returns THIS in www.THIS.whatever
  def cachecopy(s, SITE):
    # save the string s, containing the html of the page, to a local file with a special name
    with open('cached/' + FILENAME + '.cachedstuff', 'w') as f:
      f.write(s)
  # read in the content of the site and only look at stuff between <body> and <body>
  # and remove any javascript and stuff
  res = requests.get(SITE)
  s = re.search('<body>.+</body>', res.text.replace('\n', '')).group(0)

  # now, if there's a cached copy, compare with it. If there isn't one, then replcae it with this
  try:
    with open('cached/' + FILENAME + '.cachedstuff', 'w') as f:
      cached_copy = f.read()

sendmessage('Recruiting alert', 'We found something.')
