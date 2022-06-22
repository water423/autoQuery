import logging
import time
from queries import Query

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())


class AdminTravelQuery(Query):

    def admin_get_all_travels(self, headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/admintravelservice/admintravel"

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        all_travel_info = response.json()["data"]

        return all_travel_info

    def admin_add_travel(
            self,
            # login_id: str = "",
            trip_id: str = "",
            train_type_id: str = "",
            route_id: str = "",
            # start_station_id: str = "",
            # stations_id: str = "",
            # terminal_station_id: str = "",
            start_time: str = "",
            # end_time: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/admintravelservice/admintravel"

        payload = {                                 # 请求的载荷（时间、起始地、目的地）
            "routeId": route_id,
            "startingTime": start_time,
            "trainTypeId": train_type_id,
            "tripId": trip_id
        }

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"travel add success for {trip_id}!")

    def admin_update_travel(
            self,
            # login_id: str = "",
            trip_id: str = "",
            train_type_id: str = "",
            route_id: str = "",
            # start_station_id: str = "",
            # stations_id: str = "",
            # terminal_station_id: str = "",
            start_time: str = "",
            # end_time: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/admintravelservice/admintravel"

        payload = {  # 请求的载荷（时间、起始地、目的地）
            "routeId": route_id,
            "startingTime": start_time,
            "trainTypeId": train_type_id,
            "tripId": trip_id
        }

        # 发送请求、获取响应并出路
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"travel update success for {trip_id}!")

    def admin_delete_travel(
            self,
            trip_id: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/admintravelservice/admintravel/{trip_id}"
        # 发送请求、获取响应并出路
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"travel delete success for {trip_id}!")

