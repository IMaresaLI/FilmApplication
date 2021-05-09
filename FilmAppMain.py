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

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
import os,sys,base64
from filmAppDesing import Ui_MainWindow
from DatabaseManager import *


class filmApp(QtWidgets.QMainWindow):
    n = len(sqliteData().getData("films", all=True))
    def __init__(self):
        super(filmApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(open("style.css", "r").read())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.mediaPlayer = QtMultimedia.QMediaPlayer()

        self.PageSetting()

        self.ui.ExitBtn.clicked.connect(self.exitButton)
        self.ui.MinimizeBtn.clicked.connect(self.minimize)
        self.ui.FullScreenBtn.clicked.connect(self.fullscreen)

        self.ui.homeBtn.clicked.connect(self.homePage)
        self.ui.filmsBtn.clicked.connect(self.filmsPage)
        self.ui.filmAddBtn.clicked.connect(self.filmAddPage)
        self.ui.LoginBtn.clicked.connect(self.loginPage)
        self.ui.registerHomeBtn.clicked.connect(self.registerPage)
        self.ui.saveFilmBtn.clicked.connect(self.addFilm)
        self.ui.clearBtn.clicked.connect(self.addFilmClear)

        self.ui.videoBtn.clicked.connect(self.videoStart)

        self.ui.loginBtn.clicked.connect(self.login)
        self.ui.registerBtn.clicked.connect(self.register)
        self.ui.LogoutBtn.clicked.connect(self.Logout)

    def guiElements(self):
        self.n = len(sqliteData().getData("films", all=True))
        self.group = []
        self.brosur = []
        self.allTextLbl = []
        self.groupVertical = []
        for i in range(self.n):
            self.group.append(QtWidgets.QGroupBox(
                self.ui.scrollAreaWidgetContents))
            self.group[i].setObjectName("box"+str(i))
            self.group[i].setMinimumSize(200, 300)
            self.group[i].setMaximumSize(200, 300)

            self.brosur.append(QtWidgets.QLabel(self.group[i]))
            self.brosur[i].setObjectName("brosurLbl"+str(i))

            self.groupVertical.append(QtWidgets.QVBoxLayout(self.group[i]))
            self.groupVertical[i].setObjectName("verticalLayout"+str(i))
            self.groupVertical[i].setContentsMargins(0, 0, 0, 0)

            self.allTextLbl.append(QtWidgets.QPushButton(self.group[i]))
            self.allTextLbl[i].setObjectName("allText"+str(i))
            self.allTextLbl[i].clicked.connect(self.filmClick)

        x = 0
        y = 0
        for j in range(self.n):
            self.ui.FilmPageGridLayout_2.addWidget(self.group[j], x, y)
            self.groupVertical[j].addWidget(self.brosur[j])
            self.groupVertical[j].addWidget(self.allTextLbl[j])
            y += 1
            if y == 3:
                x += 1
                y = 0
        self.filmsLoad()

    def filmsLoad(self):
        n = 0
        for i in sqliteData().getData("films", all=True):
            pxmap = QtGui.QPixmap("filmArgumans/FilmBrosur/"+i[6])
            pxmap.setDevicePixelRatio(1.9)
            self.brosur[n].setPixmap(pxmap)
            self.allTextLbl[n].setText(i[1])
            n += 1

    def videoFrame(self, videoPath):
        self.mediaPlayer.setVideoOutput(self.ui.VideoWidget)
        self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl("./filmArgumans/FilmFragman/"+videoPath)))

    def videoStart(self):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else :
            self.mediaPlayer.play()
            print(self.mediaPlayer.state())
        
    def mediaStateChanged(self):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.ui.videoBtn.setIcon(
                    self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.ui.videoBtn.setIcon(
                    self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))    

    def positionChanged(self, position):
        self.ui.horizontalSlider.setValue(position)

    def durationChanged(self, duration):
        self.ui.horizontalSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.ui.videoBtn.setEnabled(False)

    def filmClick(self):
        starBtnName = self.sender().objectName()
        number = int(starBtnName.split("t")[1])+1

        data = sqliteData().getData("films", id=number, all=False)
        self.ui.filmNameLbl.setText(data[1])
        self.ui.vizyonThLbl.setText("Vizyon Tarihi : " + data[5])
        self.ui.directorNameLbl.setText("Yönetmen : " + data[2])
        self.ui.categoryFilmLbl.setText("Kategori : " + data[3])
        self.ui.originalNameLbl.setText("Orijinal Adı : " + data[4])
        self.ui.ozetTxtedt.setPlainText(data[-1])
        self.videoFrame(data[-2])
        self.ui.stackedWidget.setCurrentIndex(2)

    def addFilm(self):
        filmName = self.ui.filmNameTbx.text()
        director = self.ui.directorNameTbx.text()
        category = self.ui.filmCategoryTbx.text()
        filmOriginalName = self.ui.filmOriginalNameTbx.text()
        vizyonTh = self.ui.vizyonTrhTbx.text()
        filmImg = self.ui.filmImgTbx.text()
        filmVideo = self.ui.filmFrgVideoTbx.text()
        filmOzet = self.ui.ozetTbx.toPlainText()
        if filmName != "":
            result = QtWidgets.QMessageBox.question(
                self, "Ekleme Onayı", f"{filmName} adlı filmi eklemek istiyor musunuz?", QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            if result == QtWidgets.QMessageBox.StandardButton.Ok:
                sqliteData().filmAdd(filmName, director, category,
                           filmOriginalName, vizyonTh, filmImg, filmVideo, filmOzet)
                QtWidgets.QMessageBox.information(
                    self, "Ekleme", "Ekleme işlemi tamamlandı.")
                self.addFilmClear()
                self.dataDisplay()
                self.guiElements()

    def addFilmClear(self):
        self.ui.filmNameTbx.clear()
        self.ui.directorNameTbx.clear()
        self.ui.filmCategoryTbx.clear()
        self.ui.filmOriginalNameTbx.clear()
        self.ui.vizyonTrhTbx.clear()
        self.ui.filmImgTbx.clear()
        self.ui.filmFrgVideoTbx.clear()
        self.ui.ozetTxtedt.clear()

    def dataDisplay(self):
        try:
            self.ui.tableWidget.clear()
            datas = sqliteData().getData("films")
            column = len(datas[0])-3
            self.ui.tableWidget.setRowCount(len(datas))
            self.ui.tableWidget.setColumnCount(column)
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ("Film Adı", "Yönetmen Ismi", "Kategorisi", "Orijinal Ismi", "Vizyon Tarihi","Film Özeti"))

            rows = 0
            rowIndex = 0
            for re in datas:
                if rows != len(datas):
                    are = [{
                        'filmName': f'{re[1]}',
                        'directoryName': f'{re[2]}',
                        'filmCategory': f'{re[3]}',
                        'originalName': f'{re[4]}',
                        'vizyonTarihi': f'{re[5]}',
                        'ozet': f'{re[8]}'
                    }]

                    rows += 1

                    for i in are:
                        self.ui.tableWidget.setItem(
                            rowIndex, 0, QtWidgets.QTableWidgetItem(i['filmName']))
                        self.ui.tableWidget.setItem(
                            rowIndex, 1, QtWidgets.QTableWidgetItem(i['directoryName']))
                        self.ui.tableWidget.setItem(
                            rowIndex, 2, QtWidgets.QTableWidgetItem(i['filmCategory']))
                        self.ui.tableWidget.setItem(
                            rowIndex, 3, QtWidgets.QTableWidgetItem(i['originalName']))
                        self.ui.tableWidget.setItem(
                            rowIndex, 4, QtWidgets.QTableWidgetItem(i['vizyonTarihi']))
                        self.ui.tableWidget.setItem(
                            rowIndex, 5, QtWidgets.QTableWidgetItem(i['ozet']))
                        rowIndex += 1
        except :
            pass
        
    def login(self):
        username = self.ui.usernameTbx.text()
        pw = self.ui.pwTbx_2.text()
        encodePw = base64.b85encode(pw.encode()).decode()

        if username != "" and pw != "":
            userData = sqliteData().getData("users",username=username,all=False)
            if userData != None :
                if username == userData[1] and encodePw == userData[3]:
                    QtWidgets.QMessageBox.information(self,"Giriş Bilgisi","Giriş Onaylandı.")
                    self.ui.usernameTbx.clear()
                    self.ui.pwTbx_2.clear()
                    self.PageSetting(YesLogin=True,noLogin=False)
                    self.ui.stackedWidget.setCurrentIndex(0)
                    if userData[-1] == 'Admin':
                        self.ui.filmAddBtn.setHidden(False)
                else :
                    QtWidgets.QMessageBox.warning(self,"Giriş Hata","Girdiğiniz bilgiler yanlış.")
                    self.ui.pwTbx_2.clear()
            else :
                QtWidgets.QMessageBox.warning(self,"Giriş Hata","Girdiğiniz bilgiler yanlış.")
                self.ui.pwTbx_2.clear()
        else :
            QtWidgets.QMessageBox.warnings(self,"Giriş Hata","Kullanıcı ve şifre girilmedi.")

    def register(self):
        username = self.ui.usernameTbx.text()
        pw = self.ui.pwTbx_2.text()
        pw2 = self.ui.pw2Tbx.text()
        email = self.ui.e_mailTbx.text()
        securityQ = self.ui.securityQuestionTbx.text()

        if username != "" and pw != "" and pw2 != "" and email != "" and securityQ != "":
            if pw == pw2 :
                encodePw = base64.b85encode(pw.encode()).decode()
                print(encodePw)
                sqliteData().userAdd(username,email,encodePw,securityQ)
                QtWidgets.QMessageBox.information(self,"Kayıt Bilgisi","Başarılı bir şekilde kayıt oldunuz.")
                self.regPageClear()
                self.ui.stackedWidget.setCurrentIndex(0)
            else :
                QtWidgets.QMessageBox.warning(self,"Kayıt Hata","Şifre bilgileri birbiriyle uyuşmuyor.")
        else :
            QtWidgets.QMessageBox.warning(self,"Kayıt Hata","Tüm bilgiler doldurulmalı.")

    def regPageClear(self):
        self.ui.usernameTbx.clear()
        self.ui.pwTbx_2.clear()
        self.ui.pw2Tbx.clear()
        self.ui.e_mailTbx.clear()
        self.ui.securityQuestionTbx.clear()

    def LoginRegPageEnable(self,process):
        if process == "Login":
            self.ui.emailLbl.setHidden(True)
            self.ui.e_mailTbx.setHidden(True)
            self.ui.pwLbl2.setHidden(True)
            self.ui.pw2Tbx.setHidden(True)
            self.ui.securityQLbl.setHidden(True)
            self.ui.securityQuestionTbx.setHidden(True)
            self.ui.registerBtn.setHidden(True)
            self.ui.loginBtn.setHidden(False)
        else :
            self.ui.emailLbl.setHidden(False)
            self.ui.e_mailTbx.setHidden(False)
            self.ui.pwLbl2.setHidden(False)
            self.ui.pw2Tbx.setHidden(False)
            self.ui.securityQLbl.setHidden(False)
            self.ui.securityQuestionTbx.setHidden(False)
            self.ui.registerBtn.setHidden(False)
            self.ui.loginBtn.setHidden(True)

    def Logout(self):
        self.PageSetting(YesLogin=False,noLogin=True)
        self.mediaPlayer.stop()
        self.ui.stackedWidget.setCurrentIndex(0)

    def homePage(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.mediaPlayer.stop()

    def filmsPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.mediaPlayer.stop()
        self.guiElements()

    def filmAddPage(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.dataDisplay()
        self.mediaPlayer.stop()

    def loginPage(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.LoginRegPageEnable("Login")
        self.mediaPlayer.stop()

    def registerPage(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.LoginRegPageEnable("Reg")
        self.mediaPlayer.stop()

    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def minimize(self):
        self.showMinimized()

    def exitButton(self):
        app.exit()

    def mousePressEvent(self, event):
        try:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.dragPos = event.globalPos()
                event.accept()
        except:
            pass

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        except:
            pass

    def PageSetting(self,YesLogin=False,noLogin=True):
        self.ui.filmAddBtn.setHidden(True)
        self.ui.registerHomeBtn.setHidden(YesLogin)
        self.ui.LoginBtn.setHidden(YesLogin)
        self.ui.LogoutBtn.setHidden(noLogin)
    
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = filmApp()
    main.show()
    app.exit(app.exec_())
