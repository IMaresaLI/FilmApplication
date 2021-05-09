################################################
################################################
################################################
#########*******###*******####**********########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**********########
########**#####**#**#####**###**################
########**#####**#**#####**###**################
########**######***######**###**################
########**###############**###**################
########**###############**###**################
################################################
########Copyright © Maresal Programming#########
################################################

import sqlite3


class sqliteData():
    def __init__(self):
        self.connect = sqlite3.connect("FilmApp.db")
        self.cursor = self.connect.cursor()
   
    def userAdd(self,username,email,password,securityQuest,role='user'):
        self.cursor.execute("INSERT INTO users (username,email,password,securityQuest,role) VALUES (?,?,?,?,?)",
                       (username,email,password,securityQuest,role))
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")

    def filmAdd(self,filmName,directoryName,filmCategory,originalName,vizyonTarihi,filmImg,filmFrag,ozet):
        self.cursor.execute("INSERT INTO films (filmName,directoryName,filmCategory,originalName,vizyonTarihi,filmImg,filmFragman,ozet) VALUES (?,?,?,?,?,?,?,?)",
                       (filmName,directoryName,filmCategory,originalName,vizyonTarihi,filmImg,filmFrag,ozet))
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")

    def getData(self,tblname,username=None,id=None,all=True):
        if all == True:
            self.cursor.execute(f"Select * from {tblname}")
            data = self.cursor.fetchall()
            self.connect.close()
            return data
        else :
            if id == None:
                self.cursor.execute(f"Select * from {tblname} where username='{username}'")
                data = self.cursor.fetchone()
                self.connect.close()
                return data
            elif username == None :
                self.cursor.execute(f"Select * from {tblname} where id='{id}'")
                data = self.cursor.fetchone()
                self.connect.close()
                return data




    
