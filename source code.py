from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import random
conn=sqlite3.connect('passengers1.db')
c=conn.cursor()

def start():
    global coupon
    coupon = ["trial10", "good50", "super600", 'super10', "winwin"]
    window = Tk()
    window.geometry("400x300")
    window.title("Rock Paper Scissors Game")
    global USER_SCORE
    global COMP_SCORE
    USER_SCORE = 0
    COMP_SCORE = 0
    USER_CHOICE = ""
    COMP_CHOICE = ""
    global lol
    lol=0
    def choice_to_number(choice):
        rps = {'rock':0,'paper':1,'scissor':2}
        return rps[choice]
    '''def number_to_choice(number):
        rps={0:'rock',1:'paper',2:'scissor'}
        return rps[number]'''
    def random_computer_choice():
        return random.choice(['rock','paper','scissor'])
    def result(human_choice,comp_choice):
        global USER_SCORE
        global COMP_SCORE
        user=choice_to_number(human_choice)
        comp=choice_to_number(comp_choice)
        if(user==comp):
            pass
        elif((user-comp)%3==1):
            USER_SCORE+=1
        else:
            COMP_SCORE+=1
        text_area = Text(master=window,height=12,width=30,bg="#FFFF99")
        text_area.grid(column=0,row=4)
        answer = "Your Choice: {} \nComputer's Choice : {} \n Your Score : {} \n Computer Score : {} ".format(USER_CHOICE,COMP_CHOICE,USER_SCORE,COMP_SCORE)
        text_area.insert(END,answer)
    def check():
        global USER_SCORE
        global COMP_SCORE
        if USER_SCORE==10:
            messagebox.showinfo("Result","You have won")
            messagebox.showinfo("Coupon", "Coupon code-"+random.choice(coupon))
            window.destroy()
            return 2
        elif COMP_SCORE==10:
            messagebox.showinfo("Result","You have lost")
            messagebox.showinfo("Coupon", "Better luck next time")
            window.destroy()
            return 3
        return 1
    def count():
        global lol
        lol=lol+1
    def rock():
        global USER_CHOICE
        global COMP_CHOICE
        USER_CHOICE='rock'
        COMP_CHOICE=random_computer_choice()
        result(USER_CHOICE,COMP_CHOICE)
    def paper():
        global USER_CHOICE
        global COMP_CHOICE
        USER_CHOICE='paper'
        COMP_CHOICE=random_computer_choice()
        result(USER_CHOICE,COMP_CHOICE)
    def scissor():
        global USER_CHOICE
        global COMP_CHOICE
        USER_CHOICE='scissor'
        COMP_CHOICE=random_computer_choice()
        result(USER_CHOICE,COMP_CHOICE)
    def rock1():
        rock()
        count()
    def paper1():
        if check()==1:
            paper()
            count()
    def scissor1():
        if check()==1:
            scissor()
            count()
    def change(a):
        k=[rock1,paper1,scissor1]
        if check()== 1:
            k[a]()

    button1 = Button(text="       Rock       ",bg="skyblue",command=lambda : change(0))
    button1.grid(column=0,row=1)
    button2 = Button(text="       Paper      ",bg="pink",command=lambda :change(1))
    button2.grid(column=0,row=2)
    button3 = Button(text="      Scissor     ",bg="lightgreen",command=lambda:change(2))
    button3.grid(column=0,row=3)

    window.mainloop()

def win_choice(a):
    c=[mainpage,book,cancel,games,check,view_bookings,login,create_new_account]
    c[a]()

def randomnum(username):   #prakash code
    c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='login_random_no_list' ")
    if (c.fetchone()[0]!=1):
        c.execute("create table login_random_no_list (loginid text,random_no integer)")
    r=random.randint(1,10000)
    c.execute("select * from login_random_no_list where random_no like {}".format(r))
    if (c.fetchall()==[]):
        c.execute("INSERT INTO login_random_no_list VALUES ('{}',{})".format(username,r))
        conn.commit
        return r
    else:
        randomnum(username)

