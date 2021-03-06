#!/usr/local/bin/python2.7
# cache local copies of websites of companies and keep checking if something was posted by them
# will only look at the difference between the <html> portion
# if something is found, send an email to me
import os, sys, requests, difflib, re, datetime, time
from smtplib import SMTP

app_folder = os.path.dirname(os.path.realpath(__file__))
SAVE_FOLDER = os.path.join(app_folder, 'cached/')

# get username and password from the login.txt file
def get_info():
  try:
    with open(os.path.abspath(os.path.join(app_folder,'login.txt')), 'r') as f:
      smptpserver, username, password, from_addr, to_addr = f.read().split()
      return smptpserver, username, password, from_addr, to_addr 
  except IOError:
    print "File login.txt not found!"
    sys.exit(0)
  except:
    print "something's wrong with the login.txt file.. please check!"
    sys.exit(0)

def sendmessage(SUBJECT, TEXT):
  # REFERENCES:
  # * https://community.webfaction.com/questions/8989/sending-mail-with-python
  smptpserver, username, password, from_addr, to_addr = get_info()
  print 'sending email to', to_addr
  msg = 'Subject: {}\n\n{}'.format(SUBJECT.encode('utf-8'), TEXT.encode('utf-8'))
  s = SMTP()
  s.connect(smptpserver)
  s.login(username, password)
  s.sendmail(from_addr, [to_addr], msg)
  s.quit()

# check if the websites have any differences
def checksite(SITE):
  # will check given site for whether there hvae been any changes from the cached copy
  # if there has been any then will return the difference, else None
  # if there is no cached copy, then will cache the local one and do nothing
  FILENAME = re.search('\.[a-z]+\.', SITE)   # returns THIS in www.THIS.whatever
  if FILENAME == None:
    FILENAME = 'localhost'
  else:
    FILENAME = FILENAME.group(0)[1:-1] 
  print FILENAME
  def cachecopy(s, FILENAME):
    # save the string s, containing the html of the page, to a local file with a special name
    f = open(os.path.join(SAVE_FOLDER, FILENAME + '.cachedstuff'), 'w')
    f.write(s.encode('utf-8')); f.close()
  # read in the content of the site and only look at stuff between <body> and <body>
  # and remove any javascript and stuff
  res = requests.get(SITE)
  s = re.search('<body.+</body>', res.text.replace('\n', '')).group(0)

  # now, if there's a cached copy, compare with it. If there isn't one, then replcae it with this
  try:
    with open(SAVE_FOLDER + FILENAME + '.cachedstuff', 'r') as f:
      cached_copy = f.read()
    if (s == cached_copy):
      # nothing's happened.
      print 'no change observed'
    else:
      # update the cached copy
      cachecopy(s, FILENAME)
      site_diff = ''.join([x[2] for x in difflib.ndiff(s, cached_copy) if x[0] == '-'])
      if len(site_diff) > 10 and site_diff.count(' ') > 0:	
        # less than 10 characters difference is minor, no spaces in 10 chars means that the change is not human readable
        print "there's been a change!"
        sendmessage('Recruiting Alert for ' + SITE, site_diff)
      return site_diff
  except IOError:
    cachecopy(s, FILENAME)
  return None
# sendmessage('Recruiting alert', 'We found something.')

# test personal website
# checksite('http://derbedhruv.webfactional.com/')
if __name__ == '__main__':
  # update log informing that check was done on date
  with open('log.log', 'a') as log:
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
    log.write(sttime + 'Checked' + '\n')

  # read in list of sites, check them
  with open(os.path.abspath(os.path.join(app_folder,'companies.txt')), 'r') as f:
    companies = f.read().split()

  for company in companies:
    checksite(company)

  # add extra one for Uber - uses an API to search for positions
  uber = 'https://www.uber.com/api/jobs/filter?country=united-states-of-america&city=all&team=all&subTeam=all&keywords=associate%20product%20manager&page='
  if requests.get(uber).json()['jobs'] != []:
    print 'Uber APM has opened!'
