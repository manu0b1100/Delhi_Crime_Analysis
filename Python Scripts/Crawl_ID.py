from selenium import webdriver

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import os

# script to get first fir of each police station using selenium

driver = webdriver.Firefox()

driver.get('http://59.180.234.21:8080/citizen/firSearch.htm')
# police website link

selectDistrict = Select(driver.find_element_by_id('sdistrict'))
# select district element

selectStation = Select(driver.find_element_by_id('spolicestation'))
# select police station element

firInput = driver.find_element_by_id('regFirNo')
firarray = ['0001', '0002', '0003', '0004', '0005']
# search for initial FIRs


if (not os.path.isdir('Firs2')):
    os.mkdir('Firs2')
os.chdir('Firs2')


def getSelectedOption(id):
    select = Select(driver.find_element_by_id(id))
    selected_option = select.first_selected_option
    return selected_option.text


# get text of selected option from sequence no.

for i in range(1, len(selectDistrict.options)):  # iterate through all the options of ditricts
    selectDistrict.select_by_index(i)
    sdistrict = getSelectedOption('sdistrict')

    if (not os.path.isdir(sdistrict)):
        os.mkdir(sdistrict)
    os.chdir(sdistrict)
    countPS = len(selectStation.options)

    if countPS > 1:
        for j in range(1, countPS):  # iterate through all police stations of a district
            selectStation.select_by_index(j)
            spolicestation = getSelectedOption('spolicestation')
            if (not os.path.isdir(spolicestation)):
                os.mkdir(spolicestation)
            os.chdir(spolicestation)

            c = 0
            f = open('links.txt', 'a')
            while (c < 5):
                firInput.send_keys(firarray[c])  # search for FIR
                driver.find_element_by_id('searchButton ').click()
                driver.implicitly_wait(5)
                try:
                    firlink = driver.find_element_by_id('child_link1')
                    f.write(firlink.get_attribute('href') + "\n")
                    print(firlink.get_attribute('href'))
                    break
                except NoSuchElementException:
                    firInput.clear()
                    c += 1
            firInput.clear()
            f.close()
            os.chdir('..')
    os.chdir('..')

f.close()
