# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
from scrapy.http import Request
from articleSpider.items import ArticleItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css('#archive > div.floated-thumb > div.post-thumb > a')

        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={'front_image': parse.urljoin(response.url, image_url)},
                          callback=self.parse_detail)
        next_url = response.css('#archive > div.navigation.margin-20 > a.next.page-numbers::attr(href)').extract_first(
            '')

        if next_url:
            yield Request(url=next_url, callback=self.parse)

    @staticmethod
    def parse_detail(response):
        article_item = ArticleItem()

        title = response.css('div.entry-header > h1::text').extract_first('')
        create_date = response.css('div.entry-meta > p::text').extract_first('').strip().replace(
            ' ·', '')
        front_image = response.meta.get('front_image', '')

        article_item['title'] = title
        article_item['create_date'] = create_date
        article_item['front_image'] = [front_image]
        yield article_item
