#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: main.py
@time: 2018/12/26 10:46
@desc:
'''
from B1688 import work

# key_words = ["男装", "内衣", "鞋靴", "箱包", "配饰", "运动服饰", "运动装备", "母婴用品", "童装", "玩具", "工艺品", "宠物", "园艺", "日用百货", "办公文教",
#              "汽车用品", "食品饮料", "餐饮生鲜", "家纺家饰", "家装建材", "美容化妆", "个护家清", "3C", "手机", "家电", "电工电气", "照明", "仪表", "包装", "印刷纸业",
#              "电子元器件", "安防", "机械", "五金工具", "劳保", "橡塑", "化工", "精细", "钢材", "纺织皮革", "医药"]

key_words = ["内衣", "鞋靴", "箱包", "配饰", "运动服饰", "运动装备", "母婴用品", "童装", "玩具", "工艺品", "宠物", "园艺", "日用百货", "办公文教",
             "汽车用品", "食品饮料", "餐饮生鲜", "家纺家饰", "家装建材", "美容化妆", "个护家清", "3C", "手机", "家电", "电工电气", "照明", "仪表", "包装", "印刷纸业",
             "电子元器件", "安防", "机械", "五金工具", "劳保", "橡塑", "化工", "精细", "钢材", "纺织皮革", "医药"]

ck_str = '''cookie2=12e42c7acea3f6a9dc99196e75eaab0e; t=4e5e8eb5ddb96d721f1c8a0a6047681f; _tb_token_=e85f1baa7b1d0; cna=RRWrFE1VY2ICAdJT8LK+G/QT; cookie1=AC4JGfV6412EKKqXctv7GhoV%2BDDdWRPx3V%2FvbLO9vgU%3D; cookie17=VAmjhVgdqG8v; sg=67d; csg=bf42735f; lid=lxh767166726; unb=789408507; __cn_logon__=true; __cn_logon_id__=lxh767166726; ali_apache_track=c_mid=b2b-789408507|c_lid=lxh767166726|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; _nk_=lxh767166726; last_mid=b2b-789408507; _csrf_token=1545873330549; JSESSIONID=3EF763AD7648D225D1A4AA733C4BE0DD; _is_show_loginId_change_block_=b2b-789408507_false; _show_force_unbind_div_=b2b-789408507_false; _show_sys_unbind_div_=b2b-789408507_false; _show_user_unbind_div_=b2b-789408507_false; __rn_alert__=false; alicnweb=show_inter_tips%3Dfalse; l=aB7tJqX0yiQSyVCm2Ma5QMQuQ702id5PV_WF1MwkVTEhNR0mPEEDp0nbA_wwMfNFgrF_S002ecSw.; isg=BGRk3S_P5PPd0xA_CTNEjEuSNWKWVdnuDjxNb36FeS_tKQXzpgxq97RL7cCU8cC_'''

for n, kw in enumerate(key_words):
    work(3, kw, ck_str)
