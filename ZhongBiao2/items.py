# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#class Zhongbiao2Information(scrapy.Information):
    #all_list8 = scrapy.Field()

class Zhongbiao2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_name = scrapy.Field()
    b_number = scrapy.Field()
    agent = scrapy.Field()
    zb_person = scrapy.Field()
    gs_number = scrapy.Field()
    complain_government = scrapy.Field()
    f_1_person = scrapy.Field()
    f_2_person = scrapy.Field()
    f_3_person = scrapy.Field()
    f_person = scrapy.Field()
    s_1_person = scrapy.Field()
    s_2_person = scrapy.Field()
    s_3_person = scrapy.Field()
    s_person = scrapy.Field()
    t_1_person = scrapy.Field()
    t_2_person = scrapy.Field()
    t_person = scrapy.Field()
    first_p = scrapy.Field()
    second_p = scrapy.Field()
    third_p = scrapy.Field()
    third_p3 = scrapy.Field()
    can_p3 = scrapy.Field()
    first_p2 = scrapy.Field()
    second_p2 = scrapy.Field()
    third_p2 = scrapy.Field()
    n_first_p = scrapy.Field()
    n_second_p = scrapy.Field()
    n_third_p = scrapy.Field()
    n_p = scrapy.Field()
    n_money = scrapy.Field()
    correct_p = scrapy.Field()
    money_results = scrapy.Field()
    money2_results = scrapy.Field()