import json

import tornado.web
import tornado.ioloop


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        res = """function FindProxyForURL(url, host) {\n"""
        with open('../rules.json') as rules_file:
            rules = json.loads(rules_file.read())
        for proxy, hosts in rules.items():
            checks = ' || '.join('shExpMatch(host, "{}")'.format(host)
                                 for host in hosts)
            res += 'if ({}) {{return "PROXY {}"}}\n'.format(checks, proxy)
        res += 'return "DIRECT"}'
        self.finish(res)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3128)
    tornado.ioloop.IOLoop.current().start()