def booked_seats_write(username,boarding,destination,date,in_time,class1,r): #prakash code
    global fare
    id_num = randomnum(username)
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' '''.format(username))
    if (c.fetchone()[0] != 1):
        c.execute("""CREATE TABLE {} (
                boarding text,
                destination text,
                day text,
                time text,
                class text,
                fare integer,
                id integer
                )""".format(username))
    if r==1:
        c.execute("INSERT INTO {} VALUES ('{}','{}','{}','{}','{}',{},{})".format(username, boarding, destination, date, in_time,class1, fare, id_num))
    elif r==2:
        c.execute("INSERT INTO {} VALUES ('{}','{}','{}','{}','{}',{},{})".format(username, boarding, destination, date,in_time, class1, fare/2, id_num))
    conn.commit()

def check_cred(username,password,confirm_password=""):
    c.execute("select * from users_main_storage  where username like '{}'".format(username))
    def check_username():
        if c.fetchall()==[]:
            return True
        return False

    def password_equality():      #to check if pass and confirm pass are same while creating a new account
        if confirm_password=="":
            return True
        elif password==confirm_password:
            return True
        else:
            return False


    def check_len_pswrd():        #harsh's code
        flag = False
        if (len(password) >= 8 and len(password) <= 15):
            flag = True
        return flag

    def check_cond_pswrd():       #harsh's code
        flag = False
        for i in password:
            for j in password:
                for k in password:
                    if (i.isupper()):
                        if (j.islower()):
                            flag = True
        return flag

    def passcheck():              #to check minimum  one digit, minimum one special character is present
        count = 0
        count1 = 0
        for i in password:
            if (i in "0123456789"):
                count = 1
            elif (i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"):
                count1 = 1
        if (count == 0 or count1 == 0):
            return False
        else:
            return True

    if check_username()==False and confirm_password!="":
        messagebox.showinfo("Account","Username already exist")
    elif (( check_len_pswrd() and check_cond_pswrd() and passcheck())==False and confirm_password!=""):
        messagebox.showerror("error","password not valid\npassword requirements\nminimum 8 characters, maximum 15 characters, minimum one uppercase, minimum one lowercase, minimum  one digit, minimum one special character")
    elif password_equality()==False:
        messagebox.showinfo("Account", "Password don't match")
    elif confirm_password!="":
        c.execute("INSERT INTO users_main_storage  VALUES ('{}','{}')".format(username, password))
        conn.commit()
        messagebox.showinfo("Account","Account has been created")
        return 1
    if confirm_password=="":
        c.execute("select * from users_main_storage where username like '{}' and password like '{}' ".format(username,password))
        if(c.fetchall()!=[]):
            return 1
        else:
            messagebox.showinfo("Account","Username doesn't exist\nor\nIncorrect password")

def create_new_account():
    root = Tk()
    def valchanger(b):
        root.destroy()
        win_choice(b)
    e=StringVar()
    d=StringVar()
    f=StringVar()
    Entry(root,font=30,textvariable=e).grid(row=0,column=1)
    Entry(root,show="*",font=30,textvariable=d).grid(row=1,column=1)
    Entry(root,show="*",font=30,textvariable=f).grid(row=2,column=1)
    root.title('Flight Management System')
    root.iconbitmap('samp.ico')
    root.configure(background='white')
    def bypass():
        if check_cred(e.get(), d.get(), f.get())==1:
            valchanger(4)
    Label(root, text="Enter username", height=0, font=("Courier", 15), bg='white').grid(row=0, column=0)
    Label(root, text="Enter password", height=0, font=("Courier", 15), bg='white').grid(row=1, column=0)
    Label(root, text="Confirm password", height=0, font=("Courier", 15), bg='white').grid(row=2, column=0)
    Button(root, text="Next", font=("Courier", 15), bg='white', padx=10,command=lambda: bypass()).grid(row=3, column=1,columnspan=2)
    Button(root, text="Back", font=("Courier", 15), bg='white', padx=10,command=lambda: valchanger(4)).grid(row=3, column=0, columnspan=2)
    root.mainloop()

def login():
    root = Tk()
    def valchanger(b):
        root.destroy()
        win_choice(b)
    e = StringVar()
    d = StringVar()
    Entry(root, font=30,textvariable=e).grid(row=0, column=1)
    Entry(root, show="*", font=30,textvariable=d).grid(row=1, column=1)
    root.title('Flight Management System')
    root.iconbitmap('samp.ico')
    root.configure(background='white')
    def bypass():
        global u
        if check_cred(e.get(), d.get())==1:
            u=e.get()
            valchanger(0)
    Label(root, text="Enter username", height=0, font=("Courier", 15), bg='white').grid(row=0, column=0)
    Label(root, text="Enter password", height=0, font=("Courier", 15), bg='white').grid(row=1, column=0)
    Button(root, text="Next", font=("Courier", 15), bg='white', padx=10,command=lambda: bypass()).grid(row=2, column=1, columnspan=2)
    Button(root, text="Back", font=("Courier", 15), bg='white', padx=10,command=lambda: valchanger(4)).grid(row=2, column=0, columnspan=2)

def check():
    c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users_main_storage'")
    if (c.fetchone()[0]!=1):
        c.execute("create table users_main_storage(username text,password text)")
    root=Tk()
    def valchanger(b):
        root.destroy()
        win_choice(b)
    root.title('Flight Management System')
    root.iconbitmap('samp.ico')
    root.configure(background='white')
    Button(root, text="Create a new account", font=("Courier", 15), bg='white', padx=10,command=lambda: valchanger(7)).grid(row=1, column=0)
    Button(root, text="Login", font=("Courier", 15), bg='white', padx=100,command=lambda: valchanger(6)).grid(row=2, column=0)
    Button(root, text="Exit", font=("Courier", 15), bg='white', padx=106, command=root.destroy).grid(row=3, column=0)
    root.mainloop()

def view_bookings():

    global u
    username=u
    def View():
        tree.delete(*tree.get_children())
        try:
            c.execute("SELECT * FROM {}".format(username))
        except:
            messagebox.showinfo("Bookings", "No Bookings")
        rows = c.fetchall()
        if rows!=[]:
            for row in rows:
                tree.insert("", END, values=row)

    root = Tk()
    root.title('Flight Management System')
    root.iconbitmap('samp.ico')
    def valchanger(b):
        root.destroy()
        win_choice(b)

    tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="Boarding")
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="destination")
    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="day")
    tree.column("#4", anchor=CENTER)
    tree.heading("#4", text="time")
    tree.column("#5", anchor=CENTER)
    tree.heading("#5", text="class")
    tree.column("#6", anchor=CENTER)
    tree.heading("#6", text="fare")
    tree.column("#7", anchor=CENTER)
    tree.heading("#7", text="ID")
    tree.pack()
    View()
    button2=Button(text="Back", command=lambda:valchanger(0))
    button2.pack(padx=10,pady=10)

