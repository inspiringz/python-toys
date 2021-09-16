# -*- coding: utf8 -*-
# https://github.com/inspiringz/python-toys
import os
import xlrd
import datetime
from xlutils.copy import copy
from bs4 import BeautifulSoup


class Vuln:
    def __init__(self):
        self.ip = '' # IP 地址
        self.port = '' # 端口
        self.name = '' # 漏洞名称
        self.risk = '' # 风险等级
        self.detail = '' # 漏洞描述
        self.firm = '' # 加固建议
        self.cve = '' # CVE 编号
        self.result = '' # 扫描返回信息
        self.discom = '' # 发现方式
        self.discot = '' # 发现时间

    def list(self):
        return [self.ip, self.port, self.name, self.risk, self.detail,
        self.firm, self.cve, self.result, self.discom, self.discot]

def cellv_filter(cell_value):
    if type(cell_value) == float: # port
        cell_value = str(int(cell_value))
    if len(cell_value) >= 3 and cell_value[0] == '[' and cell_value [-1] == ']': # risk
        cell_value = cell_value[1:-1]
    if cell_value.endswith('危险'):
        cell_value = cell_value.replace('危险', '')
    if '】' in cell_value:
        cell_value = cell_value.split('】')[1]
    cell_value = cell_value.replace('\n\n', '\n')
    return cell_value

def vuln_filter(vuln):
    if '低' in vuln.risk or '信息' in vuln.risk:
        return False
    if vuln.name.strip() == '':
        return False
    for rvnk in vuln_name_filter:
        if rvnk.lower() in vuln.name.lower():
            return False
    for rvdk in vuln_detail_filter:
        if rvdk.lower() in vuln.detail.lower():
            return False
    return True

ip_count = 0
vuln_result = []
report_dir='./扫描报告'
fmt_path = './问题汇总模板.xls'


vuln_name_filter = ['ddos', '洪泛', 'flood', '溢出', '缓冲区错误漏洞', '请求响应', \
        '拒绝服务', '访问控制错误', '原理扫描', 'timestamp', 'traceroute', '支持的算法', 'ssh版本信息', \
        'www服务信息', 'rpcbind/portmap', 'ntp服务', 'python', '没有正确返回', '输入验证错误', '版本泄漏', \
        '版本信息', 'MySQL 安全漏洞', 'MySQL Server 安全漏洞',   'MariaDB 组件安全漏洞', ]

vuln_detail_filter = ['dos', '拒绝服务']

def nsfocus_clean(report_dir='./扫描报告/绿盟'):
    global vuln_result
    global ip_count
    global vuln_name_filter
    global vuln_detail_filter

    col_idx = {
        'port': 0,
        'name': 3,
        'risk': 5,
        'detail': 17,
        'firm': 18,
        'cve': 13,
        'result': 19,
        'discot': 12,
    }

    for root, dirs, files in os.walk(report_dir, topdown=False):
        for fn in files:
            if fn.startswith('~') or fn.startswith("index") \
                or not fn.endswith('.xls'):
                continue

            ip_count += 1
            fp = os.path.join(root, fn)
            workbook = xlrd.open_workbook_xls(fp, formatting_info=True)
            cur_worksheet = workbook.sheet_by_name("远程漏洞")

            print(f'[*] -> {fp}')

            for row in range(4, cur_worksheet.nrows):

                v = Vuln()
                v.ip = fn.split('.xls')[0]
                v.discom = '绿盟漏扫器'

                for item in list(v.__dict__.keys()):
                    if item == 'ip' or item == 'discom':
                        continue
                    
                    cellv = cur_worksheet.cell_value(row, col_idx[item])

                    if item == 'discot':
                        cellv = str(datetime.datetime(*xlrd.xldate_as_tuple(cellv, workbook.datemode))).split(' ')[0]

                    v.__dict__[item] = cellv_filter(cellv)

                if vuln_filter(v):
                    vuln_result.append(v)

def venustech_clean(report_dir='./扫描报告/启明'):
    global vuln_result
    global ip_count
    global vuln_name_filter
    global vuln_detail_filter

    tab_map = {
        'name': (1, 0),
        'risk': (4, 1),
        'cve': (8, 1),
        'detail': (13, 1),
        'firm': (14, 1),
    }

    for root, dirs, files in os.walk(report_dir, topdown=False):
        for fn in files:
            if fn.startswith('Report') or not fn.endswith('_main.html'):
                continue
            
            ip_count += 1
            fp = os.path.join(root, fn)
            html_doc = open(fp, 'r').read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            tables = soup.find_all("table", {"class": "VPropTable"})

            print(f'[*] -> {fp}')

            for table in tables:
                v = Vuln()
                v.ip = fn.split('_main.html')[0]
                v.discom = '启明星辰漏扫'

                trs = table.findAll('tr')
                for key in tab_map.keys():
                    locx, locy = tab_map[key]
                    tds = trs[locx].findAll('td')
                    val = tds[locy].getText().strip()
                    v.__dict__[key] = cellv_filter(val)

                if vuln_filter(v):
                    vuln_result.append(v)

def report_xls():
    global vuln_result
    global fmt_path

    for vr in vuln_result:
        print(f'[*] -- {vr.ip} | {vr.risk} | {vr.name}')

    workbook_fmt = xlrd.open_workbook(fmt_path, formatting_info=True)
    workbook_writer = copy(workbook_fmt)
    worksheet_writer = workbook_writer.get_sheet(0)

    for row in range(len(vuln_result)):
        for col in range(len(vuln_result[row].list())):
            worksheet_writer.write(row+1, col, vuln_result[row].list()[col])

    output_fp = f'./筛选结果-{datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")}.xls'
    workbook_writer.save(output_fp)
    print(f'[+] ==> IPs: {str(ip_count)} Vulns: {str(len(vuln_result))}')
    print(f'[+] ==> {output_fp}')

if __name__ == "__main__":
    nsfocus_clean()
    venustech_clean()
    report_xls()