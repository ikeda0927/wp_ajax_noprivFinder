
import requests
from bs4 import BeautifulSoup

def get_plugin_names():
    target_url = "http://plugins.svn.wordpress.org/"
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')
    with open('plugin_list.txt','w',newline='') as f:
        for a in soup.find_all('a'):
            f.write(a.get('href').replace("/","")+"\n")


if __name__ == '__main__':
    print("Making lists")
    get_plugin_names()
    print("Finished")
