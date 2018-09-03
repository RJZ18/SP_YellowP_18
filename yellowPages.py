import scrapy

searchTerm='flower+shops&geo_location_terms=Chicago%2C+IL'

class YPSpider(scrapy.Spider):
    name = "yellowpages"
    start_urls = [
        'https://www.yellowpages.com/search?search_terms={}'.format(searchTerm)
    ]

    def parse(self, response):
        for plumber in response.css('div[class="search-results organic"] div[class="result"] div[class="v-card"] div[class="info"]'):
            yield {
                'COMPANY_NAME': plumber.css('h2[class="n"] a[class="business-name"] span::text').extract(),
		'BBB_RATING': plumber.css('div[class="info-section info-primary"] span[class="bbb-rating extra-rating"]::text').extract(),
		'STREET_ADDRESS': plumber.css('div[class="info-section info-primary"] p[class="adr"] span[class="street-address"]::text').extract(),
		'CITY': plumber.css('div[class="info-section info-primary"] p[class="adr"] span[class="locality"]::text').extract(),
		'STATE': plumber.css('div[class="info-section info-primary"] p[class="adr"] span[itemprop="addressRegion"]::text').extract(),
		'POSTAL_CODE': plumber.css('div[class="info-section info-primary"] p[class="adr"] span[itemprop="postalCode"]::text').extract(),
		'PHONE': plumber.css('div[class="info-section info-primary"] div[class="phones phone primary"]::text').extract()
            }

	
        next_page = response.css('div[class="pagination"] ul li a[class="next ajax-page"]::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

