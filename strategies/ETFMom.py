from easyquant import StrategyTemplate, DefaultLogHandler


class Strategy(StrategyTemplate):
    name = 'ETFMom'
    """
    ETF相比昨收盘跌则卖出1千元，涨则买入1千元
    """
    def __init__(self, user, log_handler, main_engine):
        super().__init__(user, log_handler, main_engine)
        self.toBuy = ['159949', '159928', '512000']
        self.toSell = ['159949', '159928', '512000']
        self.rtn2close = 0.008

    def log_handler(self):
        return DefaultLogHandler(self.name, log_type='file', filepath='%s.log' % self.name)

    def strategy(self, event):
        self.log.info('\n\nETFMom策略触发')
        for symbol in self.toBuy:
            if event.data[symbol]['now'] / event.data[symbol]['close'] >= 1 + self.rtn2close:
                self.log.info('买%s' % symbol)
                self.log.info(self.user.buy(symbol, price=event.data[symbol]['ask2'], amount=round(2000/event.data[symbol]['ask2'], -2)))
                self.toBuy.remove(symbol)
                self.log.info(len(self.toBuy))
        if len(self.toSell) > 0:
            for holding in self.toSell:
                if event.data[holding]['now'] / event.data[holding]['close'] <= 1 - self.rtn2close:
                    self.log.info('卖%s' % holding)
                    self.log.info(self.user.sell(holding, price=event.data[holding]['bid2'], amount=round(2000/event.data[holding]['bid2'], -2)))
                    self.toSell.remove(holding)
                    self.log.info(len(self.toSell))
        self.log.info('\n')
