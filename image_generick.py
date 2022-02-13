from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get("https://kdm-auto.com.ua/mg-admin/")
    print(driver.title)
    driver.find_element(By.CLASS_NAME, 'login-input').send_keys('olegkostiuk@ukr.net')
    driver.find_element(By.CLASS_NAME, 'pass-input').send_keys('Kostiuk_6173')
    driver.find_element(By.CLASS_NAME, 'enter-button').click()
    admin = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'admin-site-icon')))
    print(driver.title)
    admin.click()
    Hover = ActionChains(driver).move_to_element(driver.find_element(By.ID, 'plugins'))
    Hover.perform()
    a = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/ul/li[7]/div/ul/li[8]/a')
    print(a.get_attribute('innerHTML'))
    a.click()
    image_generate = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[11]/div/div/div[2]/div[1]/div/div[1]/a[2]')))
    print(image_generate.get_attribute('innerText'))
    image_generate.click()
    while True:
        time.sleep(1)
        if (driver.find_element(By.CLASS_NAME, 'message-succes').get_attribute(
                'innerText') == 'Обработано 100% товаров'):
            break
        print(driver.find_element(By.CLASS_NAME, 'message-succes').get_attribute('innerText'))
    WebDriverWait(driver, 9999).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'message-succes'), 'Обработано 100% товаров'))
    driver.close()


if __name__ == '__main__':
    main()
