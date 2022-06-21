import logging
import time
from queries import Query

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())


class AdminBasicQuery(Query):

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

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        # 返回值为新增的车站信息
        data = response.json().get("data")
        print(data)

        return data

    def stations_get(self,  headers: dict = {}) -> str:
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
            "id": station_id,   # 用于检索车站
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












