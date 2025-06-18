import gmail
email='xxxxxxxxx@gmail.com'     #mention your gmail id
app_pass='xxxxxxxxx'            #mention app pass of same gmail account

def send_mail_for_openacn(to_mail,uacno,uname,upass,udate):
        con=gmail.GMail(email,app_pass)
        sub='Account Opened with Canara Bank'

        body=f"""Dear {uname},
        Your account has been opened successfuly with Canara Bank and details are
    ACN = {uacno}
    Pass = {upass}
    Open date = {udate}

    Kindly change your password when you login first time
    Thanks
    Canara Bank
    Aligarh
    """
        msg=gmail.Message(to=to_mail,subject=sub,text=body)
        con.send(msg)

def send_otp(to_mail,uname,uotp):
    con=gmail.GMail(email,app_pass)
    sub='OTP for password recovery'
    body=f"""Dear {uname},
        Your OTP to get password = {uotp}
  
    Kindly verify this otp to applicaation
    Thanks
    Canara Bank
    Aligarh
    """
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)
