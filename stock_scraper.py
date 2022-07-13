import requests
from bs4 import BeautifulSoup

ticker = input("Type in a ticker symbol: ")

yahoo_html = requests.get('https://finance.yahoo.com/quote/'+ticker.upper()).text
while 'Not Found on Server' in yahoo_html:
    ticker = input("Try again! Type in a valid ticker symbol: ")
    yahoo_html = requests.get('https://finance.yahoo.com/quote/'+ticker.upper()).text
yahoo_soup = BeautifulSoup(yahoo_html, 'lxml')
#yahoo_soup now contains a soup made up of a valid stock information page

robinhood_html = requests.get('https://robinhood.com/stocks/'+ticker.upper()).text
robinhood_soup = BeautifulSoup(robinhood_html, 'lxml')
#robinhood_soup now also contains a soup of a valid stock info page

company_name = yahoo_soup.find('h1', class_ = 'D(ib) Fz(18px)').text
#company_name contains the name of the stock, and its ticker symbol as a string

rh_desc_box = robinhood_soup.find('section', id = 'etf-about-header')
rh_desc = rh_desc_box.find('span', class_='css-ws71f5').text
if 'View more' in rh_desc:
    rh_desc = rh_desc[:-10]
#rh_desc contains a brief description of the company and its operations

price = yahoo_soup.find('fin-streamer', class_ = 'Fw(b) Fz(36px) Mb(-4px) D(ib)').text
#price contains the current stock price

gain_loss = yahoo_soup.find_all('fin-streamer', class_ = 'Fw(500) Pstart(8px) Fz(24px)')
#gain_loss contains the day's gain/loss in dollars at gain_loss[0],
# and in percent at gain_loss[1]

yahoo_metrics = yahoo_soup.find_all('td', class_ = 'Ta(end) Fw(600) Lh(14px)')
#yahoo_metrics contains a lot of info:
#    yahoo_metrics[0]: previous close
#    yahoo_metrics[1]: open
#    yahoo_metrics[2]: bid
#    yahoo_metrics[3]: ask
#    yahoo_metrics[4]: day's range
#    yahoo_metrics[5]: 52 week range
#    yahoo_metrics[6]: volume
#    yahoo_metrics[7]: avg. volume
#    yahoo_metrics[8]: market cap
#    yahoo_metrics[9]: beta
#    yahoo_metrics[10]: p/e ratio
#    yahoo_metrics[11]: eps
#    yahoo_metrics[12]: upcoming earnings date
#    yahoo_metrics[13]: forward dividend & yield
#    yahoo_metrics[14]: ex-dividend date
#    yahoo_metrics[15]: 1y target est

related_news = yahoo_soup.find('li', class_ = 'js-stream-content Pos(r)')
top_article = related_news.find('a').text
#top+article contains the #1 related article on yahoo finance

#tweak the following to choose what prints to the user or output file
print('Stock: '+company_name)
print('Description: '+rh_desc)
print('Current stock price: $'+price)
print('Today\'s change: ' +gain_loss[0].text+ ', '+gain_loss[1].text)
print('Today\'s volume: ' +yahoo_metrics[6].text)
print('Market Cap: ' +yahoo_metrics[8].text)
print('Top headline: \"'+top_article+'\"')
