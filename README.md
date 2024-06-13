## Chinese Document PDF
该仓库主要放置自己爬取国内一些中文论文网站、证券报告的PDF。

因涉及到版权问题，我这里只放置PDF链接和对应的下载脚本，小伙伴可以自行下载。

⚠️注意：url链接中可能会存在死链，大家注意处理。

如有帮助到，请给个Star！

### PDF包含网站
#### 中文论文
|论文网站|URL条数|
|:--|:---|
|[中国图像图形学报](http://www.cjig.cn/jig/ch/reader/issue_list_click.aspx?year_id=2023&quarter_id=1)|6100|
|[计算机科学](https://www.jsjkx.com/CN/article/showOldPictureList.do?pager=1)|29614|
|[计算机系统应用](http://www.c-s-a.org.cn/csa/issue/browser)|14054|
|[软件学报](https://www.jos.org.cn/jos/issue/browser)|7576|
|[计算机研究与发展](https://crad.ict.ac.cn/archive_list.htm)|1082|

#### 证券类
- [东方财富](https://data.eastmoney.com/report/industry.jshtml?hyid=459) 2629条

#### 财报类（来自魔搭社区）
- [主板&科创板股2023财报数据pdf](https://www.modelscope.cn/datasets/baimuqier/stocks_financial_reports/files)

### 下载脚本使用
以下载**东方财富.txt**为例，其他只需做简单修改，即可使用。
```bash
$ pip install requirements.txt
$ python download_east.py
```

