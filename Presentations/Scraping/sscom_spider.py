import scrapy


class SiteSpider(scrapy.Spider):
    name = "sscom"

    start_urls = [
        'https://www.ss.com/lv/transport/cars/audi/',
    ]


    def parse(self, response):

        # save file

        page = response.url.split("/")[-2]

        filename = 'sscom-%s.html' % page

        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log('Saved file %s' % filename)

        # process the data

        #  - find the table
        rows = response.css("#filter_frm > table:nth-child(3) > tr")

        for row in rows[2:-1]:

            res = {
                "url": row.xpath('td[2]//a/@href').extract_first(),
                "text": row.xpath('td[3]//text()').extract_first(),
                "model": row.xpath('td[4]//text()').extract_first(),
                "year": row.xpath('td[5]//text()').extract_first(),
                "engine": row.xpath('td[6]//text()').extract_first(),
                "noskr": row.xpath('td[7]//text()').extract_first(),
                "price": row.xpath('td[8]//text()').extract_first(),
            }

            yield res


# row = rows[2]

# row.xpath('td//text()').extract()


