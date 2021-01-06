# -*- coding: utf-8 -*-
from fake_useragent import UserAgent

BOT_NAME = 'MeiTuanRestaurant'

SPIDER_MODULES = ['MeiTuanRestaurant.spiders']
NEWSPIDER_MODULE = 'MeiTuanRestaurant.spiders'


ROBOTSTXT_OBEY = False

ua = UserAgent()
DEFAULT_REQUEST_HEADERS = {
    # 每次请求,随机选择一个浏览器头
    'User-Agent': ua.random,
    'Cookie': "_lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_cuid=16955ff2729c8-0a3d6889a1d5fd-8383268-1fa400-16955ff272ac8; __mta=252416950.1551925979912.1551925979912.1551925979912.1; ci=1; rvct=1; client-id=4fc38c92-2ba7-4898-b194-c45f49b253fd; _lxsdk=16955ff2729c8-0a3d6889a1d5fd-8383268-1fa400-16955ff272ac8; mtcdn=K; u=2294408295; n=qiL148082688; lt=_LYUgHM2SL4e9AVNB8y1Dl2gmCIAAAAA_gcAAF8mT_UK4vbpM4Do1TFX6tEge718GrXYu3LAeUebzWcnbGs2lz1nvelM2yo0GN8tcA; lsu=; token2=_LYUgHM2SL4e9AVNB8y1Dl2gmCIAAAAA_gcAAF8mT_UK4vbpM4Do1TFX6tEge718GrXYu3LAeUebzWcnbGs2lz1nvelM2yo0GN8tcA; uuid=5f2508d841bf44fd8a12.1551926008.2.0.0; unc=qiL148082688; lat=29.599643; lng=119.021876; _lxsdk_s=1695674abec-eef-970-ccf%7C%7C3"
}

# 设置下载延时
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS = 16
# 以下3行配置自动限速扩展
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 5

DOWNLOADER_MIDDLEWARES = {
    'MeiTuanRestaurant.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    # 'MeiTuanRestaurant.middlewares.ProxyMiddleware': 543,
}

ITEM_PIPELINES = {
    'MeiTuanRestaurant.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置
LOCAL_MONGO_HOST = '192.168.110.8'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'MeiTuanRestaurantComment'

# scrapy-redis配置
# 1(必须). 使用了scrapy_redis的去重组件，在redis数据库里做去重.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2（必须). 使用了scrapy_redis的调度器，在redis里分配请求.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 3(必须). 在redis中保持scrapy_redis用到的各个队列，从而允许暂停和暂停后回复，也就是不清理redis queues
SCHEDULER_PERSIST = True
# 配置redis服务器地址、端口、密码
REDIS_URL = 'redis://:123456@192.168.110.8:6379/0'