import requests


def poll_server(url_base: str, auth_code: str) -> dict:
    r = requests.get(url_base + "api/v1/instruction", headers=dict(token=auth_code))
    return r.json()


def get_rewards(url_base: str, auth_code: str) -> list:
    r = requests.get(url_base + "guest/" + auth_code + "/rewards/poll", headers=dict(token=auth_code))
    return r.json()["rewards"]
