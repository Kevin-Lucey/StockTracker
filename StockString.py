from MySQLConnection import Connection
import yfinance as yf
from time import sleep, perf_counter, sleep
from threading import Thread

def MakeStockList():
    c = Connection()
    conn = c.ConnectToMySQL('StockTracker')
    cursor = c.MakeCursor()

    sql = "SELECT tickerName FROM TickerSymbol;"
    cursor.execute(sql)
    stocks = cursor.fetchall()

    targlist = []

    for val in stocks:
        targlist.append(val['tickerName'])

    return targlist 

string = MakeStockList()


