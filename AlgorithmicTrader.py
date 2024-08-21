from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from MySQLConnection import Connection
import datetime
import yfinance as yf
import random

menu_text = """
    Stock Trading Recommender:
    -------------
    1) Stocks to Buy
    2) Stocks to Sell
    3) View Owned Stocks
    Enter an option:
    """

def ShowBuy():
    buy_text = """Underperforming stocks\n"""
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('stocktracker')

    cql = """SELECT (tickerName, closePrice, recommendationKey, fiftyDayAverage, trackTime)
             FROM tracker
             WHERE recommendationkey = 'buy' ALLOW FILTERING;
        """
    rows = session.execute(cql)

    buy_rows = []
    for row in rows:
        if row[0][1] < row[0][3]:
            buy_rows.append(row)

    randomIndices = [random.randint(0, len(buy_rows)) for val in range(5)]

    for i in randomIndices:
        buy_text += f"{i+1}) {buy_rows[i][0][0]} | Price: {buy_rows[i][0][1]}  | Fifty Day Average: {buy_rows[i][0][3]}\n"
    print(buy_text)
    usr_input = input("Type a stock symbol to purchase: ")
    Buy(usr_input)


def ShowSell():
    ShowOwnedStocks()
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('stocktracker')


    text = """\n\nStocks you own: \nName | Price Purchased | Time Purchased\n---------------\n"""
    c = Connection()
    conn, cur = c.ConnectToMySQL('Portfolio'), c.MakeCursor()

    sql = """SELECT * FROM ClientPortfolio"""
    cur.execute(sql)
    rows = cur.fetchall()
    
    ownedStocks = []
    for i in range(len(rows)):
        ownedStocks.append(rows[i]['tickerName'])

    keys = [yf.Ticker(val).info['recommendationKey'] for val in ownedStocks]
    

    for val, key in zip(rows, keys):
        text += f"{val['tickerName']}   | {val['price']}  | {val['buyTime']} | {key}\n"
    print(text)

    usr_input = input("Type a stock symbol to sell: ")
    Sell(usr_input)
    
def ShowOwnedStocks():
    text = """\n\nStocks you own: \nName | Price Purchased | Time Purchased | Recommendation\n---------------\n"""
    c = Connection()
    conn, cur = c.ConnectToMySQL('Portfolio'), c.MakeCursor()

    sql = """SELECT * FROM ClientPortfolio"""
    cur.execute(sql)
    rows = cur.fetchall()

    ownedStocks = []
    for i in range(len(rows)):
        ownedStocks.append(rows[i]['tickerName'])

    keys = [yf.Ticker(val).info['recommendationKey'] for val in ownedStocks]
    
    for val, key in zip(rows, keys):
        text += f"{val['tickerName']}   | {val['price']}  | {val['buyTime']} | {key}\n"
    print(text)

def Buy(sym):
    s = yf.Ticker(sym)
    hist = s.history('1d').iloc[0]
    
    c = Connection()
    conn, cur = c.ConnectToMySQL('Portfolio'), c.MakeCursor()

    sql = """INSERT INTO ClientPortfolio (tickerName, price, buyTime) VALUES (%s, %s, %s); """
    cur.execute(sql, (sym, hist['Close'], datetime.datetime.now()))

    conn.commit()
    cur.close()
    
    return 0

def Sell(sym):
    s = yf.Ticker(sym).history('1d').iloc[-1]['Close']
    print(s)
    c = Connection()
    conn, cur = c.ConnectToMySQL('Portfolio'), c.MakeCursor()

    sql = """SELECT SUM(price) AS total FROM ClientPortfolio AS c WHERE c.tickerName = %s;"""
    cur.execute(sql, (sym,))
    total = cur.fetchone()['total']
    print(total)
    sql = """DELETE FROM ClientPortfolio AS c WHERE c.tickerName = %s"""
    cur.execute(sql, (sym,))

    conn.commit()
    cur.close()
    print(f"Sold {sym} for ${round(s - total, 2)}")
    return 0


def main():
    flag = True
    while flag:
        print(menu_text)
        usr_input = input("Select An Option: ")
        if usr_input == "1":
            ShowBuy()
        elif usr_input == "2":
            ShowSell()
        elif usr_input == "3":
            ShowOwnedStocks()
        elif usr_input == "4":
            flag = False



main()

    

