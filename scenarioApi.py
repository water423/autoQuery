import sys

from scenario_component import admin_operations
import time
import threading

scenarios = {
    "adminOperations": admin_operations(),
}

def run(
        scenario,
        peak_start_time,
        peak_end_time,
        peak_qps,
        valley_start_time,
        valley_end_time,
        valley_qps,
        init_qps,
        runtime: float = 3600000
):
    start = time.time()
    print(f"start time tick:{start}")
    func = scenarios[scenario]
    while time.time() - start < runtime:
        now_time = time.time()
        if now_time>peak_start_time and now_time<peak_end_time:
            time.sleep(1/peak_qps)
            t = threading.Thread(target=func, args=())
            t.start()
            continue
        if now_time>valley_start_time and now_time<valley_end_time:
            time.sleep(1/valley_qps)
            t = threading.Thread(target=func, args=())
            t.start()
            continue
        time.sleep(1/init_qps)
        t = threading.Thread(target=func, args=())
        t.start()

if __name__ == '__main__':
    try:
        scenario,peak_start_time,peak_end_time,peak_qps,valley_start_time,valley_end_time,valley_qps,init_qps = sys.argv[1:9]
        run(scenario,peak_start_time,peak_end_time,peak_qps,valley_start_time,valley_end_time,valley_qps,init_qps)
    except Exception as e:
        print(sys.argv)
        print(e)
        print("args list: scenario, peak_start_time, peak_end_time, peak_qps, valley_start_time, valley_end_time, valley_qps, init_qps")


