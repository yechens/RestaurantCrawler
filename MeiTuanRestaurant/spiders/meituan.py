# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiders import Spider
from MeiTuanRestaurant.items import Comment
import json
import logging

logging.basicConfig(level=logging.INFO, datefmt='%Y/%m/%d %H:%M:S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('__MeiTuan__')


class MeituanSpider(Spider):
    name = 'meituan'
    cities = ['成都', '杭州', '上海', '深圳', '厦门']
    url1 = "https://sz.meituan.com/meishi/api/poi/getPoiList?cityName="
    url2 = "&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page="
    url3 = "&userId=2294408295&uuid=5f2508d841bf44fd8a12.1551926008.2.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fsz.meituan.com%2Fmeishi%2Fpn2%2F&riskLevel=1&optimusCode=1&_token=eJxVjsluglAUht%2FlbiFeuMjkroooFJRBUGq6QGQUKDIJNH333ia6aHKSfzjf4v8GtXIFC5qiRIoiQR%2FWYAHoGTXjAAnaBn9YlhYRz3I8QjQJgv8dx89JcKldCSzOIo1IkRE%2B%2FwoL5zNmKJKmBOqTfPk59miO749SMASStq2aBYTNNCvCtO38chZ8FRD7JklhVSKIhwCMFweMY7091X9q%2B8o6Xo7ZJo1L7EL1kWeHdm9Oa9OKQvtxd6Ay9aPJvC%2BddJ3sk0s8GLqdEqHBS2u7VtydtSpGJY%2B3Vn5gZDkq%2Be0gwcEOPlZXg3gjLCNnBbO%2FTj3DQsZNlf1R53N1W938bCeNnesltei8Kdzg3DWWTSJEeJ2lOXC1W8MwUJUHuhLvt1znq%2BDLjy%2FLe0Zk8VTsqtapkLbnQrfSbNpwvVLkhzIK1D6yR21rCbagNpu41exxk1kbSR8bz%2FcMl6uTe29eavm0zDO5ijXulD9Wx1NHExv51izBzy%2FqUpDI"
    comment_url1 = "https://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=5f2508d841bf44fd8a12.1551926008.2.0.0&platform=1&partner=126&originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F"
    comment_url2 = "%2F&riskLevel=1&optimusCode=1&id="
    comment_url3 = "&userId=2294408295&offset="
    comment_url4 = "&pageSize=10&sortType=1"

    def start_requests(self):
        meta = {}
        for city in self.cities:
            # print("City #", city)
            # logger.info("City #" + city)
            logger.info("欢迎来到 #" + city)
            for page in range(0, 68):
                start_url = self.url1 + city + self.url2 + str(page) + self.url3
                meta["city"] = city
                yield Request(url=start_url, callback=self.parse_home,
                              dont_filter=True, meta=meta, priority=8)
            #     break
            # break

    def parse_home(self, response):
        city = response.meta["city"]
        sites = json.loads(response.body_as_unicode())
        sites = sites["data"]["poiInfos"]
        meta = {}
        for site in sites:
            title = site["title"]
            poiId = str(site["poiId"])
            comment_url = self.comment_url1 + poiId \
                        + self.comment_url2 + poiId \
                        + self.comment_url3 + "0" \
                        + self.comment_url4
            meta["offset"] = "0"
            meta["poiId"] = poiId
            meta["city"] = city
            meta["title"] = title
            yield Request(url=comment_url, callback=self.parse_comment,
                          dont_filter=True, meta=meta, priority=6)
            # break

    def parse_comment(self, response):
        offset = response.meta["offset"]
        poiId = response.meta["poiId"]
        city = response.meta["city"]
        title = response.meta["title"]
        sites = json.loads(response.body_as_unicode())
        # 如果是第一页，一次性解析后面所有页评论
        if offset == "0":
            total = sites["data"]["total"]
            pages = total // 10
            if pages >= 25:
                pages = 25  # 每家餐厅最多取25页的评论信息
            # if total - pages * 10 > 0:
            #     pages += 1
            # logger.info("Total pages: " + str(pages))
            meta = {}
            for idx in range(pages):
                _offset = str((idx + 1) * 10)
                # response.meta["offset"] = _offset
                meta["offset"] = _offset
                meta["poiId"] = poiId
                meta["city"] = city
                meta["title"] = title
                comment_url = self.comment_url1 + poiId \
                          + self.comment_url2 + poiId \
                          + self.comment_url3 + _offset \
                          + self.comment_url4
                yield Request(url=comment_url, callback=self.parse_comment,
                              dont_filter=True, meta=meta, priority=5)
                # break

        item = Comment()
        sites = sites["data"]["comments"]
        try:
            for site in sites:
                comment = str(site["comment"]).replace("\n", "").replace(" ", "")
                star = str(site["star"])
                # logger.info(comment + "Star: " + star)
                if star != '30' and len(comment) > 0:  # 过滤评论为空或评价3星的内容
                    item["city"] = city
                    item["title"] = title
                    item["comment"] = comment
                    item["star"] = star
                    yield item
        except Exception as e:
            logger.info(e)


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl("meituan")
    process.start()
