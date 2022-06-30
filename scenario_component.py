from adminQueries import AdminQuery
from constant import Constant
from queries import Query
from utils import *
import logging

logger = logging.getLogger("data_init")
highspeed_weights = {True: 60, False: 40}
ts_address = "http://139.196.152.44:32677"

def data_init():
    # 1. 添加新的站点、路线、车次
    # 2. 添加新的用户
    #初始化管理员
    admin_query = AdminQuery(ts_address)
    admin_query.login("admin", "222222")
    # #初始化站点信息
    # for station_data in Constant.init_stations_data:
    #     admin_query.stations_post(
    #         station_data[0],
    #         station_data[1],
    #         station_data[2]
    #     )
    # #初始化路线信息
    # for route_data in Constant.init_route_data:
    #     route_id = admin_query.admin_add_route(
    #         route_data[0],
    #         route_data[1],
    #         route_data[2],
    #         route_data[3]
    #     )["id"]
    #     # 增加车次
    #     for i in range(len(Constant.train_types)):
    #         admin_query.admin_add_travel(
    #             Constant.init_train_types_id[i],
    #             Constant.train_types[i],
    #             route_id,
    #             Constant.travel_start_time
    #         )

    # 初始化用户
    # user_id = admin_query.admin_add_user(
    #     Constant.init_user["document_type"],
    #     Constant.init_user["document_num"],
    #     Constant.init_user["email"],
    #     Constant.init_user["password"],
    #     Constant.init_user["username"],
    #     Constant.init_user["gender"]
    # )
    # 初始化用户联系人
    for contact in Constant.init_user_contacts:
        admin_query.contacts_post(
            "67df7d6b-773c-44c9-8442-e8823a792095",
            contact["contact_name"],
            contact["document_type"],
            contact["document_number"],
            contact["phone_number"]
        )




if __name__ == '__main__':
    data_init()




