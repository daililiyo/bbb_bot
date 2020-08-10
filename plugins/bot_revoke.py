# -*- coding:utf-8 -*-

RESOURCES_BASE_PATH = './resources/revoke'

# ==========================================

bot_qq = 123456
# 屏蔽群 例：[12345678, 87654321]
blockGroupNumber = []
# 服务器配置
host = 'http://127.0.0.1'
port = 8888

max_info_length = 341

# ==========================================

import util.db.sql as op
import time
from iotbot import Action

try:
    import ujson as json
except:
    import json


def receive_events(ctx: dict):
    if ctx['CurrentPacket']['Data']['EventName'] == 'ON_EVENT_GROUP_REVOKE' and \
            ctx['CurrentPacket']['Data']['EventData']['UserID'] != bot_qq:
        action = Action(bot_qq,
                 port=port,
                 host=host)
        msg_set = ctx['CurrentPacket']['Data']['EventData']
        msg_seq = msg_set['MsgSeq']
        msg_group_id = msg_set['GroupID']
        msg_revoke = op.find_group_msg_by_msg_seq(msg_seq, msg_group_id)[0]
        print(msg_revoke)
        if msg_revoke is None:
            print('db.find returns null result')
            return
        if msg_revoke["msg_type"] == 'TextMsg':
            msg = "棒棒冰发现 " + msg_revoke["from_nickname"] + " 撤回了消息：\n\n"
            action.send_group_text_msg(msg_revoke["from_group_id"], msg + msg_revoke["content"])
        if msg_revoke["msg_type"] == 'PicMsg':
            msg = "棒棒冰发现 " + msg_revoke["from_nickname"] + " 撤回了图片：\n\n"
            msg_content = msg_revoke["content"] if msg_revoke["content"] is not None else ""
            action.send_group_text_msg(msg_revoke["from_group_id"], msg + msg_content)
            pics = json.loads(msg_revoke["pics"])
            for pic_id in pics:
                pic_content = op.find_img_by_id(pic_id)[0]
                action.send_group_pic_msg(
                    msg_revoke["from_group_id"],
                    fileMd5=pic_content['FileMd5'],
                    picBase64Buf=pic_content['ForwordBuf']
                )
                time.sleep(0.8)
