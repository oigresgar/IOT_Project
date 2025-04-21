import os

import requests
from dotenv import load_dotenv


class AmiLabHttp:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token

    def get_state(self, entity_id: str):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }
        return requests.get(self.url + "/states/" + entity_id, headers=headers).json()

    def post_service(
        self, entity_id: str, service: str, command: str, extra_data: dict = {}
    ):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }
        data = {
            "entity_id": entity_id,
        }
        data.update(extra_data)
        return requests.post(
            self.url + "/services/" + service + "/" + command,
            headers=headers,
            json=data,
        ).json()

    def get_snapshot(self, mock=False) -> bytes:
        if mock:
            with open("utils/mock.jpg", "rb") as f:
                return f.read()
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "image/jpeg",
        }
        return requests.get(
            self.url + "/camera_proxy/camera.amicam", headers=headers
        ).content


if __name__ == "__main__":
    load_dotenv()
    url = os.getenv("AMI_LAB_URL")
    token = os.getenv("AMI_LAB_TOKEN")
    ami_lab = AmiLabHttp(url, token)
    # print(ami_lab.get_state(entity_id="light.lampara_de_lectura"))
    print(
        ami_lab.post_service(
            entity_id="light.lampara_derecha",
            service="light",
            command="turn_off",
            # extra_data={"brightness_pct": "100", "rgb_color": [255, 0, 0]},
        )
    )

"""     img_bytes = ami_lab.get_snapshot()
    with open("snapshot.jpeg", "wb") as f:
        f.write(img_bytes)
 """
