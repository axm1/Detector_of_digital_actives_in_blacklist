from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from datetime import datetime, timedelta
import numpy as np

digital_active = input ("insert the digital active to search in multirbl: ")

options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized")
s=Service()
browser = webdriver.Chrome(service=s, options=options)

#here we try to load multirbl 10 times if it fails we quit the browser
multirbl_load_attempt_counter = 0
# this function extracts the table that contains the domains in the blacklist
def domain_container_table_extractor(browser, asset_name):
    try:
        table_container_of_blacklist = browser.find_element(By.ID, "dnsbl_data")
    except:
        print("error: I was not able to extract the table with the URL https://multirbl.valli.org/lookup/" + asset_name + ".html")
    return table_container_of_blacklist

# this function extracts the data of the domains in the blacklist
def data_blacklisted_domain_extractor(browser, asset_name, table):
    try:
        domains_in_blacklist = table.find_elements(By.CLASS_NAME, "clrBlacklisted")
    except:
        print("error: I was not able to extract the data of the table with the URL https://multirbl.valli.org/lookup/" + asset_name + ".html")
        browser.quit()

    id_domains_in_blacklist = [elem.get_attribute("id") for elem in domains_in_blacklist]

    # take every id of the domains in the blacklist

    print("the quantity of blacklists in multirbl is " + str(len(domains_in_blacklist)))

    systems_that_detect_blacklist = []
    classification_array = []
    href_of_blacklisted_domains_array = []

    for i in domains_in_blacklist:

        system_blacklist_detector = i.find_element(By.XPATH, ".//a").text
        url_of_blacklisted_domain = i.find_element(By.XPATH, ".//a").get_attribute("href")

        systems_that_detect_blacklist.append(system_blacklist_detector)
        href_of_blacklisted_domains_array.append(url_of_blacklisted_domain)

    for x in id_domains_in_blacklist:
        id = x + "_info_txt"
        try:
            classification = browser.find_element(By.ID, id).text.lower().replace("txt:", "").replace("\n", "").strip()
        except:
            classification = ""
        # remove spaces from the beginning and end

        classification_array.append(classification)

    data_package = np.stack((systems_that_detect_blacklist, classification_array, href_of_blacklisted_domains_array), axis=1)
    # print (data_set)
    return data_package
while True:
    try:
        browser.get("https://multirbl.valli.org/lookup/" + digital_active + ".html")
        break
    except:
        multirbl_load_attempt_counter = multirbl_load_attempt_counter + 1
        if multirbl_load_attempt_counter == 10:
            print("I was not able to load multirbl")
            browser.quit()

time.sleep(2)
# if the text is an invalid query, we quit the browser and print the error
if "Invalid query! No valid IPv4/IPv6 address or domainname" in browser.page_source:
    print("Invalid query! No valid IPv4/IPv6 address or domain name in multirbl")
    browser.quit()

counter_of_blacklist = 0

blacklist_counter = 0
exit_loop = False
show_message_digital_active_is_not_in_any_blacklist = False
for i in range(10):
    counter_of_blacklist = counter_of_blacklist + 1
    blacklisted_tags = browser.find_elements(By.CLASS_NAME, "clrBlacklisted")
    # if the counter_of_blacklist is equal to 10, we break
    if blacklist_counter == 10:
        break
    word_to_search = "Blacklisted: " + str(blacklist_counter)  # here we search for the word Blacklisted: plus a number from 1 to 10 in the tag

    for i in blacklisted_tags:
        if word_to_search in i.text:  # if the word Blacklisted: plus a number from 1 to 10 is found in the tag, we enter this if to search for the data

            blacklist_counter = 0
            exit_loop = False
            for i in range(10):
                blacklist_counter = blacklist_counter + 1
                blacklisted_tags = browser.find_elements(By.CLASS_NAME, "clrBlacklisted")

                # if blacklist_counter is equal to 10, we break
                if blacklist_counter == 10:
                    break
                word_to_search = "Blacklisted: " + str(blacklist_counter)

                for i in blacklisted_tags:
                    if word_to_search in i.text:  # if the word Blacklisted: plus a number from 1 to 10 is found in the tag, we enter this if to search for the data

                        table_domains_container = domain_container_table_extractor(browser, digital_active)

                        found_blacklisted_data = data_blacklisted_domain_extractor(browser, digital_active, table_domains_container)

                        for data in found_blacklisted_data:

                            system_blacklist_detector = data[0]
                            clasification = data[1]
                            request_ticket = data[2]

                            # print the data contained in a string
                            print("The asset " + digital_active + " is in the blacklist " + system_blacklist_detector +
                                    " with the classification " + clasification + " and the URL " + request_ticket)
                            show_message_digital_active_is_not_in_any_blacklist = True

if show_message_digital_active_is_not_in_any_blacklist == False:
    print("The digital activa " + digital_active + " is not in any blacklist in multirbl")
