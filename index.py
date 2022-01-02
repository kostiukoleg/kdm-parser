from multiprocessing import Pool
from Parser import Parser

lotteautoauction = Parser()

def doubler(lotteautoauction):
    driver = lotteautoauction.get_html('https://www.lotteautoauction.net/')
    return lotteautoauction.login(driver)

if __name__ == '__main__':
    pool = Pool(processes=3)
    print(pool.map(doubler, lotteautoauction))