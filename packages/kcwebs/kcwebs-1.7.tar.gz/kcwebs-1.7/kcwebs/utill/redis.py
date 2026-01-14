# -*- coding: utf-8 -*-
# from kcwebs.utill import rediss as red
import redis as red
from kcwebs import config
import json,copy
class redis:
    "redis  注意：连接池链接模式下不支持动态配置"
    db=copy.deepcopy(config.redis['db']) #默认数据库
    __redisObj=None
    __coninfo={}
    __config=copy.deepcopy(config.redis)
    __identifier=''
    def close(self,pattern=False):
        if self.__config['pattern']:
            if pattern:
                if not self.__identifier:
                    self.__identifier=self.__config['host']+self.__config['password']+str(self.__config['port'])+str(self.__config['db'])
                self.__redisObj.close()
                self.__redisObj=None
                del self.__coninfo[self.__identifier]
        elif self.__redisObj:
            self.__redisObj.close()
            self.__redisObj=None
    def __connects(self):
        """设置redis链接"""
        if self.__config['pattern']:
            self.__identifier=self.__config['host']+self.__config['password']+str(self.__config['port'])+str(self.__config['db'])
            if self.__identifier not in self.__coninfo:
                if self.__config['password']:
                    redis_pool=red.ConnectionPool(host=self.__config['host'],password=self.__config['password'],port=self.__config['port'],db=self.__config['db'])
                else:
                    redis_pool=red.ConnectionPool(host=self.__config['host'],port=self.__config['port'],db=self.__config['db'])
                self.__coninfo[self.__identifier]=red.Redis(connection_pool=redis_pool)
                if config.app['app_debug']:
                    print("建立redis连接池",self.__identifier)
            self.__redisObj=self.__coninfo[self.__identifier]
            self.__config['db']=self.db
        else:
            if self.__config['password']:
                self.__redisObj=red.Redis(host=self.__config['host'],password=self.__config['password'],port=self.__config['port'],db=self.__config['db'])
            else:
                self.__redisObj=red.Redis(host=self.__config['host'],port=self.__config['port'],db=self.__config['db'])
                
            if config.app['app_debug']:
                print("建立redis连接",self.__identifier)
        
    def __json_decode(self,strs):
        """json字符串转python类型"""
        try:
            return json.loads(strs)
        except Exception:
            return {}
    def __json_encode(self,strs):
        """转成字符串"""
        try:
            return json.dumps(strs,ensure_ascii=False)
        except Exception:
            return ""
    def getconfig(self):
        return self.__config
    def connect(self,configs):
        """设置redis链接信息 

        参数 config 参考配置信息格式

        返回 redis
        """ 
        if configs:
            if isinstance(configs,int):
                self.__config=copy.deepcopy(config.redis)
                self.__config['db']=configs
            elif isinstance(configs,dict):
                if "host" in configs:
                    self.__config['host']=configs['host']
                if "port" in configs:
                    self.__config['port']=configs['port']
                if "password" in configs:
                    self.__config['password']=configs['password']
                if "db" in configs:
                    self.__config['db']=configs['db']
            else:
                raise Exception("配置信息错误")
        else:
            self.__config=copy.deepcopy(config.redis)
        return self
    
    def redisObj(self):
        "得到一个redis连接对象，执行更多高级操作"
        self.__connects()
        return self.__redisObj
    def incrby(self,name,value,ex=0):
        """设置自增数量
        
        name，键

        value，值 自增 步长

        ex，过期时间（秒）
        """
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.incrby(name,value)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                if ex and status:
                    self.__redisObj.expire(name, ex)
                self.close()
                break
        return status
    def getstr(self,name):
        """获取name的值

        name，键
        返回键“name”处的值，如果该键不存在，则返回“none”
        """
        i=0
        while True:
            self.__connects()
            try:
                value=self.__redisObj.get(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return value
        
    def setstr(self,name,value,ex=None, px=None, nx=False, xx=False):
        """
        name，键

        value，值 只能是字符串

        ex，过期时间（秒）

        px，过期时间（毫秒）

        nx，如果设置为True，则只有key不存在时，当前set操作才执行,同#setnx(key, value)

        xx，如果设置为True，则只有key存在时，当前set操作才执行
        """
        if not ex and not px:
            if self.__config['ex']:
                ex=self.__config['ex']
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.set(name, value, ex=ex, px=px, nx=nx, xx=xx)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def append(self,name,value):
        """将字符串“value”追加到“name”处的值。如果``键`` 不存在，请使用值“name”创建它。 返回位于“name”的值的新长度。
        
        name，键

        value，值 只能是字符串
        """
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.append(name,value)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def set(self,name,value,ex=None, px=None, nx=False, xx=False):
        """
        name，键

        value，值 可以是字典 列表 或字符串

        ex，过期时间（秒）

        px，过期时间（毫秒）

        nx，如果设置为True，则只有key不存在时，当前set操作才执行

        xx，如果设置为True，则只有key存在时，当前set操作才执行
        """
        if not ex and not px:
            if self.__config['ex']:
                ex=self.__config['ex']
        value=self.__json_encode(value)
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.set(name, value, ex=ex, px=px, nx=nx, xx=xx)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def get(self,name):
        """获取name的值

        name，键
        返回键“name”处的值，如果该键不存在，则返回“none”
        """
        i=0
        while True:
            self.__connects()
            try:
                value=self.__redisObj.get(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        if value:
            value=self.__json_decode(value)
        return value
    def delete(self,name):
        """删除name的值

        name，键
        
        返回 True，如果该键不存在，则返回 0
        """
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.delete(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def rpush(self,name, *values):
        "元素从list的右边加入 ，可以添加多个"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.rpush(name, *values)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def rpop(self,name):
        "元素从list的右边移出"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.rpop(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def rpoplpush(self,src, dst):
        "元素从list的右边移出,并且从list的左边加入"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.rpoplpush(src, dst)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def rpushx(self,name, value):
        "当name存在时，元素才能从list的右边加入"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.rpushx(name, value)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def lpush(self,name, *values):
        "元素从list的左边加入，可以添加多个"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.lpush(name, *values)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def lpop(self,name):
        "元素从list的左边移出"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.lpop(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def lpushxs(self,name):
        "当name存在时，元素才能从list的左边加入"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.lpushx(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def hset(self,name,key,value):
        """在hash名称中将key设置为value如果HSET创建了新字段，则返回1，否则返回0
        
        name，名

        key，键

        mapping，值
        """
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.hset(name,key,value)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
     
    def hget(self,name,key):
        "返回hash的name中的key值"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.hget(name,key)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def hgetall(self,name):
        "返回hash名称/值对的Python dict"
        i=0
        while True:
            self.__connects()
            try:
                data=self.__redisObj.hgetall(name)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return data
    
    def hdel(self,name,key):
        """在hash名称中将key删除
        
        name，名

        key，键
        """
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.hdel(name,key)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status
    def hmset(self,name,mapping,ex=0):
        """在hash的name中为每个键设置值
        name，键

        mapping，值

        ex,过期时间(秒)
        
        """
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.hmget(name, keys, *args)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                if not ex:
                    if self.__config['ex']:
                        ex=self.__config['ex']
                if ex:
                    self.__redisObj.expire(name,ex)
                self.close()
                break
        return status
    def hmget(self,name, keys, *args):
        "返回与“keys”顺序相同的值列表``"
        i=0
        while True:
            self.__connects()
            try:
                status=self.__redisObj.hmget(name, keys, *args)
            except Exception as e:
                stre=str(e)
                if 'Error while reading from socket' in stre or 'Error 10054 while writing to socket' in stre:
                    i+=1
                    self.close(pattern=True)
                    if i>3:
                        raise Exception(e)
                else:
                    print("__redisObj_e",e)
                    raise Exception(e)
            else:
                self.close()
                break
        return status