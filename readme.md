## Basic Setup for Flipkart Scrapy

### Steps

- Setup a virtual environment
  > python3 -m venv venv
- activate virtual environment
  - `venv\Scripts\activate (for windows)`
  - `. venv/bin/activate (for linux)`
- Install required packages with command
  > pip install -r requirements.txt
- We need a docker for scrapy-splash to run (first install docker)
- run following docker command after finishing setting up docker (assumes it runs on 8050 port)
  > docker run -p 8050:8050 scrapinghub/splash
- Go to flipkart package
  > cd flipkart
- Run following command to scrap through flipkart and output the result in `output.json`
  > scrapy crawl flipkart -o output.json
