import sqlite3 as sql

#connecting to the database
con = sql.connect("library.db")

def create():
   
    query = """
                CREATE TABLE IF NOT EXISTS BookStock (
                    ISBN  varchar(50) PRIMARY KEY,
                    BookName varchar(100) NOT NULL,
                    Author varchar(100) NOT NULL,
                    Category varchar(100) NOT NULL,
                    Price number(5,2) NOT NULL,
                    Quantity int NOT NULL CHECK (Quantity>-1))
            """              
    con.execute(query)


    query2 = """
                CREATE TABLE IF NOT EXISTS Student(
                    StudentID varchar(100) PRIMARY KEY,
                    Name varchar(100) NOT NULL,
                    Stream varchar(100) NOT NULL,
                    Phone varchar(15) NOT NULL,
                    YOP int NOT NULL,
                    Fine number(5,2) DEFAULT 0)
            """
    con.execute(query2)

    query3 = """
                CREATE TABLE IssueHistory(
                    IssueID varchar(100) PRIMARY KEY,
                    StudentID varchar(100) NOT NULL,
                    ISBN varchar(100) NOT NULL,
                    DateOfIssue date NOT NULL,
                    DateOfSubmission date NOT NULL,
                    Status int NOT NULL DEFAULT 1,
                    FOREIGN KEY(StudentID) REFERENCES Student(StudentID))
            """
    con.execute(query3)

def add_stock():

    isbn    = input("Enter ISBN Number ")
    bname   = input("Enter Book Name ")
    auth    = input("Enter Author ")
    cat     = input("Enter Category ")
    price   = float(input("Enter Book Price "))
    quant   = int(input("Enter Book Quantity "))

    query = "INSERT INTO BookStock VALUES(?,?,?,?,?,?)"

    con.execute(query,[isbn,bname,auth,cat,price,quant])
    con.commit()
    print ("Book Added Successfully.\n")

def display_all():

    query = "SELECT * FROM BookStock"
    data = con.execute(query)
    for row in data.fetchall():
        print ("\t".join(list(map(str,row))))


def issue_book():
   
    isbn = input("Enter ISBN ")

    query = "SELECT Quantity FROM BookStock WHERE ISBN=?"
    data = con.execute(query,[isbn])
    val = data.fetchone()
    if val==None or val[0]==0:
        print ("Book Can't be Issued please check stock or availability")
        return
    else:
        sid = input("Enter Student Id ")
        query = "SELECT count(StudentID) from IssueHistory WHERE StudentID=? AND Status=1"
        if con.execute(query,[sid]).fetchone()[0]>5:
            print ("All Books Have been issue can't issue more")
            return
        if con.execute("SELECT Fine from Student where StudentID=?",[sid]).fetchone()[0]>0:
            print ("You have FIne Can't Issue Book")
            choice = input("Do u want to pay fine(y/n)")
            if choice == 'y':
            	con.execute("UPDATE Student SET Fine =0 where StudentID=?",[sid])
            else:
            	return
   
            return
        issueid = input("Enter Issue Id ")
        from datetime import datetime,timedelta
        today = (str(datetime.now()))[:10]
        subdate = (str(datetime.now()+timedelta(days=30)))[:10]
        query = "UPDATE BookStock SET Quantity=? where ISBN=?"
        con.execute(query,[val[0]-1,isbn])

        query2 = "INSERT INTO IssueHistory(IssueId,StudentID,ISBN,DateOfIssue,DateOfSubmission) VALUES(?,?,?,?,?)"
        con.execute(query2,[issueid,sid,isbn,today,subdate])
        con.commit()
        print ("Book Issued")


def add_student():

    sid     = input("Enter Student ID ")
    sname   = input("Enter Student Name ")
    stream  = input("Enter Student Stream ")
    phone   = input("Enter Student Phone ")
    yop     = int(input("Enter Student Passout Year "))

    query = "INSERT INTO Student(StudentID,Name,Stream,Phone,YOP) VALUES(?,?,?,?,?)"
   
    con.execute(query,[sid,sname,stream,phone,yop])
    con.commit()

    print ("Student Added Successfully")

def display_all_student():

    query = "SELECT * FROM Student"

    data = con.execute(query)

    for row in data.fetchall():
        print ("\t".join(list(map(str,row))))

def issue_det():

    query = "SELECT * FROM IssueHistory"

    data = con.execute(query)

    for row in data.fetchall():
        print ("\t".join(list(map(str,row))))
       
def submit_book():
    isbn = input("Enter ISBN ")

    query = "SELECT Quantity FROM BookStock WHERE ISBN=?"
    data = con.execute(query,[isbn])
    val = data.fetchone()

    if val == None:
        print ("Invalid ISBN Retry ")
        return
    else:
        studid = input("Enter Student Id")
        issueid = input("Enter Issue Id")
        query = "UPDATE BookStock SET Quantity=? where ISBN=?"
        con.execute(query,[val[0]+1,isbn])
        fine = cal_fine(issueid)
        query = "SELECT Fine from Student where StudentID=?"
        data = con.execute(query,[studid])
        val = data.fetchone()[0]
        fine += val
        if fine>0:
            choice = input("Do you want to pay fine (y/n)")
            if choice=="y":
                con.execute("UPDATE Student SET Fine=0 where StudentID='"+studid+"'")
            else:
                con.execute("UPDATE Student SET Fine="+str(fine)+" where StudentID='"+studid+"'")
        query = "UPDATE IssueHistory SET Status=0 WHERE IssueID=?"
        con.execute(query,[issueid])
       
        con.commit()
   
def cal_fine(issueid):
    query = "SELECT DateOfSubmission from IssueHistory WHERE IssueID=?"
    data = con.execute(query,[issueid])
    val = data.fetchone()[0].split("-")
    from datetime import date,datetime
    x = date(int(val[0]),int(val[1]),int(val[2]))
    today = (str(datetime.now()))[:10]
    today = today.split("-")
    y = date(int(today[0]),int(today[1]),int(today[2]))
    z = y - x
    if z.days > 0:
        return z.days * 5
    else:
        return 0
   
def main():

    while True:
        print ("\n\t\t\t Library Management System ")
        print ("\t\t\t -------------------------")
        print ("\t1. Add Stock")
        print ("\t2. Display Books")
        print ("\t3. Add Student")
        print ("\t4. Issue Book")
        print ("\t5. Submit Book")
        print ("\t6. View Student")
        print ("\t7. Issue Details")
        print ("\tPress 0 to Exit")
        ch = int(input("\tEnter Choice (0-7): "))

        if ch == 1:
            add_stock()
        elif ch == 2:
            display_all()
        elif ch == 3:
            add_student()
        elif ch == 4:
            issue_book()
        elif ch == 5:
            submit_book()
        elif ch == 6:
            display_all_student()
        elif ch == 7:
            issue_det()
        else:
            break
          
\
main()
