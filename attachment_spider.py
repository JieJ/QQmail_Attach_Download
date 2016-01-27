# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:20:47 2016

@author: JieJ
"""

from lxml import etree
import urllib
import urllib2
import requests
import re
import os
import time
import json


class qqmail_attachment(object):
    '''
    登录并且获得COOKIE
    更新收件箱页面的url
    更新具体邮件页面的url
    '''

    headers = dict()
    store_dir = ''

    def __init__(self, headers, store_dir):
        self.headers = headers
        self.store_dir = store_dir

    def download(self, page_lst, store_dir):
        '''
        page_lst:需要下载收件箱页面(first_index=0)
        store_dir:附件下载目录
        '''
        for i in page_lst:
            url = '''https://set3.mail.qq.com/cgi-bin/mail_list?sid=QcZ2XZ84vyq
            KcF4I&folderid=1&folderkey=1&page='''+str(i)+'''&s=inbox&topmails=0
            &showinboxtop=1&ver=928946.0&cachemod=maillist&cacheage=7200&r=
            #stattime=1453369291615'''
            page_r = requests.get(url, headers=self.headers)
            page_text = page_r.content
            page_dom = etree.HTML(page_r.content)
            mail_id_lst = page_dom.xpath("//td[@class='cx']/input/@value")

            print u"正在读取收件箱第", str(i), u'页,该页一共', len(mail_id_lst), u'封邮件'
            for j in range(len(mail_id_lst)):
                print u"正在读取第", str(j+1), u"邮件的附件下载地址..."
                new_url = '''https://set3.mail.qq.com/cgi-bin/readmail?folderid
                =1&folderkey=1&t=readmail&mailid='''+mail_id_lst[j]+'''&mode=pre
                &maxage=3600&base=12.46&ver=13301&sid=QcZ2XZ84vyqKcF4I#stattime=
                1453373021581'''
                email_r = requests.get(new_url, headers=self.headers)
                download_dom = etree.HTML(email_r.content)
                filename_lst = download_dom.xpath("//div[@class='ico_big']/a/@filename")
                download_href = download_dom.xpath("//div[@class='ico_big']/a/@down")

                if len(filename_lst) != len(download_href):
                    print u"附件名和附件下载链接不匹配！"
                    break

                print u"该邮件一共有", len(download_href), u"个附件"
                for k in range(len(download_href)):
                    filename = filename_lst[k]
                    filepath = store_dir+os.sep+filename
                    down_load_url = 'https://mail.qq.com'+download_href[k]
                    down_load_url = down_load_url.replace('&amp;', '&')

                    print u"正在下载第", str(k+1), u'个附件......'+filename
                    download_r = requests.get(down_load_url, headers=self.headers)
                    with open(filepath, "wb") as code:
                        code.write(download_r.content)
                    time.sleep(2)
                print ''
            print u'当前页面所有附件下载完成.'
            print ''
        print u'所有页面附件下载完成.'


if __name__ == '__main__':
    headers = {
        "cookie":'''o_cookie=781566599; pgv_pvid=3129801600; pt_clientip=26b20a
        bf81e27119; pt_serverip=1a250abf0e8d51ff; ptui_loginuin=781566599; ptcz
        =68851eae8980872bcd36148713d3f99faaa9ec915c966d43c254180a145a97f8; pt2g
        guin=o0781566599; uin=o0781566599; skey=@ZVxP14kSI; p_uin=o0781566599;
        p_skey=QI2hjlLAOWOuzKh805*fUJlxaSVFxpWHC726vHg8G9Y_; pt4_token=fHZTXQCR
        26kEGYcmLkNxWUyCxA1-trDnXf1DWbn1aE8_; wimrefreshrun=0&; qm_antisky=7815
        66599&cc676b78af40376e2bdcd2508fa9b0f943bb5ab51d1f7cd32b15eb49af86efa3;
        qm_flag=0; qqmail_alias=781566599@qq.com; sid=781566599&b88b209729ebc70f
        e4e640180481b119,qUUkyaGpsTEFPV091ektoODA1KmZVSmx4YVNWRnhwV0hDNzI2dkhnOE
        c5WV8.; qm_username=781566599; qm_sid=b88b209729ebc70fe4e640180481b119,
        qUUkyaGpsTEFPV091ektoODA1KmZVSmx4YVNWRnhwV0hDNzI2dkhnOEc5WV8.; qm_domain
        =https://mail.qq.com; qm_ptsk=781566599&@ZVxP14kSI; foxacc=781566599&0;
        ssl_edition=sail.qq.com; edition=mail.qq.com; username=781566599&781566
        599; webp=1; ptisp=ctc; new_mail_num=781566599&226; CCSHOW=000001'''
    }
    store_dir = 'D:\\mailbox'
    download_test = qqmail_attachment(headers, store_dir)

    page_lst = [i for i in range(10)]
    download_test.download(page_lst, store_dir)
