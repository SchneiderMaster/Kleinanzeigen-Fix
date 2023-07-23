from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time




def check_exists_path(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_selector(selector):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    return True

def check_if_broken(link):
    global windows
    windows += 1
    #open new tab
    driver.switch_to.new_window()

    #navigate to new tab
    driver.switch_to.window(driver.window_handles[windows])
    
    driver.get(link)
    imgs = WebDriverWait(driver, timeout= 10).until(lambda d: d.find_elements(By.ID, "viewad-image"))

    print(imgs.__len__())

    links = []
    for x in range(imgs.__len__()):
        links.append(imgs[x].get_attribute("src"))

    isBroken = False
    for x in range(links.__len__()):


        driver.get(links[x])
        if check_exists_path("/html/body/img") == False:
            #broken ad has been found
            isBroken = True
            break


    if isBroken:
        driver.get(link)
    else:
        driver.close()
        windows -=1
        driver.switch_to.window(driver.window_handles[windows])



if __name__ == "__main__":
    windows = 0
    driver = webdriver.Firefox()
    ################################################################################
    ########### \/ Link zu deiner Bestandsliste hier einfügen \/ ###################
    user_page = "your-user-link"
    ########### /\ Link zu deiner Bestandsliste hier einfügen /\ ###################
    ################################################################################
    driver.get(user_page)

    cookies = WebDriverWait(driver, timeout= 10).until(lambda d: d.find_element(By.CSS_SELECTOR, "#gdpr-banner-accept"))
    cookies.click()

    time.sleep(3)    

    #fetch every ad
    all_ads = []

    while True:
        local_ads = driver.find_elements(By.CLASS_NAME, "aditem")
        for x in range(local_ads.__len__()):
            all_ads.append(local_ads[x].get_attribute("data-href"))
        if check_exists_selector(".pagination-next"):
            print(driver.find_element(By.CSS_SELECTOR, ".pagination-next").get_attribute("href"))
            driver.find_element(By.CSS_SELECTOR, ".pagination-next").click()
        else:
            break

    for x in range(all_ads.__len__()):
        check_if_broken("https://www.kleinanzeigen.de" + all_ads[x])

