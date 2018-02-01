# PricingScrapper
A webscraper which uses anonymous proxy IP to scrape and has intelligence to delay scraping, changing iP on request.
Here I have tried to explain and detail out usage of TOR with PRIVOXY to avoid identity in the world of bots/internet and use dynamic proxy IP from tor to scrape/crawl website in external world.


Key Steps to Configure
1. Install two packages on your system. I am using MAC OS, so will detail below. I beleive you can visit respective URL of sites to download and set it up first.


```
brew install tor

brew install privoxy

```
Just google it and you will get versions for your OS.

2. Run following command to set a password for tor.
```
tor --hash-password dhd8adkeiuLDKGSU937
```
As you hit the above, you would get a hash output - something like below.
```
16:XXXXXF68ECB6360C5729B89A8F125CB4XXXXX
```
Copy both the password and hashed password into a file. In my case, i just used randmon password as you can see the value i passed for --hash-password. Note that you would  need to have this password used in your code later.

3. Configure the tor configuration as follows. Go to the folder where tor is installed and look for file torrc, else create one.
```
cd /usr/local/etc/tor
sudo vi torrc
```
Once file created, i entered the following.
```
ControlPort 9051

#Set your hashed password.
HashedControlPassword 16:88375728F68ECB6360C5729B89A8F125CB42E36149CCF3CAA4B4BABC64

```
Note that ControlPort used is 9051. You will need to use this in your tor programming when you initialize the controller.
However, when tor runs, it also listens on socket port 9050.

4. Once you are done with this. Go to the folder where you have tor installed and run the following command.

```
tor
```
You should see it load the above config file without any issue. Later you should see bootstrap loading and completing 100% in the logs.it will give you a message as follows:
```
Jan 31 23:21:04.000 [notice] Tor has successfully opened a circuit. Looks like client functionality is working.
Jan 31 23:21:04.000 [notice] Bootstrapped 100%: Done
```

5. Go to the privoxy sbin folder and configure privoxy to run with a configuration locally. For this, setup the proxy setting in local system as http://127.0.0.1 with port 8118. Privoxy helps you to connect to web through proxy as well as provide gateway for tor and others to reach back.

In the sbin folder of privoxy, edit config for the following section to uncomment forward-socks5t and forward 192.* section as given below.
```
#      To chain Privoxy and Tor, both running on the same system, you
#      would use something like:
#
       forward-socks5t   /               127.0.0.1:9050 .
#       forward-socks5    /               127.0.0.1:9050 .
#
#      Note that if you got Tor through one of the bundles, you may
#      have to change the port from 9050 to 9150 (or even another
#      one). For details, please check the documentation on the Tor
#      website.
#
#      The public Tor network can't be used to reach your local
#      network, if you need to access local servers you therefore
#      might want to make some exceptions:
#
        forward         192.168.*.*/     .
        forward            10.*.*.*/     .
        forward           127.*.*.*/     .
#

```
Run the proivoxy as follows.
```
sudo /usr/local/Cellar/privoxy/3.0.26/sbin/privoxy 
```

Once done, check for http://localhost:8118. You should see privoxy running.

Once the above is set, you can just run the python file and should see the output in terms of IP you are recognized with from external world and also the output of sites like amazon etc who otherwise would have given you a OOPS! error or not reachable error.
