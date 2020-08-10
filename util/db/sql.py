# 导入pymysql模块
import time

import pymysql
import json

# 连接database
from iotbot import GroupMsg, FriendMsg

f = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "",
    "password": "",
    "database": ""
}


class Mysql:
    def __init__(self, db):
        self.db = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], password=db['password'],
                                  database=db['database'])
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def commit(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as error:
            print('\033[031m', error, '\033[0m', sep='')

    def update(self, dt_update, dt_condition, table):
        sql = 'UPDATE %s SET ' % table + ','.join('%s=%r' % (k, dt_update[k]) for k in dt_update) \
              + ' WHERE ' + ' AND '.join('%s=%r' % (k, dt_condition[k]) for k in dt_condition) + ';'
        self.commit(sql)

    def insert(self, tb, dt):
        ls = [(k, dt[k]) for k in dt if dt[k] is not None]
        sql = 'insert %s (' % tb + ','.join(i[0] for i in ls) + \
              ') values (' + ','.join('%r' % i[1] for i in ls) + ');'
        self.cursor.execute(sql)
        # print(sql)
        res = self.db.insert_id()
        self.db.commit()
        return res

    def query(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res


# img
def find_img_by_id(id):
    db_client = f
    db = Mysql(db_client)
    res = db.query('''SELECT * FROM `img` WHERE FileId=%d''' % id)
    return res


# group_msg
def find_group_msg_by_msg_seq(msg_seq, from_group_id=None):
    db_client = f
    db = Mysql(db_client)
    if from_group_id is None:
        res = db.query('''SELECT * FROM `group_msg` WHERE msg_seq=%d''' % msg_seq)
    else:
        res = db.query('''SELECT * FROM `group_msg` WHERE msg_seq=%s AND from_group_id=%d''' % (msg_seq, from_group_id))
    return res


def insert_group_msg(ctx: GroupMsg):
    db_client = f
    db = Mysql(db_client)
    if ctx.MsgType == 'TextMsg':
        res = db.insert('group_msg', dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            at_user_id=None,
            content=ctx.Content,
            pics=None,
            tips="",
            redbag_info=ctx.RedBaginfo,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom
        ))
        # print(res)
    elif ctx.MsgType == 'PicMsg':
        content = json.loads(ctx.Content)
        pics = []
        for pic in content["GroupPic"]:
            ret = db.insert('img', dict(
                FileId=pic['FileId'],
                FileMd5=pic['FileMd5'],
                FileSize=pic['FileSize'],
                ForwordBuf=pic['ForwordBuf'],
                ForwordField=pic['ForwordField'],
                Url=pic['Url'],
            ))
            pics.append(ret)
        db.insert('group_msg', dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            at_user_id=content["UserID"] if "UserID" in content else None,
            content=content["Content"] if "Content" in content else None,
            pics=json.dumps(pics),
            tips=content["Tips"],
            redbag_info=ctx.RedBaginfo,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom
        ))
    elif ctx.MsgType == 'AtMsg':
        content = json.loads(ctx.Content)
        db.insert('group_msg', dict(
            current_qq=ctx.CurrentQQ,
            from_nickname=ctx.FromNickName,
            from_user_id=ctx.FromUserId,
            from_group_name=ctx.FromGroupName,
            from_group_id=ctx.FromGroupId,
            at_user_id=content["UserID"][0] if "UserID" in content else None,
            content=content["Content"] if "Content" in content else None,
            pics=None,
            tips=content["Tips"] if "Tips" in content else None,
            redbag_info=ctx.RedBaginfo,
            msg_time=ctx.MsgTime,
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq,
            msg_random=ctx.MsgRandom
        ))
    else:
        print('Unspecified message type')


# friend_msg
def insert_friend_msg(ctx: FriendMsg):
    db_client = f
    db = Mysql(db_client)
    if ctx.MsgType == 'TextMsg':
        content = ctx.Content
        db.insert('friend_msg', dict(
            current_qq=ctx.CurrentQQ,
            from_user_id=ctx.FromUin,
            content=content["Content"] if "Content" in content else None,
            pics=None,
            tips=None,
            redbag_info=ctx.RedBaginfo,
            msg_time=int(time.time()),
            msg_type=ctx.MsgType,
            msg_seq=ctx.MsgSeq
        ))
    # elif ctx.MsgType == 'PicMsg':
    #     content = json.loads(ctx.Content)
    #     print(content)
    #     pics = []
    #     for pic in content["FriendPic"]:
    #         ret = db.insert('img', dict(
    #             # FileId=pic['FileId'],
    #             FileMd5=pic['FileMd5'],
    #             FileSize=pic['FileSize'],
    #             ForwordBuf=pic['Path'],
    #             # ForwordField=pic['ForwordField'],
    #             Url=pic['Url'],
    #         ))
    #         pics.append(ret.inserted_id)
    #     db.insert('friend_msg', dict(
    #         current_qq=ctx.CurrentQQ,
    #         from_user_id=ctx.FromUin,
    #         content=content["Content"] if "Content" in content else None,
    #         pics=json.dumps(pics),
    #         tips=content["Tips"] if "Tips" in content else None,
    #         redbag_info=ctx.RedBaginfo,
    #         msg_time=int(time.time()),
    #         msg_type=ctx.MsgType,
    #         msg_seq=ctx.MsgSeq
    #     ))
    else:
        print('Unspecified message type')

# if __name__ == '__main__':
#     insert_msg()
