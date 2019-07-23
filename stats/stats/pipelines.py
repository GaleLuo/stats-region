# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class StatsPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)#这里不往下传入item,spider，handle_error则不需接受,item,spider)

        
    def do_insert(self,cursor,item):
        #执行具体的插入语句,不需要commit操作,Twisted会自动进行
        insert_sql = """
                INSERT INTO region
                    (id, region_code, region_name, parent_id, region_level,create_time,update_time)
                VALUES (%s, %s, %s, %s, %s,UNIX_TIMESTAMP(NOW()),UNIX_TIMESTAMP(NOW()))
        """
        cursor.execute(insert_sql,(item['id'],item['region_code'],item['region_name'],item['parent_id'],item['region_level']))

    def handle_error(self, failure, item, spider):
        print(failure)