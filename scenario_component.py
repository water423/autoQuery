from adminQueries import AdminQuery
from constant import Constant, InitData, AdminData
from queries import Query
from utils import *
import time
import logging

logger = logging.getLogger("data_init")
highspeed_weights = {True: 60, False: 40}
datestr = time.strftime("%Y-%m-%d", time.localtime())

# 1.admin相关增删改查：post -> get -> update -> get -> delete
def data_init():
    # 1. 添加新的站点、路线、车次
    # 2. 添加新的用户
    # 初始化管理员
    admin_query = AdminQuery(Constant.ts_address)
    admin_query.login(Constant.admin_username, Constant.admin_pwd)
    # 初始化站点信息
    for station_data in InitData.init_stations_data:
        admin_query.stations_post(
            station_data[0],
            station_data[1],
            station_data[2]
        )
    # 初始化路线信息
    for route_data in InitData.init_route_data:
        route_id = admin_query.admin_add_route(
            route_data[0],
            route_data[1],
            route_data[2],
            route_data[3]
        )["id"]
        # 增加车次
        for i in range(len(InitData.train_types)):
            admin_query.admin_add_travel(
                InitData.init_train_trips_id[i],
                InitData.train_types[i],
                route_id,
                InitData.travel_start_time
            )

    # 初始化用户
    user_id = admin_query.admin_add_user(
        InitData.init_user["document_type"],
        InitData.init_user["document_num"],
        InitData.init_user["email"],
        InitData.init_user["password"],
        InitData.init_user["username"],
        InitData.init_user["gender"]
    )
    # 初始化用户联系人
    for contact in InitData.init_user_contacts:
        admin_query.contacts_post(
            "67df7d6b-773c-44c9-8442-e8823a792095",
            contact["contact_name"],
            contact["document_type"],
            contact["document_number"],
            contact["phone_number"]
        )


def admin_operations():
    # 1. 添加新的站点、路线、车次
    # 2. 添加新的用户
    # 初始化管理员
    admin_query = AdminQuery(Constant.ts_address)
    admin_query.login(Constant.admin_username, Constant.admin_pwd)
    # 初始化站点信息
    for station_data in AdminData.admin_stations_data:
        admin_query.stations_post(
            station_data[0],
            station_data[1],
            station_data[2]
        )
    # 初始化路线信息
    route_id_list = []
    for route_data in AdminData.admin_route_data:
        route_id = admin_query.admin_add_route(
            route_data[0],
            route_data[1],
            route_data[2],
            route_data[3]
        )["id"]
        route_id_list.append(route_id)
        # 增加车次
        for i in range(len(AdminData.train_types)):
            admin_query.admin_add_travel(
                AdminData.admin_train_trips_id[i],
                AdminData.train_types[i],
                route_id,
                AdminData.travel_start_time
            )

    # 初始化用户
    user_id = admin_query.admin_add_user(
        AdminData.admin_data_user["document_type"],
        AdminData.admin_data_user["document_num"],
        AdminData.admin_data_user["email"],
        AdminData.admin_data_user["password"],
        AdminData.admin_data_user["username"],
        AdminData.admin_data_user["gender"]
    )["userId"]
    # 初始化用户联系人 没有联系人id无法删除 因此暂不添加
    # for contact in AdminData.admin_data_user_contacts:
    #     admin_query.contacts_post(
    #         "67df7d6b-773c-44c9-8442-e8823a792095",
    #         contact["contact_name"],
    #         contact["document_type"],
    #         contact["document_number"],
    #         contact["phone_number"]
    #     )

    # 进行Get查询信息
    admin_query.admin_get_all_routes()
    admin_query.configs_get()
    admin_query.trains_get()
    admin_query.stations_get()
    admin_query.contacts_get()
    admin_query.orders_get()
    admin_query.prices_get()
    admin_query.admin_get_all_travels()
    admin_query.admin_get_all_users()

    # 执行更新操作
    for station_data in AdminData.admin_stations_data:
        admin_query.stations_put(
            station_data[0],
            station_data[1],
            station_data[2]
        )
    # 更新路线信息
    for route_id in route_id_list:
        # 更新车次
        for i in range(len(AdminData.train_types)):
            admin_query.admin_update_travel(
                AdminData.admin_train_update_trip_id[i],
                AdminData.train_types[i],
                route_id,
                AdminData.travel_update_start_time
            )

    # 更新用户
    admin_query.admin_update_user(
        AdminData.admin_data_user["document_type"],
        AdminData.admin_data_user["document_num"],
        AdminData.admin_data_user["email"],
        AdminData.admin_data_user["password"],
        AdminData.admin_data_user["username"],
        AdminData.admin_data_user["gender"]
    )
    # 更新用户联系人 暂时无法更新，因为未返回联系人id
    # for contact in AdminData.admin_data_user_contacts:
    #     admin_query.contacts_put(
    #         "",
    #         user_id,
    #         contact["contact_name"],
    #         contact["document_type"],
    #         contact["document_number"],
    #         contact["phone_number"]
    #     )

    # 进行Get查询信息
    admin_query.admin_get_all_routes()
    admin_query.configs_get()
    admin_query.trains_get()
    admin_query.stations_get()
    admin_query.contacts_get()
    admin_query.orders_get()
    admin_query.prices_get()
    admin_query.admin_get_all_travels()
    admin_query.admin_get_all_users()

    # 删除添加的信息
    # 删除站点
    for station_data in AdminData.admin_stations_data:
        admin_query.stations_delete(
            station_data[0],
            station_data[1],
            station_data[2]
        )

    # 删除车次和路线
    for route_id in route_id_list:
        # 增加车次
        for i in range(len(AdminData.train_types)):
            admin_query.admin_delete_travel(
                AdminData.admin_train_trips_id[i]
            )
        admin_query.admin_delete_route(
            route_id
        )

    # 删除用户
    admin_query.admin_delete_user(
        user_id
    )

    # 进行Get查询信息
    admin_query.admin_get_all_routes()
    admin_query.configs_get()
    admin_query.trains_get()
    admin_query.stations_get()
    admin_query.contacts_get()
    admin_query.orders_get()
    admin_query.prices_get()
    admin_query.admin_get_all_travels()
    admin_query.admin_get_all_users()


