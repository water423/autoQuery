import requests
import logging
import time
from .utils import *

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())


class Query:
    """
    train-ticket query class
    """

    def __init__(self, ts_address: str) -> None:
        self.address = ts_address
        self.uid = ""
        self.token = ""
        self.session = requests.Session()
        self.session.headers.update({
            'Proxy-Connection': 'keep-alive',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        })

    # 用户/admin登录
    def login(self, username="fdse_microservice", password="111111") -> bool:
        """
        登陆并建立session，返回登陆结果
        """
        url = f"{self.address}/api/v1/users/login"

        headers = {
            'Origin': url,
            'Referer': f"{self.address}/client_login.html",
        }

        data = '{"username":"' + username + '","password":"' + \
            password + '","verificationCode":"1234"}'

        # 获取cookies
        verify_url = self.address + '/api/v1/verifycode/generate'
        r = self.session.get(url=verify_url)
        r = self.session.post(url=url, headers=headers,
                              data=data, verify=False)

        if r.status_code == 200:
            data = r.json().get("data")
            self.uid = data.get("userId")
            self.token = data.get("token")
            self.session.headers.update(
                {"Authorization": f"Bearer {self.token}"}
            )
            logger.info(f"login success, uid: {self.uid}")
            return True
        else:
            logger.error(f"login failed, code: {r.status_code}, {r.text}")
            return False

    def admin_login(self):
        return self.login

    # 请求服务相关方法
    # 查询高铁动车票
    def query_high_speed_ticket(self, place_pair: tuple = (), time: str = "", headers: dict = {}) -> List[str]:
        """
        返回TripId 列表
        :param place_pair: 使用的开始结束组对
        :param headers: 请求头
        :return: TripId 列表
        """

        # 准备请求内容
        url = f"{self.address}/api/v1/travelservice/trips/left"   # 请求url（travelservice）
        place_pairs = [("Shang Hai", "Su Zhou"),    # place_pairs （起始地，目的地）对，设立三个待选
                       ("Su Zhou", "Shang Hai"),
                       ("Nan Jing", "Shang Hai")]

        if place_pair == ():                        # 从待选中随机选择一个作为此次请求的起始地和目的地
            place_pair = random.choice(place_pairs)

        if time == "":
            time = datestr

        payload = {                                 # 请求的载荷（时间、起始地、目的地）
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:   # 响应错误则忽略并打印日志
            logger.warning(
                f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # type: dict                         # 响应正常则获取内容（字典集）

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId").get("type") + \
                d.get("tripId").get("number")
            trip_ids.append(trip_id)
        return trip_ids

    # 查询普通票
    def query_normal_ticket(self, place_pair: tuple = (), time: str = "", headers: dict = {}) -> List[str]:
        # 准备请求内容
        url = f"{self.address}/api/v1/travel2service/trips/left"  # 请求url(travel2service)
        place_pairs = [("Shang Hai", "Nan Jing"),
                       ("Nan Jing", "Shang Hai")]

        if place_pair == ():
            place_pair = random.choice(place_pairs)

        if time == "":
            time = datestr

        payload = {
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        # 发送请求、获取响应并处理
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误
            logger.warning(
                f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # type: dict                        # 响应正确

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId").get("type") + \
                d.get("tripId").get("number")
            trip_ids.append(trip_id)
        return trip_ids

    def query_high_speed_ticket_parallel(self, place_pair: tuple = (), time: str = "", headers: dict = {}) -> List[str]:
        """
        返回TripId 列表
        :param place_pair: 使用的开始结束组对
        :param headers: 请求头
        :return: TripId 列表
        """
        # 准备请求内容
        url = f"{self.address}/api/v1/travelservice/trips/left_parallel"  # 请求url(travelservice left_parallel)
        place_pairs = [("Shang Hai", "Su Zhou"),
                       ("Su Zhou", "Shang Hai"),
                       ("Nan Jing", "Shang Hai")]

        if place_pair == ():
            place_pair = random.choice(place_pairs)

        if time == "":
            time = datestr

        payload = {
            "departureTime": time,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        # 发送请求、获取响应并处理
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误
            logger.warning(
                f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # type: dict                        # 响应正确

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId").get("type") + \
                d.get("tripId").get("number")
            trip_ids.append(trip_id)
        return trip_ids

    # 高级查询（最便宜、最快、最少经过站）
    def query_advanced_ticket(self, place_pair: tuple = (), type: str = "cheapest", date: str = "", headers: dict = {}) -> List[str]:
        """
        高级查询
        :param type [cheapest, quickest, minStation]
        """
        # 准备请求内容
        url = f"{self.address}/api/v1/travelplanservice/travelPlan/{type}"  # 请求url（travelplanservice/travelPlan/{type}）
        place_pairs = [("Shang Hai", "Su Zhou"),
                       ("Su Zhou", "Shang Hai"),
                       ("Nan Jing", "Shang Hai")]

        if place_pair == ():
            place_pair = random.choice(place_pairs)

        if date == "":
            date = datestr

        payload = {
            "departureTime": date,
            "startingPlace": place_pair[0],
            "endPlace": place_pair[1],
        }

        # 发送请求、获取响应并处理
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误
            logger.warning(
                f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")                                      # 响应正确

        trip_ids = []
        for d in data:
            trip_id = d.get("tripId")
            trip_ids.append(trip_id)
        return trip_ids

    # 查询保险服务（只有一种保险服务）
    def query_assurances(self, headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/assuranceservice/assurances/types"  # 请求url（assuranceservice/assurances/types）

        # 发送请求、获取响应并处理
        response = self.session.get(url=url, headers=headers)
        if response.status_code != 200 or response.json().get("data") is None:
            logger.warning(
                f"query assurance failed, response data is {response.text}")
            return None
        _ = response.json().get("data")
        # assurance只有一种

        return [{"assurance": "1"}]

    # 查询食物服务（设定"Shang Hai", "Su Zhou" D1345 2021-07-14）
    def query_food(self, place_pair: tuple = ("Shang Hai", "Su Zhou"), train_num: str = "D1345", headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/foodservice/foods/2021-07-14/{place_pair[0]}/{place_pair[1]}/{train_num}"

        # 发送请求、获取响应并处理
        response = self.session.get(url=url, headers=headers)
        if response.status_code != 200 or response.json().get("data") is None:
            logger.warning(
                f"query food failed, response data is {response.text}")
            return None
        _ = response.json().get("data")

        # food 是什么不会对后续调用链有影响，因此查询后返回一个固定数值
        return [{
            "foodName": "Soup",
            "foodPrice": 3.7,
            "foodType": 2,
            "stationName": "Su Zhou",
            "storeName": "Roman Holiday"
        }]

    # 查询支付方式
    def query_contacts(self, headers: dict = {}) -> List[str]:
        """
        返回座位id列表
        :param headers:
        :return: id list
        """
        # 准备请求内容
        url = f"{self.address}/api/v1/contactservice/contacts/account/{self.uid}"

        # 发送请求、获取响应并处理
        response = self.session.get(url=url, headers=headers)
        if response.status_code != 200 or response.json().get("data") is None:
            logger.warning(
                f"query contacts failed, response data is {response.text}")
            return None

        data = response.json().get("data")
        # print("contacts")
        # pprint(data)

        ids = [d.get("id") for d in data if d.get("id") != None]
        # pprint(ids)
        return ids

    # 获取当前用户的所有订单的id相关信息（false）
    def query_orders(self, types: tuple = tuple([0, 1]), query_other: bool = False, headers: dict = {}) -> List[tuple]:
        """
        返回(orderId, tripId) triple list for inside_pay_service
        :param headers:
        :return:
        """
        # 准备请求内容（queryOther决定）
        url = ""

        if query_other:
            url = f"{self.address}/api/v1/orderOtherService/orderOther/refresh"  # 查询普通票(other)
        else:
            url = f"{self.address}/api/v1/orderservice/order/refresh"            # 查询高铁动车票

        payload = {
            "loginId": self.uid,
        }

        # 发送请求、获取响应并处理
        response = self.session.post(url=url, headers=headers, json=payload)
        if response.status_code != 200 or response.json().get("data") is None:
            logger.warning(
                f"query orders failed, response data is {response.text}")
            return None

        data = response.json().get("data")
        pairs = []
        for d in data:
            # status = 0: not paid
            # status=1 paid not collect
            # status=2 collected
            if d.get("status") in types:
                order_id = d.get("id")
                trip_id = d.get("trainNumber")
                pairs.append((order_id, trip_id))

        logger.info(f"queried {len(pairs)} orders")

        return pairs

    # 获取当前用户的普通票订单（true）
    def query_other_orders(self, types: tuple = tuple([0, 1]), headers: dict = {}) -> List[tuple]:
        return self.query_orders(types, True, headers)

    # 获取当前用户订单的所有信息（query_other决定是高铁票还是普通票） 目的是为了给寄送服务提供输入值
    def query_orders_all_info(self, types: tuple = tuple([0, 1]),query_other: bool = False, headers: dict = {}) -> List[dict]:
        """
        返回(orderId, tripId) triple list for consign service
        :param headers:
        :return:
        """

        if query_other:
            url = f"{self.address}/api/v1/orderOtherService/orderOther/refresh"
        else:
            url = f"{self.address}/api/v1/orderservice/order/refresh"

        payload = {
            "loginId": self.uid,
        }

        response = self.session.post(url=url, headers=headers, json=payload)
        if response.status_code != 200 or response.json().get("data") is None:
            logger.warning(
                f"query orders failed, response data is {response.text}")
            return None

        data = response.json().get("data")
        list = []
        for d in data:
            if d.get("status") in types:
                result = {}
                result["accountId"] = d.get("accountId")
                result["targetDate"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                result["orderId"] = d.get("id")
                result["from"] = d.get("from")
                result["to"] = d.get("to")
                list.append(result)

        logger.info(f"queried {len(list)} orders")

        return list

    # 使用寄送服务（请求固定值，返回新生成的订单ID）
    def put_consign(self, result, headers: dict = {}) -> str:
        # 准备请求内容
        url = f"{self.address}/api/v1/consignservice/consigns"  # 请求url consignservice/consigns
        consignload = {
            "accountId": result["accountId"],
            "handleDate": time.strftime('%Y-%m-%d', time.localtime(time.time())),
            "targetDate": result["targetDate"],
            "from": result["from"],
            "to": result["to"],
            "orderId": result["orderId"],
            "consignee": "32",
            "phone": "12345677654",
            "weight": "32",
            "id": "",
            "isWithin": False
        }

        # 发送请求、获取响应并处理
        res = self.session.put(url=url, headers=headers,
                               json=consignload)
        order_id = result["orderId"]
        if res.status_code == 200 or res.status_code == 201:
            logger.info(f"order {order_id} put consign success")
        else:
            logger.warning(
                f"order {order_id} failed, code: {res.status_code}, text: {res.text}")
            return None

        return order_id

    # 查询route(routeService)（请求固定值）
    def query_route(self, routeId: str = '92708982-77af-4318-be25-57ccb0ff69ad', headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/routeservice/routes/{routeId}"  # 请求url(routeservice/routes/{routeId})

        # 发送请求、获取响应并处理
        res = self.session.get(url=url, headers=headers)

        if res.status_code == 200:
            logger.info(f"query routeId: {routeId} success")
        else:
            logger.warning(
                f"query routeId: {routeId} fail, code: {res.status_code}, text: {res.text}")

        return

    # 支付订单（输入订单id、trip id，返回已支付的订单id）
    def pay_order(self, order_id: str, trip_id: str, headers: dict = {}) -> str:
        # 准备请求内容
        url = f"{self.address}/api/v1/inside_pay_service/inside_payment"  # 请求url(inside_pay_service/inside_payment)
        payload = {
            "orderId": order_id,
            "tripId": trip_id
        }

        # 发送请求、获取响应并处理
        res = self.session.post(url=url, headers=headers, json=payload)

        if res.status_code == 200:
            logger.info(f"order {order_id} pay success")
        else:
            logger.warning(
                f"pay order {order_id} failed, code: {res.status_code}, text: {res.text}")
            return None

        return order_id

    # 取消订单（输入订单id 返回已被取消的订单id）
    def cancel_order(self, order_id, headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/cancelservice/cancel/{order_id}/{self.uid}"
        # 请求url（cancelservice/cancel/{order_id}/{self.uid}）

        # 发送请求、获取响应并处理
        res = self.session.get(url=url, headers=headers)

        if res.status_code == 200:
            logger.info(f"order {order_id} cancel success")
        else:
            logger.warning(
                f"order {order_id} cancel failed, code: {res.status_code}, text: {res.text}")

        return order_id

    # 取票服务（输入订单id）
    def collect_order(self, order_id, headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/executeservice/execute/collected/{order_id}"
        # 请求url(executeservice/execute/collected/{order_id})

        # 发送请求、获取响应并处理
        res = self.session.get(url=url, headers=headers)
        if res.status_code == 200:
            logger.info(f"order {order_id} collect success")
        else:
            logger.warning(
                f"order {order_id} collect failed, code: {res.status_code}, text: {res.text}")

        return order_id

    # 进站（输入订单id）
    def enter_station(self, order_id, headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/executeservice/execute/execute/{order_id}"
        # executeservice/execute/execute/{order_id}

        # 发送请求、获取响应并处理
        res = self.session.get(url=url, headers=headers)
        if res.status_code == 200:
            logger.info(f"order {order_id} enter station success")
        else:
            logger.warning(
                f"order {order_id} enter station failed, code: {res.status_code}, text: {res.text}")

        return order_id

    # 查询票务高级检索（3种）
    def query_cheapest(self, date="", headers: dict = {}):
        self.query_advanced_ticket(type="cheapest", date=date)

    def query_min_station(self, date="", headers: dict = {}):
        self.query_advanced_ticket(type="minStation", date=date)

    def query_quickest(self, date="", headers: dict = {}):
        self.query_advanced_ticket(type="quickest", date=date)

    # admin面板中basic组件中的price查询
    def query_admin_basic_price(self, headers: dict = {}):
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/prices"
        response = self.session.get(url=url, headers=headers)

        if response.status_code == 200:
            logger.info(f"query price success")
            return response
        else:
            logger.warning(f"query price failed")
            return None

    # admin面板中basic组件中的config查询
    def query_admin_basic_config(self, headers: dict = {}):
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/configs"
        response = self.session.get(url=url, headers=headers)
        if response.status_code == 200:
            logger.info(f"config success")
            return response
        else:
            logger.warning(f"config failed")
            return None

    # 改签服务
    def rebook_ticket(self, old_order_id, old_trip_id, new_trip_id, new_date, new_seat_type, headers: dict = {}):
        # 准备请求内容
        url = f"{self.address}/api/v1/rebookservice/rebook"  # 请求url(rebookservice/rebook)

        payload = {
            "oldTripId": old_trip_id,
            "orderId": old_order_id,
            "tripId": new_trip_id,
            "date": new_date,
            "seatType": new_seat_type
        }
        # print(payload)
        r = self.session.post(url=url, json=payload, headers=headers)
        if r.status_code == 200:
            logger.info(r.text)
        else:
            logger.warning(
                f"Request Failed: status code: {r.status_code}, {r.text}")

        return

    # admin面板中travel组件
    def query_admin_travel(self, headers: dict = {}):   # 跑不通
        url = f"{self.address}/api/v1/admintravelservice/admintravel"

        r = self.session.get(url=url, headers=headers)
        if r.status_code == 200 and r.json()["status"] == 1:
            logger.info("success to query admin travel")
        else:
            logger.warning(
                f"faild to query admin travel with status_code: {r.status_code}")
        return

    # 最终的订票服务（包含：列车及座位等必要信息、支付方式、是否需要食物、是否需要托运行李）
    def preserve(self, start: str, end: str, trip_ids: List = [], is_high_speed: bool = True, date: str = "", headers: dict = {}):
        if date == "":
            date = datestr

        if is_high_speed:
            PRESERVE_URL = f"{self.address}/api/v1/preserveservice/preserve"
        else:
            PRESERVE_URL = f"{self.address}/api/v1/preserveotherservice/preserveOther"

        base_preserve_payload = {
            "accountId": self.uid,
            "assurance": "0",
            "contactsId": "",
            "date": date,
            "from": start,
            "to": end,
            "tripId": ""
        }

        trip_id = random_from_list(trip_ids)
        base_preserve_payload["tripId"] = trip_id

        need_food = True  # random_boolean()在进行单链trace数据构造时，默认需要食物
        if need_food:
            logger.info("need food")
            food_result = self.query_food()
            food_dict = random_from_list(food_result)
            base_preserve_payload.update(food_dict)
        else:
            logger.info("not need food")
            base_preserve_payload["foodType"] = "0"

        need_assurance = True
        if need_assurance:
            assurance_result = self.query_food()    # 虽然只有一种assurance但是此处调用查询一下使得调用链丰富
            assurance_dict = random_from_list(assurance_result)
            base_preserve_payload["assurance"] = 1

        contacts_result = self.query_contacts()
        contacts_id = random_from_list(contacts_result)
        base_preserve_payload["contactsId"] = contacts_id

        # 高铁 2-3
        seat_type = random_from_list(["2", "3"])
        base_preserve_payload["seatType"] = seat_type

        need_consign = True
        if need_consign:
            consign = {
                "consigneeName": random_str(),
                "consigneePhone": random_phone(),
                "consigneeWeight": random.randint(1, 10),
                "handleDate": date
            }
            base_preserve_payload.update(consign)

        logger.info(
            f"choices: preserve_high: {is_high_speed} need_food:{need_food}  need_consign: {need_consign}  need_assurance:{need_assurance}")

        res = self.session.post(url=PRESERVE_URL,
                                headers=headers,
                                json=base_preserve_payload)

        if res.status_code == 200 and res.json()["data"] == "Success":
            logger.info(f"preserve trip {trip_id} success")
        else:
            logger.error(
                f"preserve failed, code: {res.status_code}, {res.text}")
        return