def check_coupon(e):
    global coupon
    coupon=["trial10","good50","super600",'super10',"winwin"]
    if e in coupon:
        return 1
    elif e=='':
        return 2
    return 0

def fare_generation(b,d):             #prakash code
    if(b=='chennai'):
        if(d=='bangalore'):
            return 3000
        elif (d=='kolkata'):
            return 7000
    elif(b=='bangalore'):
        if(d=='chennai'):
            return 3000
        elif (d=='kolkata'):
               return 6000
    elif(b=='kolkata'):
        if(d=='bangalore'):
            return 6000
        elif (d=='chennai'):
               return 7000

def book():
    kite = Tk()
    kite.title('Flight Management System')
    kite.iconbitmap('samp.ico')
    loginbtn = PhotoImage(file='samp.png')
    kite.configure(background='white')
    global discount
    discount=0
    def valchanger(b):
        global discount
        kite.destroy()
        if b==0:
            discount=0
        win_choice(b)
    def statecheckdisable():
        date_dropdown1.config(state=DISABLED)
        month_dropdrown1.config(state=DISABLED)
        year_dropdrown1.config(state=DISABLED)
        time_op1.config(state=DISABLED)
    def statecheckenable():
        date_dropdown1.config(state=ACTIVE)
        month_dropdrown1.config(state=ACTIVE)
        year_dropdrown1.config(state=ACTIVE)
        time_op1.config(state=ACTIVE)
    def cocheck():
        global discount
        if(check_coupon(e.get())==1):
            z=messagebox.askyesno("coupon","Do you want to apply this 10% discount")
            if z==1:
                v.config(state='disabled')
                discount=10
        elif(check_coupon(e.get())==0):
            messagebox.showinfo("Coupon","Coupon not valid")
    def transfer():
        global fare
        g=''
        global discount
        if r.get()==1:
            fare=fare_generation(clicked.get(),clicked1.get())-fare_generation(clicked.get(),clicked1.get())*discount/100
            g='Fare='+str(fare)
        elif r.get()==2 and clicked1.get()!='choose something':
            fare=(fare_generation(clicked.get(),clicked1.get())-fare_generation(clicked.get(),clicked1.get())*discount/100)*2
            g='Fare=' + str(fare)
        Label(kite, text=g, height=0, font=("Courier", 25), bg='white').grid(row=7, column=0,sticky='W')
        if discount!=0:
            Label(kite, text='Discount='+str(discount)+'%', height=0, font=("Courier", 25), bg='white').grid(row=6, column=0,sticky='W')
    def date_check(a,b):

        if a == '2' and b in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"]:
            return 1
        elif a in ["1","3","5","7","8","10","12"] and date.get() in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]:
            return 1
        elif b in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]:
            return 1
        return 0
    def bypassbook():
        global u
        if r.get()==1 and clicked.get()!=clicked1.get() and date_check(month.get(),date.get())==1:
            booked_seats_write(u,clicked.get(),clicked1.get(),("{}-{}-{}").format(date.get(),month.get(),year.get()),clicked0.get(),clicked4.get(),1)
            valchanger(0)
        elif r.get()==2 and clicked.get()!=clicked1.get() and date_check(month.get(),date.get())==1 and date_check(month1.get(),date1.get())==1:
            booked_seats_write(u, clicked.get(), clicked1.get(),("{}-{}-{}").format(date.get(), month.get(), year.get()), clicked0.get(), clicked4.get(),2)
            booked_seats_write(u, clicked1.get(), clicked.get(),("{}-{}-{}").format(date1.get(), month1.get(), year1.get()), clicked5.get(), clicked4.get(),2)
            valchanger(0)
        elif clicked.get()==clicked1.get():
            messagebox.showwarning("Booking","Destination and Boarding point can't be same")
        else:
            messagebox.showerror("Booking","Not a valid date")




    boardingoption = ["chennai", "bangalore", "kolkata"]
    destinationoption = ["chennai", "bangalore", "kolkata"]
    flight_class=["First","Business","Premium Economy","Economy"]
    clicked = StringVar()
    clicked.set("chennai")
    clicked1 = StringVar()
    clicked1.set("chennai")
    clicked4 = StringVar()
    clicked4.set("First")
    r=IntVar()
    r.set(1)

    Radiobutton(kite, text="one-way", variable=r, value=1, bg='white', command=statecheckdisable).grid(row=0, column=0)   #row 0
    Radiobutton(kite, text="round-trip", variable=r, value=2, bg='white', command=statecheckenable).grid(row=0,column=1)

    Label(kite, text="From:", height=0, font=("Courier", 25), bg='white').grid(row=1, column=0) #row 1
    Label(kite, text="To:", height=0, font=("Courier", 25), bg='white').grid(row=1, column=1)
    Label(kite, text="Class:", height=0, font=("Courier", 25), bg='white').grid(row=1, column=2)

    c = OptionMenu(kite, clicked, *boardingoption)    #row 2
    d = OptionMenu(kite, clicked1, *destinationoption)
    l = OptionMenu(kite, clicked4, *flight_class)
    c.config(bg="white")
    d.config(bg="white")
    l.config(bg="white")
    c.grid(row=2, column=0, padx=30)
    d.grid(row=2, column=1, padx=30)
    l.grid(row=2, column=2, padx=30)


    Label(kite, text="   Departure Date:", height=0, font=("Courier", 15), bg='white').grid(row=3, column=0,sticky="W")
    Label(kite, text="   Return Date:", height=0, font=("Courier", 15), bg='white').grid(row=3, column=1,sticky="W")
    time=["1:00 AM","7:00 AM","1:00 PM","4:00 PM","9:00 PM"]


    date = StringVar()
    date.set("1")
    month = StringVar()
    month.set("1")
    year = StringVar()
    year.set("2021")


    dates=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    months=["1","2","3","4","5","6","7","8","9","10","11","12"]
    years=["2021","2022"]

    departure_date_frame = Frame(kite,bg='white')
    date_dropdown = OptionMenu(departure_date_frame, date, *dates)  # row 4
    month_dropdrown = OptionMenu(departure_date_frame, month, *months)
    year_dropdrown = OptionMenu(departure_date_frame, year, *years)
    date_dropdown.config(bg="white")
    month_dropdrown.config(bg="white")
    year_dropdrown.config(bg="white")
    date_dropdown.grid(row=0, column=0, padx=30)
    month_dropdrown.grid(row=0, column=1, padx=30)
    year_dropdrown.grid(row=0, column=2, padx=30)
    clicked0 = StringVar()
    clicked0.set("1:00 AM")
    time_op = OptionMenu(departure_date_frame, clicked0, *time)
    time_op.config(bg="white")
    time_op.grid(row=0, column=3, padx=30, sticky="W")
    departure_date_frame.grid(row=4, column=0)

    date1 = StringVar()
    date1.set("1")
    month1 = StringVar()
    month1.set("1")
    year1 = StringVar()
    year1.set("2021")

    return_date_frame = Frame(kite, bg='white')
    date_dropdown1 = OptionMenu(return_date_frame, date1, *dates)  # row 4
    month_dropdrown1 = OptionMenu(return_date_frame, month1, *months)
    year_dropdrown1 = OptionMenu(return_date_frame, year1, *years)
    date_dropdown1.config(bg="white")
    month_dropdrown1.config(bg="white")
    year_dropdrown1.config(bg="white")
    date_dropdown1.grid(row=0, column=0, padx=30)
    month_dropdrown1.grid(row=0, column=1, padx=30)
    year_dropdrown1.grid(row=0, column=2, padx=30)
    clicked5 = StringVar()
    clicked5.set("1:00 AM")
    time_op1 = OptionMenu(return_date_frame, clicked5, *time)
    time_op1.config(bg="white")
    time_op1.grid(row=0, column=3, padx=30, sticky="W")
    return_date_frame.grid(row=4, column=1)




    Label(kite, text="Coupon code", height=0, font=("Courier", 25), bg='white').grid(row=5, column=0)     #row 3
    Button(kite, text="Check", font=("Courier", 15), bg='white', command=lambda : cocheck()).grid(row=5, column=2, sticky='ew')
    e = StringVar()
    v = Entry(kite, font=30, textvariable=e)
    v.grid(row=5, column=1)


    Button(kite, text="Cancel", font=("Courier", 15), bg='white', command=lambda: valchanger(0)).grid(row=8, column=0,sticky='ew') #row 6
    Button(kite, text="Check fare", font=("Courier", 15), bg='white',command=transfer).grid(row=8, column=1, sticky='ew')

    Label(kite, text="book:", font=("Courier", 36), bg='white').grid(row=9, column=0, sticky='ew')   #row 7
    Button(kite, image=loginbtn, borderwidth=0,command=lambda : bypassbook()).grid(row=9, column=1)

    kite.mainloop()

