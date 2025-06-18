#impot TK,Label,Frame,Entry componant
from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter import *
from time import strftime
#import combobox class
from tkinter.ttk import Combobox
import os,shutil                        
import time
from PIL import Image,ImageTk
import random
import project_tables
import sqlite3
import project_mails

#generate captcha code
def generate_captcha():
    captcha=[]
    for i in range(3):
        c=chr(random.randint(65,90))
        captcha.append(c)

        n=random.randint(0,9)
        captcha.append(str(n))
    
    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh():
    captcha=generate_captcha()
    captcha_lbl.configure(text=captcha)

root=Tk()                                               
root.state("zoomed")                                    
root.configure(bg='sky blue')
root.title("Canara Bank")                               
root.resizable(width=False,height=False)

title_lbl=Label(root,text="Canara Bank Automation",bg="sky blue",font=('Arial',40,"bold","underline"))           
title_lbl.pack()

today_lbl=Label(root,text=time.strftime("%A,%d %B %Y"),bg="sky blue",font=('Arial',13,"bold"),fg='blue')
today_lbl.pack(pady=5)

time_lbl = Label(root,bg="sky blue",fg="blue",font=('Arial', 13, 'bold'))
time_lbl.pack(pady=2)

# Function to update time
def show_time():
    time_lbl.config(text=strftime('%I:%M:%S %p'))
    time_lbl.after(1000, show_time)

show_time()

right_img=Image.open("images/logo.jpg").resize((300,140))
right_img_bitmap=ImageTk.PhotoImage(right_img,master=root)

logo_lbl=Label(root,image=right_img_bitmap)
logo_lbl.place(relx=.81,rely=0) 

left_img=Image.open("images/logo2.jpg").resize((300,140))
left_img_bitmap=ImageTk.PhotoImage(left_img,master=root)

logo_lbl=Label(root,image=left_img_bitmap)
logo_lbl.place(relx=0,rely=0) 

footer_lbl=Label(root,text="Developed By:Raunak Bharti",bg='sky blue',fg='blue',font=('Arial',12,"bold"))
footer_lbl.pack(side='bottom',pady=5)


def main_screen():
    #create forgot function
    def forgot():
        frm.destroy()
        forgot_screen()
        
    #create login function
    def login():
        uacn=acn_entry.get()
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget("text")
        actual_cap=actual_cap.replace(' ','')
        
        if utype=="Admin":
            if uacn=='0' and upass=="admin":
                if ucap==actual_cap:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid captcha')
            else:
                messagebox.showerror('Login','Invalid ACN/PASS/TYPE')
        elif utype=="User":
            if ucap==actual_cap:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and accounts_pass'
                curobj.execute(query,(uacn,))

                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("User","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(uacn)

            else:
                messagebox.showerror('Login','Invalid captcha')
            
        else:
            messagebox.showerror("Login","Kindly Select Valid User Type")
    
    def reset():
        user_combo.set('----Select-----')
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        inputcap_entry.delete(0,"end")

    frm=Frame(root)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)

    user_lbl=Label(frm,text="User Type",bg='white',fg='black',font=('Arial',15,"bold"))
    user_lbl.place(relx=.3,rely=.1)

    #create 'Admin','User' and state 
    user_combo=Combobox(frm,values=['Admin','User','----Select----'],font=('',15),state='readonly')
    user_combo.current(2)
    user_combo.place(relx=.45,rely=.1)

    #create acn_lbl code
    acn_lbl=Label(frm,text="ACN",bg='white',fg='black',font=('Arial',15,"bold"))
    acn_lbl.place(relx=.3,rely=.2)

    #user input acn
    acn_entry=Entry(frm,font=('Arial',15),bd=5)
    acn_entry.place(relx=.45,rely=.2)
    acn_entry.focus()

    #create password code
    pass_lbl=Label(frm,text="Pass",bg='white',fg='black',font=('Arial',15,"bold"))
    pass_lbl.place(relx=.3,rely=.3)

    pass_entry=Entry(frm,font=('Arial',15),bd=5,show="*")
    pass_entry.place(relx=.45,rely=.3)

    #create captcha code
    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),bg='sky blue',fg='black',font=('Arial',15,"bold"))
    captcha_lbl.place(relx=.45,rely=.4)

    #Refresh img_button
    refresh_btn_img=Image.open("images/refresh.png").resize((80,50))
    refresh_btn_img_bitmap=ImageTk.PhotoImage(refresh_btn_img,master=root)

    refresh_lbl=Label(frm,image=refresh_btn_img_bitmap,bg='white', cursor="hand2")
    refresh_lbl.place(relx=.55,rely=.39)

    #Prevent garbage collection
    refresh_lbl.image = refresh_btn_img_bitmap  

    # ---- Bind click to refresh ----
    refresh_lbl.bind("<Button-1>", lambda event: refresh())

    #create text field
    inputcap_lbl=Label(frm,text="Captcha",bg='white',fg='black',font=('Arial',15,"bold"))
    inputcap_lbl.place(relx=.3,rely=.5)

    inputcap_entry=Entry(frm,font=('Arial',15),bd=5)
    inputcap_entry.place(relx=.45,rely=.5)

    #create login button
    login_btn=Button(frm,text="login",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=login)
    login_btn.place(relx=.48,rely=.6)

    #create reset button
    reset_btn=Button(frm,text="reset",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=reset)
    reset_btn.place(relx=.55,rely=.6)

    #create forgot_password button
    forgot_btn=Button(frm,text="forgot password",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=forgot)
    forgot_btn.place(relx=.48,rely=.7)

