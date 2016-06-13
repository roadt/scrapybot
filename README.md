

ScrapyBot
==========================

This is simple scrapybot to scratch out some data i need, it uses scrapy-framework.

it has a mongo backend, i write a simple & flexiable toy mongo piple. to automatically sync data to mongodb.
[scrapymongo](https://github.com/roadt/scrapymongo).

Current  spiders in it. 
    
    * qidan  - famous chinese online novel site.
	* pptv - chinese online video site
	* deviantart -  art/pictures sharing site
	* freelancer.com - a popular freelancer site
	* proxylist(plist) -   freeproxylists.net 
    * crunchbase -  a YP, company information site.  ( not work now  due to site redesign)
    * manta  - small business info site. (site is not reachable now)

	* cache - a web crawler for cache whole site with externdable filter method 


and a simple flask webapp to visulize scraped data  for
	
	* qidan



Try it
========================
	    git clone https://github.com/roadt/scrapybot
		git submodule update
		scrapy crawl qidian     # make sure your default (local) mongodb is up.
		
or scrapy to csv file

	    scrapy crawl qidian -o qidian.csv   [download example result data](./qidian.csv)

start flask app
	  $ web/qidian/app.sh


More examples:

	# cache whole dmoz site (restrict link resolution among dmoz.org site)
	scrapy crawl cache  -a url=http://www.dmoz.org -a regex=dmoz.org
	
	# scrap a dev art (pic or file)
	scrapy crawl devart -a url=http://xxx.deviantart.com/art/YYYY
		
 
 MIT License.
=======


