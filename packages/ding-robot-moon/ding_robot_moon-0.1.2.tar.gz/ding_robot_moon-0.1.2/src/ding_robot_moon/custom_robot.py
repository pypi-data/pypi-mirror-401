import requests


class CustomRobot:
    url = "https://oapi.dingtalk.com/robot/send"
    headers = {
        "Content-Type": "application/json"
    }
    def __init__(self, token):
        self.token = token
        

    def send_text(self, text, atMobiles:list[str]=[], isAtAll:bool=False):
        url = f"{self.url}?access_token={self.token}"
        data = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": isAtAll
            }
        }
        resp = requests.post(url=url, headers=self.headers, json=data)
        return resp.status_code, resp.text

