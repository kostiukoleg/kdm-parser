from Parser import Parser

lotteautoauction = Parser("Hyundai", "hyundai", "현대자동차")
lotteautoauction.rm_csv()
lotteautoauction.create_csv()
lotteautoauction.create_folder('./py_img')
lotteautoauction.clear_folder('./py_img/')
driver = lotteautoauction.get_html('https://www.lotteautoauction.net/')
lotteautoauction.login(driver)
lotteautoauction.get_auction(driver)
lotteautoauction.manufactured(driver)
lotteautoauction.click_next_page(driver,10,20)

#lotteautoauction.click_previous(driver)
#get_manufactured(driver, CATEGORY)
#click_next_page(driver)
#cars_list=[]
#get_car(driver, cars_list)
#save_csv(cars_list, 'test.csv')
#driver.quit()