# -*- coding: utf-8 -*-
import scrapy

from ..items import MovieItem

class FilmSpider(scrapy.Spider):
    name = 'film'
    allowed_domains = ['www.dygang.net']
    start_urls = ['http://www.dygang.net/ys/index.htm']+['http://www.dygang.net/ys/index_%d.htm'%(i) for i in range(1,10)]

    def parse(self, response):
        tables = response.xpath('//a[@class="classlinkclass"]')
        for table in tables:
            item = MovieItem()
            movie_name = table.xpath('./text()').extract_first()
            jump_href = table.xpath('./@href').extract_first()
            item['movie_name'] = movie_name
            #电影详情页
            movie_det_url = jump_href

            yield scrapy.Request(url=movie_det_url, callback=self.parse_movie_detail,meta={'key':item})

    def parse_movie_detail(self,response):
        item = response.meta['key']

        #详情页数据
        movie_pic = response.xpath('//img[@width="120"][@height="150"]/@src').extract_first()
        movie_intract = response.xpath('//td[@id="dede_content"]/p[4]/text()').extract_first()
        movie_download_url=response.xpath('//td[@bgcolor="#ffffbb"]//a/@href').extract()[1]
        if not movie_intract:
            movie_intract = '暂无简介'
        if not movie_download_url:
            movie_download_url = '暂无下载地址'
        item['movie_pic'] = movie_pic
        item['movie_intract'] = movie_intract
        item['movie_download_url'] = movie_download_url
        yield item