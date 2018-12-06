import pathlib
import os
from Crawler.CrawlerCommands import save_html, open_html
import requests
from Crawler.Objects import Parameters
import datetime
from bs4 import BeautifulSoup
import smtplib

keyword = ''
email = ""
password = ""
targetEmail = ""


def crawl(url, name, path):

    parameters = Parameters(url, path, name)

    currentBasePath = pathlib.Path(parameters.basePath)
    currentPath = pathlib.Path(parameters.basePath + parameters.name)

    # Check whether the path lib exist or not.
    if currentBasePath.exists():
        if not currentPath.exists():
            r = requests.get(parameters.url)
            save_html(r.content, parameters.basePath + parameters.name)
    else:
        os.makedirs(parameters.basePath)
        print(path + " has been created. ")
        r = requests.get(parameters.url)
        save_html(r.content, parameters.basePath + parameters.name)

    if(currentPath.exists()):
        parsePage(parameters.basePath + name)
    else:
        print("nothing here")


def parsePage(filePath):
    html = open_html(filePath)
    soup = BeautifulSoup(html, 'html.parser')

    all_day_programs = soup.select('.guide__guide-container .guide__hour-row ')
    for hour_programs in all_day_programs:
        programs = hour_programs.select('a')

        for program in programs:
            if keyword in program.select_one('.program__title').text.strip().lower():
                print(program.select_one('.program__title').text.strip())
                print(program.select_one('.program__starttime').text.strip())
                sendMail(program)


def sendMail(program):

    subject = program.select_one('.program__title').text.strip()
    body = program.select_one('.program__title').text.strip()
    body = body +"\nStart time: " + program.select_one('.program__starttime').text.strip()

    message = 'Subject: {}\n\n{}'.format(subject, body)
    # Next, log in to the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)


    # Send the mail
    server.sendmail(email, targetEmail, message)
    server.quit()
    print("Email send succesfull")


def main():
    url = 'https://www.tvgids.nl/gids/sbs6'
    name = 'tv_gids_sbs6' + datetime.datetime.now().strftime("%Y-%m-%d")
    path = 'C://tvgids_pages//sbs6//'
    crawl(url, name, path)

main()