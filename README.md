

ScrapyBot
==========================

This is simple scrapybot to scratch out some data i need, it uses scrapy-framework.

it has a mongo backend, i write a simple & flexiable toy mongo piple. to automatically sync data to mongodb.
[scrapymongo](https://github.com/roadt/scrapymongo).

Currently 3 spiders in it. 
    
    * qidan  - famous chinese online novel site.    (status: work)
    * crunchbase -  a YP, company information site.  (status: not work now  due to site redesign)
    * manta  - small business info site (status: still draft, and need further turning) 
    


Try it
========================
	    git clone https://github.com/roadt/scrapybot
		git submodule update
		scrapy crawl qidian     # make sure your default (local) mongodb is up.
		
or scrapy to csv file

	    scrapy crawl qidian -o qidian.csv   [download example result data](./qidian.csv)





   
 Project for my personal use.
 
 MIT License.

=======
scrapybot
=========

a scrapybot  for my personal use

