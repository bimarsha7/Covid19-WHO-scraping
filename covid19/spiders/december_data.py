import scrapy
from covid19.items import DecemberCases
import json

class DecemberCovidCases(scrapy.Spider):
    name='decembercases'
    allowed_domains = ['covid19.who.int']
    headers = {
        # "Accept": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        # "cache-control": "no-cache",
        # "cookie":" _ga=GA1.2.945375872.1642095141; _gid=GA1.2.1804903097.1642095141; __cfruid=7a9d984579a4b418cecd5b98248a576bc998d4ff-1642178923; _gcl_au=1.1.1902551285.1642178927; _gat_gtag_UA_162461105_1=1",
        # "dnt": "1",
        # "pragma": "no-cache",
        "Referer": "https://covid19.who.int/region/searo/country/np",
        # "sec-ch-ua": " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97",
        # sec-ch-ua-mobile: ?0
        "Sec-ch-ua-platform": "Linux",
        "Sec-fetch-dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    # 'https://covid19.who.int/page-data/index/page-data.json',
    def start_requests(self):
        start_url = [
            'https://covid19.who.int/page-data/region/searo/country/np/page-data.json',
        ]
        
        for url in start_url:
            yield scrapy.Request(url=url,
                callback=self.parse_api,
                headers= self.headers
                )

    def parse_api(self,response):
        item = DecemberCases()
        
        data =response.json()
        daily_data = data['result']['pageContext']['byDay']['rows'][697:708]
        # metrics = data['result']['pageContext']['byDay']['metrics']
        
        confirmed = []
        dec_day = []
        for day in daily_data:
            dec_day.append(day[0]) #get the timestamp of days dec 01 to dec 10
            confirmed.append(day[7]) #get the daily confirmed cases 
        #convert to daily confirmed tuples
        daily_confirmed_tup = list(zip(confirmed[1:],confirmed))

        daily_increase = [(x-y) for x,y in daily_confirmed_tup]
        daily_change = [((x-y)/y)*100 for x,y in daily_confirmed_tup]

        # remove extra zeros in the timestamp data,get only first 10 numbers
        days_tmstmp = [str(tstp)[:10] for tstp in dec_day[1:]] #take from index 1, as index 0 contain November 30
        
        item['day_timestamp'] = days_tmstmp
        item['daily_confirmed_cases'] = confirmed[1:] #skip Nov 30s' daily cases
        item['daily_increase'] = daily_increase
        item['daily_change_percent'] = daily_change
        
        yield item
        

