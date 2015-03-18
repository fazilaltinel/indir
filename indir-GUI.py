# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import requests
import sys, time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(554, 250)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 46, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.txtUrl = QtGui.QLineEdit(self.centralwidget)
        self.txtUrl.setGeometry(QtCore.QRect(110, 20, 431, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.txtUrl.setFont(font)
        self.txtUrl.setMaxLength(500)
        self.txtUrl.setObjectName(_fromUtf8("txtUrl"))

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.txtKayitYeri = QtGui.QLineEdit(self.centralwidget)
        self.txtKayitYeri.setGeometry(QtCore.QRect(110, 80, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.txtKayitYeri.setFont(font)
        self.txtKayitYeri.setMaxLength(500)
        self.txtKayitYeri.setObjectName(_fromUtf8("txtKayitYeri"))

        self.btnBasla = QtGui.QPushButton(self.centralwidget)
        self.btnBasla.setGeometry(QtCore.QRect(170, 130, 231, 41))

        self.btnBasla.clicked.connect(self.startDownloading)

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnBasla.setFont(font)
        self.btnBasla.setObjectName(_fromUtf8("btnBasla"))

        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(112, 190, 441, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.speed = QtGui.QLabel(self.centralwidget)
        self.speed.setGeometry(QtCore.QRect(3, 190, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.speed.setFont(font)
        self.speed.setObjectName(_fromUtf8("speed"))

        self.btnAc = QtGui.QPushButton(self.centralwidget)
        self.btnAc.setGeometry(QtCore.QRect(480, 80, 71, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAc.setFont(font)
        self.btnAc.setObjectName(_fromUtf8("btnAc"))

        self.btnAc.clicked.connect(self.saveAs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 554, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        """
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        self.menubar.addMenu(self.menuAbout)
        """
        MainWindow.setMenuBar(self.menubar)


        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        #self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "URL ", None))
        self.label_2.setText(_translate("MainWindow", "Kayıt Yeri", None))
        self.btnBasla.setText(_translate("MainWindow", "İndirmeyi Başlat", None))
        self.speed.setText(_translate("MainWindow", "Toplam\nİndirilen", None))
        self.btnAc.setText(_translate("MainWindow", "Aç", None))
        #self.menuAbout.setTitle(_translate("MainWindow", "Hakkında", None))

    def saveAs(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(MainWindow, u"Klasör Seç"))
        self.txtKayitYeri.setText(directory)

    def startDownloading(self):
        baglanti = str(self.txtUrl.text())
        konum = str(self.txtKayitYeri.text())
        ayrik = baglanti.split("/")
        dosyaAdi = ayrik[len(ayrik)-1]

        try:
            r = requests.get(baglanti,stream=True)
        except requests.exceptions.ConnectionError:
            QtGui.QMessageBox.critical(MainWindow, "Hata", u"Bağlantı Kurulamadı.\n"
                                                           u"Lütfen internet bağlatınızı kontrol edin.")
        if r.status_code == 200:
            dosyaBoyut = float(r.headers.get('content-length'))
            if konum == None:
                dosya = open(dosyaAdi,"w")
            else:
                dosya = open(konum+"/"+dosyaAdi,"w")
            if dosyaBoyut is None:
                QtGui.QMessageBox.warning(MainWindow, "Dosya Boyutu", u"Dosya boyutu tanımlanamadı!\n"
                                                           u"Dosya indiriliyor...")
                dosya.write(r.content)
            else:
                self.statusbar.showMessage(u"Dosya büyüklüğü: %.2f MB" % (dosyaBoyut/(1024*1024)))
                self.btnBasla.setText(u"Dosya İndiriliyor...")
                ind = 0
                dosyaBoyut = int(dosyaBoyut)
                basla = 0
                for data in r.iter_content(chunk_size=8192):
                    ind += len(data)
                    dosya.write(data)
                    yuzde = int(100*ind/dosyaBoyut)
                    tmm = int(50*ind/dosyaBoyut)
                    QtCore.QCoreApplication.processEvents()
                    self.speed.setText(u"Toplam\nİndirilen %.1f Kb" % (float(ind)/(1024)))
                    self.progressBar.setValue(yuzde)

            dosya.close
            self.btnBasla.setText(u"İndirmeyi Başlat")
            QtGui.QMessageBox.about(MainWindow, u"İndirme Başarılı", u"\nDosya başarıyla indirildi.\t\t  \n")
            self.txtKayitYeri.setText("")
            self.txtUrl.setText("")
            self.speed.setText(u"Toplam\nİndirilen")
            self.progressBar.setValue(0)
            self.statusbar.showMessage("")
        else:
            print "Baglanti hatasi! Tekrar deneyin."

    def About(self):
        QtGui.QMessageBox.about(MainWindow, u"Hakkında", u"\nKodlama: Fazıl ALTINEL\t \n"
                                                        u"\nGUI & Entegrasyon: Yunus YILDIRIM\t \n")

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    MainWindow.setWindowTitle(u"Python İndirme Yöneticisi")
    sys.exit(app.exec_())

