import scrapy


class CompanyIndexSpider(scrapy.Spider):
    name = 'company_index'
    allowed_domains = ['www.adapt.io']
    start_urls = [
        'http://www.adapt.io/directory/industry/telecommunications/A-1/']

    def parse(self, response):

        urls = response.xpath(
            '//div[@class="DirectoryTopInfo_alphabetLinkListWrapper__4a1SM"]//a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_following_urls)

    def parse_following_urls(self, response):

        print("procesing:"+response.url)
        name = response.xpath(
            '//div[@class="DirectoryList_seoDirectoryList__aMaj8"]//a/text()').extract()

        urls = response.xpath(
            '//div[@class="DirectoryList_seoDirectoryList__aMaj8"]//a/@href').extract()

        data = zip(name, urls)
        for item in data:
            dict = {
                'record_type': 'company_index',
                'company_name': item[0],
                'source_url': item[1],
            }
            yield dict
        for url in urls:
            yield scrapy.Request(url, callback=self.company_profiles)

        next_page = response.xpath(
            '//div[@class="DirectoryList_actionBtnLink__Seqhh undefined"]/a/@href').get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse_following_urls)

    def company_profiles(self, response):
        Company_name = response.xpath(
            '//div[@class="CompanyTopInfo_leftContentWrap__3gIch"]/h1/text()').extract()

        Company_location = []
        addrl = str(response.xpath(
            '//span[@itemprop="addressLocality"]/text()').extract_first())
        addrR = str(response.xpath(
            '//span[@itemprop="addressRegion"]/text()').extract_first())
        addrC = str(response.xpath(
            '//span[@itemprop="addressCountry"]/text()').extract_first())
        location = addrl+", "+addrR+", "+addrC
        if location:
            Company_location.append(location)
        else:
            Company_location.append("Not Available")

        Company_website = []
        Company_website.append(response.xpath(
            '//div[@class="CompanyTopInfo_websiteUrl__13kpn"]/text()').extract())
        if not Company_website:
            Company_website.append("Not Available")

        Company_webdomain = []
        webdomain = str(response.xpath(
            '//div[@class="CompanyTopInfo_websiteUrl__13kpn"]/text()').extract())[13:]
        if webdomain:
            Company_webdomain.append(webdomain)
        else:
            Company_webdomain.append("Not Available")

        Company_industry = []
        Company_industry.append(response.xpath(
            '//div[@class="CompanyTopInfo_contentWrapper__2Jkic"]/span[contains(string(),"Industry")]/following-sibling::span/text()').extract())
        if not Company_industry: 
            Company_industry.append("Not Available")

        Company_employee_size = []
        Company_employee_size.append(response.xpath(
            '//div[@class="CompanyTopInfo_contentWrapper__2Jkic"]/span[contains(string(),"Head Count")]/following-sibling::span/text()').extract())
        if not Company_employee_size:
            Company_employee_size.append("Not Available")

        Company_revenue = []
        Company_revenue.append(response.xpath(
            '//div[@class="CompanyTopInfo_contentWrapper__2Jkic"]/span[contains(string(),"Head Count")]/following-sibling::span/text()').extract())
        if not Company_revenue:
            Company_revenue.append("Not Available")

        Contact_name = response.xpath(
            '//div[@class="TopContacts_contactName__3N-_e"]/a/text()').extract()
        
        Contact_jobtitle = []
        for i in range(len(Contact_name)):
            jobtitle = response.xpath(
                '//p[@class="TopContacts_jobTitle__3M7A2"]/text()').extract()
            if jobtitle:
                Contact_jobtitle.append(jobtitle)
            else:
                Contact_jobtitle.append("Not Available")

        Contact_email_domain = []
        for i in range(len(Contact_name)):
            domain = (str(response.xpath(
                '//button[@class="simpleButton mailPhoneBtn emailBtn"]/text()').extract()[i]))
            if domain:
                Contact_email_domain.append(domain[domain.index('@')+1:])
            else:
                Contact_email_domain.append("Not Available")

        Contact_detail = []
        if Contact_name:
            for i in range(len(Contact_name)):
                Contact_detail.append({'Contact_name': Contact_name[i],
                                    'Contact_jobtitle': Contact_jobtitle[i],
                                    'Contact_email_domain': Contact_email_domain[i]})
            Contact_details = [Contact_detail]
        else:
            Contact_details = ["None"]

        data = zip(Company_name, Company_location, Company_website, Company_webdomain, Company_industry,
                   Company_employee_size, Company_revenue, Contact_details)

        for item in data:
            dict = {
                'record_type': 'company_profiles',
                'company_name': item[0],
                'company_location': item[1],
                'company_website': item[2],
                'company_webdomain': item[3],
                'company_industry': item[4],
                'company_employee_size': item[5],
                'company_revenue': item[6],
                'contact_details': item[7]
            }
            yield dict