def cancel():
    global u
    username = u
    def View():
        tree.delete(*tree.get_children())
        try:
            c.execute("SELECT * FROM {}".format(username))
        except:
            messagebox.showinfo("Bookings", "No Bookings")
        rows = c.fetchall()
        if rows != []:
            for row in rows:
                tree.insert("", END, values=row)

    root = Tk()
    root.title('Flight Management System')
    root.iconbitmap('samp.ico')
    def valchanger(b):
        root.destroy()
        win_choice(b)
    def cancel_bypass():
        c.execute("select * from {} where id={}".format(username, e.get()))
        if (c.fetchall() == []):
            messagebox.showerror("Booking","ID not found")
        else:
            p = messagebox.askyesno("Booking", "Are you sure you want to cancel the booking")
            if p == 1:
                c.execute("Delete FROM {} WHERE id = {}".format(username,e.get()))
                conn.commit()
                messagebox.showinfo("Booking", "You have successfully cancelled")
                View()
    def delete_txt(b):
        if delete_txt:
            e.set('')
    tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')

    tree.column("#1", anchor=CENTER)
    tree.heading("#1", text="Boarding")
    tree.column("#2", anchor=CENTER)
    tree.heading("#2", text="destination")
    tree.column("#3", anchor=CENTER)
    tree.heading("#3", text="day")
    tree.column("#4", anchor=CENTER)
    tree.heading("#4", text="time")
    tree.column("#5", anchor=CENTER)
    tree.heading("#5", text="class")
    tree.column("#6", anchor=CENTER)
    tree.heading("#6", text="fare")
    tree.column("#7", anchor=CENTER)
    tree.heading("#7", text="ID")
    tree.pack()
    View()
    e=StringVar()
    v=Entry(root, font=30, textvariable=e)
    e.set("Enter Booking ID")
    v.bind("<Button-1>",delete_txt)
    button2 = Button(text="Back", command=lambda: valchanger(0))
    button3 = Button(text="Cancel Booking", command=cancel_bypass)
    v.pack()
    button3.pack(padx=10, pady=10)
    button2.pack(padx=10, pady=10)

