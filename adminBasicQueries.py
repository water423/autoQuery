import logging
import time
from queries import Query

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())


class AdminBasicQuery(Query):

    # station相关增删改查
    def stations_post(self, station_id: str = "", name: str = "", stay_time: int = 15, headers: dict = {}) -> str:
        """
        添加车站stations
        :param station_id: 新增station的id
        :param name: 新增station的名称
        :param stay_time: 新增station的的停靠时间
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/stations"

        # 请求载荷，对应@requestbody注解
        payload = {
            "id": station_id,
            "name": name,
            "stayTime": stay_time,
        }

        # 发送请求、获取响应
        # 重复添加某一id对应的station不会抛出异常，但也不会覆盖或造成影响
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为新增的车站信息
        data = response.json().get("data")
        print(data)
        return data

    def stations_get(self, headers: dict = {}) -> str:
        """
        获取所有车站信息
        :param headers: 请求头
        :return 所有车站组成的列表，每个车站的具体信息为字典形式，整合成string返回
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/stations"

        # 发送请求、获取响应
        response = self.session.get(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def stations_put(self, station_id: str = "", name: str = "", stay_time: int = 15, headers: dict = {}) -> str:
        """
        修改某一车站信息
        :param station_id: station的id
        :param name: 修改后station的名称
        :param stay_time: 修改后station的的停靠时间
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/stations"

        # 请求载荷，对应@requestbody注解
        payload = {
            "id": station_id,
            "name": name,
            "stayTime": stay_time,
        }

        # 发送请求、获取响应
        # 对于此put请求而言，如果输入的payload代表的车站(由id决定)不存在则修改车站信息会抛出异常
        # {"status":0,"msg":"Station not exist","data":null}
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为修改后的车站信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def stations_delete(self, station_id: str = "", name: str = "", stay_time: int = 15, headers: dict = {}) -> str:
        """
        删除某一车站信息
        :param station_id: 删除station的id
        :param name: 删除station的名称（可以不正确）
        :param stay_time: 删除station的的停靠时间（可以不正确）
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/stations"

        # 请求载荷，对应@requestbody注解
        payload = {
            "id": station_id,  # 用于检索车站
            "name": name,
            "stayTime": stay_time,
        }

        # 发送请求、获取响应
        # 对于此delete请求而言，如果输入的payload代表的车站(由id决定)不存在则删除车站会抛出异常
        # {"status": 0, "msg": "Station not exist", "data": null}
        response = self.session.delete(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为删除车站的信息（id + 输入的name + 0）
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    # contact相关增删改查
    def contacts_post(self, account_id: str = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                      contact_name: str = "Contacts_X", document_type: int = 1,
                      document_number: str = "DocumentNumber_X", phone_number: str = "19921940977",
                      headers: dict = {}):
        """
        添加联系人contact
        # :param contact_id: 新增contact的id (不需要输入，在新建时随机生成)
        :param account_id: 新增contact的账户id
        :param contact_name: 新增contact的名称
        :param document_type:
        :param document_number:
        :param phone_number:
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/contacts"

        # 请求载荷
        payload = {
            "accountId": account_id,
            "name": contact_name,
            "documentType": document_type,
            "documentNumber": document_number,
            "phoneNumber": phone_number
        }

        # 发送请求、获取响应
        # 重复添加同一个contact是不会导致异常的，其内部生成的id不同
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为null（{"status":1,"msg":"Create Success","data":null}）
        return

    def contacts_get(self, headers: dict = {}) -> str:
        """
        获取所有联系人
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/contacts"

        # 发送请求、获取响应
        response = self.session.get(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def contacts_put(self, contact_id: str, account_id: str = "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                     contact_name: str = "Contacts_Y", document_type: int = 2,
                     document_number: str = "DocumentNumber_Y", phone_number: str = "19921940900",
                     headers: dict = {}) -> str:
        """
        修改某一联系人信息
        :param contact_id: 新增contact的id
        :param account_id: 新增contact的账户id
        :param contact_name: 新增contact的名称
        :param document_type:
        :param document_number:
        :param phone_number:
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/contacts"

        # 请求载荷，对应@requestbody注解
        payload = {
            "id": contact_id,
            "accountId": account_id,
            "name": contact_name,
            "documentType": document_type,
            "documentNumber": document_number,
            "phoneNumber": phone_number
        }

        # 发送请求、获取响应
        # 对于此put请求而言，如果输入的payload代表的联系人(由id决定)不存在则修改车站信息会抛出异常
        # {"status":0,"msg":"Contacts not found","data":null}
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为修改后的联系人信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def contacts_delete(self, contact_id: str = "", headers: dict = {}) -> str:
        """
        删除某一联系人信息
        :param contact_id: 删除contact的id
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/contacts"+"/"+contact_id

        # 发送请求、获取响应
        # 对于此delete请求而言，如果输入id代表的联系人不存在也仅仅会返回输入的contactId
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为输入的contactId
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    # trains相关增删改查
    def trains_post(self, train_id: str = "ManSu", economy_class: int = 2147483647,
                    confort_class: int = 2147483647, average_speed : int = 80,
                    headers: dict = {}) -> str:
        """
        添加车型
        :param train_id: 新增train的id (需要输入)
        :param economy_class: 经济座
        :param confort_class: 商务座
        :param average_speed:平均速度
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/trains"

        # 请求载荷
        payload = {
            "id": train_id,
            "economyClass": economy_class,
            "confortClass": confort_class,
            "averageSpeed": average_speed
        }

        # 发送请求、获取响应
        # 重复添加同一个trainType无影响
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值新增车型的信息，若为新增的车型则返回None,若新增的车型已经存在则返回train的具体信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def trains_get(self, headers: dict = {}) -> str:
        """
        获取所有车型
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/trains"

        # 发送请求、获取响应
        response = self.session.get(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def trains_put(self, train_id: str = "ManSu", economy_class: int = 2147483647,
                   confort_class: int = 2147483647, average_speed : int = 50,
                   headers: dict = {}) -> str:
        """
        修改某一车型信息
        :param train_id: 新增train的id (需要输入)
        :param economy_class: 经济座
        :param confort_class: 商务座
        :param average_speed:平均速度
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/trains"

        # 请求载荷，对应@requestbody注解
        payload = {
            "id": train_id,
            "economyClass": economy_class,
            "confortClass": confort_class,
            "averageSpeed": average_speed
        }

        # 发送请求、获取响应
        # 对于此put请求而言，如果输入的payload代表的联系人(由id决定)不存在则返回值为false，若修改成功则返回值为true
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为true/false
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def trains_delete(self, train_id: str = "ManSu", headers: dict = {}) -> bool:
        """
        删除某一车型信息
        :param train_id: 删除contact的id
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/trains"+"/"+train_id

        # 发送请求、获取响应
        # 对于此delete请求而言，如果输入id代表的train不存在会抛出异常
        # {"status":0,"msg":"there is no train according to id","data":null}
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 删除成功 返回值为true
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    # configs相关增删改查
    def configs_post(self, name: str = "ConfigTest", value: str = "0.5",
                     description: str = "ConfigTest Description", headers: dict = {}) -> str:
        """
        添加配置信息config
        :param name: 新增config的名称
        :param value: 值
        :param description: 描述信息
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/configs"

        # 请求载荷
        payload = {
            "name": name,
            "value": value,
            "description": description
        }

        # 发送请求、获取响应
        # 重复添加同一个config会抛出异常
        # {"status":0,"msg":"Config ConfigTest already exists.","data":null}
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None :  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值新增配置的信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def configs_get(self, headers: dict = {}) -> str:
        """
        获取所有配置信息
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/configs"

        # 发送请求、获取响应
        response = self.session.get(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def configs_put(self,  name: str = "ConfigTest", value: str = "1",
                    description: str = "ConfigTest Description", headers: dict = {}) -> str:
        """
        添加配置信息config
        :param name: 新增config的名称
        :param value: 值
        :param description: 描述信息
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/configs"

        # 请求载荷，对应@requestbody注解
        payload = {
            "name": name,
            "value": value,
            "description": description
        }

        # 发送请求、获取响应
        # 对于此put请求而言，如果输入的payload代表的config(由name决定)不存在则抛出异常
        # {"status":0,"msg":"Config ConfigTest11 doesn't exist.","data":null}
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为修改后的配置信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def configs_delete(self, name: str = "ConfigTest", headers: dict = {}) -> bool:
        """
        删除某一配置信息
        :param name: 删除config的name
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/configs"+"/"+name

        # 发送请求、获取响应
        # 对于此delete请求而言，如果输入id代表的config不存在会抛出异常
        # {"status":0,"msg":"Config ConfigTest11 doesn't exist.","data":null}
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 删除成功 返回值被删除的配置信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    # prices相关增删改查
    def prices_post(self, train_type: str = "DongCheOne",
                    route_id: str = "f3d4d4ef-693b-4456-8eed-59c0d717dd08", basic_price_rate: float = 0.5,
                    first_class_price_rate : float = 1, headers: dict = {}) -> str:
        """
        添加价格price
        # :param price_id: 新增price的id(不需要输入，在创建时自动生成)
        :param train_type: 车型
        :param route_id: 对应route的id
        :param basic_price_rate
        :param first_class_price_rate
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/prices"

        # 请求载荷
        payload = {
            "trainType": train_type,
            "routeId": route_id,
            "basicPriceRate":basic_price_rate,
            "firstClassPriceRate": first_class_price_rate,
        }

        # 发送请求、获取响应
        # 重复添加train_type route_id相等的price会重复添加，因为生成的id不同
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值新增配置的信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def prices_get(self, headers: dict = {}) -> str:
        """
        获取所有价格信息
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/prices"

        # 发送请求、获取响应
        response = self.session.get(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def prices_put(self, price_id:str, train_type: str = "GaoTie2",
                   route_id: str = "1367db1f-461e-4ab7-87ad-2bcc05fd9cb7", basic_price_rate: float = 0.5,
                   first_class_price_rate: float = 1.2, headers: dict = {}) -> str:
        """
        添加价格price
        :param price_id: price的id(需要输入，用于索引)
        :param train_type: 车型
        :param route_id: 对应route的id
        :param basic_price_rate
        :param first_class_price_rate
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/prices"

        # 请求载荷
        payload = {
            "id": price_id,
            "trainType": train_type,
            "routeId": route_id,
            "basicPriceRate":basic_price_rate,
            "firstClassPriceRate": first_class_price_rate,
        }

        # 发送请求、获取响应
        # 对于此put请求而言，如果输入的payload代表的config(由name决定)不存在则抛出异常
        # {"status":0,"msg":"No that config","data":null}
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为修改后的price信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data

    def prices_delete(self, price_id: str, train_type: str = "GaoTie2",
                      route_id: str = "1367db1f-461e-4ab7-87ad-2bcc05fd9cb7", basic_price_rate: float = 0.5,
                      first_class_price_rate: float = 1.2, headers: dict = {}) -> str:
        """
        删除价格price
        :param price_id: price的id(需要输入，用于索引)
        :param train_type: 车型
        :param route_id: 对应route的id
        :param basic_price_rate
        :param first_class_price_rate
        :param headers: 请求头
        :return
        """

        # 请求url
        url = f"{self.address}/api/v1/adminbasicservice/adminbasic/prices"

        # 请求载荷
        payload = {
            "id": price_id,
            "trainType": train_type,
            "routeId": route_id,
            "basicPriceRate": basic_price_rate,
            "firstClassPriceRate": first_class_price_rate,
        }

        # 发送请求、获取响应
        # 对于此delete请求而言，如果输入id代表的price不存在会抛出异常
        # {"status":0,"msg":"No that config","data":null}
        response = self.session.delete(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 删除成功 返回值被删除的配置信息
        data = response.json().get("data")  # 用string形式返回
        print(data)
        return data
