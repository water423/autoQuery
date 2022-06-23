import logging
import time
from queries import Query

logger = logging.getLogger("auto-queries")
datestr = time.strftime("%Y-%m-%d", time.localtime())


class AdminUserQuery(Query):

    def admin_get_all_users(self, headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminuserservice/users"

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None

        all_user_info = response.json()["data"]

        return all_user_info

    # 添加新用户，其中gender为0和1，document_type选择1为身份证号
    def admin_add_user(
            self,
            document_type: str = "",
            document_num: str = "",
            email: str = "",
            password: str = "",
            username: str = "",
            gender: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminuserservice/users"

        payload = {
            "userName": username,
            "password": password,
            "gender": gender,
            "email": email,
            "documentType": document_type,
            "documentNum": document_num
        }

        # 发送请求、获取响应并出路
        response = self.session.post(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"travel add success for {username}!")

    def admin_update_user(
            self,
            document_type: str = "",
            document_num: str = "",
            email: str = "",
            password: str = "",
            username: str = "",
            gender: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminuserservice/users"

        payload = {
            "userName": username,
            "password": password,
            "gender": gender,
            "email": email,
            "documentType": document_type,
            "documentNum": document_num
        }

        # 发送请求、获取响应并出路
        response = self.session.put(url=url, headers=headers, json=payload)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"travel update success for {username}!")

    def admin_delete_user(
            self,
            user_id: str = "",
            headers: dict = {}):
        if headers == {}:
            headers = self.session.headers

        # 请求url
        url = f"{self.address}/api/v1/adminuserservice/users/{user_id}"
        # 发送请求、获取响应并出路
        response = self.session.delete(url=url, headers=headers)

        if response.status_code != 200 or response.json().get("data") is None:  # 响应错误则忽略并打印日志
            logger.warning(f"request for {url} failed. response data is {response.text}")
            return None
        logger.info(f"travel delete success for {user_id}!")
