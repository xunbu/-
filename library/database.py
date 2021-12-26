import sqlite3
import os
import datetime

class Database:
    def connect(self,data_name):
        self.data_name=data_name
        if os.path.isfile('{}'.format(data_name)):
            self.conn=sqlite3.connect('{}'.format(data_name))
        else:
            Database.createdatabase(self)
    def createdatabase(self):
        self.conn=sqlite3.connect('{}'.format(self.data_name))
        c=self.conn.cursor()
        self.conn.commit()
        c.execute('''create table user(
                        user_id text primary key not null,
                        user_name text not null,
                        user_password text not null,
                        user_sex date,
                        user_birthday date
                        )''')#读者表
        c.execute('''create table admin(
                        admin_id text primary key not null,
                        admin_name text not null,
                        admin_password text not null
                        )''')#管理员表
        c.execute('''create table book(
                        book_id  INTEGER PRIMARY KEY, 
                        book_name text not null,
                        book_author text,
                        book_type text,
                        book_number integer not null, 
                        book_place text
                        )''')#图书表
        c.execute('''create table borrow(
                        borrow_id integer PRIMARY KEY autoincrement,
                        bookid integer not null,
                        bookname text not null,
                        userid text not null,
                        username text not null,
                        date date not null,
                        dateback date not null,
                        ifback text not null
                        )''')#借书表
        c.execute('''CREATE TRIGGER user_t
                    after UPDATE of user_name ON user
                    begin
                    update borrow set username=new.user_name where userid=new.user_id;
                    end;''')#user_t触发器 在修改user.user_name时修改borrow.username
        c.execute('''CREATE TRIGGER book_t
                    after UPDATE of book_name ON book
                    begin
                    update borrow set bookname=new.book_name where bookid=new.book_id;
                    end;''')#user_t触发器 在修改user.user_name时修改borrow.username
        self.conn.commit()
    ############创建字典
    def createdir(self):
        self.userdir={}
        self.bookdir={}
        self.admindir={}
        self.borrowdir={}
        c=self.conn.cursor()
        user=c.execute('select * from user')
        for row in user:
            self.userdir[row[0]]=[row[1],row[2],row[3],row[4]]
        admin=c.execute('select * from admin')
        for row in admin:
            self.admindir[row[0]]=[row[1],row[2]]
        book=c.execute('select * from book order by book_id')
        for row in book:
            self.bookdir[row[0]]=[row[1],row[2],row[3],row[4],row[5]]
        borrow=c.execute('select * from borrow order by borrow_id desc')
        for row in borrow:
            self.borrowdir[row[0]]=[row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
        self.conn.commit()
    ############用户表
    def adduser(self,inputtuple):
        c=self.conn.cursor()
        #inputtuple=tuple(map(str,inputtuple))
        #xunbutest\',"","","超人","");--'
        #c.execute("insert into user values {}".format(str(inputtuple)))#这种写法会被sql注入
        c.execute("insert into user values(?,?,?,?,?)",inputtuple)
        self.conn.commit()
    def ifuserexist(self,inputtuple):
        if inputtuple[0] in self.userdir.keys():
            if inputtuple[1] == self.userdir[inputtuple[0]][1]:
                return self.userdir[inputtuple[0]][0]
            else:
                return 0
        else:
            return 0
    def alluser(self):
        list1=[]
        for key in self.userdir:
            searchuser_key(self,key,list1)
        return(list1)
    def deleteuser(self,userid):
        c=self.conn.cursor()
        c.execute('delete from user where user_id==?',(userid,))
        self.conn.commit()
        return 1
    def updateuser(self,inputlist):
        #inputlist=[userid,username,password,sex,birhday]
        c=self.conn.cursor()
        userid=inputlist[0]
        username=inputlist[1]
        password=inputlist[2]
        sex=inputlist[3]
        birthday=inputlist[4]
        if not userid in self.userdir.keys():
            return 0
        if username!='':
            c.execute('update user set user_name=? where user_id==?',(username,userid))
        if password!='':
            c.execute('update user set user_password=? where user_id==?',(password,userid))
        if sex!='':
            c.execute('update user set user_sex=? where user_id==?',(sex,userid))
        if birthday!='':
            c.execute('update user set user_birthday=? where user_id==?',(birthday,userid))
        self.conn.commit()
        return userid
    def multisearch_user(self,inputlist):
        list1=[]
        c=self.conn.cursor()
        #inputlist=[username,sex,birthday]
        #userdir={id:[name,password,sex,birthday]}
        for key in self.userdir:
            if ((inputlist[0] in self.userdir[key][0] or inputlist[0]=='') and 
                (inputlist[1] in self.userdir[key][2] or inputlist[1]=='') and 
                (inputlist[2] == self.userdir[key][3] or inputlist[2]=='')):
                searchuser_key(self,key,list1) 
        return list1
    def adminusercz(self,inputlist):
        list1=[]
        #inputlist=[userid,username,sex,birthday]
        if inputlist[0]!='':
            if inputlist[0] in self.userdir.keys():
                searchuser_key(self,inputlist[0],list1)
        else:
            list1=Database.multisearch_user(self,inputlist[1:])
        return list1
    ############图书表
    def addbook(self,inputtuple):
        c=self.conn.cursor()
        c.execute('insert into book values(?,?,?,?,?,?)',inputtuple)
        self.conn.commit()
        return 1
    def deletebook(self,id):
        c=self.conn.cursor()
        c.execute('delete from book where book_id==?',(id,))
        self.conn.commit()
        return 1
    def allbook(self):
        list1=[]
        for key in self.bookdir:
            searchbook_key(self,key,list1)
        return(list1)
    def multisearch(self,inputlist):
        list1=[]
        c=self.conn.cursor()
        #inputlist=[书名,作者,类型,库存,位置]
        #bookdir={id:[name,author,type,number,place]}
        for key in self.bookdir:
            if ((inputlist[0] in self.bookdir[key][0] or inputlist[0]=='') and 
                (inputlist[1] in self.bookdir[key][1] or inputlist[1]=='') and 
                (inputlist[2] in self.bookdir[key][2] or inputlist[2]=='') and
                (inputlist[3] == str(self.bookdir[key][3]) or inputlist[3]=='') and
                (inputlist[4] in self.bookdir[key][4] or inputlist[4]=='')):
                searchbook_key(self,key,list1) 
        return list1
    def allbook2(self):
        list1=[]
        for key in self.bookdir:
            searchbook_key(self,key,list1)
        return(list1)
    def updatebooknumber(self,id):
        number=self.bookdir[id][3]
        number=int(number)-1
        c=self.conn.cursor()
        c.execute('update book set book_number=? where book_id==?',(number,int(id)))
        self.conn.commit()
        return 1
    def updatebooknumber_plus(self,id):
        number=self.bookdir[id][3]
        number=int(number)+1
        c=self.conn.cursor()
        c.execute('update book set book_number=? where book_id==?',(number,int(id)))
        self.conn.commit()
        return 1
    def adminbookcz(self,inputlist):
        list1=[]
        #inputlist=[bookid,bookname,bookauthor,booktype]
        if inputlist[0]!='':
            if not inputlist[0].isdigit():
                return 0
            else:
                if int(inputlist[0]) in self.bookdir.keys():
                    searchbook_key(self,int(inputlist[0]),list1)
        else:
            list1=Database.multisearch(self,inputlist[1:])
        return list1
    def updatebook(self,inputlist):
        #inputlist=[bookid,bookname,bookauthor,booktype,booknumber,bookplace]
        c=self.conn.cursor()
        bookid=inputlist[0]
        bookname=inputlist[1]
        bookauthor=inputlist[2]
        booktype=inputlist[3]
        booknumber=inputlist[4]
        bookplace=inputlist[5]
        if bookid.isdigit():
            bookid=int(bookid)
            if not bookid in self.bookdir.keys():
                return 0
        else:
            return 'error'
        if bookname!='':
            c.execute('update book set book_name=? where book_id==?',(bookname,bookid))
        if booktype!='':
            c.execute('update book set book_type=? where book_id==?',(booktype,bookid))
        if bookauthor!='':
            c.execute('update book set book_author=? where book_id==?',(bookauthor,bookid))
        if booknumber!='':
            c.execute('update book set book_number=? where book_id==?',(booknumber,bookid))
        if bookplace!='':
            c.execute('update book set book_place=? where book_id==?',(bookplace,bookid))
        self.conn.commit()
        return id
    ############管理员表
    def addadmin(self,inputtuple):
        c=self.conn.cursor()
        c.execute('insert into admin values(?,?,?)',inputtuple)
        self.conn.commit()
    def ifadminexist(self,inputtuple):
        if inputtuple[0] in self.admindir.keys():
            if inputtuple[1] == self.admindir[inputtuple[0]][1]:
                return self.admindir[inputtuple[0]][0]
            else:
                return 0
        else:
            return 0
    ############借书表
    def allborrow(self):
        list1=[]
        for key in self.borrowdir:
            searchborrow_key(self,key,list1)
        return(list1)
    def addborrow(self,inputtuple):
        c=self.conn.cursor()
        c.execute("insert into borrow values(NULL,?,?,?,?,?,'0000-00-00','否')",inputtuple)
        self.conn.commit()
    def givebackborrow(self,inputtuple):
        #inputtuple=(nowtime,bookid,userid)
        c=self.conn.cursor()
        c.execute('update borrow set dateback=? where bookid=? and userid=?',inputtuple)
        c.execute("update borrow set ifback='是' where bookid=? and userid=?",(inputtuple[1],inputtuple[2]))
        self.conn.commit()
        return 1
    def userborrow(self,userid):
        list1=[]
        for key in self.borrowdir:
            if userid in self.borrowdir[key][2] and self.borrowdir[key][6]=='否':
                list1.append([])
                i=len(list1)-1
                list1[i].extend(self.borrowdir[key])
        return(list1)
    def adminborrowcz(self,inputlist):
        list1=[]
        #inputlist=[borrowid,bookid,bookname,userid,username,ifback,borrowday]
        if inputlist[0]!='':
            if not inputlist[0].isdigit():
                return 0
            else:
                if int(inputlist[0]) in self.borrowdir.keys():
                    searchborrow_key(self,int(inputlist[0]),list1)
        else:
            list1=Database.multisearch_borrow(self,inputlist[1:])
        return list1
    def multisearch_borrow(self,inputlist):
        list1=[]
        c=self.conn.cursor()
        #inputlist=[bookid,bookname,userid,username,ifback,,borrowday]
        #borrowdir={borrow_id:[bookid,bookname,userid,username,借阅日期,归还日期,ifback]}
        if inputlist[5]!='':
            day=datetime.datetime.strptime(inputlist[5],'%Y-%m-%d')
            for key in self.borrowdir:
                borrowdate=datetime.datetime.strptime(self.borrowdir[key][4],'%Y-%m-%d')
                dayminus=(day-borrowdate).days
                if ((inputlist[0] == str(self.borrowdir[key][0]) or inputlist[0]=='') and 
                (inputlist[1] in self.borrowdir[key][1] or inputlist[1]=='') and 
                (inputlist[2] == self.borrowdir[key][2] or inputlist[2]=='') and
                (inputlist[3] in self.borrowdir[key][3] or inputlist[3]=='') and
                (inputlist[4] in self.borrowdir[key][6] or inputlist[4]=='')and
                (dayminus>=0)):
                    searchborrow_key(self,key,list1) 
        else:
            for key in self.borrowdir:
                if ((inputlist[0] == str(self.borrowdir[key][0]) or inputlist[0]=='') and 
                (inputlist[1] in self.borrowdir[key][1] or inputlist[1]=='') and 
                (inputlist[2] == self.borrowdir[key][2] or inputlist[2]=='') and
                (inputlist[3] in self.borrowdir[key][3] or inputlist[3]=='') and
                (inputlist[4] in self.borrowdir[key][6] or inputlist[4]=='')):
                    searchborrow_key(self,key,list1) 
        return list1
    def updateborrow(self,inputlist):
        #inputlist=[borrowid,userid,username]
        #borrowdir={borrow_id:[bookid,bookname,userid,username,借阅日期,归还日期,ifback]}
        c=self.conn.cursor()
        borrowid=inputlist[0]
        userid=inputlist[1]
        username=inputlist[2]
        if borrowid!='':
            if borrowid.isdigit():
                borrowid=int(borrowid)
                if not borrowid in self.borrowdir.keys():
                    return 0
            else:
                return 'error'
            if self.borrowdir[borrowid][6]=='否':
                c.execute("update borrow set ifback='是' where borrow_id==?",(borrowid,))

        else:
            for key in self.borrowdir:
                if(not(userid==''and username=='')and
                   (userid==self.borrowdir[key][2] or userid=='')and
                   (username==self.borrowdir[key][3] or username=='')):
                    if self.borrowdir[key][6]=='否':
                        c.execute("update borrow set ifback='是' where borrow_id==?",(key,))   
        self.conn.commit()
        return borrowid


def searchbook_key(self,key,list1):
    list1.append([key])
    i=len(list1)-1
    list1[i].extend(self.bookdir[key])
    return(list1)
def searchborrow_key(self,key,list1):
    list1.append([key])
    i=len(list1)-1
    list1[i].extend(self.borrowdir[key])
    return(list1)
def searchuser_key(self,key,list1):
    list1.append([key])
    i=len(list1)-1
    list1[i].extend(self.userdir[key])
    return(list1)
















if __name__=='__main__':
    databasetest=Database()
    databasetest.connect('library.db')
    conn=databasetest.conn
    c=conn.cursor()
    a=c.execute("select * from borrow ")
    for row in a:
        print(row)

