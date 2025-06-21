import scrapy
import datetime as dt
from parser import get_path

dt_now = dt.datetime.now().strftime("%Y-%m-%d")

class ReviewSpider(scrapy.Spider):
    name = "ikyuspider"

    async def start(self): # CHANGE HOTEL ID AND PAGE RANGE BEFORE USING.
        urls = [f"https://www.ikyu.com/<HOTELID>/review/p{page + 1}/" for page in range(<PAGE RANGE>)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs) -> None:
        page = response.url.split("/")[-2]
        output_dir = get_path()
        file_path = output_dir / "html"
        file_path.mkdir(exist_ok=True)
        filename = file_path / f"ikyu-review-{page}.html"
        review_block = response.text
        with open(filename, "w", encoding="utf-8") as f:
            f.write(review_block)
        self.log(f"Saved file {filename}")