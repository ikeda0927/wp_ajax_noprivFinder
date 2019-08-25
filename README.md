# wp_ajax_nopriv Finder
#### 概要  
 　ワードプレスプラグインのファイルに"wp_ajax_nopriv"か"wp ajax nopriv"が含まれている物を見つけ出すやつです。  
#### 前提
　想定しているPythonのバージョンはPython3.7以降です。
#### 使い方
　まず、 __getList.py__ で現在のワードプレスプラグインのリストを取得します。  
~~~
python3 getList.py
~~~
これで __plugin_list.txt__ が得られます。  

　そして __analyze.py__ を実行します。  
実行するときはplugin_list.txtの行番号(分析開始位置と分析終了位置を指定するため)を引数として渡します。

~~~
python3 analyze.py 0 10
~~~
上の例ではplugin_list.txtの上から11個目までのプラグインを分析します。  

　もし、分析したプラグインの中に"wp_ajax_nopriv"か"wp ajax nopriv"のどちらかの文字列が見つかれば標準出力として"#### Found! ####"が出力され、 __plugin_result.txt__ に見つかった位置が記されます。  

※このプログラムが正常に終了した場合、分析中にダウンロードしたプラグインのファイルは削除されるため、plugin_result.txtの行の最初に書かれたプラグイン名を頼りにもう一度ダウンロードしなおしてください。

※分析終了位置の最大値(plugin_list.txtの総行数)は
~~~
wc -l plugin_list.txt
~~~
か何かを実行して、出た値から1を引くような感じで見つけてください。
