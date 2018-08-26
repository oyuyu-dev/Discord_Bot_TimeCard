# -*- coding: utf-8 -*-

import discord
import os
import datetime

#作業中のユーザを格納
users = {}

client = discord.Client()

@client.event
async def on_ready():
    print('test')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # 「$作業開始」で始まるか調べる
    if message.content.startswith("$作業開始"):
        # Botだった場合反応しない
        if client.user != message.author:
            #ユーザが作業中かどうか判定  
            if message.author.name in users:
                # メッセージ作成
                m = message.author.name + ":新しく作業を開始するためには現在の作業を一度終了してください"
                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)
                
            else: 
                #現在時刻を取得
                now_time = datetime.datetime.now()
            
                #タスク管理クラスをインスタンス化
                task = taskManage(message.author.name)
            
                #作業開始時間を記録
                task.set_start_time(now_time)

                #作業中ユーザを登録
                users[message.author.name] = task

                # メッセージ作成
                m = message.author.name + "：出勤打刻を確認しました：" + str(now_time)

                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)
    
    # 「$作業終了」で始まるか調べる
    if message.content.startswith("$作業終了"):
        # Botだった場合反応しない
        if client.user != message.author:
            #ユーザが作業中か判定
            if message.author.name in users:
                #現在時刻を取得
                now_time = datetime.datetime.now()
            
                #作業中ユーザの辞書からタスク管理クラスのインスタンスを取得
                task = users[message.author.name]
            
                #作業開始時間を記録
                task.set_end_time(now_time)

                #データをログに書きこみ
                task.write_log()

                # メッセージ作成
                m = message.author.name + "：退勤打刻を確認しました：" + str(now_time)

                #作業が終了したので辞書リストから削除
                users.pop(message.author.name)

                # メッセージが送られてきたチャンネルへメッセージを送ります
                await client.send_message(message.channel, m)
            
            #作業中でない場合
            else:
                # メッセージ作成
                m = message.author.name + ":作業中ではありません。作業を開始してください。"
                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)


    # 「$作業終了」で始まるか調べる
    if message.content.startswith("$作業タイトル"):
        # Botだった場合反応しない
        if client.user != message.author:
            #ユーザが作業中か判定
            if message.author.name in users:
                
                #メッセージ内容を取得
                summary = message.content
                
                #：でメッセージを分割
                summary_list = summary.split(":",1)

                #作業中ユーザの辞書からタスク管理クラスのインスタンスを取得
                task = users[message.author.name]
            
                #：以降のメッセージを取得
                task.set_summary(summary_list[1])

                #辞書に更新したオブジェクトを格納
                users[message.author.name] = task

                # メッセージ作成
                m = message.author.name + "：タイトルの設定を確認しました"

                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)

            #作業中でない場合
            else:
                # メッセージ作成
                m = message.author.name + ":作業中ではありません。作業を開始してください。"
                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)


    # 「$作業終了」で始まるか調べる
    if message.content.startswith("$作業内容"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            #ユーザが作業中か判定
            if message.author.name in users:
                
                #メッセージ内容を取得
                summary = message.content
                
                #：でメッセージを分割
                summary_list = summary.split(":",1)

                #作業中ユーザの辞書からタスク管理クラスのインスタンスを取得
                task = users[message.author.name]
            
                #：以降のメッセージを取得
                task.set_description(summary_list[1])

                #辞書に更新したオブジェクトを格納
                users[message.author.name] = task

                # メッセージ作成
                m = message.author.name + "：内容の設定を確認しました"

                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)

            else:
                # メッセージ作成
                m = message.author.name + ":作業中ではありません。作業を開始してください。"
                # メッセージが送られてきたチャンネルへメッセージ送信
                await client.send_message(message.channel, m)


#タスク情報を一括保持する機能を提供する
class taskManage():
    
    #各時間とテキストデータを初期化、ユーザ名を格納
    def __init__(self,user):
        self.user = user
        self.start_time = None
        self.end_time = None
        self.description = None
        self.summary = None

    #作業開始時間:setter
    def set_start_time(self,start_time):
        self.start_time = start_time

    #作業終了時間:setter
    def set_end_time(self,end_time):
        self.end_time = end_time
    
    #作業概要:setter
    def set_summary(self,summary):
        self.summary = summary

    #詳細説明:setter
    def set_description(self,text):
        self.description = text

    #作業開始時間:getter
    def get_start_time(self):
        return self.start_time

    #作業終了時間:getter
    def get_end_time(self):
        return self.end_time
    
    #作業概要:getter
    def get_summary(self):
        return self.summary

    #詳細説明:getter
    def get_description(self):
        return self.description

    #作業データを.dataファイルへ書き込み
    def write_log(self):
        
        #/work_log/以下に格納される。ディレクトリは今のところあらかじめ準備
        file_path = ".\\work_log\\" + self.user + ".data"
        
        #ファイルが存在していない場合はファイル作成
        if not os.path.isfile(file_path):
            with open(file_path, mode='w',encoding='utf-8') as f:
                f.write("---------------------------------------------------------------------------------------------\n")
                f.write("作業開始時刻:"+str(self.start_time)+"\n")
                f.write("作業終了時刻:"+str(self.end_time)+"\n")
                f.write("作業概要:"+self.summary+"\n")
                f.write("作業詳細:"+self.description+"\n")
        
        #ファイルが既に存在している場合は追記
        else :
            with open(file_path, mode='a',encoding='utf-8') as f:
                f.write("---------------------------------------------------------------------------------------------\n")
                f.write("作業開始時刻:"+str(self.start_time)+"\n")
                f.write("作業終了時刻:"+str(self.end_time)+"\n")
                f.write("作業概要:"+self.summary+"\n")
                f.write("作業詳細:"+self.description+"\n")

# token にデベロッパサイトで取得したトークンを入れる
client.run("token")