from scenario_component import *
from constant import *


# 正常preserve流程
# login -> 查询余票成功 -> 正常预定&refresh
def preserve_successfully():
    # 如何保证对应的查询方式均可以找到余票而不会存在no route的情形，需要将查询方式与起点、终点绑定
    # 选择查询的(起点，终点)对，使用init中的数据
    place_pairs = []
    for route_data in InitData.init_route_data:  # init_route_data内部的每个route都会与train绑定从而形成travel
        place_pair = (route_data[2], route_data[3])
        place_pairs.append(place_pair)
    query_place_pair = random_from_list(place_pairs)
    print(query_place_pair)
    # 选择查询的方式
    query_types = ["normal", "high_speed", "min_station", "cheapest", "quickest"]
    query_type = random_from_list(query_types)
    print(query_type)
    trip_info = query_left_tickets_successfully(query_type, query_place_pair)
    preserve_and_refresh(trip_info)


# 异常preserve流程(no route)
# login -> 查询余票(no route) -> admin添加相关信息 -> 查询余票成功 -> 正常预定&refresh -> 删除相关数据
def preserve_unsuccessfully():
    # 选择查询的方式
    query_types = ["normal", "high_speed", "min_station", "cheapest", "quickest"]
    query_type = random_from_list(query_types)
    print(query_type)
    query_left_tickets_unsuccessfully(query_type)  # 查询失败
