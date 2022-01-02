from JSParser import JSParser
from multiprocessing import current_process, Pool
import time
import configparser
import urllib.parse
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")

j = JSParser()

def main():
    time_start = time.time()
    j.login(config['GLOVIS']['LOGIN_LINK'])
    link = '{}?&ac={}&acc={}&atn={}'.format(config['GLOVIS']['URL'], urllib.parse.quote_plus("TQhYt3GD6GvgPdVw1QX+Wg=="), urllib.parse.quote_plus("u9cesU3il5ljSzAzHZzmEg=="), str(config['GLOVIS']['ATN_NUM']))
    r = j.fetch(link)
    DATE = j.get_auction_date(r)
    MAX_PAGE = j.get_max_page(r)
    print("Дата Аукціона", DATE, "Кількість сторінок", MAX_PAGE)
    if(config['GLOVIS']['AUTOCODE'] == '0'):
        j.rm_csv("car_id3.txt")
        j.create_txt("car_id3.txt")
    #     categories = [config['LOTTE']['CATEGORY']] if not len(config['LOTTE']['CATEGORIES'].split(","))>1 else config['LOTTE']['CATEGORIES'].split(",")
    #     for category in categories:
    #         print(category)
    #         if(category == "Renault"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(3), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             #MAX_PAGE = j.get_max_page(s_page)
    #             print(s_page.find("div.boarddv p.sti3 span.inlne span")[3].text)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), str(3), str(1), MAX_PAGE)
    #         elif(category == "Mini Cooper"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(72), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), str(72), str(1), MAX_PAGE)
    #         elif(category == "Genesis"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(146), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), str(146), str(1), MAX_PAGE)
    #         elif(category == "Kia Motors"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(2), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), str(2), str(1), MAX_PAGE)
    #         elif(category == "Hyundai"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(5), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), 5, 1, MAX_PAGE)
    #         elif(category == "BMW"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(67), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), 67, 1, MAX_PAGE)
    #         elif(category == "Audi"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(70), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), 70, 1, MAX_PAGE)
    #         elif(category == "Chevrolet"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(1), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), 1, MAX_PAGE)
    #         elif(category == "SsangYong"):
    #             s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], config['GLOVIS']['ATN_NUM'], str(4), 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
    #             MAX_PAGE = j.get_max_page(s_page)
    #             j.get_pages(str(config['GLOVIS']['ATN_NUM']), 4, 1, MAX_PAGE)
            # elif(category == "Bentley"):
            #     s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], 209, 4, 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
            #     MAX_PAGE = j.get_max_page(s_page)
            #     j.get_pages(int(config['GLOVIS']['ATN_NUM']), 4, 1, int(MAX_PAGE))
            # elif(category == "Cadillac"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=CA&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CA')
            # elif(category == "Aston Martin"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=AS&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'AS')
            # elif(category == "Mercedes Benz"):
            #     s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], 209, 68, 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
            #     MAX_PAGE = j.get_max_page(s_page)
            #     j.get_pages(int(config['GLOVIS']['ATN_NUM']), 68, 1, int(MAX_PAGE))
            # elif(category == "Jaguar"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=JA&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'JA')
            # elif(category == "Land Rover"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=LR&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LR')
            # elif(category == "Peugeot"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=PU&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'PU')
            # elif(category == "Volkswagen"):
            #     s_page = j.fetch('{}?searchAuctno={}&prodmancd={}&ac={}&atn={}&acc={}'.format( config['GLOVIS']['URL'], 209, 71, 'TQhYt3GD6GvgPdVw1QX+Wg==', 'hHmv6fGU8/9XeUf4aKXBZg==', 'u9cesU3il5ljSzAzHZzmEg==' ))
            #     MAX_PAGE = j.get_max_page(s_page)
            #     j.get_pages(int(config['GLOVIS']['ATN_NUM']), 71, 1, int(MAX_PAGE))
            # elif(category == "Nissan"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=NI&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'NI')
            # elif(category == "Lincoln"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=LI&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LI')
            # elif(category == "Toyota"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=TO&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'TO')
            # elif(category == "Chrysler"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=CL&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CL')
            # elif(category == "Citroen"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=CT&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'CT')
            # elif(category == "Ferrari"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=FE&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FE')
            # elif(category == "Fiat"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=FT&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FT')
            # elif(category == "Ford"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=FO&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'FO')
            # elif(category == "Honda"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=HO&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'HO')
            # elif(category == "Lamborghini"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=LA&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LA')
            # elif(category == "Lancia"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=LC&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'LC')
            # elif(category == "Maserati"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=MA&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'MA')
            # elif(category == "Mitsubishi"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=MI&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'MI')
            # elif(category == "Porsche"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=PO&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'PO')
            # elif(category == "SAAB"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=SA&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SA')
            # elif(category == "Subaru"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=SR&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SR')
            # elif(category == "Volvo"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=VO&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'VO')
            # elif(category == "Suzuki"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=SZ&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'SZ')
            # elif(category == "Rolls Royce"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=RR&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'RR')
            # elif(category == "Daewoo"):
            #     s_page = parse(config['LOTTE']['URL']+"?set_search_maker=TT&searchPageUnit=20&pageIndex=1", get_max_page)
            #     get_pages(int(config['LOTTE']['FPAGE']), s_page, 20, 'TT')
        j.get_pages(str(config['GLOVIS']['ATN_NUM']), 1, MAX_PAGE)# 1, MAX_PAGE
    elif(config['GLOVIS']['AUTOCODE'] == '1'):
        j.rm_csv()
        j.create_csv()
        j.create_folder('./py_img3')
        j.clear_folder('./py_img3/')
        all_links = j.get_all_links()
        with Pool(30) as p:#20
            p.map(j.get_car, all_links)
    elif(config['GLOVIS']['AUTOCODE'] == '2'):
        j.rm_csv("missed_car_id3.txt")
        print(MAX_PAGE)
        j.get_missed_car_pages(str(config['GLOVIS']['ATN_NUM']), 1, MAX_PAGE)
        j.rm_csv()
        j.create_csv()
        j.create_folder('./py_img3')
        j.clear_folder('./py_img3/')
        all_links = j.get_all_links(config['GLOVIS']['CAR_LINK'], "missed_car_id3.txt")
        with Pool(30) as p:#20
            p.map(j.get_car, all_links)
    elif(config['GLOVIS']['AUTOCODE'] == '3'):
        j.rm_csv("car_id3.txt")
        j.create_txt("car_id3.txt")
        j.get_pages(str(config['GLOVIS']['ATN_NUM']), 1, MAX_PAGE)
        j.rm_csv()
        j.create_csv()
        j.create_folder('./py_img3')
        j.clear_folder('./py_img3/')
        all_links = j.get_all_links()
        with Pool(20) as p:
            p.map(j.get_car, all_links)
    time_end = time.time() 
    print(time_end - time_start)

if __name__ == '__main__':
    main()