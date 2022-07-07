from scenario_component import *
from constant import *


# 正常preserve流程
# login -> 查询余票成功 -> 正常预定&refresh
def preserve_successfully() -> List[dict]:
    # 新建用户并登陆or使用特定用户登陆
    # query = new_user()
    query = Query(Constant.ts_address)
    query.login("b7551865fce611ec868ab0359fb6e508","111111")

    # 如何保证对应的查询方式均可以找到余票而不会存在no route的情形:需要使用init中的数据,将查询方式与起点、终点绑定
    # 选择查询的(起点，终点)对
    place_pairs = []
    for route_data in InitData.init_route_data:  # init_route_data内部的每个route都会与train绑定从而形成travel
        start = route_data[2]
        end = route_data[3]
        # 此处的是station对应的id，需要到init_station_data列表中查找对应的name信息
        for station_data in InitData.init_stations_data:
            if station_data[0] == start:  # route_data[2]是起始站
                start = station_data[1]  # id换成name
            if station_data[0] == end:  # route_data[2]是起始站
                end = station_data[1]  # id换成name
        place_pair = (start, end)
        place_pairs.append(place_pair)
    query_place_pair = random_from_list(place_pairs)
    print(f"[start station & end station] : {query_place_pair} ")
    # 选择查询的方式
    query_types = ["normal", "high_speed", "min_station", "cheapest", "quickest"]
    query_type = random_from_list(query_types)
    print("[query_type] : " + query_type)

    # 查询余票
    trip_info = query_left_tickets_successfully(query, query_type, query_place_pair, "2022-07-06")
    # 订票并刷新订单
    all_orders_info = preserve_and_refresh(query, trip_info, 0)

    # 退出并删除用户（暂时不可用）
    userid_deleted = query.uid
    # admin = AdminQuery(Constant.ts_address)
    # admin.login(Constant.admin_username, Constant.admin_pwd)
    # admin.admin_delete_user(userid_deleted)

    return all_orders_info


# 异常preserve流程(no route)
# login -> 查询余票(no route) -> admin添加相关信息 -> 查询余票成功 -> 正常预定&refresh -> 删除相关数据
def preserve_unsuccessfully():
    # 登陆
    query = Query(Constant.ts_address)
    query.login("b7551865fce611ec868ab0359fb6e508","111111")

    # 选择查询的方式
    query_types = ["normal", "high_speed", "min_station", "cheapest", "quickest"]
    query_type = random_from_list(query_types)
    print(query_type)
    query_left_tickets_unsuccessfully(query, query_type)  # 查询失败
    # admin添加相关路线 -> preserve成功....


# rebook失败后成功(一套完整的流程)
# login -> preserve_successfully -> rebook失败(not paid) -> pay and rebook成功 -> 取票进站台
def routine():
    # 新建用户并登陆or使用特定用户登陆
    # query, user_data = new_user()
    query = Query(Constant.ts_address)
    query.login("b7551865fce611ec868ab0359fb6e508", "111111")

    # 成功预定(query查票 -> preserve -> refresh)，返回所有符合条件的订单（默认为0，1）
    all_orders_info = preserve_successfully()
    # 选择一个订单作为此次处理的对象，输入的order的状态已经是符合条件的了 preserve_and_refresh的参数types来确定
    order_info = random_from_list(all_orders_info)  # 可能是高铁动车也可能是普通列车
    print(order_info)

    # rebook失败
    # rebook(query, order_info)

    # pay and rebook成功
    pay_and_rebook_successfully(query, order_info)

    # 取票进站


# rebook两次后取消
# login -> preserve_successfully -> rebook两次失败 -> cancel
def rebook_twice_and_cancel():
    print()
