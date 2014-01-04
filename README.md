## FreeDoge - the open source Django Dogecoin faucet

Please feel free to let me know what you think!  (Or if you find
bugs!)

**DISCLAIMER:** Wrote most of this while inebriated so there's a lot of fixing/cleaning up to do.

Wanna send some DOGE my way? :)  DKx9wmgB1DwdT5hLnPiKbpzLgFTtDcDZGS

#### Setting up your own faucet

0. Install dependencies.  Get the [Heroku toolbelt](https://toolbelt.heroku.com/) and install virtualenvwrapper:  
```pip install virtualenvwrapper```
1. Create a virtual environment:  
```mkvirtualenv freedoge```
2. Clone the code:  
```mkdir ~/freedoge && cd ~/freedoge && git clone https://github.com/craigatron/freedoge.git .```
3. Create a Heroku app and deploy:  

        heroku create    
        git push heroku master
4. Set each of the environment variables in [config.example](https://github.com/craigatron/freedoge/blob/master/config.example)  
```heroku config:set DOGEUSER=username```
5. Sync the remote database:  
```heroku run python manage.py syncdb```

Feel free to get in touch with me if you have any issues!
