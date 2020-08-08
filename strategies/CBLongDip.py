from easyquant import StrategyTemplate, DefaultLogHandler


class Strategy(StrategyTemplate):
    name = 'CBLongDip'
    """
    对有较高YTD保护的转债，急跌抄底
    """

    def log_handler(self):
        return DefaultLogHandler(self.name, log_type='file', filepath='%s.log' % self.name)

    def strategy(self, event):
        print('\n\n可转债动量策略触发')
        self.log.info('\n\n可转债动量策略触发')
        self.log.info('行情数据: 精测转债 %s' % event.data['600519'])
        # self.log.info('检查持仓')
        # self.log.info(self.user.balance)
        # self.log.info('买转债')
        # self.log.info(self.user.buy('159949', price=event.data['']['close'], amount=100))
        self.log.info('\n')
