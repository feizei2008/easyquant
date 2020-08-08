import easyquotation
import easyquant
from easyquant import DefaultQuotationEngine, DefaultLogHandler, PushBaseEngine
from dateutil.parser import parse
import multiprocessing
from time import sleep
from datetime import datetime, time
from logging import INFO

# amStart = "09:30:00"
# amEnd = "11:30:00"
# pmStart = "13:00:00"
# pmEnd = "15:00:00"
# if (parse(amStart).time() < datetime.now().time() < parse(amEnd).time()
#         or parse(pmStart).time() < datetime.now().time() < parse(pmEnd).time()):

# CBMomSub = ['123025', '113555', '113577', '128077', '113013', '123029', '128052', '123013', '123031',
#             '128086', '127004', '128053', '128030', '113520', '123022', '128091', '128054', '123037',
#             '128088', '123034', '128036', '113548', '113571', '113521', '128078', '113514', '113579',
#             '127015']
CBMomSub = ['113556', '123018', '128051', '123050', '110062', '128088', '128067', '128079', '128073']
ETFMomSub = ['159949', '159928', '512000', '600519']


def run_child():
    """
    Running in the child process.
    """

    subSymbols = CBMomSub + ETFMomSub

    class myEngine(PushBaseEngine):
        EventType = 'sina'

        def init(self):
            self.source = easyquotation.use('sina')

        def fetch_quotation(self):
            return self.source.stocks(subSymbols)

    broker = 'ht'
    need_data = 'ht.json'
    quotation_engine = myEngine  # DefaultQuotationEngine
    quotation_engine.PushInterval = int(3)  # 每秒推送一次行情
    log_type = 'file'  # 'stdout'
    log_filepath = 'htMulti.log'
    log_handler = DefaultLogHandler(name='华泰多策略', log_type=log_type, filepath=log_filepath)

    m = easyquant.MainEngine(
        broker,
        need_data,
        quotation_engines=[quotation_engine],
        log_handler=log_handler
    )
    m.load_strategy(names=['CBMom', 'ETFMom'])
    m.start()

    while True:
        sleep(1)


def run_parent():
    """
    Running in the parent process.
    """
    print("启动股票策略守护父进程")

    # Chinese futures market trading period (day/night)
    DAY_START = time(9, 30)
    DAY_END = time(11, 30)

    NIGHT_START = time(13, 00)
    NIGHT_END = time(18, 00)

    child_process = None

    while True:
        current_time = datetime.now().time()
        trading = False

        # Check whether in trading period
        if (
                (DAY_START <= current_time <= DAY_END)
                or (NIGHT_START <= current_time <= NIGHT_END)
        ):
            trading = True

        # Start child process in trading period
        if trading and child_process is None:
            print("启动子进程")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("子进程启动成功")

        # 非记录时间则退出子进程
        if not trading and child_process is not None:
            print("关闭子进程")
            child_process.terminate()
            child_process.join()
            child_process = None
            print("子进程关闭成功")

        sleep(5)


if __name__ == "__main__":
    run_parent()
