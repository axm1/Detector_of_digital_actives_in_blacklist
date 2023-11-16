from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from datetime import datetime, timedelta
import numpy as np

digital_active = input ("insert the digital active to search in multirbl")

options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized")
s=Service()
browser = webdriver.Chrome(service=s, options=options)

#here we try to load multirbl 10 times if it fails we quit the browser
multirbl_load_attempt_counter = 0

#this function extract the table that contains the domains in blacklist
def domain_container_table_extractor(browser, nombre_activo):
    try:
        table_container_of_blacklist = browser.find_element(By.ID, "dnsbl_data")
    except:
        print ("error i was not able to extract the table with the url https://multirbl.valli.org/lookup/" + nombre_activo + ".html")
    return table_container_of_blacklist

#this function extract the data of the domains in blacklist
def data_blacklisted_domain_extractor (browser,nombre_activo,tabla):
    try:
        domains_in_blacklist = tabla.find_elements(By.CLASS_NAME, "clrBlacklisted") 
    except:
        print ("error i was not able to extract the data of the table with the url https://multirbl.valli.org/lookup/" + nombre_activo + ".html")
        browser.quit()

    id_domains_in_blacklist = [elem.get_attribute("id") for elem in domains_in_blacklist]
    
    #take every id of the domains in blacklist
    
    print("la cantidad de blacklist en multirbl son "+ str(len(domains_in_blacklist)))
    
    sistems_that_detects_blacklist = []
    clasification_array = []
    href_of_blacklisted_domains_array = []
    
    for i in domains_in_blacklist:
        
        sistem_blacklist_detector = i.find_element(By.XPATH,".//a").text
        url_of_blacklisted_domain = i.find_element(By.XPATH,".//a").get_attribute("href")
        
        sistems_that_detects_blacklist.append(sistem_blacklist_detector)
        href_of_blacklisted_domains_array.append(url_of_blacklisted_domain)
        
    for x in id_domains_in_blacklist:
        id = x+"_info_txt"
        try:
            clasification = browser.find_element(By.ID, id).text.lower().replace("txt:","").replace("\n","").strip()
        except:clasification=""
        #remover espacios del final y del principio
        
        clasification_array.append(clasification)
        
    data_packcage = np.stack((sistems_that_detects_blacklist,clasification_array,href_of_blacklisted_domains_array), axis=1)
    #print (conjunto_datos)
    return data_packcage


while True:
    try:
        browser.get("https://multirbl.valli.org/lookup/" + digital_active + ".html")
        break
    except:
        multirbl_load_attempt_counter = multirbl_load_attempt_counter + 1
        if multirbl_load_attempt_counter == 10:
            print ("i was not able to load multirbl")
            browser.quit()            

time.sleep(2)
# if the text is invalid query we quit the browser and print the error
if "Invalid query! No valid IPv4/IPv6 address or domainname" in browser.page_source:
    print ("Invalid query! No valid IPv4/IPv6 address or domainname in multirbl")
    browser.quit()

#here 
counter_of_blacklist = 0



blacklist_counter = 0
salir = False
for i in range(10):
    counter_of_blacklist = counter_of_blacklist + 1
    blacklisted_tags = browser.find_elements(By.CLASS_NAME, "clrBlacklisted")
    # if counter_of_blacklist is equal to 10 we break
    if blacklist_counter == 10:
        break
    word_to_search = "Blacklisted: " + str(blacklist_counter) #here we search for the word Blacklisted: plus a number from 1 to 10 in the tag

    for i in blacklisted_tags:
        if word_to_search in i.text: # if the word Blacklisted: plus a number from 1 to 10 is found in the tag we enter this if to search for the data
                        
            
                        contador_de_blacklist = 0
                        salir = False
                        for i in range(10):
                            contador_de_blacklist = contador_de_blacklist + 1
                            etiquetas_de_blacklisted = browser.find_elements(By.CLASS_NAME, "clrBlacklisted")
                            
                            # si contador_de_blacklist es igual a 10 hacemos break
                            if contador_de_blacklist == 10:
                                break
                            palabra_buscar = "Blacklisted: " + str(contador_de_blacklist)
                            
                            for i in etiquetas_de_blacklisted:
                                if palabra_buscar in i.text: # si se encuentra la palabra Blacklisted: mas algun numero del 1 al 10 en la etiqueta se entra a este if para buscar los datos
                                    
                                    table_domains_container = domain_container_table_extractor(browser, digital_active)

                                    finded_blacklisted_data= data_blacklisted_domain_extractor(browser, digital_active, table_domains_container)
                                    
                                    for data in finded_blacklisted_data:
                                        
                                        sistem_blacklist_detector = data[0]
                                        clasification = data[1]
                                        requerimiento_ticket = data[2]
                                        
                                        #print the data contained in string
                                        print ("the active" + digital_active + " is in the blacklist " + sistem_blacklist_detector + " with the clasification " + clasification + " and the url " + requerimiento_ticket)




