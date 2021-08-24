import scrapy


class CompanyProfilesSpider(scrapy.Spider):
    name = 'company_profiles'
    allowed_domains = ['www.adapt.io']
    start_urls = ['http://www.adapt.io/']

    def parse(self, response):
        pass
