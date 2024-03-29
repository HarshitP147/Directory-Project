
from tkinter import *
import tkinter.messagebox as ms
import mysql.connector as m
from PIL import ImageTk,Image
from tabulate import tabulate   

#Establishing a connection
con=m.connect()
cur=con.cursor()
cur.execute("create database if not exists Directory")
cur.execute("use directory")

#Making a Window application
root=Tk()
root.title('Project Telephone directory')
root.geometry('406x406')
root.resizable(0,0)
photo = PhotoImage(file='./prjicon.png')
root.iconphoto(False,photo)
root.focus()


#Creating Table
cur.execute("create table if not exists records"
            "(S_no  int(2)  primary key,"
            "Name  varchar(32)  not null,"
            "Mobile  int unique not null,"
            "Telephone  int unique not null,"
            "Email   varchar(32),"
            "Res_add  varchar(75))")

#Frames for different programs
fr=Frame(root)
fr.grid(row=0,column=0)

fr1=LabelFrame(root)
fr1.grid(row=1,column=0)

m_i = ImageTk.PhotoImage(Image.open("./directory.png"))
lb=Label(fr,image=m_i)
lb.grid(column=1)


#Function for the Buttons

#1. Displaying the records
def disp():
    root_1=Toplevel()
    root_1.title("Displaying of records")
    root_1.geometry('890x421')
    root_1.resizable(0,0)
    root_1.iconphoto(False,photo)

    def headers():
        cur.execute('select * from records')
        rs=cur.fetchall()
        cur.execute('desc records')
        lst=[]
        for i in cur.fetchall():
            lst.append(i[0])
        return lst,rs

    l,r=headers()
    x=tabulate(r,l,tablefmt='psql')
    tk=Text(root_1,width=110,borderwidth=2)
    tk.insert(INSERT,x)
    tk.pack()

    qt_b=Button(root_1,text="Done",padx=423.5,pady=2.5,command=root_1.destroy,relief='groove')
    qt_b.pack()

    root_1.mainloop()
 
#2. Lookup for a person
def lookup():
    root_2=Toplevel()
    root_2.title("Lookup for a person")
    root_2.geometry('344x279')
    root_2.resizable(0,0)
    root_2.iconphoto(False,photo)
    root_2.focus()
    
    fr=Frame(root_2)
    fr.grid(row=0,column=0)

    lb1=Label(fr,text="Enter the telephone number ")
    lb1.grid(row=2,column=0)

    et=Entry(fr,borderwidth=2,width=30)
    et.grid(row=2,column=1,columnspan=2)

    disp=Text(root_2,height=12,width=42)
    disp.grid(row=3,column=0,columnspan=1)


    def check():
        ph=et.get()
        disp.delete('1.0','end')
        
        if ph=='':
            ms.showerror('No data entered',"Please enter a telephone number!!")
        else:
            if str(ph).isnumeric()==True:
                cur.execute('select * from records where Telephone='+str(ph))
                res=cur.fetchall()
                if res==[]:
                    ms.showwarning("Empty record","No such record exists in this directory")
                else:
                    disp.insert(INSERT,'Name :'+res[0][1])
                    disp.insert(INSERT,'\nMob.:'+str(res[0][2]))
                    disp.insert(INSERT,'\nTele.:'+str(res[0][3]))
                    disp.insert(INSERT,'\nEmail:'+str(res[0][4]))
            else:
                ms.showerror("Error",'Please enter a proper telephone number!')
                
        et.delete(0,END)
        
    cb=Button(root_2,text="Check",command=check,padx=150,pady=3,relief='groove')
    cb.grid(row=2,column=0)

    qtb=Button(root_2,text="Done",command=root_2.destroy,padx=150,pady=3,relief='groove')
    qtb.grid(row=4,column=0)

    root_2.mainloop()
    
