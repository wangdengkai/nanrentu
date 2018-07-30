'''
这是爬取男人图网站图片
首页
http://www.nanrentu.cc/
内地帅哥
http://www.nanrentu.cc/nd/index.html
港台帅哥
http://www.nanrentu.cc/gt/index.html
日韩帅哥
http://www.nanrentu.cc/rh/index.html
欧美帅哥
http://www.nanrentu.cc/om/index.html

每个页面中所有的明星的专题连接网址
<div class="partacpic">
    <ul>
        <li>
            <a href="/gt/ruanjjingtian">
                <img alt="阮经天">


进入明星个人页面
图片连接主页:
<div id="partac">
    <div class="partacpic">
        <ul class="P2">
            <li>
                <a href="/gt/wuzun/2268.html" title="吴尊登<芭莎男士>二月封面大片曝光">


下一页连接:获取current,标签的兄弟标签,获取兄弟的href,有就继续请求,没有就结束.
<div id="partac">
    <div class="pagelist">
        <a class="current">
        <a >



具体照片页面
<div id="parta">
    <div class="imgbox">
        <div class="picshow">
            <img src="/uploads/allinmg" alt="飞轮海>


下一页连接,选择最后一个,-1
<div id="parta">
    <div class="pagelist">
        <a href='6167_5.html>

'''
import scrapy
from nanrentu.items import  NanrentuItem


class NanRenTuspiderSpider(scrapy.Spider):
    """创建爬虫"""

    #爬虫名称
    name = "nanRen"
    #爬取区域
    allowed_domains = ['www.nanrentu.cc']
    #开始爬取路径
    start_urls =[
        'http://www.nanrentu.cc/nd/index.html',
        'http://www.nanrentu.cc/gt/index.html',
        'http://www.nanrentu.cc/rh/index.html',
        'http://www.nanrentu.cc/om/index.html'
    ]

    def parse(self,response):

        #每个页面中所有的明星的专题连接网址
        # <div class="partacpic">
        # <ul>
        # <li>
        # <a href="/gt/ruanjjingtian">
        # <img alt="阮经天">
        #获取所有明星的连接页面
        mingxing_list = response.css('.partacpic ul li a::attr(href)').extract()
        for mingxing in mingxing_list:
            yield response.follow(mingxing,callback=self.sigle_index)



    def sigle_index(self,response):
        '''
        这里处理明星个人页面
        :return:
        '''
        # 进入明星个人页面
        # 图片连接主页:
        # <div id="partac">
        # <div class="partacpic">
        # <ul class="P2">
        # <li>
        # <a href="/gt/wuzun/2268.html" title="吴尊登<芭莎男士>二月封面大片曝光">

        #获取当前页面所有明星不同类别具体图片连接
        img_list =response.css('#partac .partacpic ul[class="P2"] li a::attr(href)').extract()
        #遍历不同页面进行请求
        for img in img_list:
            #请求详情页面
            yield response.follow(img,callback=self.img_show)
        #
        # 下一页连接:获取current,标签的兄弟标签,获取兄弟的href,有就继续请求,没有就结束.
        # <div id="partac">
        # <div class="pagelist">
        # <a class="current">
        # <a >

        #获取下一页连接
        next_url = response.css('#partac .pagelist a[class="curent"]+a::attr(href)').extract_first()
        if next_url is not None:
            yield response.follow(next_url,callback=self.img_show)
    def img_show(self,response):
        '''实例化对象'''
        item  = NanrentuItem()
        #<div id="Cdh"> 您所在的位置,[港台帅哥,吴尊]
        item['folder_path'] = response.css("#Cdh a::text").extract()

        # 具体照片页面

        # <img src="/uploads/allinmg" alt="飞轮海 id='bigimg'>
        #
        item['img_url'] = response.css("#bigimg::attr(src)").extract_first()
        item['img_url'] = response.urljoin(item['img_url'])
        #
        # 下一页连接,选择最后一个,-1
        # <div id="parta">
        # <div class="pagelist">
        # <a href='6167_5.html>
        print(item['img_url'])
        print(item['folder_path'])
        yield item
        try:
            next_url = response.css("#parta .pagelist a::attr(href)").extract()[-1]
        except Exception as e:
            print(e)

        else:
            if next_url is not None:
                yield response.follow(next_url,callback=self.img_show)
                print(next_url)
