import json
import logging
import os
import time

import schedule

import req_model


def main(js: json):
    for i in range(3):
        time.sleep(i * 5)
        if js["username"] != "" and js["password"] != "":
            msg = req_model.upload(js["username"], js["password"])
            if msg == "":
                print(time.strftime("%H:%M") + " " + "打卡失败！！！！")
                req_model.push_msg(time.strftime("%H:%M") + " " + "打卡失败！！！！", js)
            elif json.loads(msg)["m"] == "今天已经填报了" or json.loads(msg)["m"] == "操作成功":
                msg = '{} {} AT {}'.format(js['username'], json.loads(msg)["m"], time.strftime("%H:%M"))
                print(msg)
                req_model.push_msg(msg, js)
                return
            else:
                print(time.strftime("%H:%M") + " " + json.loads(msg)["m"])
                req_model.push_msg(time.strftime("%H:%M") + " " + json.loads(msg)["m"], js)


if __name__ == '__main__':
    data = {}
    with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
        try:
            data = json.load(f)
        except:
            logging.error(" parse json data failed, please check data again")
    for item in data:
        schedule.every().day.at(data[item]["time"]).do(main, data[item])
    while 1:
        time.sleep(1)
        schedule.run_pending()
