CREATE TABLE `info3` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `linkman` varchar(255) DEFAULT NULL,
  `tel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `total_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_num` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6210 DEFAULT CHARSET=utf8;