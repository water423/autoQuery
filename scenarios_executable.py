from scenario_component import *


# 正常preserve流程
# login -> 查询余票成功 -> 正常预定&refresh
def preserve_successfully():
    query_types = ["normal", "high_speed", "min_station", "cheapest", "quickest"]
    query_type = random_from_list(query_types)
    print(query_type)
    trip_info = query_left_tickets_successfully("normal", ("Shang Hai","Nan Jing"))
    preserve_and_refresh(trip_info)


# 异常preserve流程(no route)
# login -> 查询余票(no route) -> admin添加相关信息 -> 查询余票成功 -> 正常预定&refresh -> 删除相关数据
def preserve_unsuccessfully():
    print("xxx")