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
    # if query_type == "cheapest":
    #     query.query_cheapest(place_pair=place_pair)
    # if query_type == "min_station":
    #     query.query_min_station(place_pair=place_pair)
    # if query_type == "quickest":
    #     query.query_quickest(place_pair=place_pair)
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

# 订票服务（包含：列车及座位等必要信息、支付方式、是否需要食物、是否需要托运行李）
    # query查询到trip信息随机选择一个trip并传入此函数，则通过train_type就可以判断是否是高铁动车票，date与查询日期一致
    def preserve(self, trip_info: dict, date: str = "", headers: dict = {}):
        # start: str, end: str, trip_ids: List = [], is_high_speed: bool = True
        if headers == {}:
            headers = self.session.headers
        if date == "":
            date = datestr

        # {'tripId': {'type': 'D', 'number': '1345'},
        #  'trainTypeId': 'DongCheOne', 'startingStation': 'Shang Hai', 'terminalStation': 'Su Zhou',
        #  'startingTime': 1367622000000, 'endTime': 1367622960000,
        #  'economyClass': 1073741822, 'confortClass': 1073741822,
        #  'priceForEconomyClass': '22.5', 'priceForConfortClass': '50.0'}
        # 解析trip_info得到start end tripId等信息
        start = trip_info.get("startingStation")
        end = trip_info.get("terminalStation")
        trip_id = trip_info.get("tripId")   # {'type': 'D', 'number': '1345'}

        if trip_id.get("type") == 'D' or trip_id.get("type") == 'G':  # 以D或者G开头的是preserve
            preserve_url = f"{self.address}/api/v1/preserveservice/preserve"
        else:                          # 以K或者Z开头的是preserveOther
            preserve_url = f"{self.address}/api/v1/preserveotherservice/preserveOther"

        base_preserve_payload = {
            "accountId": self.uid,
            "assurance": "0",
            "contactsId": "",
            "date": date,
            "from": start,
            "to": end,
            "tripId": trip_id.get("type") + trip_id.get("number") # 合并
        }

        # 选择座位
        seat_type = random_from_list(["2", "3"])
        base_preserve_payload["seatType"] = seat_type

        # 选择联系人：必选项
        # 两种选择方式：新建联系人 or 选择已有联系人
        # 随机选择是否需要新建联系人
        new_contact = random_boolean()
        if new_contact:
            # 新建一个联系人，在前端逻辑中新建联系人 -> 获取所有联系人 -> 根据ui选择联系人
            # 为了可复用性，如果新增联系人则后续需要删掉（或者保证每次的新增均不相同）
            logger.info("choose new contact")
            contacts_id = self.add_contact()  # 新增联系人并返回contactId
            base_preserve_payload["contactsId"] = contacts_id
        else:
            logger.info("choose contact already existed")
            contacts_result = self.query_contacts()
            contacts_id = random_from_list(contacts_result)
            base_preserve_payload["contactsId"] = contacts_id

        # 随机选择是否需要食物
        need_food = random_boolean()
        if need_food:
            logger.info("need food")
            # 查询食物的参数为 place_pair train_num即tripID
            food_result = self.query_food(place_pair=(start, end), train_num =trip_id)
            food_dict = random_from_list(food_result)
            base_preserve_payload.update(food_dict)
        else:
            logger.info("not need food")
            base_preserve_payload["foodType"] = "0"

        # 随机选择是否需要保险
        need_assurance = random_boolean()
        if need_assurance:  # 如果需要保险则查询保险并使得assurance参数为1，否则默认为0
            assurance_result = self.query_food()  # 系统内置只有一种assurance
            # assurance_dict = random_from_list(assurance_result)
            base_preserve_payload["assurance"] = 1

        # 随机选择此时需不需要托运
        need_consign = random_boolean()
        if need_consign:
            consign = {
                "consigneeName": random_str(),
                "consigneePhone": random_phone(),
                "consigneeWeight": random.randint(1, 10),
                "handleDate": date
            }
            base_preserve_payload.update(consign)

        logger.info(
            f"[preserve choices] tripId:{trip_id}  "
            f"new_contact:{new_contact} need_food:{need_food}  "
            f"need_consign: {need_consign}  need_assurance:{need_assurance}")

        res = self.session.post(url=preserve_url,
                                headers=headers,
                                json=base_preserve_payload)

        if res.status_code == 200 and res.json()["data"] == "Success":
            logger.info(f"preserve trip {trip_id} success")
        else:
            logger.error(
                f"preserve failed, code: {res.status_code}, {res.text}")

        # 最后删除新建的联系人，保证可复用性
        if new_contact:
            self.login("admin", "222222")
            self.contacts_delete(contact_id=contacts_id)

        return


# 4.预定成功且刷新订单
# 输入 query对象，因为preserve的前提是登陆成功
def preserve_and_refresh(trip_info: dict, date: str = ""):
    # 用户登陆
    query = Query(Constant.ts_address)
    query.login(Constant.user_username, Constant.user_pwd)
    query.preserve(trip_info=trip_info, date=date)
    query.query_orders()  # refresh


# if __name__ == '__main__':