#3. Addition of new records    
def new_record():
    root_3=Toplevel()
    root_3.title("Add a record")
    root_3.iconphoto(False,photo)
    root_3.resizable(0,0)
    root_3.geometry('398x241')
    root_3.focus()

    con=m.connect(host='localhost',user='root',passwd='tiger')
    cur=con.cursor()
    cur.execute('use directory')

    #Frame for entry and label object
    fr=LabelFrame(root_3,padx=2,pady=5)
    fr.grid(row=0,column=0)

    lb1=Label(fr,text="Enter name of the person")
    lb1.grid(row=0,column=0)

    en1=Entry(fr,width=40,borderwidth=2)
    en1.grid(row=0,column=1)

    lb2=Label(fr,text="Enter mobile number")
    lb2.grid(row=1,column=0)

    en2=Entry(fr,width=40,borderwidth=2)
    en2.grid(row=1,column=1)

    lb3=Label(fr,text="Enter telephone number")
    lb3.grid(row=2,column=0)

    en3=Entry(fr,width=40,borderwidth=2)
    en3.grid(row=2,column=1)

    lb4=Label(fr,text="Enter E-mail address")
    lb4.grid(row=3,column=0)

    en4=Entry(fr,width=40,borderwidth=2)
    en4.grid(row=3,column=1)

    #res_add=res+city+pin
    lb5=Label(fr,text="Enter the address")
    lb5.grid(row=4,column=0)

    en5=Entry(fr,width=40,borderwidth=2)
    en5.grid(row=4,column=1)

    lb6=Label(fr,text="Enter the city")
    lb6.grid(row=5,column=0)

    en6=Entry(fr,width=40,borderwidth=2)
    en6.grid(row=5,column=1)

    lb7=Label(fr,text="Enter the PIN")
    lb7.grid(row=6,column=0)

    en7=Entry(fr,width=40,borderwidth=2)
    en7.grid(row=6,column=1)

    wr=Label(fr,text="Please enter proper values for the same",font=("Calibri",8),padx=98,relief='groove')
    wr.grid(row=7,columnspan=2)

    #Command for the button
    def add_rec():
        name=str(en1.get())
        mb=en2.get()
        tele=en3.get()
        eml=str(en4.get())
        ads=str(en5.get())+' '+str(en6.get())+' '+str(en7.get())
        
        def count():
            cur.execute("select S_no from records order by S_no ")
            rs=cur.fetchall()
            if rs==[]:
                return 1
            else:
                for x in rs:
                    k=x[0]
                return k+1
        sno=count()
       
        if name=='':
            ms.showwarning("Error",'No name entered! Please enter a name!!')
        
        elif mb=='' and tele=='':
            ms.showwarning("Error",'No number entered! Please enter a number')        
        else:
            try:
                if mb=='':
                    mb='NULL'
                if tele=='':
                    tele='NULL'
                elif eml=='':
                    eml='NULL'
                elif ads=='':
                    ads=='NULL'
                    
                rec=(sno,name,mb,tele,eml,ads)
                
                cur.execute("insert into records values"+str(rec))
                con.commit()
                
                ms.showinfo("Done",'This record is entered in the directory.')
                
                en1.delete(0,END)
                en2.delete(0,END)
                en3.delete(0,END)
                en4.delete(0,END)
                en5.delete(0,END)
                en6.delete(0,END)
                en7.delete(0,END)
                
            except m.errors.IntegrityError:
                ms.showerror("Error",'Telephone number already exists in the directory!!')

    Add=Button(root_3,text="Add the records",padx=152,pady=2.5,relief='groove',command=add_rec)
    Add.grid(row=1,column=0)

    dn=Button(root_3,text="Done",padx=180,pady=2.5,relief='groove',command=root_3.destroy)
    dn.grid(row=2,column=0)

    root_3.mainloop()
          
#4. Deleting a record  
def delete():
    root_4=Toplevel()
    root_4.title("Deleting Records")
    root_4.geometry('404x111')
    root_4.resizable(0,0)
    root_4.iconphoto(False,photo)
    root_4.focus()

    fr=LabelFrame(root_4)
    fr.grid(row=0,column=0)

    del_lb=Label(fr,text="Enter a telephone number to delete")
    del_lb.grid(row=0,column=0)

    del_en=Entry(fr,width=32,borderwidth=2)
    del_en.grid(row=0,column=1)

    def del_rec():
        tele=del_en.get()
        
        if tele=='':
            ms.showerror("Error",'Please enter a telephone number!')

        elif tele.isnumeric()==False:
            ms.showwarning("Error",'Please enter a proper telephone number!')
            del_en.delete(0,END)
        else:
            fn=ms.askyesno("Wait",'Are you sure you want to delete this record permanently?')
            if fn==True:
                cur.execute("delete from records where Telephone="+tele)
                con.commit()
                
                ms.showinfo("Done",'The record has been permanently deleted from this directory.')
                
                del_en.delete(0,END)

    dele=Button(fr,text="Delete this record",padx=148.5,pady=2.25,relief='groove',command=del_rec)
    dele.grid(row=1,column=0,columnspan=2)

    chk=Button(fr,text="Check current records",padx=137,pady=2.25,relief='groove')
    chk.grid(row=2,column=0,columnspan=2)

    dn=Button(root_4,text="Done",padx=183,pady=2.25,relief='groove',command=root_4.destroy)
    dn.grid(row=1,column=0)

    root_4.mainloop()
              
#5. Closing of the directory
def destroy():
    x=ms.askokcancel("Quit","Are you sure you want to close the Directory?")
    if x==1:
        root.destroy()
    
#Frame 2 -Buttons
show_rec=Button(fr1,text='Display all the present telephone numbers',command=disp,padx=87,pady=5)
show_rec.grid(row=1,column=0,columnspan=3)

lookup=Button(fr1,text='Lookup for a person',padx=143.5,pady=5,command=lookup)
lookup.grid(row=2,column=0,columnspan=3)

adding=Button(fr1,text="Addition of a new number",command=new_record,padx=128.25,pady=5)
adding.grid(row=3,column=0,columnspan=3)

root_4=Button(fr1,text="Delete records",padx=159.5,pady=5,command=delete)
root_4.grid(row=4,column=0,columnspan=3)

leave=Button(fr1,text="Close Directory",command=destroy,padx=157.5,pady=5)
leave.grid(row=5,column=0,columnspan=3)


root.mainloop()