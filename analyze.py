
import requests
import zipfile
import os
import linecache
import glob
import re
import shutil
import sys

file_name_pattern = "\.+((py)|(txt)|(php))$"
fnpatter = re.compile(file_name_pattern)
pattern = "((wp\sajax\snopriv)|(wp_ajax_nopriv))+"
repatter = re.compile(pattern)

def download_file(url):
    print("Downloading")
    filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename
    return False

def zip_extract(filename):
    print("  Extracting")
    target_directory = '.'
    try:
        zfile = zipfile.ZipFile(filename)
    except zipfile.BadZipfile:
        return None
    fname = filename.split('/')[-1]
    zfile.extractall(target_directory)
    return fname.replace(".zip","")

def folder_search(path):
    files =glob.glob(path+"/**", recursive=True)
    # print(files)
    return files

def analyze_core(efname):
    print("    analyzing "+efname)
    files= folder_search(efname)
    for file in files:
        fnresult = fnpatter.search(file)
        if(fnresult):
            # print(file)
            with open(file,'r',newline='', encoding="utf8", errors='ignore') as f:
                s=f.read()
                # print(len(s))
                # print(s)
                sresult = repatter.search(s)
                if(sresult):
                    print("      #### Found! ####")
                    with open("plugin_result.txt",'a',newline='')as resultfile:
                        resultfile.write(file+"\n")
    print("    analyze finished")


def analyze_plugin(start,end):
    url ="https://downloads.wordpress.org/plugin/"
    with open('plugin_list.txt','r',newline='') as f:
        for i in range(start):
            f.readline()
        for i in range(end-start):
            fname =f.readline().replace("\n","")+".zip"
            # print(fname)
            file = download_file(url+fname)
            efname = zip_extract(file)
            os.remove(fname)#zipfileの削除
            if(efname):
                analyze_core(efname)
                shutil.rmtree(efname)




if __name__ == '__main__':
    print("Start analyze.")
    analyze_plugin(int(sys.argv[1]),int(sys.argv[2]));
    # analyze_core("test")
    # print("Download")
    # file = download_file("https://downloads.wordpress.org/plugin/2cpay.zip")
    # fname = zip_extract(file)
    # print(fname)
