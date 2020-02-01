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
        i = 0 # for testing
        for tr in response.css('div div.container-fluid div.row main div.card div.card-body tbody tr'):
            i += 1
            if (i > 4):
                break
            nextCollege = {}
            td_list = tr.css('td')
            nameA = td_list[0].css('div.t-title div.t-title__details')
            nextCollege["name"] = nameA.css('a::text').get()
            nextCollege["r_admission"] = td_list[3].css(':not(span)::text')[1].get().strip()
            nextCollege["online_fee"] = int(td_list[5].css(':not(span)::text')[1].get().strip()[1:])
            nextCollege["essay"] = True if td_list[6].css(':not(span)::text')[1].get().strip().lower()[:3]=="yes" else False
            link = nameA.css('a::attr(href)').get()
            request = response.follow(link, callback=self.parse_document_tab,
                                      meta={"subdata": nextCollege})
            yield request


    def parse_document_tab(self, response):
        data = response.meta['subdata']
        data["website"] = response.css('html body div div main div div div div div div p a::attr(href)').get().strip('/')
        data["difficulty"] = response.css('html body div div main div div div div div div div div dl')[0].css('dd::text')[0].get()
        data["gpa"] = float(response.css('html body div div main div div div div div div div div dl')[1].css('dd::text')[0].get())
        data["room_board"] = int(response.css('html body div div main div div div div div div div div dl')[2].css('dd::text')[2].get()[1:].replace(',',''))
        data["athletics_div"] = response.css('html body div div main div div div div div div div div dl')[4].css('dd::text')[4].get()

        yield data