def games():

    root = Tk()
    def valchanger(b):
        root.destroy()
        win_choice(b)
    def game_changer():
        root.destroy()
        start()
        mainpage()
    Button(root, text="Rock Paper Scissor", font=("Courier", 15), bg='white', padx=110,command=lambda: game_changer()).grid(row=0, column=0,sticky='ew')
    Button(root, text="Back", font=("Courier", 15), bg='white', padx=110,command=lambda: valchanger(0)).grid(row=1, column=0,sticky='ew')
    root.mainloop()

def mainpage():
    root=Tk()
    def valchanger(b):
        root.destroy()
        win_choice(b)

    root.title('Flight Management System')
    root.iconbitmap('samp.ico')
    # root.geometry("400x400")
    loginbtn = PhotoImage(file='samp.png')
    root.configure(background='white')
    mylabel=Label(root,text="Flight Management System",height=0,font=("Courier",25),bg='white').grid(row=0,column=1)
    imglabel=Label(root,image=loginbtn).grid(row=0,column=0)
    Button(root,text="Book a flight",font=("Courier", 15), bg='white',padx=182,command=lambda: valchanger(1)).grid(row=1,column=0,columnspan=2)
    Button(root, text="Cancel a flight", font=("Courier", 15), bg='white',padx=170,command=lambda: valchanger(2)).grid(row=2, column=0, columnspan=2)
    Button(root, text="View your bookings", font=("Courier", 15), bg='white', padx=152,command=lambda: valchanger(5)).grid(row=3, column=0, columnspan=2)
    Button(root, text="play Games to win coupons", font=("Courier", 15), bg='white', padx=110,command=lambda: valchanger(3)).grid(row=4, column=0,columnspan=2)
    Button(root, text="Log out", font=("Courier", 15), bg='white', padx=23,command=lambda: valchanger(4)).grid(row=5, column=0,columnspan=2)
    root.mainloop()

check()


