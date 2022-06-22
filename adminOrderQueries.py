import logging
import time
from queries import Query

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())


class AdminOrderQuery(Query):

    # order相关增删改查
    def orders_post(self, bought_date: str = "1655783404439", travel_date: str = "1501257600000",
                    travel_time: str = "1367629320000", account_id: str = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                    contacts_name: str = "Contacts_One", document_type: int = 1,
                    contacts_document_number: str = "DocumentNumber_One", train_number: str = "G1237",
                    coach_number: int = 1, seat_class: int = 2, seat_number: str = "FirstClass-30",
                    order_from: str = "nanjing", order_to: str = "shanghaihongqiao", status: int = 0,
                    price: str = "100.0", headers: dict = {}) -> str:
        """
        添加订单
        # :param id;  (不需要输入，创建时生成)
        :param bought_date;
        :param travel_date;
        :param travel_time;
        :param account_id;   # Which Account Bought it
        :param contacts_name;     # Tickets bought for whom
        :param document_type;
        :param contacts_document_number;
        :param train_number;
        :param coach_number;
        :param seat_class;
        :param seat_number;
        :param order_from;
        :param order_to;
        :param status;
        :param price;
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminorderservice/adminorder"

        if bought_date == "":
            bought_date = datestr

        if travel_date == "":
            travel_date = datestr

        if travel_time == "":
            travel_time = datestr

        # 请求载荷，对应@requestbody注解
        payload = {
            "boughtDate": bought_date,
            "travelDate": travel_date,
            "travelTime": travel_time,
            "accountId": account_id,
            "contactsName": contacts_name,
            "documentType": document_type,
            "contactsDocumentNumber": contacts_document_number,
            "trainNumber": train_number,
            "coachNumber": coach_number,
            "seatClass": seat_class,
            "seatNumber": seat_number,
            "from": order_from,
            "to": order_to,
            "status": status,
            "price": price
        }

        # 发送请求、获取响应
        response = self.session.post(url=url, headers=headers, json=payload)

        # 功能异常
        # {"timestamp":1655891248872,"status":500,"error":"Internal Server Error",
        # "exception":"org.springframework.web.client.HttpClientErrorException",
        # "message":"403 null","path":"/api/v1/adminorderservice/adminorder"}

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")
        print(data)
        return data

    def orders_get(self, headers: dict = {}) -> str:
        """
        获取所有订单信息
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminorderservice/adminorder"

        # 发送请求、获取响应
        response = self.session.get(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def orders_put(self, order_id: str, bought_date: str = "1655783404439", travel_date: str = "1501257600000",
                   travel_time: str = "1367629320000", account_id: str = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                   contacts_name: str = "Contacts_Two", document_type: int = 2,
                   contacts_document_number: str = "DocumentNumber_One", train_number: str = "G1237",
                   coach_number: int = 1, seat_class: int = 2, seat_number: str = "FirstClass-30",
                   order_from: str = "nanjing", order_to: str = "shanghaihongqiao", status: int = 0,
                   price: str = "100.0", headers: dict = {}) -> str:

        # 请求url
        url = f"{self.address}/api/v1/adminorderservice/adminorder"

        # 请求载荷，对应@requestbody注解
        payload = {
            "id": order_id,
            "boughtDate": bought_date,
            "travelDate": travel_date,
            "travelTime": travel_time,
            "accountId": account_id,
            "contactsName": contacts_name,
            "documentType": document_type,
            "contactsDocumentNumber": contacts_document_number,
            "trainNumber": train_number,
            "coachNumber": coach_number,
            "seatClass": seat_class,
            "seatNumber": seat_number,
            "from": order_from,
            "to": order_to,
            "status": status,
            "price": price
        }

        # 发送请求、获取响应
        # 功能不可用
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为修改后的车站信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def orders_delete(self, order_id: str = "", train_number: str = "", headers: dict = {}) -> str:
        """
        删除某一订单信息
        :param order_id: 删除order的id
        :param train_number: 删除order的车型，通过是D/G/K等来判断从order(G/D)还是order_other(K)处理
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminorderservice/adminorder/{order_id}/{train_number}"

        # 发送请求、获取响应
        # 对于此delete请求而言，order_id为主，train_number中的首字母即D K G等需要正确（其后的数字不正确无影响）
        # order_id不存在或order与对应的车型不匹配 则{"status":0,"msg":"Order Not Exist.","data":null}
        # {"status": 0, "msg": "Station not exist", "data": null}
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为删除order的信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data
