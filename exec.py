from adminQueries import *
from queries import *
import logging
import time
from scenario_component import *
from scenarios_executable import *

url = 'http://139.196.152.44:32677'   # 请求目的地址（腾讯云）


def main():

    q = Query(url)  # 新建Query类对象，传入url即所有请求的目的地址，Query类中均定义的是原子性请求

    if not q.login():
        return

    try:
        print("发送请求")
        start = "Su Zhou"
        end = "Shang Hai"
        high_speed_place_pair = (start, end)
        preserve_successfully()
    except Exception:
        logger.exception('actions got an exception')

    # time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    main()