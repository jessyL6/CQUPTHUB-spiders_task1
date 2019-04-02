# -*- coding: utf-8 -*-
import scrapy
import json
import urllib2
import re
from scrapy.http import Request
from ZhongBiao2.items import Zhongbiao2Item
#from ZhongBiao2.items import Zhongbiao2Information
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Zhongbiao2Spider(scrapy.Spider):
    name = 'zhongbiao2'
    #allowed_domains = ['www.cqggzy.com']
    begin_URL = "https://www.cqggzy.com/web/services/PortalsWebservice/getInfoList?response=application/json&pageIndex="
    mid_url = 1
    end_URL = "&pageSize=18&siteguid=d7878853-1c74-4913-ab15-1d72b70ff5e7&categorynum=005002&title=&infoC=&_=1549819578722"   
    start_urls = [begin_URL + str(mid_url) + end_URL]
    num = 1

    def parse(self, response):
        i=1
        for i in range(0,872):
            yield scrapy.Request(url=self.begin_URL + str(i) + self.end_URL,callback=self.page_in)

    def page_in(self,response):
        #print response.body 
        content = response.body
        
        time = re.compile(r'infodate\\":\\"(.*?)\\')
        time_results = re.findall(time,content)
        '''print(time_results)
        for time_result in time_results:
            print time_result'''

        title = re.compile(r'title\\":\\"(.*?)\\')
        title_results = re.findall(title,content)
        '''print(title_results)
        for title_result in title_results:
            print title_result'''

        location = re.compile(r'infoC\\":\\"(.*?)\\')
        location_results = re.findall(location,content)
        '''print(location_results)
        for location_result in location_results:
            print location_result'''

        half_complex_tweb = re.compile(r'005002001\\(.*?)\\')
        half_complex_tweb_results = re.findall(half_complex_tweb,content)
        '''print(half_complex_tweb_results)
        for half_complex_tweb_result in half_complex_tweb_results:
            print half_complex_tweb_result'''

        half_complex_endweb = re.compile(r'005002001\\.*?\\(.*?)\\"')
        half_complex_endweb_results = re.findall(half_complex_endweb,content)
        '''print(half_complex_endweb_results)
        for half_complex_endweb_result in half_complex_endweb_results:
            print half_complex_endweb_result'''

        
        base_URL = "https://www.cqggzy.com/jyjg/005002/005002001"
        task_1 = [str(q) for q in half_complex_tweb_results]
        for k in range(0,len(half_complex_tweb_results)):
            task_1[k] = 'date: ' + time_results[k] + ' ; ' + 'title: ' + title_results[k] + ' ; ' + 'location: ' + location_results[k] + ' ; ' + 'web: ' + base_URL + half_complex_tweb_results[k] + half_complex_endweb_results[k] + '\n'
            #print(task_1[k])
        #with open('/home/jessyl/ZhongBiao2/第一部分爬取内容.txt','a') as f1:
         #   f1.writelines(task_1)

        for j in range(0,len(half_complex_tweb_results)):
            finall_in_url =base_URL + half_complex_tweb_results[j] + half_complex_endweb_results[j]
            #print finall_in_url
            yield Request(url=finall_in_url,callback=self.next)

    def next(self,response):
        content2 = response.body
        html = etree.HTML(response.text)
        all_list=html.xpath('//tbody//text()')
        #print(all_list)
        #print(type(all_list))
 
        all_list = [''.join(x.split()) for x in all_list]
        all_list2 = [str(i) for i in all_list]
        all_list3 = ''.join(all_list2)

        #way1:
        #all_list4 = all_list3.replace("\n      ","")
        #all_list5 = all_list4.replace(" ","")
        #'\n      '; str=....    ; str.replace("\n      ","")
        #all_list6 = all_list5.replace("\n\n","")
        #all_list7 = all_list6.replace("\r","")
        #all_list8 = all_list7.replace("\n\n\n","")
        #test1 = re.sub('\n\n','\n',all_list8)
        #print(test1)
        #test = test1.split(" ")
        #print(test)

        #way2:
        all_list4 = re.sub('\n      ','',all_list3)
        all_list5 = re.sub('\r','',all_list4)
        all_list6 = re.sub('\n\n','',all_list5)
        all_list7 = re.sub('\n\n\n','',all_list6)
        all_list8 = re.sub('\n','',all_list7)
        all_list9 = re.sub('\\\\',' ',all_list8)

        #information = Zhongbiao2Information()
        #information['all_list8'] = all_list8 + '\n'

        print(all_list8)
        test = all_list9.split(" ")
        print('\n')
        #print(test)
        #print response.body

        print (str(self.num))

        item = Zhongbiao2Item()

        project_name = re.compile(r'项目名称(.*?)招')
        if re.findall(project_name,all_list9) !=[]:
            project_name_results = re.findall(project_name,all_list9)[0]
        else:
            project_name_results = ""
        project_name_result = '项目名称: ' + project_name_results
        item['p_name'] = project_name_result + '\n'
        print(project_name_result)

        project_zhaobiao_number = re.compile(r'招标公告编号(.*?)招+')
        if re.findall(project_zhaobiao_number,all_list9) !=[]:
            project_zhaobiao_number_results = re.findall(project_zhaobiao_number,all_list9)[0]
        else:
            project_zhaobiao_number_results = ""
        project_zhaobiao_number_result = '招标公告编号: ' + project_zhaobiao_number_results
        item['b_number'] = project_zhaobiao_number_result + '\n'
        print(project_zhaobiao_number_result)

        project_zhaobiao_agent = re.compile(r'招标代理机构(.*?)公司')
        if re.findall(project_zhaobiao_agent,all_list9) !=[]:
            project_zhaobiao_agent_results = re.findall(project_zhaobiao_agent,all_list9)[0]
        else:
            project_zhaobiao_agent_results = ""
        project_zhaobiao_agent_result = '招标代理机构: ' + project_zhaobiao_agent_results + '公司'
        item['agent'] = project_zhaobiao_agent_result + '\n'
        print(project_zhaobiao_agent_result)

        project_zhaobiao_person = re.compile(r'招标人(.*?)联系电话')
        if re.findall(project_zhaobiao_person,all_list9) !=[]:
            project_zhaobiao_person_results = re.findall(project_zhaobiao_person,all_list9)[0]
        else:
            project_zhaobiao_person_results = ""
        project_zhaobiao_person_result = '招标人 ' + project_zhaobiao_person_results
        item['zb_person'] = project_zhaobiao_person_result + '\n'
        print(project_zhaobiao_person_result)

        project_sign_in_num = re.compile(r'工商注册号(.*?)组织机构代码')
        if re.findall(project_sign_in_num,all_list9) !=[]:
            project_sign_in_num_results = re.findall(project_sign_in_num,all_list9)[0]
        else:
            project_sign_in_num_results = ""
        project_sign_in_num_result = '工商注册号 :' + project_sign_in_num_results
        item['gs_number'] = project_sign_in_num_result + '\n'
        print(project_sign_in_num_result)

        complain_government = re.compile(r'投诉受理部门(.*?)联系电话')
        if re.findall(complain_government,all_list9) !=[]:
            complain_government_results = re.findall(complain_government,all_list9)[0]
        else:
            complain_government_results = ""
        complain_government_result = '投诉受理部门 :' + complain_government_results
        item['complain_government'] = complain_government_result + '\n'
        print(complain_government_result)

        if '一标段' in all_list9:
            first_1 = re.compile(r'一标段第一中标候选人(.*?)第二中标候选人')
            first_1_results = re.findall(first_1,all_list9)[0]
            first_1_result = '一标段第一中标候选人: ' + first_1_results
            item['f_1_person'] = first_1_result + '\n'
            print(first_1_result)

            first_2 = re.compile(r'一标段.*?第二中标候选人(.*?)第三中标候选人')
            first_2_results = re.findall(first_2,all_list9)[0]
            first_2_result = '一标段第二中标候选人: ' + first_2_results
            item['f_2_person'] = first_2_result + '\n'
            print(first_2_result)

            first_3 = re.compile(r'一标段.*?第三中标候选人(.*?)拟中标人')
            first_3_results = re.findall(first_3,all_list9)[0]
            first_3_result = '一标段第三中标候选人: ' + first_3_results
            item['f_3_person'] = first_3_result + '\n'
            print(first_3_result)

            first = re.compile(r'一标段.*?拟中标人(.*?)工商注册号')
            first_results = re.findall(first,all_list9)[0]
            first_result = '一标段拟中标候选人: ' + first_results
            item['f_person'] = first_result + '\n'
            print(first_result)
        if '二标段' in all_list9:
            second_1 = re.compile(r'二标段第一中标候选人(.*?)第二中标候选人')
            second_1_results = re.findall(second_1,all_list9)[0]
            second_1_result = '二标段第一中标候选人: ' + second_1_results
            item['s_1_person'] = second_1_result + '\n'
            print(second_1_result)

            second_2 = re.compile(r'二标段.*?第二中标候选人(.*?)第三中标候选人')
            second_2_results = re.findall(second_2,all_list9)[0]
            second_2_result = '二标段第一中标候选人: ' + second_2_results
            item['s_2_person'] = second_2_result + '\n'
            print(second_2_result)

            second_3 = re.compile(r'二标段.*?第三中标候选人(.*?)拟中标人')
            second_3_results = re.findall(second_3,all_list9)[0]
            second_3_result = '二标段第二中标候选人: ' + second_3_results
            item['s_3_person'] = second_3_result + '\n'
            print(second_3_result)

            second = re.compile(r'二标段.*?拟中标人(.*?)工商注册号')
            second_results = re.findall(second,all_list9)[0]
            second_result = '二标段第三中标候选人: ' + second_results
            item['s_person'] = second_result + '\n'
            print(second_result)

        if '三标段' in all_list9:
            third_1 = re.compile(r'三标段第一中标候选人(.*?)第二中标候选人')
            third_1_results = re.findall(third_1,all_list9)[0]
            third_1_result = '三标段第一中标候选人: ' + third_1_results
            item['t_1_person'] = third_1_result + '\n'
            print(third_1_result)

            third_2 = re.compile(r'三标段.*?第二中标候选人(.*?)第三中标候选人')
            third_2_results = re.findall(third_2,all_list9)[0]
            third_2_result = '三标段第二中标候选人: ' + third_2_results
            item['t_2_person'] = third_2_result + '\n'
            print(third_2_result)

            third_3 = re.compile(r'三标段.*?第三中标候选人(.*?)拟中标人')
            third_3_results = re.findall(third_3,all_list9)[0]
            third_3_result = '三标段第三中标候选人: ' + third_3_results
            item['t_3_person'] = third_3_result + '\n'
            print(third_3_result)

            third = re.compile(r'三标段.*?拟中标人(.*?)工商注册号')
            third_results = re.findall(third,all_list9)[0]
            third_result = '三标段拟中标候选人: ' + third_results
            item['t_person'] = third_result + '\n'
            print(third_result)

        first_person = re.compile(r'第一中.*?选人(.*?)第二')
        if re.findall(first_person,all_list9) !=[]:
            first_person_results = re.findall(first_person,all_list9)[0]
            first_person_result = '第一中标候选人 (+ 中标金额) :' + first_person_results 
        else:
            first_person_result = ""
        item['first_p'] = first_person_result + '\n'
        print(first_person_result)
       
        second_person = re.compile(r'第二中.*?选人(.*?)第三')
        if re.findall(second_person,all_list9) !=[]:
            second_person_results = re.findall(second_person,all_list9)[0]
            second_person_result = '第二中标候选人 (+ 中标金额):' + second_person_results 
        else:
            second_person_result = ""
        item['second_p'] = second_person_result + '\n'
        print(second_person_result)
       
        third_person = re.compile(r'第三中.*?选人(.*?)中标人')
        if re.findall(third_person,all_list9) !=[]:
            third_person_results = re.findall(third_person,all_list9)[0]
            third_person_result = '第三中标候选人 (+ 中标金额):' + third_person_results 
        else:
            third_person_result = ""
        if '拟' in third_person_result:
            third_person_result = re.sub('拟','',third_person_result)
        item['third_p'] = third_person_result + '\n'
        print(third_person_result)

        third_person3 = re.compile(r'第三中标（选）候选人(.*?)中标（选）人')
        if re.findall(third_person3,all_list9) !=[]:
            third_person_results3 = re.findall(third_person3,all_list9)[0]
            third_person_result3 = '第三中标候选人 (+ 中标金额):' + third_person_results3 
        else:
            third_person_result3 = ""
        item['third_p3'] = third_person_result3 + '\n'
        print(third_person_result3)
      
        can_person = re.compile(r'公司中标（选）人(.*?)中标价说明')
        if re.findall(can_person,all_list9) !=[]:
            can_person_results3 = re.findall(can_person,all_list9)[0]
            can_person_result3 = '中标（选）人 (+ 中标（选）价):' + can_person_results3 
        else:
            can_person_result3 = ""
        item['can_p3'] = can_person_result3 + '\n'
        print(can_person_result3)
  
        first_person2 = re.compile(r'中标候选人.*?1~3.*?1(.*?)2')
        if re.findall(first_person2,all_list9) !=[]:
            first_person_results2 = re.findall(first_person2,all_list9)[0]
            first_person_result2 = '第一中标候选人 (+ 中标金额) :' + first_person_results2 
        else:
            first_person_result2 = ""
        item['first_p2'] = first_person_result2 + '\n'
        print(first_person_result2)

        second_person2 = re.compile(r'中标候选人.*?1~3.*?(.*?)3')
        if re.findall(second_person2,all_list9) !=[]:
            second_person_results2 = re.findall(second_person2,all_list9)[0]
            second_person_result2 = '第二中标候选人 (+ 中标金额):' + second_person_results2 
        else:
            second_person_result2 = ""
        item['second_p2'] = second_person_result2 + '\n'
        print(second_person_result2)

        third_person2 = re.compile(r'中标候选人.*?1~3.*?3(.*?)公司')
        if re.findall(third_person2,all_list9) !=[]:
            third_person_results2 = re.findall(third_person2,all_list9)[0]
            third_person_result2 = '第三中标候选人 (+ 中标金额):' + third_person_results2 
        else:
            third_person_result2 = ''
        item['third_p2'] = third_person_result2 + '\n'
        print(third_person_result2)

        first_temp_person = re.compile(r'第一拟中标人(.*?)第二拟中标人')
        if re.findall(first_temp_person,all_list9) !=[]:
            first_temp_person_results = re.findall(first_temp_person,all_list9)[0]
            first_temp_person_result = '第一拟中标人 :' + first_temp_person_results
        else:
            first_temp_person_result = ""
        item['n_first_p'] = first_temp_person_result + '\n'
        print(first_temp_person_result) 
  
        second_temp_person = re.compile(r'第二拟中标人(.*?)第三拟中标人')
        if re.findall(second_temp_person,all_list9) !=[]:
            second_temp_person_results = re.findall(second_temp_person,all_list9)[0]
            second_temp_person_result = '第二拟中标人 :' + second_temp_person_results
        else:
            second_temp_person_result = ""
        item['n_second_p'] = second_temp_person_result + '\n'
        print(second_temp_person_result)

        third_temp_person = re.compile(r'第三拟中标人(.*?)拟中标人')
        if re.findall(third_temp_person,all_list9) !=[]:
            third_temp_person_results = re.findall(third_temp_person,all_list9)[0]
            third_temp_person_result = '第三拟中标人 :' + third_temp_person_results
        else:
            third_temp_person_result = ""
        item['n_third_p'] = third_temp_person_result + '\n'
        print(third_temp_person_result)

        temp_person = re.compile(r'拟中标人(.*?)中标')
        if re.findall(temp_person,all_list9) !=[]:
            temp_person_results = re.findall(temp_person,all_list9)[0]
        else:
            temp_person_results = ""
        temp_person_result = '拟中标人 :' + temp_person_results
        item['n_p'] = temp_person_result + '\n'
        print(temp_person_result)

        n_money = re.compile(r'拟中标人.*?中标金额(.*?)工商注册号')
        if re.findall(n_money,all_list9) !=[]:
            n_money_results = re.findall(n_money,all_list9)[0]  
        else:
            n_money_results = ""
        n_money_result = '拟中标金额 :' + n_money_results
        item['n_money'] = n_money_result + '\n'
        print(n_money_result)

        correct_person = re.compile(r'中标人(.*?)公司')
        if re.findall(correct_person,all_list9) !=[]:
            correct_person_result = re.findall(correct_person,all_list9)[0]
        else:
            correct_person_result = ""
        correct_person_results = '中标人 :' + correct_person_result +'公司'
        if correct_person_results == temp_person_result:
            correct_person_results = "" 
        item['correct_p'] = correct_person_results + '\n'
        print(correct_person_results)

        money = re.compile(r'中标价(.*?)年')
        if re.findall(money,all_list9) !=[]:
            money_result = re.findall(money,all_list9)[0] 
        else:
            money_result = ""
        money_results = '中标价 :' + money_result
        if money_results == n_money_result:
            money_results = ""
        item['money_results'] = money_results + '\n'
        print(money_results)

        money2 = re.compile(r'中标金额(.*?)工商注册号')
        if re.findall(money2,all_list9) !=[]:
            money2_result = re.findall(money2,all_list9)[0] 
        else:
            money2_result = ""
        money2_results = '中标价 :' + money2_result
        if money2_results == n_money_result:
            money2_results = ""
        item['money2_results'] = money2_results + '\n'
        print(money2_results)

        self.num += 1

        yield item