#create new_frame after login
def admin_screen():
    def open_acn():
        #create new fun open_acn_db
        def open_acn_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            ugender=gender_combo.get()
            ubal=0.0
            uopendate=time.strftime("%A,%d %B %Y")
            upass=generate_captcha().replace(' ','')

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            
            query='insert into accounts values(null,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,ugender,uopendate,ubal))
            conobj.commit()
            conobj.close()
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query="Select max(accounts_acno) from accounts"
            curobj.execute(query)

            uacno=curobj.fetchone()[0]
            conobj.close()

            try:
                project_mails.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                msg=f'Account opened with ACN {uacno} and mail sent to {uemail},Kindly check spam also '
                messagebox.showinfo('Open Account',msg)
            except Exception as msg:
                messagebox.showerror("Open Account",msg)

        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            gender_combo.current(3)
            name_entry.focus()

        #create iframe after click open_btn
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is open account screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()

        name_lbl=Label(ifrm,text="Name",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        name_lbl.place(relx=.1,rely=.12)

        name_entry=Entry(ifrm,font=('Arial',15),bd=5)
        name_entry.place(relx=.1,rely=.2)
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        email_lbl.place(relx=.39,rely=.43)

        email_entry=Entry(ifrm,font=('Arial',15),bd=5)
        email_entry.place(relx=.39,rely=.5)

        pan_lbl=Label(ifrm,text="Pan",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        pan_lbl.place(relx=.1,rely=.43)

        pan_entry=Entry(ifrm,font=('Arial',15),bd=5)
        pan_entry.place(relx=.1,rely=.5)

        mob_lbl=Label(ifrm,text="Mob",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        mob_lbl.place(relx=.39,rely=.12)

        mob_entry=Entry(ifrm,font=('Arial',15),bd=5)
        mob_entry.place(relx=.39,rely=.2)

        aadhar_lbl=Label(ifrm,text="Aadhar",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        aadhar_lbl.place(relx=.68,rely=.12)

        aadhar_entry=Entry(ifrm,font=('Arial',15),bd=5)
        aadhar_entry.place(relx=.68,rely=.2)

        gender_lbl=Label(ifrm,text="Gender",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        gender_lbl.place(relx=.68,rely=.43)

        gender_combo=Combobox(ifrm,values=['Male','Female','Others','----Select----'],font=('',15),state='readonly')
        gender_combo.current(3)
        gender_combo.place(relx=.68,rely=.5)

        open_btn=Button(ifrm,width=15,text="open_account",bg="white",font=('Arial',15,"bold"),fg="black",bd=5,command=open_acn_db)
        open_btn.place(relx=.3,rely=.7)

        reset_btn=Button(ifrm,command=reset,width=15,text="reset",bg="white",font=('Arial',15,"bold"),fg="black",bd=5)
        reset_btn.place(relx=.6,rely=.7)

    def delete_acn():
        def send_otp():
            uacn=acn_entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Delete Account","Record not found")
            else:
                otp=str(random.randint(1000,9999))
                project_mails.send_otp(tup[3],tup[1],otp)
                messagebox.showinfo('Delete Account','otp send to registered mail id')

                otp_entry=Entry(ifrm,font=('Arial',15),bd=5)
                otp_entry.place(relx=.45,rely=.5)

                def verify():
                    uotp=otp_entry.get()
                    if otp==uotp:
                        resp=messagebox.askyesno("Delete Account",f"Do you want to delete this account?")
                        if not resp:
                            frm.destroy()
                            admin_screen()
                            return
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='delete from accounts where accounts_acno=?'
                        curobj.execute(query,(uacn,))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("Delete Account","Account Deleted")
                        frm.destroy()
                        admin_screen()
                    else:
                        messagebox.showerror("Delete Account","Incorrect OTP")

                verify_btn=Button(ifrm,command=verify,text="Verify",bg="sky blue",font=('Arial',15,"bold"),bd=5)
                verify_btn.place(relx=.7,rely=.5) 

        #create iframe after click delete_btn
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is delete account screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()
 
        acn_lbl=Label(ifrm,text="ACN",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        acn_lbl.place(relx=.3,rely=.2)

        acn_entry=Entry(ifrm,font=('Arial',15),bd=5)
        acn_entry.place(relx=.45,rely=.2)
        acn_entry.focus()

        otp_btn=Button(ifrm,command=send_otp,text="Send OTP",bg="white",font=('Arial',15,"bold"),bd=5)
        otp_btn.place(relx=.49,rely=.6)
        

    def view_acn():
        def view_details():
            uacn=acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("View Account","Record not found")
            else:
                # show details as labels
                user_lbl = Label(ifrm ,text="User Name = " + tup[1],bg='white', font=('Arial', 13, "bold"))
                user_lbl.place(relx=.3, rely=.5)

                user_lbl = Label(ifrm,text="Aval Bal = " + str(tup[7]),bg='white', font=('Arial', 13, "bold"))
                user_lbl.place(relx=.3, rely=.57)

                user_lbl = Label(ifrm,text="ACN Open date = " + tup[6],bg='white', font=('Arial', 13, "bold"))
                user_lbl.place(relx=.3, rely=.64)
                
                user_lbl = Label(ifrm,text="Email = " + tup[3],bg='white', font=('Arial', 13, "bold"))
                user_lbl.place(relx=.3, rely=.71)

                user_lbl = Label(ifrm,text="Mob = " + tup[4],bg='white', font=('Arial', 13, "bold"))
                user_lbl.place(relx=.3, rely=.78) 
               
        #create iframe after click delete_btn
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.15,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is view account screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()

        acn_lbl=Label(ifrm,text="ACN",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        acn_lbl.place(relx=.3,rely=.2)

        acn_entry=Entry(ifrm,font=('Arial',15),bd=5)
        acn_entry.place(relx=.45,rely=.2)
        acn_entry.focus()

        view_btn=Button(ifrm,command=view_details,text="View",bg="white",font=('Arial',15,"bold"),bd=5)
        view_btn.place(relx=.7,rely=.7)

    def logout():
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()
            main_screen()

    frm=Frame(root)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)

    wel_lbl=Label(frm,text="Welcome Admin",bg='white',font=('Arial',15,"bold"),fg='blue')
    wel_lbl.place(relx=.0,rely=.0)

    logout_btn=Button(frm,width=14,text="logout",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=logout)
    logout_btn.place(relx=.88,rely=0)

    open_btn=Button(frm,width=15,text="open_account",bg="white",font=('Arial',15,"bold"),fg="blue",bd=5,command=open_acn)
    open_btn.place(relx=.26,rely=0)

    delete_btn=Button(frm,width=15,text="delete_account",bg="white",font=('Arial',15,"bold"),fg="blue",bd=5,command=delete_acn)
    delete_btn.place(relx=.43,rely=0)

    view_btn=Button(frm,width=15,text="view_account",bg="white",font=('Arial',15,"bold"),fg="blue",bd=5,command=view_acn)
    view_btn.place(relx=.6,rely=0)

#create forgot screen
def forgot_screen():
    def back():
        frm.destroy()
        main_screen()

    def send_otp():
        uacn=acn_entry.get()
        uemail=email_entry.get()
        ucaptcha=inputcap_entry.get()
        if ucaptcha!=forgot_captcha.replace(' ',''):
            messagebox.showerror('forgot password','Invalid captcha')
            return

        #authenticate acn & email
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))

        tup=curobj.fetchone()
        curobj.close()
        if tup==None:
            messagebox.showerror("Forgot Password","Record not found")
        else:
            otp=str(random.randint(1000,9999))
            project_mails.send_otp(uemail,tup[1],otp)
            messagebox.showinfo('Forgot Pass','otp send to given/registered mail id')

            otp_entry=Entry(frm,font=('Arial',15),bd=5)
            otp_entry.place(relx=.45,rely=.7)

            def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    messagebox.showinfo("Forgot Password",f"Your Pass = {tup[2]}")
                else:
                    messagebox.showerror("Forgot Password","Incorrect OTP")
            verify_btn=Button(frm,command=verify,text="Verify",bg="sky blue",font=('Arial',15,"bold"),bd=5)
            verify_btn.place(relx=.7,rely=.7)            
      
    frm=Frame(root)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)

    back_btn=Button(frm,width=15,text="back",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=back)
    back_btn.place(relx=0,rely=0)

    acn_lbl=Label(frm,text="ACN",bg='white',fg='black',font=('Arial',15,"bold"))
    acn_lbl.place(relx=.3,rely=.2)

    acn_entry=Entry(frm,font=('Arial',15),bd=5)
    acn_entry.place(relx=.45,rely=.2)
    acn_entry.focus()

    email_lbl=Label(frm,text="Email",bg='white',fg='black',font=('Arial',15,"bold"))
    email_lbl.place(relx=.3,rely=.3)

    email_entry=Entry(frm,font=('Arial',15),bd=5)
    email_entry.place(relx=.45,rely=.3)

    #create captcha for forgot screen
    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg='sky blue',fg='black',font=('Arial',15,"bold"))
    captcha_lbl.place(relx=.45,rely=.4)

    refresh_btn_img=Image.open("images/refresh.png").resize((80,50))
    refresh_btn_img_bitmap=ImageTk.PhotoImage(refresh_btn_img,master=root)

    refresh_lbl=Label(frm,image=refresh_btn_img_bitmap,bg='white', cursor="hand2")
    refresh_lbl.place(relx=.55,rely=.39)

    refresh_lbl.image = refresh_btn_img_bitmap  

    refresh_lbl.bind("<Button-1>", lambda event: refresh())

    inputcap_entry=Entry(frm,font=('Arial',15),bd=5)
    inputcap_entry.place(relx=.45,rely=.5)

    otp_btn=Button(frm,command=send_otp,text="Send OTP",bg="sky blue",font=('Arial',15,"bold"),bd=5)
    otp_btn.place(relx=.46,rely=.6)

    reset_btn=Button(frm,text="reset",bg="sky blue",font=('Arial',15,"bold"),bd=5)
    reset_btn.place(relx=.55,rely=.6)

#create user screen
def user_screen(uacn=None):
    def logout():
        resp=messagebox.askyesno("logout","Do you want to logout?")
        if resp:
            frm.destroy()
            main_screen()

    def update_btn_screen():
        def update_db():
            uname=name_entry.get()
            upass=pass_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            upan=pan_entry.get()
            uaadhar=aadhar_entry.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query='update accounts set accounts_name=?,accounts_pass=?,accounts_email=?,accounts_mob=?,accounts_pan=?,accounts_aadhar=? where accounts_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,upan,uaadhar,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","Profile Updated")
            frm.destroy()
            user_screen(uacn)

        #create iframe for update
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is update screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        name_lbl=Label(ifrm,text="Name",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        name_lbl.place(relx=.1,rely=.12)

        name_entry=Entry(ifrm,font=('Arial',15),bd=5)
        name_entry.place(relx=.1,rely=.2)
        name_entry.insert(0,tup[1])
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        email_lbl.place(relx=.39,rely=.43)

        email_entry=Entry(ifrm,font=('Arial',15),bd=5)
        email_entry.place(relx=.39,rely=.5)
        email_entry.insert(0,tup[3])

        pan_lbl=Label(ifrm,text="Pan",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        pan_lbl.place(relx=.1,rely=.43)

        pan_entry=Entry(ifrm,font=('Arial',15),bd=5)
        pan_entry.place(relx=.1,rely=.5)
        pan_entry.insert(0,tup[5])

        mob_lbl=Label(ifrm,text="Mob",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        mob_lbl.place(relx=.39,rely=.12)

        mob_entry=Entry(ifrm,font=('Arial',15),bd=5)
        mob_entry.place(relx=.39,rely=.2)
        mob_entry.insert(0,tup[4])

        aadhar_lbl=Label(ifrm,text="Aadhar",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        aadhar_lbl.place(relx=.68,rely=.12)

        aadhar_entry=Entry(ifrm,font=('Arial',15),bd=5)
        aadhar_entry.place(relx=.68,rely=.2)
        aadhar_entry.insert(0,tup[6])

        pass_lbl=Label(ifrm,text="Pass",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        pass_lbl.place(relx=.68,rely=.43)
        
        pass_entry=Entry(ifrm,font=('Arial',15),bd=5)
        pass_entry.place(relx=.68,rely=.5)
        pass_entry.insert(0,tup[2])

        update_btn=Button(ifrm,width=15,text="Update",bg="white",font=('Arial',15,"bold"),fg="black",bd=5,command=update_db)
        update_btn.place(relx=.55,rely=.7)

    def deposit_btn_screen():
        def deposit():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            t=str(time.time())
            utxnid='txn'+t[:t.index('.')]
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into stmts values(?,?,?,?,?,?)'
            curobj.execute(query,(uacn,uamt,'CR.',time.strftime("%d-%m-%Y %r"),ubal,utxnid))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn)

        #create iframe for deposit
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is deposit screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()

        amt_lbl=Label(ifrm,text="Amount",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        amt_lbl.place(relx=.3,rely=.2)

        amt_entry=Entry(ifrm,font=('Arial',15),bd=5)
        amt_entry.place(relx=.45,rely=.2)
        amt_entry.focus()

        dep_btn=Button(ifrm,command=deposit,text="Deposit",bg="white",font=('Arial',15,"bold"),bd=5)
        dep_btn.place(relx=.49,rely=.6)
        
    def withdraw_btn_screen():
        def withdraw():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()

                t=str(time.time())
                utxnid='txn'+t[:t.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='insert into stmts values(?,?,?,?,?,?)'
                curobj.execute(query,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y %r"),ubal-uamt,utxnid))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw",f"{uamt} Amount Withdrawn")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Withdraw",f"Insufficiant Bal {ubal}")
        
        #create iframe for withdraw
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is withdraw screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()
    
        amt_lbl=Label(ifrm,text="Amount",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        amt_lbl.place(relx=.3,rely=.2)

        amt_entry=Entry(ifrm,font=('Arial',15),bd=5)
        amt_entry.place(relx=.45,rely=.2)
        amt_entry.focus()

        dep_btn=Button(ifrm,command=withdraw,text="Withdraw",bg="white",font=('Arial',15,"bold"),bd=5)
        dep_btn.place(relx=.49,rely=.6)
        

    def check_btn_screen():
        #create iframe for check
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is check details screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        details=f'''Account No. = {tup[0]}

        Opening date = {tup[6]}

        Available Bal = {tup[7]}

        Email Id = {tup[3]}

        Mob No. = {tup[4]}
'''
        details_lbl=Label(ifrm,text=details,bg='white',fg='black',font=('arial','13','bold'))
        details_lbl.place(relx=.33,rely=.25)

    def transfer_btn_screen():
        def transfer():
            toacn=to_entry.get()
            uamt=float(amt_entry.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(toacn,))
            to_tup=curobj.fetchone()[0]
            conobj.close()

            if to_tup==None:
                messagebox.showerror("Transfer","To ACN does not exist")
                return


            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query_deduct='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                query_credit='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
                
                curobj.execute(query_deduct,(uamt,uacn))
                curobj.execute(query_credit,(uamt,toacn))

                conobj.commit()
                conobj.close()

                t=str(time.time())
                utxnid1='txn_db'+t[:t.index('.')]
                utxnid2='txn_cr'+t[:t.index('.')]

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='insert into stmts values(?,?,?,?,?,?)'
                query2='insert into stmts values(?,?,?,?,?,?)'
               
                curobj.execute(query1,(uacn,uamt,'DB.',time.strftime("%d-%m-%Y %r"),ubal-uamt,utxnid1))
                curobj.execute(query2,(toacn,uamt,'CR.',time.strftime("%d-%m-%Y %r"),ubal+uamt,utxnid2))

                conobj.commit()
                conobj.close()

                messagebox.showinfo("Transfer",f"{uamt} Amount Transfer")
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer",f"Insufficiant Bal {ubal}")
        
        

        #create iframe for transfer
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is transfer screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()
              
        to_lbl=Label(ifrm,text="TO ACN",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        to_lbl.place(relx=.3,rely=.2)

        to_entry=Entry(ifrm,font=('Arial',15),bd=5)
        to_entry.place(relx=.45,rely=.2)
        to_entry.focus()

        amt_lbl=Label(ifrm,text="Amount",bg='sky blue',fg='black',font=('Arial',15,"bold"))
        amt_lbl.place(relx=.3,rely=.4)

        amt_entry=Entry(ifrm,font=('Arial',15),bd=5)
        amt_entry.place(relx=.45,rely=.4)

        tr_btn=Button(ifrm,command=transfer,text="Transfer",bg="white",font=('Arial',15,"bold"),bd=5)
        tr_btn.place(relx=.49,rely=.6)
        
    def history_btn_screen():
        ifrm=Frame(frm,highlightcolor='blue',highlightthickness=3,highlightbackground='blue')
        ifrm.configure(bg='sky blue')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)

        title_lbl=Label(ifrm,text="This is txn history screen",bg='sky blue',font=('Arial',15,"bold"),fg='black')
        title_lbl.pack()

        import tktable
        table_headers=("Txn ID","Amount","Txn Type","Updated Bal","Date")
        mytable=tktable.Table(ifrm,table_headers,col_width=150,headings_bold=True)
        mytable.pack(pady=10)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select stmts_txnid,stmts_amt,stmts_type,stmts_update_bal,stmts_date from stmts where stmts_acn=?'
        curobj.execute(query,(uacn,))
        for tup in curobj:
            mytable.insert_row(tup)
        conobj.close()
        import sys
        del sys.modules['tktable']

    def getdetail():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=?'
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        return tup
    
    def update_picture():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'images/{uacn}.png')

        profile_img=Image.open(f"images/{uacn}.png").resize((150,130))
        bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
        profile_img_lbl.image=bitmap_profile_img
        profile_img_lbl.configure(image=bitmap_profile_img)

    frm=Frame(root)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.8)


    wel_lbl=Label(frm,text=f"Welcome,{getdetail()[1]}",bg='white',font=('Arial',15,"bold"),fg='blue')
    wel_lbl.place(relx=.0,rely=.0)

    logout_btn=Button(frm,width=14,text="logout",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=logout)
    logout_btn.place(relx=.88,rely=0)

    if os.path.exists(f'images/{uacn}.png'):
        path=f"images/{uacn}.png"
    else:
        path="images/default_pic.jpg"
        
    profile_img=Image.open(path).resize((150,130))
    bitmap_profile_img=ImageTk.PhotoImage(profile_img,master=root)
    profile_img_lbl=Label(frm,image=bitmap_profile_img)
    profile_img_lbl.image=bitmap_profile_img
    profile_img_lbl.place(relx=.005,rely=.1)
  
    update_pic=Button(frm,command=update_picture,width=13,text="update picture",bg="sky blue",font=('Arial',15,"bold"),bd=5)
    update_pic.place(relx=.0,rely=.3)

    check_btn=Button(frm,width=13,text="check details",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=check_btn_screen)
    check_btn.place(relx=.0,rely=.4)

    deposit_btn=Button(frm,width=13,text="deposit",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=deposit_btn_screen)
    deposit_btn.place(relx=.0,rely=.5)

    withdraw_btn=Button(frm,width=13,text="withdraw",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=withdraw_btn_screen)
    withdraw_btn.place(relx=.0,rely=.6)

    update_btn=Button(frm,width=13,text="update",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=update_btn_screen)
    update_btn.place(relx=.0,rely=.7)

    transfer_btn=Button(frm,width=13,text="transfer",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=transfer_btn_screen)
    transfer_btn.place(relx=.0,rely=.8)

    history_btn=Button(frm,width=13,text="history",bg="sky blue",font=('Arial',15,"bold"),bd=5,command=history_btn_screen)
    history_btn.place(relx=.0,rely=.9)

main_screen()
root.mainloop()                                        




















