import time
from enum import Enum

import logging
logger = logging.getLogger(__name__)

class TimeServer():
    """ 一つの関数の記録 """
    def __init__(self, name, parent_server):
        self.name = name
        self.elapsed_time = 0
        self.callednum = 0
        self.parent_server = parent_server
        
        # 自分の直下の関数の結果
        self.children = {}
    
    def add_time(self, elapsed_time):
        self.elapsed_time += elapsed_time
        self.callednum += 1
    
    def get_or_create_child(self, name):
        """ 子にnameが存在すれば取得. 存在しなければ作成して返す. """
        if child := self.children.get(name):
            return child

        self.children[name] = TimeServer(name, self)
        return self.children[name]

class TimerManager():
    """
    全測定結果を集計する
    測定を行うとき, 最初にこのクラスをインスタンス化しておく
    """
    def __init__(self):
        # ルートノード. 子ツリーとしてデータを保持する. 自身は時間データを持たない
        self.root_time_server = TimeServer("root", None)
        # 現在測定中の関数のTimeServer
        self.current_timeserver = self.root_time_server
        self.current_title = ""
        
        self.output_done = False
        self.total_time = 0

    def add_timer(self, name):
        """ 新しい関数に入る """
        self.current_timeserver = self.current_timeserver.get_or_create_child(name)
    
    def stop_timer(self, name, elapsed_time):
        """ 時間保存 """
        if self.current_timeserver.name != name:
            # 念のためのチェック
            logger.error(f"Error: timer is not match! current:{self.current_timeserver.name}" \
                         f", specified:{name}")
            return False

        self.current_timeserver.add_time(elapsed_time)
        self.current_timeserver = self.current_timeserver.parent_server
        return True

    def output_result(self, logpath):
        self.output_done = True
        
        self.total_time = 0
        for child_server in self.root_time_server.children.values():
            self.total_time += child_server.elapsed_time
        
        if self.total_time == 0:
            logger.info("Total time is zero")
            return
        
        with open(logpath, mode="w") as writer:
            for child_server in self.root_time_server.children.values():
                self._output_each_result(writer, child_server, 0)
        
    def _output_each_result(self, writer, server, level):
        indent = "    "*level 
        percentage = server.elapsed_time/self.total_time * 100
        log = f"{indent}{server.name}: {server.elapsed_time:.6f} ({percentage:.3f}%), {server.callednum}\n"
        
        writer.write(log)
        
        for child_server in server.children.values():
            self._output_each_result(writer, child_server, level+1)

# 時間を記録するグローバルオブジェクト
_timer_manager = TimerManager()

class TimerState(Enum):
    MEASURING = 0
    STOP = 1

class Timer():
    """
    時間計測用クラス
    インスタンス化すると計測開始, stopを呼ぶかデストラクタが呼ばれると計測停止.
    """
    def __init__(self, name):
        self.name = name
        self.start_time = time.time()
        self.state = TimerState.MEASURING
        
        _timer_manager.add_timer(self.name)
        
    def __del__(self):
        if self.state != TimerState.STOP:
            self.stop()
            print(f"TimeMeasure({self.name}) was not stopped")
    
    def stop(self):
        elapsed_time = time.time() - self.start_time
        self.state = TimerState.STOP
        
        _timer_manager.stop_timer(self.name, elapsed_time)

def output_result(path):
    """ 結果出力 """
    _timer_manager.output_result(path)

def get_timer_manager():
    return _timer_manager
