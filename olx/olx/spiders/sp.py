from olx.items import OlxItem
import scrapy

from bs4 import BeautifulSoup as bs
import json
import re


class SpSpider(scrapy.Spider):
	name = 'sp'
	allowed_domains = ['www.olx.ua']

	def start_requests(self):
		url = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/lugansk/?currency=USD'

		yield scrapy.Request(url=url, callback=self.get_pages)

	def get_pages(self, response):
		page_number = response.xpath('//span[@class="item fleft"][last()]/a/span/text()').get()

		for page in range(1, int(page_number) + 1):
			url = f'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/lugansk/?page={page}&currency=USD'
			yield scrapy.Request(url=url, callback=self.get_page_data)

	def get_page_data(self, response):
		data = response.xpath('//div[@class="offer-wrapper"]')
		for item in data:
			url = item.xpath('.//h3/a/@href').get()
			yield scrapy.Request(url=url, callback=self.get_item_data)

	def get_item_data(self, response):
		item = OlxItem()

		token = re.search("var phoneToken = '[a-zA-Z0-9]+", response.text).group(0)[18:]
		data = response.xpath('//ul[@id="contact_methods_below"]/li/@class').get()
		uid = None
		
		try:
			uid = data.strip('link-phone clr rel  atClickTracking contact-a activated')
			uid  = eval(uid)['id']
		except:
			item['phone_number'] = None
		else:
			url = f'https://www.olx.ua/uk/ajax/misc/contact/phone/{uid}/?pt={token}'
			yield scrapy.Request(url=url, callback=self.get_phone_numbers, cb_kwargs=dict(item_obj=item))

		item['title'] = response.xpath('//div[@class="offer-titlebox"]/h1/text()').get().strip()

		item['price'] = response.xpath('//strong[@class="pricelabel__value arranged"]/text()').get()

		item['description'] = response.xpath('//div[@class="clr lheight20 large"]/text()').get()
        
		photo_urls = []
		for i in response.xpath('//ul[@id="descGallery"]/li'):
			url = i.xpath('./a/@href').get()
			photo_urls.append(url)

		item['photo_urls'] = photo_urls

		item['user_name'] = response.xpath('//div[@class="offer-user__actions"]/h4/a/text()').get()

		item['user_url'] = response.xpath('//div[@class="offer-user__actions"]/h4/a/@href').get()

		item['address'] = response.xpath('//div[@class="offer-user__address"]/address/p/text()').get()
	
		yield item
	
	def get_phone_numbers(self, response, item_obj):
		phone_data = eval(response.text)['value']
		if 'span' in phone_data:
			soup = bs(phone_data, 'lxml')
			numbers = []
			for phone_number in soup.find_all('span'):
				if phone_number.text != '000 000 000':
					numbers.append(phone_number.text)
			item_obj['phone_number'] = numbers
		else:
			if phone_data != '000 000 000':
				item_obj['phone_number'] = phone_data

		yield item_obj