from adminQueries import AdminQuery
from constant import Constant, InitData, AdminData
from queries import Query
from utils import *
import time
import logging
import operator
import uuid


logger = logging.getLogger("data_init")
highspeed_weights = {True: 60, False: 40}
datestr = time.strftime("%Y-%m-%d", time.localtime())

# admin相关增删改查：post -> get -> update -> get -> delete
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


# 新增用户并登陆
def new_user() -> Query:
    admin_query = AdminQuery(Constant.ts_address)
    admin_query.login(Constant.admin_username, Constant.admin_pwd)
    # 利用uuid新建一个用户的用户名，密码默认为111111
    new_username = uuid.uuid1().hex  # 转换成str
    res = admin_query.admin_add_user("1", "5599488099312X", "ts@fd1.edu.cn", "111111", new_username, "1")
    print(f"[new user] : userId : {res.get('userId')} , username : {res.get('userName')} , pwd : {res.get('password')}")
    # 登陆
    query = Query(Constant.ts_address)
    query.login(new_username, "111111")
    return query


# 用户登陆并成功查询到余票(普通查询):输入起始站and终点站，日期以及查询类型
# 查询类型： normal , high_speed , cheapest , min_station , quickest
def query_left_tickets_successfully(query: Query,
                                    query_type: str = "normal", place_pair: tuple = (), date: str = "") -> dict:
    # 用户登陆
    # query = Query(Constant.ts_address)
    # query.login(username=username, password=pwd)
    # 查询余票(确定起始站、终点站以及列车类型)
    # 类型：普通票、高铁票、高级查询（最快、最少站、最便宜）
    all_trip_info = []  # 成功查询的结果
    if query_type == "normal":
        all_trip_info = query.query_normal_ticket(place_pair=place_pair, time=date)
    if query_type == "high_speed":
        all_trip_info = query.query_high_speed_ticket(place_pair=place_pair, time=date)
    if query_type == "cheapest":
        all_trip_info = query.query_cheapest(place_pair=place_pair, date=date)
    if query_type == "min_station":
        all_trip_info = query.query_min_station(place_pair=place_pair, date=date)
    if query_type == "quickest":
        all_trip_info = query.query_quickest(place_pair=place_pair, date=date)
    # 随机选择一个trip来返回，作为后续preserve的对象（输入）
    trip_info = random_from_list(all_trip_info)
    print(f"[trip info selected] : {trip_info}")
    return trip_info


# 用户登陆并查询余票失败（没有station）
# 输入一个不存在的起始站点或终止站点(通过控制输入值来保证查不到travel)
def query_left_tickets_unsuccessfully(query: Query,
                                      query_type: str = "normal",
                                      place_pair: tuple = ("start_station_fail", "end_station_fail"),
                                      date: str = ""):
    # 用户登陆
    # query = Query(Constant.ts_address)
    # query.login(username=username, password=pwd)
    # 查询余票(确定起始站、终点站以及列车类型)
    # 查票失败：系统中没有输入的起始站、终点站所以找不到对应trip，返回值为空
    all_trip_info = []
    if query_type == "normal":
        all_trip_info = query.query_normal_ticket(place_pair=place_pair, time=date)
    if query_type == "high_speed":
        all_trip_info = query.query_high_speed_ticket(place_pair=place_pair, time=date)
    if query_type == "cheapest":
        all_trip_info = query.query_cheapest(place_pair=place_pair, date=date)
    if query_type == "min_station":
        all_trip_info = query.query_min_station(place_pair=place_pair, date=date)
    if query_type == "quickest":
        all_trip_info = query.query_quickest(place_pair=place_pair, date=date)
    if all_trip_info is None or len(all_trip_info) == 0:   # 如不存在则返回值为null或[]
        logger.warning("query left tickets unsuccessfully : "
                       "no route found because of unknown start station or end station")
    else:
        logger.warning("error : query left tickets successfully , Unsatisfied query conditions")


# 预定成功且刷新订单
# 输入 query对象，因为preserve的前提是登陆成功
def preserve_and_refresh(query: Query, trip_info: dict, date: str = ""):
    # query = Query(Constant.ts_address)  # 用户登陆
    # query.login(username=username, password=pwd)
    query.preserve(trip_info=trip_info, date=date)  # 订票
    query.query_orders()  # refresh刷新订单


# 查询新加的两个站之间是否有直接的线路
def search_route2staion(query, search_id_pair: list = ["chongqingbei", "guiyangbei"],):
    routes = query.admin_get_all_routes()
    for ele in routes:
        stations = ele["stations"]
        if operator.eq(stations, search_id_pair):
            return ele["id"]
    return ""


# 使用admin添加查询失败的线路站点车次，并重新查询返回trip相关信息
def admin_add_route_search(
        search_id_pair: tuple = ("chongqingbei", "guiyangbei"),
        search_name_pair: tuple = ("Chong Qing Bei", "Gui Yang Bei"),
        miss_station_id: str = "guiyangbei",
        miss_station_name: str = "Gui Yang Bei",
):
    query = AdminQuery(Constant.ts_address)
    # 添加缺失的站点
    query.stations_post(
        miss_station_id,
        miss_station_name,
        5
    )
    origin_route_id = search_route2staion(query, list(search_id_pair))

    # 添加路线,获取route_id
    route_id = query.admin_add_route(
        search_id_pair[0]+","+search_id_pair[1],
        "0,500",
        search_id_pair[0],
        search_id_pair[1]
    )["id"]
    if origin_route_id != "":
        query.admin_delete_route(route_id)
        route_id = origin_route_id
    # 添加车次
    train_type = random.choice(AdminData.train_types)
    travel_data = query.admin_add_travel(
        AdminData.random_train_type_reflection[train_type],
        train_type,
        route_id,
        AdminData.travel_start_time
    )

    trip_info = query_left_tickets_successfully("normal", search_name_pair)
    return trip_info








