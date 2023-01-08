tickerDict = []

with open('ticker.txt','r',encoding='UTF-8') as inf:
    tickerDict = eval(inf.read())
def changeKor(ticker):
    if ticker in tickerDict:
        return tickerDict[ticker]
    else:
        return 'NONE'
