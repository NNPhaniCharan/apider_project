from typing import Iterable

import scrapy
from scrapy import Request


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def start_requests(self):
        yield scrapy.Request(url = "https://www.audible.com/search",callback=self.parse,headers={"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})

    def parse(self, response):
        product_container = response.xpath('//div[@class="adbl-impression-container "]/div/span[2]/ul/li')

        for product in product_container:
            book_title = product.xpath('.//h3[contains(@class,"bc-heading")]/a/text()').get()
            subtitle = product.xpath('..//li[contains(@class,"subtitle")]/text()').get()
            book_author = product.xpath('..//li[contains(@class,"authorLabel")]/span/a/text()').get()
            narratorLabel = product.xpath('..//li[contains(@class,"narratorLabel")]/span/a/text()').get()
            seriesLabel = product.xpath('..//li[contains(@class,"seriesLabel")]/span/a/text()').get()
            book_length = product.xpath('..//li[contains(@class,"runtimeLabel")]/span/text()').get()
            releaseDateLabel = product.xpath('..//li[contains(@class,"releaseDateLabel")]/span/text()').get()
            languageLabel = product.xpath('..//li[contains(@class,"languageLabel")]/span/text()').get()

            yield {
                'title' : book_title,
                'author' : book_author,
                'length' : book_length,
            }

        pagination = response.xpath('//ul[contains(@class,"pagingElements")]')
        next_page_url = pagination.xpath('..//li/span[contains(@class,"nextButton")]/a/@href').get()

        if(next_page_url):
            yield response.follow(url=next_page_url,callback=self.parse, headers={"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})