# 2.用户登陆并成功查询到余票(普通查询):输入起始站and终点站，以及查询类型
# 查询类型： normal , high_speed , cheapest , min_station , quickest
def query_left_tickets_successfully(query_type: str = "normal", place_pair: tuple = ()) -> dict:
    # 用户登陆
    query = Query(Constant.ts_address)
    query.login(Constant.user_username, Constant.user_pwd)
    # 查询余票(确定起始站、终点站以及列车类型)
    # 类型：普通票、高铁票、高级查询（最快、最少站、最便宜）
    all_trip_info = []  # 成功查询的结果
    if query_type == "normal":
        all_trip_info = query.query_normal_ticket(place_pair=place_pair)
    if query_type == "high_speed":
        all_trip_info = query.query_high_speed_ticket(place_pair=place_pair)
    if query_type == "cheapest":
        all_trip_info = query.query_cheapest(place_pair=place_pair)
    if query_type == "min_station":
        all_trip_info = query.query_min_station(place_pair=place_pair)
    if query_type == "quickest":
        all_trip_info = query.query_quickest(place_pair=place_pair)
    # 随机选择一个trip来返回，作为后续preserve的对象（输入）
    trip_info = random_from_list(all_trip_info)
    print(trip_info)
    return trip_info


# 3.用户登陆并查询余票失败（没有station）
# 输入一个不存在的起始站点或终止站点
def query_left_tickets_unsuccessfully(query_type: str = "normal",
                                      place_pair: tuple = ("start_station_fail","end_station_fail")):
    # 用户登陆
    query = Query(Constant.ts_address)
    query.login(Constant.user_username, Constant.user_pwd)
    # 查询余票(确定起始站、终点站以及列车类型)
    # 查票失败：系统中没有输入的起始站、终点站所以找不到对应trip，返回值为空
    trip_info = []  # 失败查询结果应该为null
    if query_type == "normal":
        trip_info = query.query_normal_ticket(place_pair=place_pair)
    if query_type == "high_speed":
        trip_info = query.query_high_speed_ticket(place_pair=place_pair)
    if len(trip_info) == 0:
        logger.warning("query left tickets unsuccessfully : "
                       "no route found because of unknown start station or end station")


# 4.预定成功且刷新订单
# 输入 query对象，因为preserve的前提是登陆成功
def preserve_and_refresh(trip_info: dict, date: str = ""):
    # 用户登陆
    query = Query(Constant.ts_address)
    query.login(Constant.user_username, Constant.user_pwd)
    query.preserve(trip_info=trip_info, date=date)
    query.query_orders()  # refresh


# if __name__ == '__main__':





