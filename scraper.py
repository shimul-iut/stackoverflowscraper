from __future__ import print_function
from bs4 import BeautifulSoup as bs
from terminaltables import AsciiTable
import requests
import argparse
import os

def find_body(url):

    parse = requests.get(url)
    soup = bs(parse.content, 'html.parser')
    return soup.find('body')

def find_details(url):

    body = find_body(url)
    find_title = body.find_all('a', class_='question-hyperlink')
    titles = [i.text for i in find_title]
    titles = [x.replace("\r\n","").strip() for x in titles]

    find_timestamps = body.find_all('span', class_='relativetime')
    timestamps = [i.text for i in find_timestamps]
    timestamps = [x.replace("\r\n","").strip() for x in timestamps]

    find_votecounts = body.find_all('span', class_='vote-count-post')
    find_votecounts = [i.text for i in find_votecounts]
    find_votecounts = [x.replace("\r\n","").strip() for x in find_votecounts]

    merged_list = tuple(zip(titles, timestamps, find_votecounts))
    return merged_list

def find_links(url):

    body = find_body(url)
    find_link = body.find_all('a', class_='question-hyperlink')
    links = []
    for link in find_link:
        links.append(('https://stackoverflow.com' + link.get('href')))
    links =  [x.replace("\r\n","") for x in links]
    return links

def get_data_from_the_title(value, a):
    if "LP" in value:
        links = find_links('https://stackoverflow.com/search?tab=newest&q=%5b'+a+'%5d%20is%3aquestion%20created%3a7d..')[:10]
        url = links[int(value[2:]) - 1]
    elif "MV" in value:
        links = find_links('https://stackoverflow.com/search?q=['+a+']+is%3Aquestion+created%3A7d..&tab=votes')[:10]
        url = links[int(value[2:]) - 1]
    else:
        print('wrong input')
    print(url)
    os.system("xdg-open " + url)

def print_tables(a):

    table_data1 = [
        ['#', 'Latest 10 '+ a + ' questions posted past week', 'Created at', 'Votes']
    ]
    latest_data  = find_details('https://stackoverflow.com/search?tab=newest&q=%5b'+a+'%5d%20is%3aquestion%20created%3a7d..')[:10]

    count = 0
    for i in range(len(latest_data)):
        count = count + 1
        table_data1.append(["LP" + str(count), latest_data[i][0], latest_data[i][1], latest_data[i][2]])

    table = AsciiTable(table_data1)
    table.inner_row_border = True
    print (table.table)
    print ('\n')
    table_data2 = [
        ['#' , 'Most Voted 10 '+ a + ' questions posted past week', 'Created at', 'Votes']
    ]

    latest_voted =  find_details('https://stackoverflow.com/search?q=['+a+']+is%3Aquestion+created%3A7d..&tab=votes')[:10]

    count = 0
    for i in range(len(latest_voted)):
        count = count + 1
        table_data2.append(["MV" + str(count), latest_voted[i][0], latest_voted[i][1], latest_voted[i][2]])

    table = AsciiTable(table_data2)
    table.inner_row_border = True
    print (table.table)

def print_links_latest(a, b):

    table_data = [
        ['Link for the selected question latest from past week']
    ]
    latest_data  = find_links('https://stackoverflow.com/search?tab=newest&q=%5b'+a+'%5d%20is%3aquestion%20created%3a7d..')[:10]

    table_data.append([latest_data])

    table = AsciiTable(table_data)
    table.inner_row_border = True
    print (table.table)

def find_details_temp(url):

    find_timestamps = find_body(url).find_all('span', class_='relativetime')
    timestamps = [i.text for i in find_timestamps]
    timestamps = [x.replace("\r\n","").strip() for x in timestamps]

    print(timestamps)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This is a simple Stackoverflow scarper!')
    #parser.add_argument("--searchfor", default="android", type=str)
    parser.add_argument("--searchfor", type=str, default=False)
    args = parser.parse_args()
    searchfor = args.searchfor

    if searchfor :
        print_tables(searchfor)
    else :
        print('no paramenters provided')
    value = raw_input("Please enter a string:\n")
    get_data_from_the_title(value, searchfor)
