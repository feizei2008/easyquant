from easyquant import StrategyTemplate, DefaultLogHandler


class Strategy(StrategyTemplate):
    name = '测试策略2'

    def log_handler(self):
        return DefaultLogHandler(self.name, log_type='file', filepath='%s.log' % self.name)

    def strategy(self, event):
        print('\n\n策略2触发')
        self.log.info('\n\n策略2触发')
        self.log.info('行情数据: 茅台 %s' % event.data['600519'])
        # self.log.info('检查持仓')
        # self.log.info(self.user.balance)
        # self.log.info('买转债ETF')
        self.log.info(self.user.buy('600519', price=event.data['600519']['close'], amount=100))
        # self.log.info(self.user.buy('511380', price=event.data['511380']['close'], amount=100))
        self.log.info('\n')

