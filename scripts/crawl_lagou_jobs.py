import scrapy

class JobsSpider(scrapy.Spider):
    
    name = 'jobs'

    start_urls = ['https://www.lagou.com/']

    def parse(self, response):
        for job in response.xpath('//li[contains(@class,"position_list_item")]'):
            yield {
                'name': job.css('a.position_link::text').extract_first().strip(),
                'salary_min': job.css('span.salary::text').re_first('(\d+)K-.*'),
                'salary_max': job.css('span.salary::text').re_first('.*-(\d+)K'),
                'location':job.css('div.industry').xpath('.//span[3]/text()').extract_first().strip(),
                'tags':','.join(job.css('div.labels div.pli_btm_l span::text').extract()),
                'experience_requirement':job.css('div.position_main_info').xpath('.//span[1]/text()').re_first('(\d+-\d+)'),          
                'degree_requirement':job.css('div.position_main_info').xpath('.//span[2]/text()').extract_first(),
            }