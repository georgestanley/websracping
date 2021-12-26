# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from .items import CompaniesItem, InsiderTradesItem


class InsidertradingPipeline:

    def __init__(self) -> None:
        self.create_connection()
        self.create_table()

        
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user = 'root',
            passwd= 'helloworld123',
            database = 'insider_trades'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        #self.curr.execute("""DROP TABLE IF EXISTS companies""")
        self.curr.execute("""create table IF NOT EXISTS companies(
            company_id INT AUTO_INCREMENT PRIMARY KEY,
            company_name text,
            path text,
            insider_trades_weblink text,
            created_at timestamp)""")
        #self.curr.execute("""DROP TABLE IF EXISTS trades""")
        self.curr.execute("""create table IF NOT EXISTS trades(
            tranx_id INT AUTO_INCREMENT PRIMARY KEY,
            company_id INT,
            date text,
            trader text,
            quantity text,
            short_val text,
            type text,
            created_at timestamp)""")    

    def process_item(self, item, spider):
        if isinstance(item,CompaniesItem):
            self.store_db_companies(item)
            #print('Pipeline:'+ item['company_name'][0] )
            return item
        elif isinstance(item,InsiderTradesItem):
            self.store_db_trades(item)
            #print('Pipeline:'+ item['company_name'][0] )
            return item

    def store_db_companies(self, item):
        self.curr.execute("""insert into companies(company_name,path,insider_trades_weblink,created_at) values (%s,%s,%s, now())""",
        (
            item['company_name'],
            item['path'],
            item['insider_trades_weblink'],

        ) )
        self.conn.commit()
    
    def store_db_trades(self, item):
        self.curr.execute("""insert into trades (company_id,
            date,
            trader ,
            quantity ,
            short_val,
            type,
            created_at)values (%s,%s,%s,%s,%s,%s,now())""",
        (
            item['company_id'],
            item['date'],
            item['trader'],
            item['quantity'],
            item['short_val'],
            item['type']
        ) )
        self.conn.commit()
