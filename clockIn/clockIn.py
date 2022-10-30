import json
import logging
import os
import time

import req_model


def main():
    data = {}
    with open(os.path.dirname(__file__) + "/config.json", "r") as f:
        try:
            data = json.load(f)
        except:
            logging.error(" parse json data failed, please check data again")
            return
    for item in data:
        for i in range(3):
            time.sleep(i * 5)
            print("now {} clock in {}:".format(item, i))
            if data[item]["username"] != "" and data[item]["password"] != "":
                msg = req_model.upload(data[item]["username"], data[item]["password"])
                if msg == "":
                    print("{} 打卡失败!!".format(time.strftime("%H:%M")))
                    req_model.push_msg("{} 打卡失败!!".format(time.strftime("%H:%M")), data[item])
                elif json.loads(msg)["m"] == "今天已经填报了" or json.loads(msg)["m"] == "操作成功":
                    print("{} {}".format(time.strftime("%H:%M"), json.loads(msg)["m"]))
                    req_model.push_msg("{} {}".format(time.strftime("%H:%M"), json.loads(msg)["m"]), data[item])
                    break
                else:
                    print("{} {}".format(time.strftime("%H:%M"), json.loads(msg)["m"]))
                    req_model.push_msg("{} {}".format(time.strftime("%H:%M"), json.loads(msg)["m"]), data[item])
            else:
                print("{}'s username or password is null".format(item))
                break


if __name__ == '__main__':
    main()
