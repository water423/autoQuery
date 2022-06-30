from queries import Query
from utils import *
import logging

logger = logging.getLogger("autoquery-scenario")
highspeed_weights = {True: 60, False: 40}


def data_init():
    # 1. 添加新的站点、路线、车次
    # 2. 添加新的用户
    #
    c = 1


