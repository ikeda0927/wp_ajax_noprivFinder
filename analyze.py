
import requests
import zipfile
import os
import linecache
import glob
import re
import shutil
import sys

#ファイル名に関する正規表現
file_name_pattern = "\.+((py)|(txt)|(php))$"
fnpatter = re.compile(file_name_pattern)
#wp_ajax_noprivという文字列を見つけるための正規表現
pattern = "((wp\sajax\snopriv)|(wp_ajax_nopriv))+"
repatter = re.compile(pattern)

#ワードプレスプラグインのzipファイルを取得する
def download_file(pnum,url):
    print(str(pnum)+" : Downloading")
    filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename
    return False

#zipファイルを解凍する
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

#プラグイン内の全てのファイルへのパスを取得
def folder_search(path):
    files =glob.glob(path+"/**", recursive=True)
    return files

#wp_ajax_noprivという文字列を実際に探すところ
def analyze_core(efname):
    print("    analyzing "+efname)
    files= folder_search(efname)
    for file in files:
        fnresult = fnpatter.search(file)
        if(fnresult):
            try:
                with open(file,'r',newline='', encoding="utf8", errors='ignore') as f:
                    s=f.read()
                    sresult = repatter.search(s)
                    if(sresult):
                        print("      #### Found! ####")
                        with open("plugin_result_"+sys.argv[1]+"-"+sys.argv[2]+".txt",'a',newline='')as resultfile:
                            resultfile.write(file+"\n")
            except IsADirectoryError:
                pass

    print("    analyze finished")

#プラグインリストを読み込んで分析する
def analyze_plugin(start,end):
    url ="https://downloads.wordpress.org/plugin/"
    with open('plugin_list.txt','r',newline='') as f:
        for i in range(start):
            f.readline()
        for i in range(end-start+1):
            fname =f.readline().replace("\n","")+".zip"
            file = download_file(start+i,url+fname)
            efname = zip_extract(file)
            #zipfileの削除
            os.remove(fname)
            if(efname):
                analyze_core(efname)
                #調査したプラグインの削除
                shutil.rmtree(efname)


if __name__ == '__main__':
    print("Start analyze.")
    analyze_plugin(int(sys.argv[1]),int(sys.argv[2]));
