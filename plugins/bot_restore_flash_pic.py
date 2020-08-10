# -*- coding:utf-8 -*-

RESOURCES_BASE_PATH = './resources/restore_flash_pic'

# ==========================================

# 屏蔽群 例：[12345678, 87654321]
blockGroupNumber = []
# 服务器配置
host = 'http://127.0.0.1'
port = 8888

# ==========================================

from iotbot import Action, GroupMsg
from enum import Enum

try:
    import ujson as json
except:
    import json


def receive_group_msg(ctx: GroupMsg):
    userGroup = ctx.FromGroupId

    if Tools.commandMatch(userGroup, blockGroupNumber):
        return

    if not Tools.picOnly(ctx.MsgType):
        return

    msg = ctx.Content

    bot = Action(
        qq_or_bot = ctx.CurrentQQ,
        host = host,
        port = port
    )

    content = json.loads(msg)

    if content["Tips"] == '[群消息-QQ闪照]':
        Tools.sendPictures(bot, userGroup, content['FileMd5'], content['ForwordBuf'], '你竟然发闪照[表情176]')


class Model(Enum):
    ALL = '_all'

    BLURRY = '_blurry'

    SEND_AT = '_send_at'

    SEND_DEFAULT = '_send_default'


class Status(Enum):
    SUCCESS = '_success'

    FAILURE = '_failure'


class Tools():

    @staticmethod
    def picOnly(msgType):
        return True if msgType == 'PicMsg' else False

    @classmethod
    def sendPictures(cls, bot, userGroup, FileMd5, ForwordBuf, content='', atUser=0):
        bot.send_group_pic_msg(
            toUser=int(userGroup),
            fileMd5=FileMd5,
            picBase64Buf=ForwordBuf,
            atUser=int(atUser),
            content=str(content)
        )

    @staticmethod
    def sendText(userGroup, msg, bot, model=Model.SEND_DEFAULT, atQQ=''):
        if msg != '' and msg != Status.FAILURE:
            if model == Model.SEND_DEFAULT:
                bot.send_group_text_msg(
                    toUser=int(userGroup),
                    content=str(msg)
                )
            if model == Model.SEND_AT:
                if atQQ == '':
                    raise Exception('没有指定 at 的人！')
                at = f'[ATUSER({atQQ})]\n'
                bot.send_group_text_msg(
                    toUser=int(userGroup),
                    content=at + str(msg)
                )

    @staticmethod
    def commandMatch(msg, commandList, model=Model.ALL):
        if model == Model.ALL:
            for c in commandList:
                if c == msg:
                    return True
        if model == Model.BLURRY:
            for c in commandList:
                if msg.find(c) != -1:
                    return True
        return False

    @staticmethod
    def atQQ(userQQ):
        return f'[ATUSER({userQQ})]\n'

    @staticmethod
    def identifyAt(content):
        try:
            result = json.loads(content)
            return [result['Content'], result['UserID']]
        except:
            return Status.FAILURE
