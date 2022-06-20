from .queries import Query
from .utils import *
import logging

logger = logging.getLogger("autoquery-scenario")
highspeed_weights = {True: 60, False: 40}


# 查询订单并且取消
# （情形：在完成预定后，进行订单查询，点击其后的cancel按钮，对订单进行取消）（对于未支付和已支付未取票的订单可以进行取消）
def query_and_cancel(q: Query):
    # 决定查询的是高铁动车票还是普通票（utils中的方法，返回key）
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders(types=tuple([0, 1]))  # 查询到的订单的状态需要为0 1（未支付/未取票）
    else:
        pairs = q.query_orders(types=tuple([0, 1]), query_other=True)

    if not pairs:  # 若没有相关订单则直接返回
        return

    # (orderId, tripId)
    pair = random_from_list(pairs)  # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.cancel_order(order_id=pair[0])  # 调用cancel方法来取消订单
    if not order_id:  # 取消失败则直接返回
        return

    logger.info(f"{order_id} queried and canceled")


def query_and_cancel_before_pay(q: Query):
    # 决定查询的是高铁动车票还是普通票（utils中的方法，返回key）
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders(types=tuple([0]))  # 查询到的订单的状态需要为0 1（未支付/未取票）
    else:
        pairs = q.query_orders(types=tuple([0]), query_other=True)

    if not pairs:  # 若没有相关订单则直接返回
        return

    # (orderId, tripId)
    pair = random_from_list(pairs)  # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.cancel_order(order_id=pair[0])  # 调用cancel方法来取消订单
    if not order_id:  # 取消失败则直接返回
        return

    logger.info(f"{order_id} queried and canceled")


def query_and_cancel_after_pay(q: Query):
    # 决定查询的是高铁动车票还是普通票（utils中的方法，返回key）
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders(types=tuple([1]))  # 查询到的订单的状态需要为0 1（未支付/未取票）
    else:
        pairs = q.query_orders(types=tuple([1]), query_other=True)

    if not pairs:  # 若没有相关订单则直接返回
        return

    # (orderId, tripId)
    pair = random_from_list(pairs)  # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.cancel_order(order_id=pair[0])  # 调用cancel方法来取消订单
    if not order_id:  # 取消失败则直接返回
        return

    logger.info(f"{order_id} queried and canceled")


# 查询订单并且取票
# （情形：在完成预定后，进行订单查询，点击其后的collect按钮，对订单进行取票）（对于已支付未取票的订单可以进行取票）
def query_and_collect(q: Query):
    # 决定查询的是高铁动车票还是普通票（utils中的方法，返回key）
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders(types=tuple([1]))  # 订单状态为1（已支付未取票）
    else:
        pairs = q.query_orders(types=tuple([1]), query_other=True)

    if not pairs:  # 若没有相关订单则直接返回
        return

    # (orderId, tripId)
    pair = random_from_list(pairs)  # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.collect_order(order_id=pair[0])  # 调用collect方法来取票
    if not order_id:  # 取票失败则直接返回
        return

    logger.info(f"{order_id} queried and collected")


# 查询订单并且进站
# （情形：在完成预定并且取票后，进行enter station组件中订单查询，点击其后的enter按钮，进站）（对于已取票的订单可以进站）
def query_and_execute(q: Query):
    # 决定查询的是高铁动车票还是普通票（utils中的方法，返回key）
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders(types=tuple([2]))   # 订单状态为2（已取票）
    else:
        pairs = q.query_orders(types=tuple([2]), query_other=True)

    if not pairs:   # 若没有相关订单则直接返回
        return

    # (orderId, tripId)
    pair = random_from_list(pairs)   # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.enter_station(order_id=pair[0])  # 调用enter方法来进站
    if not order_id:  # 进站失败则直接返回
        return

    logger.info(f"{order_id} queried and entered station")


# 查询并且预定车票
# 首页的ticket reserve组件中进行车票查询及预定
def query_and_preserve(q: Query):
    start = ""
    end = ""
    trip_ids = []

    high_speed = random_from_weighted(highspeed_weights)  # 决定是预定 高铁动车 / 普通车(other)
    if high_speed:
        start = "Shang Hai"
        end = "Su Zhou"
        high_speed_place_pair = (start, end)
        trip_ids = q.query_high_speed_ticket(place_pair=high_speed_place_pair)  # 调用查询高铁动车的方法
    else:
        start = "Shang Hai"
        end = "Nan Jing"
        other_place_pair = (start, end)
        trip_ids = q.query_normal_ticket(place_pair=other_place_pair)  # 调用查询普通车次的方法

    _ = q.query_assurances()  # 调用查询保险的方法（只有一个返回值）（此处调用只是增加场景内容，对于preserve的结果是没有影响的）

    q.preserve(start, end, trip_ids, high_speed)  # 调用预定方法（其中是否预定食物 是否托运行李 如何支付均在方法内通过随机确定）


# 查询且托运行李
# （情形：在预定车票时选择了行李托运并且填写对应信息，后在order查询界面中点击consign按钮，查询并修改托运信息，后确定）
def query_and_consign(q: Query):
    # 决定查询的是高铁动车票还是普通票（utils中的方法，返回key）
    if random_from_weighted(highspeed_weights):
        list = q.query_orders_all_info()  # 查询高铁动车票
    else:
        list = q.query_orders_all_info(query_other=True)  # 查询普通票

    if not list:  # 如果当前用户没有相关订单则直接return
        return

    # (orderId, tripId)
    res = random_from_list(list)   # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.put_consign(res)   # 调用put consign方法来托运
    if not order_id:  # 托运失败则直接返回
        return

    logger.info(f"{order_id} queried and put consign")


# 查询订单并且支付
# （情形：在完成预定preserve后，生成订单，进入order list组件中订单查询，点击pay按钮对订单进行支付）（对于未支付的订单可以支付）
def query_and_pay(q: Query):
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders(types=tuple([0]))  # 订单状态0 未支付   # types=tuple([0, 1])
    else:
        pairs = q.query_orders(types=tuple([0]), query_other=True)

    if not pairs:
        return

    # (orderId, tripId)
    pair = random_from_list(pairs)  # 从订单列表中随机选择一个订单作为处理对象

    order_id = q.pay_order(pair[0], pair[1])  # 调用pay order方法来支付
    if not order_id:  # 支付失败直接返回
        return

    logger.info(f"{order_id} queried and paid")


# 查询订单并且改签(暂时没用到)
# （情形：完成预定，支付且未取票，则可以改签）
def query_and_rebook(q: Query):
    if random_from_weighted(highspeed_weights):
        pairs = q.query_orders_all_info(types=tuple([1]))  # 订单状态1 支付且未取票   # types=tuple([0, 1])
    else:
        pairs = q.query_orders_all_info(types=tuple([1]), query_other=True)

    if not pairs:
        return

    # result["accountId"] = d.get("accountId")
    # result["targetDate"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # result["orderId"] = d.get("id")
    # result["from"] = d.get("from")
    # result["to"] = d.get("to")
    pair = random_from_list(pairs)  # 从订单列表中随机选择一个订单作为处理对象

    # rebook_ticket(self, old_order_id, old_trip_id, new_trip_id, new_date, new_seat_type, headers: dict = {})
    order_id = q.rebook_ticket(pair[0], pair[1])  # 调用pay order方法来支付
    if not order_id:  # 支付失败直接返回
        return

    logger.info(f"{order_id} queried and paid")