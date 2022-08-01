from adminQueries import *
from queries import *
import logging
import time
from scenario_component import *
from scenarios_executable import *

url = "http://120.53.105.200:30467"   # 请求目的地址（腾讯云）


def main():

    q = Query(url)  # 新建Query类对象，传入url即所有请求的目的地址，Query类中均定义的是原子性请求

    if not q.login("admin","222222"):
        return

    try:
        print("发送请求")
        # routine0()
        # rebook_twice_and_cancel()
        # consign_and_preserve()
        preserve_unsuccessfully()
    except Exception:
        logger.exception('actions got an exception')

    # time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    main()