import scrapy


class CollegeSpider(scrapy.Spider):
    name = "colleges"

    def try_cast(self, val, t):
        try:
            return t(val), True
        except:
            return None, False

    def start_requests(self):
        urls = [
            "https://www.collegedata.com/en/prepare-and-apply/common-application-guide/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        objects = []
        # i = 0 # for testing
        for tr in response.css('div div.container-fluid div.row main div.card div.card-body tbody tr'):
            # i += 1
            # if (i > 4):
            #     break
            nextCollege = {}
            td_list = tr.css('td')
            nameA = td_list[0].css('div.t-title div.t-title__details')
            nextCollege["name"] = nameA.css('a::text').get()
            nextCollege["r_admission"] = td_list[3].css(':not(span)::text')[1].get().strip()
            nextCollege["online_fee"], _ = self.try_cast(td_list[5].css(':not(span)::text')[1].get().strip()[1:], int)
            nextCollege["essay"] = True if td_list[6].css(':not(span)::text')[1].get().strip().lower()[:3]=="yes" else False
            link = nameA.css('a::attr(href)').get()
            request = response.follow(link, callback=self.parse_overview,
                                      meta={"subdata": nextCollege})
            yield request
            # req2 = response.follow(link+'?tab=profile-students-tab', callback=self.parse_students,
            #                           meta={"subdata": nextCollege})
            # yield req2


    def parse_overview(self, response):
        data = response.meta['subdata']
        data["website"] = ''.join(response.css('html body div div main div div div div div div p')[1].css('*::text').getall()).strip().strip("Website:").strip().strip("/")
        # response.css('html body div div main div div div div div div p')[1].css('*::text')[1].get().strip().strip("Website:").strip().strip("/")
        data["difficulty"] = response.css('html body div div main div div div div div div div div dl')[0].css('dd::text')[0].get()
        data["gpa"], _ = self.try_cast(response.css('html body div div main div div div div div div div div dl')[1].css('dd::text')[0].get(), float)
        data["room_board"], _ = self.try_cast(response.css('html body div div main div div div div div div div div dl')[2].css('dd::text')[2].get()[1:].replace(',',''), int)
        data["athletics_div"] = response.css('html body div div main div div div div div div div div dl')[4].css('dd::text')[4].get()
        # yield data
        req2 = response.follow(response.url+'?tab=profile-students-tab', callback=self.parse_students,
                                  meta={"subdata": data})
        yield req2

    def parse_students(self, response):
        data = response.meta['subdata']
        data["grad_within"] = {}
        four = response.css('main div div.container-fluid div.row div div div div div dl')[-2].css('dd::text')[1].get().strip()[:-1]
        try:
            data["grad_within"]["4years_grate"] = float(four)
        except ValueError:
            data["grad_within"]["4years_grate"] = None
        five = response.css('main div div.container-fluid div.row div div div div div dl')[-2].css('dd::text')[2].get().strip()[:-1]
        data["grad_within"]["5years_grate"], _ = self.try_cast(five, float)
        # try:
        #     data["grad_within"]["5years_grate"] = float(five)
        # except ValueError:
        #     data["grad_within"]["5years_grate"] = None
        six = response.css('main div div.container-fluid div.row div div div div div dl')[-2].css('dd::text')[3].get().strip()[:-1]
        try:
            data["grad_within"]["6years_grate"] = float(six)
        except ValueError:
            data["grad_within"]["6years_grate"] = None
        yield data


