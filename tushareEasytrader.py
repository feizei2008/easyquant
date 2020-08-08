import easytrader
import json
import tushare as ts
from threading import Timer

with open('ht.json') as f:
    r = json.load(f)
    user = easytrader.use('ht_client')
    user.prepare(user=r['user'], password=r['password'], comm_password=r['comm_password'])
    # print(user.balance)

buyList = ['113566', '127003', '128094', '123049', '123032', '113581', '123047', '123017', '128079', '128077',
           '123015', '113514', '123018', '113571', '113509', '128041']
sellList = []

# df = ts.get_realtime_quotes(buyList) #Single stock symbol
# print(df[['code','name','time','price','bid','ask','open','high']])

def CBMom():
    for i in buyList:
        df = ts.get_realtime_quotes(i)
        if (float(df['price']) / float(df['open']) - 1) > 0.026:  # and float(df['price']) == float(df['high']):
            user.buy(i, price=float(df['price']), amount=10 if i.startswith('12') else 1)
            print("buy %s" % df['name'])
            buyList.remove(i)
            sellList.append(i)
    if len(sellList) > 0:
        for j in sellList:
            df1 = ts.get_realtime_quotes(j)
            if (float(df1['price']) / float(df1['high']) - 1) < -0.2:
                user.sell(j, price=float(df1['price']), amount=10 if j.startswith('12') else 1)
                print("sell %s" % df1['name'])
                sellList.remove(j)
    t = Timer(3, CBMom)
    t.start()

if __name__ == "__main__":
    CBMom()
