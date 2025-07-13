import pytest 
import time
import os
from timelogger import Timer, output_result, get_timer_manager

def nestedfunc_for_test():
    timer = Timer("nestedfunc1")
    time.sleep(0.1)
    timer.stop()

def nestedfunc_for_test2():
    timer = Timer("nestedfunc2")
    time.sleep(0.1)
    timer.stop()

def func_for_test():
    timer = Timer("func1")
    for _ in range(10):
        nestedfunc_for_test()
        nestedfunc_for_test2()
    timer.stop()

def func_for_test2():
    timer = Timer("func2")
    time.sleep(0.1)
    timer.stop()

def test_timer():
    func_for_test()
    func_for_test2()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    result_path = os.path.join(script_dir, "test.txt")
    output_result(result_path)
    
    # Check result
    root_server = get_timer_manager().root_time_server
    server = root_server.children.get("func1")
    assert(server is not None)
    assert(server.elapsed_time > 1.9 and server.elapsed_time < 2.1)

    server = server.children.get("nestedfunc1")
    assert(server is not None)
    assert(server.elapsed_time > 0.9 and server.elapsed_time < 1.1)
