对人民网领导留言板2023.5-2023.11的数据进行爬虫和文本分析，数据量为39万条（时间有限，全部爬取的话为200万条左右）。
爬虫解决的问题有：
1. 网不好时抓取内容为空的程序稳定性处理；
2. 访问次数太多后被网站限制访问的处理；
3. 只有一页没有下一页的页面的处理；
4. 对无回复留言的处理；
5. 对于不存在的fid的页面处理（这使得不用整理页面fid，确定最小值fid和最大值fid后即可进行爬取）；
6. 对没有在日期范围内的留言的页面处理；
7. 对无留言页面的处理。
Note:该数据无法使用接口爬取，因为网页在每条留言详情页面的接口链接上加了一个随机“signature”作为反爬虫。文本分析使用“cntext”库使用不同情感词典

Crawler and text analysis was carried out on the data of the leadership message board 2023.5-2023.11 of the People's Daily Online, and the amount of data was 390,000 pieces (limited time, about 2 million pieces if all crawled). The problems that crawlers solve are:
1. When the network is not good, grab the content of the empty program stability processing;
2. The processing of access restricted by the website after too many visits;
3. Processing of pages with only one page and no next page;
4. Handling of no reply messages;
5. Page processing for non-existent Fids (this makes it possible to crawl after determining the minimum and maximum Fids without collating the page Fids);
6. Page processing for messages that are not within the date range;
7. Handling of pages without messages. Note: This data cannot be crawled using the interface because the page adds a random "signature" to the interface link of each message detail page as an anti-crawler. Text analysis uses the "cntext" library using different sentiment dictionaries
