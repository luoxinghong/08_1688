1. 功能
将关键字输入到文件的key_words列表中，即可获得1688上相关关键字的公司电话，主营产品，公司名称，联系人名字。程序通过商品id+电话号码去重。

2. 环境
Python3.6+selenium+mysql

3. 使用步骤
①安装python3.6 ，参考网址：https://blog.csdn.net/weixin_37998647/article/details/79265364

②安装程序依赖包， pip install selenium requests lxml pymysql futures

③配置selenium，参考地址：https://blog.csdn.net/weixin_40283480/article/details/80753468

④安装mysql数据库，程序默认的数据库用户为root,密码lxh123，端口3306，数据库1688，表为info4(程序运行时请自行修改为你本机的配置),参考网址：https://blog.csdn.net/wokaowokaowokao12345/article/details/76736152

⑤建表语句：
create database 1688 charset=utf8;
----------------------------------------
CREATE TABLE `info4` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `linkman` varchar(255) DEFAULT NULL,
  `tel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7355 DEFAULT CHARSET=utf8;
----------------------------------------
CREATE TABLE `total_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_num` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40298 DEFAULT CHARSET=utf8；
