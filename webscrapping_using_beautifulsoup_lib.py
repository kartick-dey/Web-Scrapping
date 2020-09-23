from bs4 import BeautifulSoup
import urllib.request
import csv
import requests
import re
import os
import urllib
import sys
import time
from selenium import webdriver

status = []

if not os.path.exists('Status.csv'):
    with open('Status.csv', 'w+', encoding = 'utf-8') as csvStatusFile:
        csvStatusData = csv.writer(csvStatusFile)
        csvStatusData.writerow(['Column1'])
else:
    with open('Status.csv', 'r', encoding = 'utf-8') as csvStatusFile:
        csvStatusData = csv.DictReader(csvStatusFile)
        for row in csvStatusData:
            status.append(row['Column1'])

if not os.path.exists('datafile.csv'):
    with open('datafile.csv', 'w+') as csvFileWrite:
        csvOutputWriter = csv.writer(csvFileWrite)
        csvOutputWriter.writerow(['Column1','Colummn2','Column3', 'Column4'])

with open('datafilefinal.csv', 'r', encoding = 'utf-8') as csvFile:
    csvData = csv.DictReader(csvFile)
    counter = 0
    for row in csvData:
        url = row['Column2'].strip()
        List = url.split('/')
        try:
            urlForData = List[0]+'//'+List[2]+'/'+List[3]+'/'+List[4]+'.htm'
            brandName = List[5].replace('.htm', '')
            counter = counter + 1
            if url not in status:
                try:
                    webPage = urllib.request.urlopen(urlForData)
                    soup = BeautifulSoup(webPage, 'html.parser')
                    table = soup.find('table', attrs = {'class' : 'table-bordered table table-hide-5 table-hide-1 table-font-md'})
                    # print('table : ', table)
                    if table:
                        trs = table.find_all('tr')
                        for tr in trs:
                            # print(tr)
                            tds = tr.find_all('td')
                            if len(tds) > 1:
                                # print(len(tds))
                                for td in tds:
                                    if td.find('h4'):
                                        h4 = td.find('h4')
                                        SubstituteDrugName = h4.text
                                        with open('datafile.csv', 'a', encoding = 'utf-8') as outputCSVfile:
                                            outputWriter = csv.writer(outputCSVfile)
                                            outputWriter.writerow([url, urlForData, brandName, SubstituteDrugName])
                    with open('Status.csv', 'a', encoding = 'utf-8') as csvOutputStatusFile:
                        csvOutputStatusData = csv.writer(csvOutputStatusFile)
                        csvOutputStatusData.writerow([url])

                except requests.exceptions.MissingSchema:
                    pass

                except Exception as e:
                    try:
                        webPage = requests.get(urlForData)
                        webPage = webPage.text
                        soup = BeautifulSoup(webPage, 'html.parser')
                        table = soup.find('table', attrs = {'class' : 'table-bordered table table-hide-5 table-hide-1 table-font-md'})
                        # print('table : ', table)
                        if table:
                            trs = table.find_all('tr')
                            for tr in trs:
                                # print(tr)
                                tds = tr.find_all('td')
                                if len(tds) > 1:
                                    # print(len(tds))
                                    for td in tds:
                                        if td.find('h4'):
                                            h4 = td.find('h4')
                                            SubstituteDrugName = h4.text
                                            with open('datafile.csv', 'a', encoding = 'utf-8') as outputCSVfile:
                                                outputWriter = csv.writer(outputCSVfile)
                                                outputWriter.writerow([url, urlForData, brandName, SubstituteDrugName])
                        with open('Status.csv', 'a', encoding = 'utf-8') as csvOutputStatusFile:
                            csvOutputStatusData = csv.writer(csvOutputStatusFile)
                            csvOutputStatusData.writerow([url])

                    except requests.exceptions.MissingSchema:
                        pass
        except Exception as e:
            pass 

        track = "Number of Data Download done....-> {}".format(counter)
        print(track, end = '')
        print('\b'*len(track), end = '', flush = True)

exit = input("Press 'enter' to exit.........")
