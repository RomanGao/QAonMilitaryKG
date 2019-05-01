#!/usr/bin/env python3
# coding: utf-8
# File: militarygraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 19-3-11

import os
import re
import json
import jieba
import jieba.posseg as pseg
import pymongo

class MilitaryGraph:
    def __init__(self):
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.datapath = os.path.join(cur, 'data/military.json')
        self.conn = pymongo.MongoClient()
        db_name = 'military_qa'
        col_name = 'data'
        self.col = self.conn[db_name][col_name]
        self.attributes ={'同型': ['同型'], '机高': ['机高'],
                          '战斗全重': ['战斗全重'], '水下排水量': ['水下排水量'],
                          '处理器': ['处理器'], '主炮': ['主炮'],
                          '制导系统': ['制导系统'], '全重': ['全重'],
                          '纬度': ['纬度'], '炮口初速': ['炮口初速'],
                          '发射性能': ['发射性能'], '兵装': ['兵装'],
                          '型号': ['型号'],
                          '长度': ['长度', '全长', '多长'], '翼展': ['翼展', '翼长'],
                          '全枪长': ['全枪长', '枪长'], '射程': ['射程'],
                          '前型': ['前型'],
                          '发射地点': ['发射地点', '发射地点'], '首飞时间': ['首飞时间', '首飞', '初次飞行', '首次飞行'],
                          '发动机数量': ['发动机数量', '几个发动机', '多少个发动机', '发动机个数', '发动机数目', '发动机个','发动机数'], '乘员': ['乘员'],
                          '战斗射速': ['战斗射速'], '生产单位': ['生产单位', '产商', '制造商', '厂家', '制造机构'],
                          '最大行程': ['最大行程', '最常距离'], '炮管长度': ['炮管长度', '炮管长', '炮管全长'],
                          '气动布局': ['气动布局'], '武备': ['武备'],
                          '武器装备': ['武器装备'], '引信': ['引信'],
                          '参战情况': ['参战情况'],
                          '动力装置': ['动力装置'], '飞行速度': ['飞行速度'],
                          '服役时间': ['服役时间'], '新造时': ['新造时'],
                          '活动范围': ['活动范围'], '弹匣容弹量': ['弹匣容弹量'],
                          '编制': ['编制'], '高度': ['高度'],
                          '制造厂': ['制造厂'], '口径': ['口径'],
                          '鱼雷': ['鱼雷'], '经度': ['经度'],
                          '研发时间': ['研发时间'], '简介': ['简介'],
                          '首次轨道发射': ['首次轨道发射'],
                          '挂载点': ['挂载点'], '刀锋宽度': ['刀锋宽度'],
                          '续航距离': ['续航距离'], '枪械': ['枪械'],
                          '最大速度': ['最大速度'], '运载火箭': ['运载火箭'],
                          '生产年限': ['生产年限'], '全枪重': ['全枪重'],
                          '空重': ['空重'], '水雷': ['水雷'],
                          '枪炮': ['枪炮'], '水上排水量': ['水上排水量', '排水量'],
                          '诞生时间': ['诞生时间'], '内置武器': ['内置武器'],
                          '机长': ['机长'], '中心直径': ['中心直径', '直径'],
                          '装药类型': ['装药类型'], '最大起飞重量': ['最大起飞重量', '起飞重量'],
                          '有效射程': ['有效射程'], '现状': ['现状'],
                          '研制时间': ['研制时间'], '舰舰导弹': ['舰舰导弹'],
                          '下水时间': ['下水时间', '下水'], '机炮': ['机炮'],
                          '弹长': ['弹长'], '退役时间': ['退役时间', '退役'],
                          '最大射程': ['最大射程'], '改装时': ['改装时'],
                          '刀重': ['刀重'], '自持力': ['自持力'],
                          '产国': ['产国'], '航速': ['航速'],
                          '制造商': ['制造商'], '型宽': ['型宽'],
                          '弹重': ['弹重'], '刀长': ['刀长'],
                          '舰长': ['舰长'], '研发厂商': ['研发厂商'],
                          '旋翼直径': ['旋翼直径'], '导弹': ['导弹'],
                          '满排吨位': ['满排吨位'], '底盘类型': ['底盘类型'],
                          '刀锋长度': ['刀锋长度'], '弹径': ['弹径'],
                          '全长': ['全长'], '竣工时': ['竣工时'],
                          '发射日期': ['发射日期'], '宽度': ['宽度'],
                          '总重': ['总重'], '建造时间': ['建造时间'],
                          '射控装置': ['射控装置'], '图片': ['图片'],
                          '轨道': ['轨道'], '改装前': ['改装前'],
                          '发动机': ['发动机'], '最大航程': ['最大航程'],
                          '研发单位': ['研发单位'], '大类': ['大类'],
                          '关注度': ['关注度'], '最大飞行速度': ['最大飞行速度'],
                          '火炮': ['火炮'], '战地机型': ['战地机型'],
                          '防空兵器': ['防空兵器'], '潜航深度': ['潜航深度'],
                          '轨道卫星': ['轨道卫星'], '尾翼装置': ['尾翼装置'],
                          '乘员与载员': ['乘员与载员'], '名称': ['名称'],
                          '引信装置': ['引信装置'], '次型': ['次型'],
                          '车长': ['车长'], '武装': ['武装'],"航长":['航长'],
                          '反舰导弹': ['反舰导弹'],
                          '满载排水量': ['满载排水量'], '装备': ['装备']}

        self.big_cates ={'火炮': ['火炮'], '飞行器': ['飞行器'],
                         '舰船舰艇': ['舰船舰艇'], '坦克装甲车辆': ['坦克装甲车辆'],
                         '太空装备': ['太空装备'], '爆炸物': ['爆炸物'],
                         '导弹武器': ['导弹武器'], '枪械与单兵': ['枪械与单兵', '枪械', '枪', '单兵']}
        self.second_cates = {'榴弹发射器': ['榴弹发射器'], '炸弹': ['炸弹', '炸药'],
                             '手榴弹': ['手榴弹'], '电子战机': ['电子战机'],
                             '机枪': ['机枪'], '宇宙飞船': ['宇宙飞船', '飞船'],
                             '加农炮': ['加农炮'], '救护车': ['救护车'],
                             '攻击机': ['攻击机'], '非自动步枪': ['非自动步枪', '步枪'],
                             '火箭弹': ['火箭弹'], '地雷': ['地雷'],
                             '高射炮': ['高射炮'], '航天飞机': ['航天飞机'],
                             '航天机构': ['航天机构', '航天局', '航天部门'], '舰舰导弹': ['舰舰导弹'],
                             '通用飞机': ['通用飞机'], '岸舰导弹': ['岸舰导弹', '导弹'],
                             '舰炮': ['舰炮'], '巡洋舰': ['巡洋舰'],
                             '气垫艇/气垫船': ['气垫艇/气垫船','气垫艇','气垫船'], '装甲指挥车': ['装甲指挥车', '装甲车', '指挥车'],
                             '无人机': ['无人机'], '氢弹': ['氢弹'],
                             '坦克炮': ['坦克炮'], '干线': ['干线'],
                             '原子弹': ['原子弹'], '冲锋枪': ['冲锋枪'],
                             '导弹艇': ['导弹艇'], '水雷战舰艇': ['水雷战舰艇'],
                             '侦察机': ['侦察机'], '试验机': ['试验机'],
                             '舰地（潜地）导弹': ['舰地（潜地）导弹','舰地导弹','潜地导弹', '导弹'],
                             '支线': ['支线'], '军事卫星': ['军事卫星'],
                             '地空导弹': ['地空导弹'], '航空炮': ['航空炮'],
                             '战列舰': ['战列舰'], '无后坐炮': ['无后坐炮'],
                             '空地导弹': ['空地导弹'], '加农榴弹炮': ['加农榴弹炮'],
                             '运输机': ['运输机'], '自行火炮': ['自行火炮'],
                             '地地导弹': ['地地导弹'], '空舰导弹': ['空舰导弹'],
                             '教练机': ['教练机'], '其他特种装甲车辆': ['其他特种装甲车辆'],
                             '火箭筒': ['火箭筒'], '空间探测器': ['空间探测器', '探测器'],
                             '预警机': ['预警机'], '航空母舰': ['航空母舰', '航母'],
                             '迷彩服': ['迷彩服'],'弹炮结合系统': ['弹炮结合系统'],
                             '科学卫星': ['科学卫星'], '空空导弹': ['空空导弹','导弹'],
                             '迫击炮': ['迫击炮'],
                             '应用卫星': ['应用卫星', '卫星'], '保障辅助舰艇': ['保障辅助舰艇'],
                             '刀具': ['刀具'], '霰弹枪': ['霰弹枪'],
                             '自动步枪': ['自动步枪'], '手枪': ['手枪'],
                             '反弹道导弹': ['反弹道导弹'], '两栖作战舰艇': ['两栖作战舰艇'],
                             '特种坦克': ['特种坦克', '坦克'], '运输直升机': ['运输直升机', '直升机'],
                             '巡逻舰/艇': ['巡逻舰/艇', '巡逻舰', '巡逻舰艇', '巡逻舰艇'], '加油机': ['加油机'],
                             '反坦克炮': ['反坦克炮'],
                             '越野车': ['越野车'], '步兵战车': ['步兵战车'],
                             '战斗机': ['战斗机'], '护卫舰': ['护卫舰'],
                             '工程抢修车': ['工程抢修车'],'反潜机': ['反潜机'],
                             '常规潜艇': ['常规潜艇'], '装甲侦察车': ['装甲侦察车'],
                             '舰空导弹': ['舰空导弹'], '运载火箭': ['运载火箭'],
                             '中子弹': ['中子弹'], '飞艇': ['飞艇'],
                             '航天基地': ['航天基地'], '鱼雷': ['鱼雷'],
                             '轰炸机': ['轰炸机'], '技术试验卫星': ['技术试验卫星', '卫星'],
                             '狙击枪': ['狙击枪'], '水雷': ['水雷'],
                             '装甲车载炮': ['装甲车载炮'], '榴弹炮': ['榴弹炮'],
                             '驱逐舰': ['驱逐舰'], '装甲运兵车': ['装甲运兵车'],
                             '火箭炮': ['火箭炮'], '多用途直升机': ['多用途直升机', '直升机'],
                             '核潜艇': ['核潜艇'], '武装直升机': ['武装直升机', '直升机'],
                             '布/扫雷车': ['布/扫雷车', '扫雷车', '扫雷车'], '潜舰导弹': ['潜舰导弹', '导弹'],
                             '主战坦克': ['主战坦克', '坦克']}
        self.weapons = self.load_weapons()
        self.weapon_dict = {i:i for i in self.weapons}
        self.countries = {'荷兰': ['荷兰'], '阿根廷': ['阿根廷'], '瑞士': ['瑞士'],
                          '伊朗': ['伊朗'], '以色列': ['以色列'], '前南斯拉夫': ['前南斯拉夫'],
                          '越南': ['越南'], '葡萄牙': ['葡萄牙'], '乌克兰': ['乌克兰'],
                          '新西兰': ['新西兰'], '奥地利': ['奥地利'], '希腊': ['希腊'],
                          '塞尔维亚': ['塞尔维亚'], '比利时': ['比利时'],
                          '俄罗斯': ['俄罗斯'], '前捷克斯洛伐克': ['前捷克斯洛伐克'],
                          '捷克': ['捷克'], '土耳其': ['土耳其'], '缅甸': ['缅甸'],
                          '美国': ['美国'], '德国': ['德国'], '巴西': ['巴西'],
                          '印度尼西亚': ['印度尼西亚'], '法国': ['法国'],
                          '瑞典': ['瑞典'], '前苏联': ['前苏联'],
                          '朝鲜': ['朝鲜'],
                          '埃及': ['埃及'], '墨西哥': ['墨西哥'], '巴基斯坦': ['巴基斯坦'],
                          '马来西亚': ['马来西亚'], '澳大利亚': ['澳大利亚'], '泰国': ['泰国'],
                          '欧盟': ['欧盟'], '波兰': ['波兰'],
                          '韩国': ['韩国'], '日本': ['日本'],
                          '罗马尼亚': ['罗马尼亚'], '克罗地亚': ['克罗地亚'], '智利': ['智利'],
                          '匈牙利': ['匈牙利'], '意大利': ['意大利'], '英国': ['英国'],
                          '丹麦': ['丹麦'], '挪威': ['挪威'], '哈萨克斯坦': ['哈萨克斯坦'],
                          '爱尔兰': ['爱尔兰'], '伊拉克': ['伊拉克'],
                          '中国': ['中国','中华人民共和国'], '印度': ['印度'],
                          '保加利亚': ['保加利亚'], '斯洛伐克': ['斯洛伐克'],
                          '西班牙': ['西班牙'], '秘鲁': ['秘鲁'],
                          '阿联酋': ['阿联酋'], '卢森堡': ['卢森堡'],
                          '巴拿马': ['巴拿马'], '新加坡': ['新加坡'],
                          '波黑': ['波黑'], '南非': ['南非'],
                          '苏/俄': ['苏/俄', '苏联', '俄罗斯'], '加拿大': ['加拿大'], '芬兰': ['芬兰']}

        self.compares = {
                            '$gt': ['高于','大于','长于','高过','大过','长过','多于', '远于', '远过', '之后', '晚于', '后于'],
                            '$lt': ['低于', '小于', '短于', '低过', '短过', '少于', '近于', '近过', '未达到', '没达到', '之前', '先于', '早于'],
                            '$lte': ['不高于','不大于','不长于','不高过','不大过','不长过','不多于', '不远于', '不远过'],
                            '$gte': ['不低于', '不小于', '不短于', '不低过', '不短过', '不少于', '不近于', '不近过', '达到'],
                            '$eq': ['等于', '差不多'],
                            '$ne': ['不等于', '不是']}
        self.counts = ['多少', '几', '几多']
        self.mosts = {
                          -1:['最大', '最远', '最长', '最高', '最久', '最快', '最多', '最强'],
                          1:['最小', '最短', '最近', '最低', '最矮', '最慢', '最少', '最弱'],
                     }

        self.unit_dict = {
            '海里': [1852, '米'],
            '英里': [1610, '米'],
            '/节': [1852, '米'],
            'km/节': [1000, '米'],
            '吨': [1000, '千克'],
            '-吨': [1000, '千克'],
            '公里': [1000, '米'],
            '公里/节': [1000, '米'],
            '公里/小时': [1000, '米'],
            '海里节': [1852, '米'],
            '海里，节': [1852, '米'],
            '海里/节': [1852, '米'],
            '海哩/节': [1852, '米'],
            '海浬/节': [1852, '米'],
            '毫米': [0.001, '米'],
            '节': [1852, '米'],
            '节/海里': [1852, '米'],
            '节海里': [1852, '米'],
            '节行驶英里': [1852, '米'],
            '节下海里': [1852, '米'],
            '克': [0.001, '千克'],
            '里': [1852, '米'],
            '里/节': [1852, '米'],
            '米': [1, '米'],
            '千克': [1, '克'],
            '千米': [1000, '米'],
            '千米/节': [1000, '米'],
            '千米/时': [1000, '米'],
            '千米/小时': [1000, '米'],
            '千米每小时': [1000, '米'],
            '万海里/节': [18520000, '米'],
            '英里，节': [1610, '米'],
            '英里/节': [1610, '米'],
            '余英里': [1610, '米'],
            '约海里': [1852, '米'],
            '最大海里': [1852, '米'],
            '厘米': [0.01, '米'],
            '分米': [0.1, '米'],
            '人': [1, '人'],
            '位': [1, '位']}

        unit_dict = {i:len(i) for i in self.unit_dict}
        unit_wds = [i[0] for i in sorted(unit_dict.items(), key = lambda asd: asd[1], reverse=True)]
        unit_regex = '([0-9]+.?[0-9]+)(%s)+' % '|'.join(unit_wds)
        time_regex = '[0-9]{4}年[0-9]{0,4}月?[0-9]{0,4}日?'
        self.unit_pattern = re.compile(unit_regex)
        self.time_pattern = re.compile(time_regex)
        self.country_dict = self.build_dict(self.countries)
        self.big_dict = self.build_dict(self.big_cates)
        self.small_dict = self.build_dict(self.second_cates)
        self.attribute_dict = self.build_dict(self.attributes)
        self.compare_dict = self.build_dict(self.compares)
        self.most_dict = self.build_dict(self.mosts)
        self.add_jieba(self.country_dict, 'n_country')
        self.add_jieba(self.big_dict, 'n_big')
        self.add_jieba(self.small_dict, 'n_small')
        self.add_jieba(self.attribute_dict, 'n_attr')
        self.add_jieba(self.compare_dict, 'n_compare')
        self.add_jieba(self.most_dict, 'n_most')
        self.add_jieba(self.weapons, 'n_weapon')

        return

    '''加载武器实体'''
    def load_weapons(self):
        weapons = []
        for record in open(self.datapath):
            data = json.loads(record)
            weapons.append(data['名称'])
        return list(set(weapons))

    '''构造映射字典'''
    def build_dict(self, dict):
        wd_dict = {}
        for cate, wds in dict.items():
            for wd in wds:
                wd_dict[wd] = cate
        return wd_dict

    '''检测单位'''
    def detect_entity(self, question):
        units = [i[0] + i[1] for i in self.unit_pattern.findall(question) if i]
        times = self.time_pattern.findall(question)
        return times, units

    '''检查年份并统一时间'''
    def standard_year(self, sent):
        sent = sent.replace(' ', '')
        pattern_year = re.compile('[0-9]{4}年')
        pattern_month = re.compile('[0-9]{1,4}月')
        pattern_day = re.compile('[0-9]{1,4}日')
        default_day = ''
        default_month = ''
        month = pattern_month.findall(sent)
        day = pattern_day.findall(sent)
        year = pattern_year.findall(sent)
        if year:
            year = year[0].replace('年', '')
            if month:
                default_month = month[0].replace('月', '')
            if day:
                default_day = day[0].replace('日', '')
            if year:
                date_new = year + self.full_date(default_month) + self.full_date(default_day)
            else:
                date_new = ''
        else:
            return ''
        return date_new

    '''补全日期'''
    def full_date(self, date):
        if not date:
            date = '01'
        if int(date) < 10 and len(date) < 2:
            date = '0' + date
        return date

    '检测是否有数字'
    def check_num(self, sent):
        pattern = re.compile('\d+')
        res = pattern.findall(str(sent))
        return res[0]

    '''检查单位并统一数量'''
    def standard_unit(self, unit_value):
        num = self.check_num(unit_value)
        unit = unit_value.replace(num, '')
        unit_info = self.unit_dict.get(unit, [1, 'default'])
        plus = unit_info[0]
        num_standrd = float(num) * plus
        return num_standrd

    '''将实体标记和实体词加入到jieba当中'''
    def add_jieba(self, wds, tag):
        for wd in wds:
            jieba.add_word(wd, tag=tag, freq=300000)
        return

    '''问句解析'''
    def question_parser(self, question):
        times, units = self.detect_entity(question)
        self.add_jieba(times, 'n_time')
        self.add_jieba(units, 'n_unit')
        wds = [(i.word, i.flag) for i in pseg.cut(question)]
        parser_dict = {}
        parser_dict['n_attrs'] = [wd for wd,flag in wds if flag == 'n_attr']
        parser_dict['n_times'] = [wd for wd,flag in wds if flag == 'n_time']
        parser_dict['n_bigs'] = [wd for wd,flag in wds if flag == 'n_big']
        parser_dict['n_smalls'] = [wd for wd,flag in wds if flag == 'n_small']
        parser_dict['n_countries'] = [wd for wd,flag in wds if flag == 'n_country']
        parser_dict['n_compares'] = [wd for wd,flag in wds if flag == 'n_compare']
        parser_dict['n_mosts'] = [wd for wd,flag in wds if flag == 'n_most']
        parser_dict['n_units'] = [wd for wd,flag in wds if flag == 'n_unit']
        parser_dict['n_weapons'] = [wd for wd,flag in wds if flag == 'n_weapon']
        parser_dict['pattern'] = [flag for wd, flag in wds if flag in ['n_attr', 'n_time', 'n_big', 'n_small', 'n_unit', 'n_country', 'n_compare', 'n_most', 'n_weapon']]
        # parser_dict['wds'] = wds
        return parser_dict

    '''答案搜索'''
    def search_answer(self, parser_dict):
        print('step1:问句解析 >>', parser_dict)
        pattern = parser_dict['pattern']
        print('step2:查询模板 >>',pattern)
        search_data = []
        condition = {}
        targets = ['名称']
        search_flag = 1

        if pattern in [['n_country', 'n_small'], ['n_small', 'n_country']]:
            country = self.country_dict.get(parser_dict.get('n_countries')[0])
            n_small = self.small_dict.get(parser_dict.get('n_smalls')[0])
            condition = {'产国': country, '类型':n_small}
            targets = ['名称']
            search_data.append({'condition':condition, 'targets':targets})

        elif pattern in [['n_country', 'n_big'], ['n_big', 'n_country']]:
            country = self.country_dict.get(parser_dict.get('n_countries')[0])
            n_big = self.big_dict.get(parser_dict.get('n_bigs')[0])
            condition = {'产国': country, '类型': n_big}
            targets = ['名称']
            search_data.append({'condition': condition, 'targets': targets})

        elif pattern in [['n_country', 'n_weapon'], ['n_weapon']]:
            n_weapon = self.weapon_dict.get(parser_dict.get('n_weapons')[0])
            condition = {'名称': n_weapon}
            targets = ['简介']
            search_data.append({'condition': condition, 'targets': targets})

        # 单实体多属性查询
        elif pattern in [['n_country', 'n_weapon'],
                         ['n_weapon', 'n_attr'],
                         ['n_weapon', 'n_attr', 'n_attr'],
                         ['n_weapon', 'n_attr', 'n_attr', 'n_attr'],
                         ['n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
                         ['n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
                         ['n_country', 'n_weapon', 'n_attr'],
                         ['n_country', 'n_weapon', 'n_attr', 'n_attr'],
                         ['n_country', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
                         ['n_country', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
                         ['n_country', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr']
                         ]:
            n_weapon = self.weapon_dict.get(parser_dict.get('n_weapons')[0])
            condition = {'名称': n_weapon}
            targets = [self.attribute_dict.get(attr) for attr in parser_dict.get('n_attrs')]
            search_data.append({'condition': condition, 'targets': targets})

        # 多实体多属性查询
        elif pattern in [
            ['n_weapon', 'n_weapon', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_weapon','n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr', 'n_attr'],
            ]:
            n_weapons = [self.weapon_dict.get(weapon) for weapon in parser_dict.get('n_weapons')]
            condition = {'名称': {"$in": n_weapons}}
            targets = [self.attribute_dict.get(attr) for attr in parser_dict.get('n_attrs')]
            search_data.append({'condition': condition, 'targets': targets})

        # 实体、实体属性相间隔
        elif pattern in [
            ['n_weapon', 'n_attr','n_weapon', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_weapon', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_country','n_weapon', 'n_attr'],
            ['n_weapon', 'n_attr', 'n_attr', 'n_weapon', 'n_attr'],
            ['n_weapon', 'n_attr', 'n_attr', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_attr', 'n_weapon', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_country',' n_weapon', 'n_attr', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_attr', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_country', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_country', 'n_weapon', 'n_attr', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_attr', 'n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_country','n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ['n_country','n_weapon', 'n_attr', 'n_attr', 'n_attr', 'n_country','n_weapon', 'n_attr', 'n_attr', 'n_attr'],
            ]:
            n_indxes = [indx for indx, name in enumerate(pattern) if name == 'n_weapon']
            n_weapons = [self.weapon_dict.get(weapon) for weapon in parser_dict.get('n_weapons')]
            n1_weapon = n_weapons[0]
            n2_weapon = n_weapons[1]
            targets1 = [self.attribute_dict.get(weapon) for indx, weapon in enumerate(parser_dict.get('n_attrs')) if indx < n_indxes[1]-1]
            targets2 = [self.attribute_dict.get(weapon) for indx, weapon in enumerate(parser_dict.get('n_attrs')) if indx >= n_indxes[1]-1]
            condition1 = {'名称': n1_weapon}
            condition2 = {'名称': n2_weapon}
            search_data.append({'condition':condition1, 'targets': targets1})
            search_data.append({'condition':condition2, 'targets': targets2})

        # 比较查找，单操作符+操作数的实体
        elif pattern in [
                        ['n_attr', 'n_compare', 'n_unit', 'n_small'],
                        ['n_small', 'n_attr', 'n_compare', 'n_unit'],
                        ['n_attr', 'n_compare', 'n_time', 'n_small'],
                        ['n_attr', 'n_time', 'n_compare',  'n_small'],
                        ['n_small', 'n_attr', 'n_compare', 'n_time'],
                        ['n_small', 'n_attr', 'n_time', 'n_compare'],
                        ['n_attr', 'n_compare', 'n_unit', 'n_big'],
                        ['n_big', 'n_attr', 'n_compare', 'n_unit'],
                        ['n_attr', 'n_compare', 'n_time', 'n_big'],
                        ['n_attr', 'n_time', 'n_compare', 'n_big'],
                        ['n_big', 'n_attr', 'n_compare', 'n_time'],
                        ['n_big', 'n_attr', 'n_time', 'n_compare'],
                        ]:

            n_attr = self.attribute_dict.get(parser_dict.get('n_attrs')[0])
            n_compare = self.compare_dict.get(parser_dict.get('n_compares')[0])

            if 'n_unit' in pattern:
                n_unit = self.standard_unit(parser_dict.get('n_units')[0])
                if 'n_small' in pattern:
                    n_small = self.small_dict.get(parser_dict.get('n_smalls')[0])
                    condition = {n_attr:{n_compare:n_unit}, '类型':n_small}
                else:
                    n_big = self.big_dict.get(parser_dict.get('n_bigs')[0])
                    condition = {n_attr:{n_compare:n_unit}, '大类':n_big}
            else:
                n_time = self.standard_year(parser_dict.get('n_times')[0])
                if 'n_small' in pattern:
                    n_small = self.small_dict.get(parser_dict.get('n_smalls')[0])
                    condition = {n_attr: {n_compare: n_time}, '类型': n_small}
                else:
                    n_big = self.big_dict.get(parser_dict.get('n_bigs')[0])
                    condition = {n_attr: {n_compare: n_time}, '大类': n_big}

            targets = [n_attr]
            search_data.append({'condition':condition, 'targets':targets})

        # 比较查找，双操作符+操作数的实体
        elif pattern in [
            ['n_attr', 'n_compare', 'n_unit', 'n_compare', 'n_unit', 'n_small'],
            ['n_small', 'n_attr', 'n_compare', 'n_unit', 'n_compare', 'n_unit'],
            ['n_attr', 'n_compare', 'n_time', 'n_compare', 'n_time', 'n_small'],
            ['n_attr', 'n_time', 'n_compare', 'n_time', 'n_compare',  'n_small'],
            ['n_small', 'n_attr', 'n_compare', 'n_time', 'n_compare', 'n_time'],
            ['n_small', 'n_attr', 'n_time', 'n_compare', 'n_time', 'n_compare'],
            ['n_attr', 'n_compare', 'n_unit', 'n_compare', 'n_unit', 'n_big'],
            ['n_big', 'n_attr', 'n_compare', 'n_unit', 'n_compare', 'n_unit'],
            ['n_attr', 'n_compare', 'n_time', 'n_compare', 'n_time', 'n_big'],
            ['n_attr', 'n_time', 'n_compare', 'n_time', 'n_compare', 'n_big'],
            ['n_big', 'n_attr', 'n_compare', 'n_time', 'n_compare', 'n_time'],
            ['n_big', 'n_attr', 'n_time', 'n_compare', 'n_time', 'n_compare'],
            ]:
            n_attr = self.attribute_dict.get(parser_dict.get('n_attrs')[0])
            n_compares = [self.compare_dict.get(compare) for compare in parser_dict.get('n_compares')]

            if 'n_unit' in pattern:
                n_units = [self.standard_unit(unit) for unit in parser_dict.get('n_units')]
                if 'n_small' in pattern:
                    n_small = self.small_dict.get(parser_dict.get('n_smalls')[0])
                    condition = {n_attr:{n_compares[0]:n_units[0], n_compares[1]:n_units[1]}, '类型':n_small}
                else:
                    n_big = self.big_dict.get(parser_dict.get('n_bigs')[0])
                    condition = {n_attr:{n_compares[0]:n_units[0], n_compares[1]:n_units[1]},'大类':n_big}
            else:
                n_times = [self.standard_year(year) for year in parser_dict.get('n_times')]
                if 'n_small' in pattern:
                    n_small = self.small_dict.get(parser_dict.get('n_smalls')[0])
                    condition = {n_attr:{n_compares[0]:n_times[0], n_compares[1]:n_times[1]}, '类型': n_small}
                else:
                    n_big = self.big_dict.get(parser_dict.get('n_bigs')[0])
                    condition = {n_attr:{n_compares[0]:n_times[0], n_compares[1]:n_times[1]}, '大类': n_big}
            targets = [n_attr]
            search_data.append({'condition':condition, 'targets':targets})

        # 属性最值查找
        elif pattern in [['n_small', 'n_attr', 'n_most'],
                         ['n_attr', 'n_most', 'n_small'],
                         ['n_big', 'n_attr', 'n_most'],
                         ['n_attr', 'n_most', 'n_big'],
                        ]:
            search_flag = 0
            n_attr = self.attribute_dict.get(parser_dict.get('n_attrs')[0])
            n_most = self.most_dict.get(parser_dict.get('n_mosts')[0])
            if 'n_small' in pattern:
                n_small = self.small_dict.get(parser_dict.get('n_smalls')[0])
                condition = {'类型': n_small, 'sort_key':{n_attr: n_most}}
            else:
                n_big = self.big_dict.get(parser_dict.get('n_bigs')[0])
                condition = {'大类': n_big, 'sort_key': {n_attr: n_most}}
            targets.append(n_attr)
            search_data.append({'condition':condition, 'targets':targets})

        result = self.query_mongo(search_flag, search_data)
        return result

    '''查询mongo数据库'''
    def query_mongo(self, search_flag, search_data):
        result = []
        if search_flag:
            result = self.query_mongo_attr(search_data)
        else:
            result = self.query_mongo_sort(search_data)
        return result

    '''查询mongo数据库，正常'''
    def query_mongo_attr(self, search_data):
        result = []
        for search in search_data:
            condition = search['condition']
            targets = search['targets']
            for res in self.col.find(condition):
                result.append([res.get('名称') + target + ':' + str(res.get(target,'null')) for target in targets if res.get(target, 'null') != 'null'])
        return result

    '''按照最值方法查找mongo数据库'''
    def query_mongo_sort(self, search_data):
        result = []
        for search in search_data:
            condition = {key:value for key, value in search['condition'].items() if key != 'sort_key'}
            sort_condition = [(i,j) for i, j in search['condition'].get('sort_key').items()]
            targets = search['targets']
            for res in self.col.find(condition).sort(sort_condition).limit(1):
                result_ = [res.get('名称') + target + ':' + str(res.get(target, 'null')) for target in targets]
                result.append(result_)
        return result

    '问答主函数'
    def qa_main(self, question):
        parser_dict = self.question_parser(question)
        results = self.search_answer(parser_dict)
        if results == [[]]:
            print('小勇：对不起，目前暂时还无法回答此类问题...')
        else:
            print('小勇：共找到%s个答案， 下面是具体明细：'% len(results))
            for result in results:
                print(result)
        return

if __name__ == '__main__':
    handler = MilitaryGraph()
    while 1:
        question = input("用户：").strip()
        handler.qa_main(question)