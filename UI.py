# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import  QIcon
from database import Database
import datetime
import hashlib

class Stats:
    def __init__(self,conn):
        self.conn=conn
        self.userid=''
        self.username=''
        self.adminid=''
        self.adminname=''
        self.userdir={}
        self.admindir={}
        self.bookdir={}
        self.borrowdir={}
        #######开始界面
        self.ui_star = QUiLoader().load('./resources/star.ui')
        self.ui_star.pushButton.clicked.connect(self.get_ui_userlogin)
        self.ui_star.pushButton_2.clicked.connect(self.get_ui_giveback)
        self.ui_star.pushButton_3.clicked.connect(self.get_ui_search)
        self.ui_star.pushButton_4.clicked.connect(self.get_ui_adminlogin)
        #######用户登陆界面
        self.ui_userlogin=QUiLoader().load('./resources/userlogin.ui')
        self.ui_userlogin.pushButton.clicked.connect(self.userlogin)
        self.ui_userlogin.pushButton_2.clicked.connect(self.get_ui_usersignup)
        self.ui_userlogin.pushButton_3.clicked.connect(self.get_ui_star)
        self.ui_userlogin.pushButton_4.clicked.connect(self.get_ui_userchangepassword)
        #######用户注册界面
        self.ui_usersignup=QUiLoader().load('./resources/usersignup.ui')
        self.ui_usersignup.pushButton.clicked.connect(self.usersignup)
        self.ui_usersignup.pushButton_2.clicked.connect(self.get_ui_userlogin)
        self.ui_usersignup.comboBox.addItems(['男','女','其他'])
        #######用户更改密码界面
        self.ui_userchangepassword=QUiLoader().load('./resources/changeuserpassword.ui')
        self.ui_userchangepassword.pushButton.clicked.connect(self.userchangepassword)
        self.ui_userchangepassword.pushButton_2.clicked.connect(self.get_ui_userlogin)
        #######用户借书界面
        self.ui_borrow=QUiLoader().load('./resources/borrow.ui')
        self.ui_borrow.pushButton.clicked.connect(self.borrow)
        self.ui_borrow.pushButton_2.clicked.connect(self.userborrowlist)
        self.ui_borrow.pushButton_3.clicked.connect(self.get_ui_star)
        #######还书界面
        self.ui_giveback=QUiLoader().load('./resources/giveback.ui')
        self.ui_giveback.pushButton.clicked.connect(self.giveback)
        self.ui_giveback.pushButton_2.clicked.connect(self.get_ui_star)
        #######查询界面
        self.ui_search=QUiLoader().load('./resources/search.ui')
        self.ui_search.pushButton.clicked.connect(self.search_pushButton)
        self.ui_search.pushButton_2.clicked.connect(self.get_ui_star)
        #######管理员登录界面
        self.ui_adminlogin=QUiLoader().load('./resources/adminlogin.ui')
        self.ui_adminlogin.pushButton.clicked.connect(self.adminlogin)
        self.ui_adminlogin.pushButton_2.clicked.connect(self.get_ui_adminsignup)
        self.ui_adminlogin.pushButton_3.clicked.connect(self.get_ui_star)
        #######管理员注册界面
        self.ui_adminsignup=QUiLoader().load('./resources/adminsignup.ui')
        self.ui_adminsignup.pushButton.clicked.connect(self.adminsignup)
        self.ui_adminsignup.pushButton_2.clicked.connect(self.get_ui_adminlogin)

        #######管理员界面
        self.ui_admin=QUiLoader().load('./resources/admin.ui')
        self.ui_admin.pushButton.clicked.connect(self.get_ui_star)
        self.ui_admin.Button_book_cr.clicked.connect(self.book_cr)
        self.ui_admin.Button_book_sc.clicked.connect(self.book_sc)
        self.ui_admin.Button_book_cz.clicked.connect(self.admin_book_cz)
        self.ui_admin.Button_book_gg.clicked.connect(self.book_gg)
        self.ui_admin.Button_book_display.clicked.connect(self.book_display)
        self.ui_admin.Button_record_cz.clicked.connect(self.record_cz)
        self.ui_admin.Button_record_gg.clicked.connect(self.record_gg)
        self.ui_admin.Button_record_display.clicked.connect(self.record_display)
        self.ui_admin.comboBox.addItems(['','是','否'])
        self.ui_admin.comboBox_2.addItems(['','男','女','其他'])
        self.ui_admin.Button_user_cr.clicked.connect(self.adduser_admin)
        self.ui_admin.Button_user_sc.clicked.connect(self.user_sc)
        self.ui_admin.Button_user_cz.clicked.connect(self.user_cz)
        self.ui_admin.Button_user_gg.clicked.connect(self.user_gg)
        self.ui_admin.Button_user_display.clicked.connect(self.user_display)
    ########开始界面
    def get_ui_star(self):
        self.ui_admin.close()
        self.ui_giveback.close()
        self.ui_borrow.close()
        self.ui_adminlogin.close()
        self.ui_adminsignup.close()
        self.ui_userlogin.close()
        self.ui_usersignup.close()
        self.ui_search.close()
        self.ui_star.show()
    ########用户登陆界面
    def get_ui_userlogin(self):
        self.ui_star.close()
        self.ui_usersignup.close()
        self.ui_userchangepassword.close()
        self.ui_userlogin.show()
    def userlogin(self):
        Database.createdir(self)
        id=self.ui_userlogin.lineEdit.text()
        password=self.ui_userlogin.lineEdit_2.text().encode("utf-8")
        password=hashlib.sha1(password).hexdigest()
        inputtuple=(id,password)
        a=Database.ifuserexist(self,inputtuple)
        if a==0:
            QMessageBox.about(self.ui_userlogin,'提示','账号不存在或密码错误')
        else:
            self.userid=id
            self.username=a
            self.get_ui_borrow()
    ########用户注册界面
    def get_ui_usersignup(self):
        self.ui_star.close()
        self.ui_userlogin.close()
        self.ui_usersignup.show()
    def usersignup(self):
        Database.createdir(self)
        id=self.ui_usersignup.lineEdit.text()
        name=self.ui_usersignup.lineEdit_2.text()
        password=self.ui_usersignup.lineEdit_3.text().encode("utf-8")
        password=hashlib.sha1(password).hexdigest()
        password_2=self.ui_usersignup.lineEdit_4.text().encode("utf-8")
        password_2=hashlib.sha1(password_2).hexdigest()
        sex=self.ui_usersignup.comboBox.currentText()
        qdate=self.ui_usersignup.dateEdit.date()
        birthday=qdate.toString('yyyy-MM-dd')
        if id in self.userdir.keys():
            QMessageBox.about(self.ui_usersignup,'提示','账号已被使用')
            return 0
        if id=='' or ' 'in id:
            QMessageBox.about(self.ui_usersignup,'提示','账号不能含有空格')
        else:
            if password!=password_2:
                QMessageBox.about(self.ui_usersignup,'提示','密码前后输入不一致')
            else:
                inputtuple=(id,name,password,sex,birthday)
                Database.adduser(self,inputtuple)
                QMessageBox.about(self.ui_usersignup,'提示','注册成功')
                self.userid=id
                self.username=name
                self.get_ui_borrow()
    ########用户修改密码界面
    def get_ui_userchangepassword(self):
        self.ui_userlogin.close()
        self.ui_userchangepassword.show()
    def userchangepassword(self):
        Database.createdir(self)
        userid=self.ui_userchangepassword.lineEdit.text()
        useroldpassword=self.ui_userchangepassword.lineEdit_2.text().encode("utf-8")
        useroldpassword=hashlib.sha1(useroldpassword).hexdigest()
        usernewpassword=self.ui_userchangepassword.lineEdit_3.text().encode("utf-8")
        usernewpassword=hashlib.sha1(usernewpassword).hexdigest()
        usernewpassword2=self.ui_userchangepassword.lineEdit_4.text().encode("utf-8")
        usernewpassword2=hashlib.sha1(usernewpassword2).hexdigest()
        inputtuple=(userid,useroldpassword)
        a=Database.ifuserexist(self,inputtuple)
        if a==0:
            QMessageBox.about(self.ui_userchangepassword,'提示','账号不存在或旧密码错误')
            return 0
        if usernewpassword=='':
            QMessageBox.about(self.ui_userchangepassword,'提示','新密码不能为空')
            return 0
        if usernewpassword==usernewpassword2:
            inputlist=[userid,'',usernewpassword,'','']
            Database.updateuser(self,inputlist)
            QMessageBox.about(self.ui_userchangepassword,'提示','更改成功')
            self.get_ui_userlogin()
        else:
            QMessageBox.about(self.ui_userchangepassword,'提示','前后输入密码不一致')
    ########用户借书界面
    def get_ui_borrow(self):
        self.ui_userlogin.close()
        self.ui_usersignup.close()
        self.ui_borrow.show()
        self.ui_borrow.label_name.setText('欢迎<'+self.username+'>读者')
    def borrow(self):
        userid=self.userid
        Database.createdir(self)
        id=self.ui_borrow.lineEdit.text()
        if not id.isdigit():
            QMessageBox.about(self.ui_borrow,'提示','图书id一定是数字')
            return 0
        id=int(id)
        if id not in self.bookdir.keys():
            QMessageBox.about(self.ui_borrow,'提示','此书不存在')
        else:
            if self.bookdir[id][3]<=0:
                QMessageBox.about(self.ui_borrow,'提示','此书已无剩余')
                return 0
            for key in self.borrowdir:
                if id==self.borrowdir[key][0] and self.userid==self.borrowdir[key][2] and self.borrowdir[key][6]=='否':
                    QMessageBox.about(self.ui_borrow,'提示','不能借阅已借阅的书')
                    return 0
            nowtime=datetime.date.today()
            inputtuple=(id,self.bookdir[id][0],userid,self.userdir[userid][0],nowtime)
            Database.addborrow(self,inputtuple)
            a=Database.updatebooknumber(self,id)
            if a==1:
                QMessageBox.about(self.ui_borrow,'提示','操作成功')
    def userborrowlist(self):
        table=self.ui_borrow.tableWidget
        Database.createdir(self)
        displaylist=Database.userborrow(self,self.userid)
        table.setRowCount(0)
        for y in range(len(displaylist)):
            table.insertRow(y)
            x=0
            while x<=len(displaylist[y])-1:
                table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                x+=1    
    ########还书界面
    def get_ui_giveback(self):
        self.ui_star.close()
        self.ui_giveback.show()
    def giveback(self):
        Database.createdir(self)
        bookid=self.ui_giveback.lineEdit.text()
        userid=self.ui_giveback.lineEdit_2.text()
        a=0#a记录是否有删除
        if not bookid.isdigit():
            QMessageBox.about(self.ui_giveback,'提示','图书ID一定是数字')
            return 0
        else:
            bookid=int(bookid)
        for key in self.borrowdir:
            if bookid==self.borrowdir[key][0] and userid==self.borrowdir[key][2] and self.borrowdir[key][6]=='否':
                nowtime=datetime.date.today()
                Database.givebackborrow(self,(nowtime,bookid,userid))
                Database.updatebooknumber_plus(self,bookid)
                a=1
        if a==1:
            QMessageBox.about(self.ui_giveback,'提示','归还成功')
    ########查询界面
    def get_ui_search(self):
        self.ui_star.close()
        self.ui_search.show()
    def search_pushButton(self):
        Database.createdir(self)
        bookname=self.ui_search.lineEdit.text()
        bookauthor=self.ui_search.lineEdit_2.text()
        booktype=self.ui_search.lineEdit_3.text()
        inputlist=[bookname,bookauthor,booktype,'','']#库存位置缺省
        table=self.ui_search.tableWidget
        table.setRowCount(0)
        displaylist=Database.multisearch(self,inputlist)
        #displaylist=[[1002, '中国文化导论', '布吉岛', '暂无', 2, '暂无'], [1003, '实分析', '黄寒松', '暂无', 3, '暂无']]

        for y in range(len(displaylist)):
            table.insertRow(y)
            x=0
            while x<=5:
                table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                x+=1
    ########管理员登录界面
    def get_ui_adminlogin(self):
        self.ui_star.close()
        self.ui_adminsignup.close()
        self.ui_adminlogin.show()
    def adminlogin(self):
        Database.createdir(self)
        id=self.ui_adminlogin.lineEdit.text()
        password=self.ui_adminlogin.lineEdit_2.text().encode("utf-8")
        password=hashlib.sha1(password).hexdigest()
        inputtuple=(id,password)
        a=Database.ifadminexist(self,inputtuple)
        if a==0:
            QMessageBox.about(self.ui_adminlogin,'提示','账号不存在或密码错误')
        else:
            self.adminid=id
            self.adminname=a
            self.get_ui_admin()
    ########管理员注册界面
    def get_ui_adminsignup(self):
        self.ui_star.close()
        self.ui_adminlogin.close()
        self.ui_adminsignup.show()
    def adminsignup(self):
        id=self.ui_adminsignup.lineEdit.text()
        name=self.ui_adminsignup.lineEdit_2.text()
        password=self.ui_adminsignup.lineEdit_3.text().encode("utf-8")
        password=hashlib.sha1(password).hexdigest()
        password_2=self.ui_adminsignup.lineEdit_4.text().encode("utf-8")
        password_2=hashlib.sha1(password_2).hexdigest()
        if id=='' or ' 'in id:
            QMessageBox.about(self.ui_adminsignup,'提示','账号不能含有空格')
        else:
            if password!=password_2:
                QMessageBox.about(self.ui_adminsignup,'提示','密码前后输入不一致')
            else:
                inputtuple=(id,name,password)
                Database.addadmin(self,inputtuple)
                QMessageBox.about(self.ui_adminsignup,'提示','注册成功')
                self.userid=id
                self.adminname=name
                self.get_ui_admin()
    ########管理员界面
    def get_ui_admin(self):
        self.ui_adminlogin.close()
        self.ui_adminsignup.close()
        self.ui_admin.show()
        self.ui_admin.label_name.setText('欢迎<'+self.adminname+'>管理员')
    def book_cr(self):
        bookid=self.ui_admin.lineEdit_bid.text()
        bookname=self.ui_admin.lineEdit_bname.text()
        bookauthor=self.ui_admin.lineEdit_bauthor.text()
        booktype=self.ui_admin.lineEdit_btype.text()
        bookplace=self.ui_admin.lineEdit_bplace.text()
        booknumber=self.ui_admin.lineEdit_bnumber.text()
        if not( bookid.isdigit() and  booknumber.isdigit()):
            QMessageBox.about(self.ui_admin,'提示','id与库存必须是数字')
        else:
            if bookname=='':
                QMessageBox.about(self.ui_admin,'提示','书名不能为空')
            else:
                inputlist=[int(bookid),bookname,bookauthor,booktype,int(booknumber),bookplace]
                for i in range(len(inputlist)):
                    if inputlist[i]=='':
                        inputlist[i]='暂无'
                a=Database.addbook(self,tuple(inputlist))
                if a==1:
                    self.admin_book_cz()
    def book_sc(self):
        str_bookid=self.ui_admin.lineEdit_bid.text()
        if not str_bookid.isdigit():
            QMessageBox.about(self.ui_admin,'提示','请检查图书id')
            return 0
        bookid=int(str_bookid)
        for key in self.borrowdir:
            if bookid == self.borrowdir[key][0]:
                if self.borrowdir[key][6]=='否':
                    QMessageBox.about(self.ui_admin,'提示','此图书正在被借阅，无法删除')
                    return 0
        a=Database.deletebook(self,bookid)
        if a==1:
            QMessageBox.about(self.ui_admin,'提示','删除成功')
    def admin_book_cz(self):
        Database.createdir(self)
        bookid=self.ui_admin.lineEdit_bid.text()
        bookname=self.ui_admin.lineEdit_bname.text()
        bookauthor=self.ui_admin.lineEdit_bauthor.text()
        booktype=self.ui_admin.lineEdit_btype.text()
        booknumber=self.ui_admin.lineEdit_bnumber.text()
        bookplace=self.ui_admin.lineEdit_bplace.text()
        table=self.ui_admin.tableWidget
        inputlist=[bookid,bookname,bookauthor,booktype,booknumber,bookplace]
        displaylist=Database.adminbookcz(self,inputlist)
        if displaylist==0:
            QMessageBox.about(self.ui_admin,'提示','若使用序号查询,序号必须为数字')
        else:
            table.setRowCount(0)
            for y in range(len(displaylist)):
                table.insertRow(y)
                x=0
                while x<=len(displaylist[y])-1:
                    table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                    x+=1
    def book_gg(self):
        Database.createdir(self)
        bookid=self.ui_admin.lineEdit_bid.text()
        bookname=self.ui_admin.lineEdit_bname.text()
        bookauthor=self.ui_admin.lineEdit_bauthor.text()
        booktype=self.ui_admin.lineEdit_btype.text()
        booknumber=self.ui_admin.lineEdit_bnumber.text()
        bookplace=self.ui_admin.lineEdit_bplace.text()
        inputlist=[bookid,bookname,bookauthor,booktype,booknumber,bookplace]
        a=Database.updatebook(self,inputlist)
        if a=='error':
            QMessageBox.about(self.ui_admin,'提示','请检查图书id')
        else:
            self.admin_book_cz()
    def book_display(self):
        Database.createdir(self)
        displaylist=Database.allbook(self)
        table=self.ui_admin.tableWidget
        table.setRowCount(0)
        for y in range(len(displaylist)):
            table.insertRow(y)
            x=0
            while x<=5:
                table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                x+=1
    ####借书
    def record_cz(self):
        Database.createdir(self)
        borrowid=self.ui_admin.lineEdit_rid.text()
        bookid=self.ui_admin.lineEdit_rbid.text()
        bookname=self.ui_admin.lineEdit_rbname.text()
        userid=self.ui_admin.lineEdit_ruid.text()
        username=self.ui_admin.lineEdit_runame.text()
        ifback=self.ui_admin.comboBox.currentText()
        borrowday=self.ui_admin.lineEdit_day.text()
        table=self.ui_admin.tableWidget_2
        inputlist=[borrowid,bookid,bookname,userid,username,ifback,borrowday]
        displaylist=Database.adminborrowcz(self,inputlist)
        if displaylist==0:
            QMessageBox.about(self.ui_admin,'提示','若使用序号查询,序号必须为数字')
        else:
            table.setRowCount(0)
            for y in range(len(displaylist)):
                x=0
                table.insertRow(y)
                while x<=len(displaylist[y])-1:
                    table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                    x+=1
    def record_gg(self):
        Database.createdir(self)
        borrowid=self.ui_admin.lineEdit_rid.text()
        userid=self.ui_admin.lineEdit_ruid.text()
        username=self.ui_admin.lineEdit_runame.text()
        inputlist=[borrowid,userid,username]
        a=Database.updateborrow(self,inputlist)
        if a=='error':
            QMessageBox.about(self.ui_admin,'提示','请检查序号')
        else:
            self.record_cz()
    def record_display(self):
        Database.createdir(self)
        table=self.ui_admin.tableWidget_2
        displaylist=Database.allborrow(self)
        table.setRowCount(0)
        for y in range(len(displaylist)):
            table.insertRow(y)
            x=0
            while x<=len(displaylist[y])-1:
                table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                x+=1
    ####用户
    def adduser_admin(self):
        Database.createdir(self)
        id=self.ui_admin.lineEdit_userid.text()
        name=self.ui_admin.lineEdit_username.text()
        password=self.ui_admin.lineEdit_userpassword.text().encode("utf-8")
        password=hashlib.sha1(password).hexdigest()
        sex=self.ui_admin.comboBox_2.currentText()
        birthday=self.ui_admin.lineEdit_userbirthday.text()
        if id in self.userdir.keys():
            QMessageBox.about(self.ui_admin,'提示','账号已被使用')
            return 0
        if id=='' or ' 'in id:
            QMessageBox.about(self.ui_admin,'提示','账号不能含有空格')
        else:
            inputtuple=(id,name,password,sex,birthday)
            Database.adduser(self,inputtuple)
            QMessageBox.about(self.ui_usersignup,'提示','添加成功')
            self.user_display()
    def user_sc(self):
        userid=self.ui_admin.lineEdit_userid.text()
        for key in self.borrowdir:
            if userid == self.borrowdir[key][2]:
                if self.borrowdir[key][6]=='否':
                    QMessageBox.about(self.ui_admin,'提示','此用户正在借阅图书，无法删除')
                    return 0
        a=Database.deleteuser(self,userid)
        if a==1:
            QMessageBox.about(self.ui_admin,'提示','删除成功')
    def user_gg(self):
        Database.createdir(self)
        userid=self.ui_admin.lineEdit_userid.text()
        username=self.ui_admin.lineEdit_username.text()
        password=self.ui_admin.lineEdit_userpassword.text().encode("utf-8")
        password=hashlib.sha1(password).hexdigest()
        sex=self.ui_admin.comboBox_2.currentText()
        birthday=self.ui_admin.lineEdit_userbirthday.text()
        inputlist=[userid,username,password,sex,birthday]
        a=Database.updateuser(self,inputlist)
        self.user_cz()
    def user_cz(self):
        Database.createdir(self)
        userid=self.ui_admin.lineEdit_userid.text()
        username=self.ui_admin.lineEdit_username.text()
        sex=self.ui_admin.comboBox_2.currentText()
        birthday=self.ui_admin.lineEdit_userbirthday.text()
        table=self.ui_admin.tableWidget_3
        inputlist=[userid,username,sex,birthday]
        displaylist=Database.adminusercz(self,inputlist)
        table.setRowCount(0)
        for y in range(len(displaylist)):
            x=0
            table.insertRow(y)
            while x<=len(displaylist[y])-1:
                table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                x+=1
    def user_display(self):
        table=self.ui_admin.tableWidget_3
        Database.createdir(self)
        displaylist=Database.alluser(self)
        table.setRowCount(0)
        for y in range(len(displaylist)):
            table.insertRow(y)
            x=0
            while x<=len(displaylist[y])-1:
                table.setItem(y,x,QTableWidgetItem(str(displaylist[y][x])))
                x+=1

