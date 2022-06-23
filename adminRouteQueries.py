import logging
import time
from queries import Query

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())
station_list_example = "[\"beijingxi\",\"shijiazhuang\",\"zhengzhoudong\",\"xiangyangdong\",\"chongqingbei\"]"
distance_list_example = "[0,150,360,500,670,1100]"


class AdminRouteQuery(Query):

    def admin_get_all_routes(self, headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminrouteservice/adminroute"

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        all_route_info = response.json()["data"]

        return all_route_info

    # 添加线路，车站列表和距离列表形式可以参见文件头部的example
    def admin_add_route(
            self,
            station_list: str = "",
            distance_list: str = "",
            start_station: str = "",
            end_station: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminrouteservice/adminroute"

        payload = {
            "distanceList": f"{distance_list}",
            "endStation": f"{end_station}",
            "startStation": f"{start_station}",
            "stationList": f"{station_list}"
        }
        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"route add success for!")

    def admin_delete_route(
            self,
            routeId: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminrouteservice/adminroute/{routeId}"
        # 发送请求、获取响应并出路
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"route delete success for routeID {routeId}")

