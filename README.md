# Simple script to keep checking recruiting websites for updates
Check the campus hiring websites of big companies for updates on campus events and hiring events. As a Stanford student, there are a lot of opportunities to interview with big (non-tech) companies, and the best way to do this is to go to Stanford recruiting events. Unfortunately, they usually update stuff on their Stanford-specific webpages. I wanted a customized alert system which would inform me when companies post things on their websites and send me an email. 

Another motivation to do this is that I'm not taking any CS courses this quarter and I wanted to keep my coding (Python) skills sharp.

# How to use
Anyone can easily make use of this script! It has been written in a very modular fashion. You'd need to do the following:
* Clone the repo, preferably on a server where you'll be running it on a cronjob. You could also setup a cronjob to run it on your own computer, but that'd complicate things.
* Within the cloned repo folder, create the following files:
  * `login.txt` - This should contain the following, separated by a newline (i.e. each of the following should be on a newline):
    1. mailbox server for outgoing mails. I'm using webfaction (and this script is hosted on a cronjob on webfaction)
    2. username for mailbox
    3. password for mailbox
    4. the email address FROM which the mail wuold be sent - this could be pretty much anything
    5. the email address TO whom the notification mail would be sent - this should be your personal email address which you should have push notifications for, for this whole thing to really work well.
  * `companies.txt` - this file contains a web url ON EACH NEW LINE of the specific recruiting/events/job openings page which you want to check. It should be the sort of webpage that the company keeps updating to post new job openings (or anything you're interested in) on. **NOTE** - The urls should be of the form `http://something.something.something/whatever`, for instance `www.job.net` or `jobs.startup.ai` - the regex checks for this pattern and will throw an error if it doesn't find it. Yes, this is a TODO to make the regex system more robust. Feel free to reach out or send a pull request if you have a better regex!
  * `log.log` - you shouldn't need to create this file, but it'd be good to create an empty one using `touch log.log` - this will contain the timestamp and log of whatever happened.
  
* Finally, setup a cronjob by running the following on your terminal
  ```
  crontab -e
  ```
  and entering the following line (assuming you cloned the check-recruiting directory to your $HOME directory):
  ```
  0 15 * * * ~/check_recruiting/check_recruit.py >> ~/check-recruiting/log.log
  ```
  THe 0 and 15 means that this script will run at 15:00 hrs UTC everyday - that's 8AM Pacific Time (early in the morning where I stay). Do change it to whatever's convenient for you - see [here](http://stackoverflow.com/questions/5200551/how-to-set-a-cron-job-to-run-at-a-exact-time) if you're lost. The `>>` means that any error messages from the output of running the python script will be written to the log file as well, so you can check it and see what happened.
  
Please create an issue if you face any problems - I'm happy to make a robust, reusable piece of code here!
