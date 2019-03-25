import requests
import json
import threading



def qingqiu(
        url="https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=530&salary=10001,15000&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E6%8A%95%E8%B5%84%E7%BB%8F%E7%90%86&kt=3&=10001&at=9a1286fe007343a3814416d6c85149d9&rt=e64ecc55cfa04c15bba0d12e000b930a&_v=0.72906389&userCode=1007625844&x-zp-page-request-id=6626a2b7e5b940dbb80a83b21762e320-1552458010604-278814"
):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }, timeout=50)
    print(response)
    we = json.loads(response.text)
    wq = we["data"]
    wr = wq["results"]
    for i in wr:

        er = i["city"]["display"]
        p = i["positionURL"]
        q = i["workingExp"]["name"]
        f = i["salary"]
        l = i["company"]["name"]
        o = i["eduLevel"]["name"]
        print(er, p, q, f, l, o)  # 城市er 链接p 年限q 补助aa 工资f  公司l 职位a 学历o


class _Timer(threading.Thread):
    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


class LoopTimer(_Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        _Timer.__init__(self, interval, function, args, kwargs)

    def run(self):
        while True:
            if not self.finished.is_set():
                self.finished.wait(self.interval)
                self.function(*self.args, **self.kwargs)
            else:
                break


if __name__ == '__main__':
    t = LoopTimer(3.0, qingqiu)
    t.start()
