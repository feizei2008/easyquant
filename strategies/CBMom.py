from easyquant import StrategyTemplate, DefaultLogHandler


class Strategy(StrategyTemplate):
    name = 'CBMom'
    """
    日内涨幅超过2.6%买，高点回落3%卖
    sh转债11开头，最小买入量1
    sz转债12开头，最小买入量10
    """
    def __init__(self, user, log_handler, main_engine):
        super().__init__(user, log_handler, main_engine)
        self.toBuy = ['113556', '123018', '128051', '123050', '110062', '128088', '128067', '128079', '128073']
        self.toSell = []
        self.rtn2open = 1.026
        self.rtn2high = 0.972

    def log_handler(self):
        return DefaultLogHandler(self.name, log_type='file', filepath='%s.log' % self.name)

    def strategy(self, event):
        self.log.info('\n\nCBMom策略触发')
        for symbol in self.toBuy:
            if event.data[symbol]['now'] / event.data[symbol]['open'] >= self.rtn2open:
                self.log.info('买%s' % symbol)
                self.log.info(self.user.buy(symbol, price=event.data[symbol]['ask2'], amount=10 if symbol.startswith('12') else 1))
                self.toBuy.remove(symbol)
                self.log.info(len(self.toBuy))
                self.toSell.append(symbol)
                self.log.info(len(self.toSell))
        if len(self.toSell) > 0:
            for holding in self.toSell:
                if event.data[holding]['now'] / event.data[holding]['high'] <= self.rtn2high:
                    self.log.info('卖%s' % holding)
                    self.log.info(self.user.sell(holding, price=event.data[holding]['bid2'], amount=10 if holding.startswith('12') else 1))
                    self.toSell.remove(holding)
        self.log.info('\n')
