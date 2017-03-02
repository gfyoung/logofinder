# logofinder

Web scraper to find website logos.

# Usage

This script requires that you pass in a `start_url` parameter so that the script knows where to start searching, which you can pass in using the `-a` flag to `scrapy`. The command then is:
~~~python
scrapy runspider logospider.py --loglevel=WARNING -a start_url=https://www.google.com
~~~

# How it Works

The script collects all image links (those with the `<a href>` tag) along with their corresponding image data from the website.
Afterwards, we pass all of the images through `tensorflow` to get an approximate identification of each image. Then, combining
these identifications along with keywords scraped from the website (e.g. from `<meta>` tags), we can then determine which image, if any, could be a logo for the website.
