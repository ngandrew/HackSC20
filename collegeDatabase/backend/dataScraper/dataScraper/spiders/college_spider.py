import scrapy


class CollegeSpider(scrapy.Spider):
    name = "colleges"

    def start_requests(self):
        urls = [
            "https://www.collegedata.com/en/prepare-and-apply/common-application-guide/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        objects = []
        for td in response.css('div div.container-fluid div main div div tbody tr td'):
            nextCollege = {}
            nameA = td.css('div.t-title div.t-title__details')
            nextCollege["name"] = nameA.css('a::text').get()
            nextCollege["link"] = nameA.css('a::attr(href)').get()
            objects.append(nextCollege)
        yield {'colleges': objects}
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
