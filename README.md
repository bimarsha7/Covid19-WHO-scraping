## Covid19 data scraping from "covid19.who.int"

**Scraped Data**

### A. latest number of confirmed cases and deaths for Nepal
### B. list the top 10 countries data, sorted by descending order of total cumulative cases


Page URL : 'https://covid19.who.int/region/searo/country/np'

- Run `scrapy crawl covidcases`
<!-- to save a json file: "covidcases.json" -->
- Run `scrapy crawl covidcases -o covidcases.json`

#### OUTPUT
```
{'confirmed_cases': '845,501',
 'confirmed_deaths': '11,613',
 'countries_cumulative_cases': [('United States of America', '62,973,416'),
                                ('India', '36,582,129'),
                                ('Brazil', '22,716,091'),
                                ('The United Kingdom', '14,967,821'),
                                ('France', '12,903,125'),
                                ('Russian Federation', '10,747,125'),
                                ('Turkey', '10,270,349'),
                                ('Italy', '8,155,645'),
                                ('Spain', '7,930,528'),
                                ('Germany', '7,835,451')]}
```
**Explanation**
- `confirmed_cases` : The total number of covid19 cnfirmed cases.
- `confirmed_deaths` : The total number of confirmed deaths by Covid19 in Nepal
- `countries_cumulative_cases`: Top 10 countries with their total covid 19 cases as of January 2022.

### C. Steps to extract confirmed_cases, daily increase, and daily_change % for december 01 to december 10 ,as shown by interactive graph
Page URL: 'https://covid19.who.int/region/searo/country/np'

#### STEPS of extraction
1. Check Fetch/XMLHttpRequest (XHR) section of Network section by Inspecting the browsers' page and check for data in the url: 'https://covid19.who.int/page-data/region/searo/country/np/page-data.json'

2. Check for the date range of dec 01 2021 to dec 02 2021, which was found to be in the range: 698 to 708
    `data = data['result']['pageContext']['byDay']['rows'][697:708]` 
    <!-- here 697 is taken to calcualte daily change from nov 30 to dec 01. -->
3. Iterate through `data` and get the confirmed cases:
- Calculate daily increase subtracting next value to the previos value
- Calcualte daily change by dividing the above value by next value

<!-- Run to store the data in mongodb" -->
- Run `scrapy crawl decembercases`


#### OUTPUT
**MongoDB query**
1. To create database
`use Covid`
2. To create timeseries collection
`Covid> db.createCollection("Nepal",{timeseries:{timeField:"day_timestamp", granularity:"seconds"}})`
{ ok: 1 }

3. To read the stored timeseries data
` db.Nepal.find()`
```
[
  {
    day_timestamp: ISODate("2021-12-01T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c1"),
    daily_confirmed_cases: 285,
    daily_change_percent: 16.3265306122449,
    daily_increase: 40
  },
  {
    day_timestamp: ISODate("2021-12-02T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c2"),
    daily_confirmed_cases: 298,
    daily_change_percent: 4.56140350877193,
    daily_increase: 13
  },
  {
    day_timestamp: ISODate("2021-12-03T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c3"),
    daily_confirmed_cases: 223,
    daily_change_percent: -25.16778523489933,
    daily_increase: -75
  },
  {
    day_timestamp: ISODate("2021-12-04T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c4"),
    daily_confirmed_cases: 220,
    daily_change_percent: -1.345291479820628,
    daily_increase: -3
  },
  {
    day_timestamp: ISODate("2021-12-05T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c5"),
    daily_confirmed_cases: 200,
    daily_change_percent: -9.090909090909092,
    daily_increase: -20
  },
  {
    day_timestamp: ISODate("2021-12-06T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c6"),
    daily_confirmed_cases: 238,
    daily_change_percent: 19,
    daily_increase: 38
  },
  {
    day_timestamp: ISODate("2021-12-07T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c7"),
    daily_confirmed_cases: 272,
    daily_change_percent: 14.285714285714285,
    daily_increase: 34
  },
  {
    day_timestamp: ISODate("2021-12-08T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c8"),
    daily_confirmed_cases: 255,
    daily_change_percent: -6.25,
    daily_increase: -17
  },
  {
    day_timestamp: ISODate("2021-12-09T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599c9"),
    daily_confirmed_cases: 197,
    daily_change_percent: -22.745098039215687,
    daily_increase: -58
  },
  {
    day_timestamp: ISODate("2021-12-10T05:45:00.000Z"),
    _id: ObjectId("61e50f8ff6fe24a6aa4599ca"),
    daily_confirmed_cases: 232,
    daily_change_percent: 17.766497461928935,
    daily_increase: 35
  }
]
```