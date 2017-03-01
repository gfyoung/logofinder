# logofinder

Web scraper to find website logos.

# Usage

This script requires that you pass in a `start_url` parameter so that the script knows where to start searching, which you can pass in using the `-a` flag to `scrapy`. The command then is:
~~~python
scrapy runspider logospider.py --loglevel=WARNING -a start_url=https://www.google.com
~~~
