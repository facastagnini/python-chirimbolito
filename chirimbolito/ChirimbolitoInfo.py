#!/usr/bin/env python3

import urllib2
import json
import time
from datetime import date, timedelta
from ballpark import business

class ChirimbolitoInfo(object):

  screen = []
  walletBalance = []
  dollars = ['USD', 'AUD', 'CAD'] #currencies with displayable symbols
  lastCheck = 0   # initialize the last check time in the past to force the first price refresh
  priceYesterday = '-' # yesterday's price
  yesterday = '-' # Yesterday's date
  priceLast = '-' # last price

  def __init__(self,configuration):
    self.configuration = configuration
    self.create_screens()
    self.refresh()

  def create_screens(self):
    '''Create a screen for each bitcoin address to monitor'''
    self.screen.append(['no data','no data']) # show the price of 1 BTC
    for x in range(len(self.configuration["addresses"])):
      # create the screen variable
      self.screen.append(['screen %s' % (x + 1),'no data'])
      # create the variable to store the wallet balance
      self.walletBalance.append(0)

  def reportError(self, s):
    for x in len(self.screen):
      self.screen[x] = [s, s]

  def parse_summary(self):
    s1 = '1BTC = %s %s' % (business(self.priceLast), self.configuration["currency"])
    s2 = 'Monit: %s wallets' % (len(self.configuration["addresses"]))
    return [s1, s2]

  def checkPriceYesterday(self):
    '''
    Get the price of 1 BTC from yesterday's close.
    Source: CoinDesk Bitcoin Price Index

    "End-of-day high, low, and closing XBP is based on Coordinated Universal Time (UTC).
    As trades occur continuously, a day opens at 00:00:00 and closes at the end of 23:59:59, ie 00:00:00 of the next day."
    '''

    # we should pull yesterday's price only once a day
    today = date.today()
    if (today - timedelta(1)) != self.yesterday:
      # fetch the json data from coindesk
      try:
        url = 'https://api.coindesk.com/v1/bpi/historical/close.json?for=yesterday&currency=***'.replace('***', self.configuration["currency"])
        req = urllib2.Request(url, None, headers={ 'User-Agent': 'Mozilla/5.0' })
        f = urllib2.urlopen(req)
      except Exception as e:
        self.reportError(e)
        return None

      # get yesterday's close price from the response
      if f:
        pricesData = f.read()
        f.close()
        try:
          prices_json = json.loads(pricesData)
          self.yesterday = today - timedelta(1)
          self.priceYesterday = prices_json['bpi'][self.yesterday.strftime('%Y-%m-%d')]
        except ValueError:
          self.reportError(e)
          return None

  def checkPrice(self):
    '''Get the current price of 1 BTC'''
    # fetch the json data from coindesk
    try:
      url = 'https://api.coindesk.com/v1/bpi/currentprice/***.json'.replace('***', self.configuration["currency"])
      req = urllib2.Request(url, None, headers={ 'User-Agent': 'Mozilla/5.0' })
      f = urllib2.urlopen(req)
    except Exception as e:
      self.reportError(e)
      return None

    # get current price from the response
    if f:
      pricesData = f.read()
      f.close()
      try:
        prices_json = json.loads(pricesData)
      except ValueError:
        return None
      self.priceLast = prices_json['bpi'][self.configuration["currency"]]['rate_float']

  def checkWalletsBalance(self):
    '''Query the balance of the wallets'''
    for x in range(len(self.configuration["addresses"])):
      # query the internet
      try:
        url = 'https://blockchain.info/rawaddr/***'.replace('***', self.configuration["addresses"][x]['address'])
        req = urllib2.Request(url, None, headers={ 'User-Agent': 'Mozilla/5.0' })
        f = urllib2.urlopen(req)
      except Exception as e:
        self.reportError(e)
        return None

      # get wallet balance from the response
      if f:
        pricesData = f.read()
        f.close()
        try:
          prices_json = json.loads(pricesData)
        except ValueError:
          return None

        # btc ballance in wallets is expressed in satoshis, this converts it to BTC
        self.walletBalance[x] = prices_json['final_balance'] / 100000000.0

  def refresh(self):
    '''Refresh data and screens'''

    # fisrt refresh data if necessary
    now = time.time()
    since = now - self.lastCheck
    if since >= self.configuration["refresh_delay"] or since < 0.0:
      self.checkPrice()
      self.checkPriceYesterday()
      self.checkWalletsBalance()
      self.lastCheck = time.time()

      # Second refresh the screens
      self.screen[0] = self.parse_summary()
      for x in range(len(self.configuration["addresses"])):
        s1 = self.configuration['addresses'][x]['description']
        s2 = '%s BTC = %s %s' % (business(self.walletBalance[x]), business(self.walletBalance[x] * self.priceLast), self.configuration["currency"])
        self.screen[ x + 1 ] = [s1, s2]
