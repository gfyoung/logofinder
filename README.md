[![Build Status](https://travis-ci.org/gfyoung/statWrappers.svg?branch=master)](https://travis-ci.org/gfyoung/logofinder)

[![Build status](https://ci.appveyor.com/api/projects/status/edjo1iro1numouem?svg=true)](https://ci.appveyor.com/project/gfyoung/logofinder)

# logofinder

Web scraper to find website logos.

# Usage

This script requires that you pass in a `start_url` parameter so that the script knows where to start searching, which you can pass in using the `-a` flag to `scrapy`. The command then is:
~~~python
scrapy runspider logospider.py -a start_url=https://www.google.com
~~~
