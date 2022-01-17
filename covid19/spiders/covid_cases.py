import scrapy
from covid19.items import Covid19Item

class CovidCases(scrapy.Spider):
    name='covidcases'
    allowed_domains = ['covid19.who.int']
    def start_requests(self):
        urls = [
            'https://covid19.who.int/region/searo/country/np',
            
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # return super().start_requests() 
    
    def parse(self, response):
        item = Covid19Item()

        confirmedCasesAndDeaths = response.xpath('//span[@class="sc-AxhCb jXrfEx"]/text()').extract()
        CovidCasesDeaths = []
        for num in confirmedCasesAndDeaths:
            CovidCasesDeaths.append(num)

        item['confirmed_cases'] = CovidCasesDeaths[0]
        item['confirmed_deaths'] = CovidCasesDeaths[1]

        dataTableHref = response.xpath('//*[@id="gatsby-focus-wrapper"]/div/div[1]/div/div[2]/nav/ul/li[3]/a/@href').extract()
        spl = response.request.url.split('/')
        base_url = '/'.join(spl[:-5])
        data_table_url = base_url + ''.join(dataTableHref)
        if data_table_url:
            yield scrapy.Request(url=response.urljoin(data_table_url),
                callback=self.parse_data_table, 
                meta={'dataTable':item})

    def parse_data_table(self, response):
        countries = response.xpath('//div[@class="column_name td"]/div/span/text()').extract()[2:12]
        cumulative_cases = response.xpath('//div[@class="column_Cumulative_Confirmed td"]/div/div/div[1]/text()').extract()[:10]
        item = response.meta['dataTable']

        # item['country'] = countries
        # item['cumulative_cases'] = cumulative_cases
        item['countries_cumulative_cases'] = list(zip(countries,cumulative_cases))

        yield scrapy.Request(ur=response.url)
        
