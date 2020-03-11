from __future__ import print_function
from bs4 import BeautifulSoup as bs
from terminaltables import AsciiTable
import requests
import argparse
import os

#Retrived URL for the latest questions posted in past week
def latest_post_urls(a):
    return 'https://stackoverflow.com/search?tab=newest&q=%5b'+a+'%5d%20is%3aquestion%20created%3a7d..'
#Retrived URL for the most voted questions posted in past week
def most_voted_posts_url(a):
    return 'https://stackoverflow.com/search?q=['+a+']+is%3Aquestion+created%3A7d..&tab=votes'

#Initial parsing of the search result page using BeautifulSoup
def find_body(url):

    parse = requests.get(url)
    soup = bs(parse.content, 'html.parser')
    return soup.find('body')

#Scrapping some basic data regarding the questions
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

#Scrapping hyperlinks of the questions
def find_links(url):

    body = find_body(url)
    find_link = body.find_all('a', class_='question-hyperlink')
    links = []
    for link in find_link:
        links.append(('https://stackoverflow.com' + link.get('href')))
    links =  [x.replace("\r\n","") for x in links]
    return links

#Opening the chosen title's associated link inside the bash console performing shell command using os.system()
def get_data_from_the_title(value, a):
    if "LP" in value:
        links = find_links(latest_post_urls(a))[:10]
        url = links[int(value[2:]) - 1]
    elif "MV" in value:
        links = find_links(most_voted_posts_url(a))[:10]
        url = links[int(value[2:]) - 1]
    else:
        print('wrong input')
        return
    print("The stackoverflow URL for the question is : \n")
    print(url)
    os.system("xdg-open " + url)

#Showing the posts inside a Tabular view
def print_tables(a):

    table_data1 = [
        ['#', 'Latest 10 '+ a + ' questions posted past week', 'Created at', 'Votes']
    ]
    latest_data  = find_details(latest_post_urls(a))[:10]

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

    latest_voted =  find_details(most_voted_posts_url(a))[:10]

    count = 0
    for i in range(len(latest_voted)):
        count = count + 1
        table_data2.append(["MV" + str(count), latest_voted[i][0], latest_voted[i][1], latest_voted[i][2]])

    table = AsciiTable(table_data2)
    table.inner_row_border = True
    print (table.table)

#main function

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This is a simple Stackoverflow scarper!')
    parser.add_argument("--searchfor", type=str, default=False)
    args = parser.parse_args()
    searchfor = args.searchfor

    if searchfor :
        print_tables(searchfor)
    else :
        print('no paramenters provided')
    print('\n')
    value = raw_input("Please enter the ID of the question you want to view (i.e : MV8):\n")
    get_data_from_the_title(value, searchfor)
