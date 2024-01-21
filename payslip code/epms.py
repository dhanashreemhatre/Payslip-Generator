import tkinter as tk
from jinja2 import Environment, FileSystemLoader
import sqlite3,time,os
from tkinter import messagebox,ttk
from tkcalendar import DateEntry 
import webbrowser
from pyhtml2pdf import converter
from babel import numbers

class EmployeeSystem:
    def __init__(self,root):
        self.root=root
        self.root.title("Employee Payroll Management System | Developed for Aetos Digital")

        # -----------------databasecreation--------------------#
          # Connect to SQLite database
        con = sqlite3.connect('epm.db')
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_code INTEGER PRIMARY KEY,
                designation TEXT,
                name TEXT,
                email TEXT,
                department TEXT,
                dob TEXT,
                doj TEXT,
                contact TEXT,
                UAN TEXT,
                bank_account TEXT,
                pan_number TEXT
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS emp_salary (
                salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_code INTEGER,
                month TEXT,
                year INTEGER,
                absents INTEGER,
                total_days INTEGER,
                base_salary DECIMAL(10, 2),
                std_da DECIMAL(10, 2),
                medical DECIMAL(10, 2),
                hra DECIMAL(10, 2),
                other_allowance DECIMAL(10, 2),
                educational_allowance DECIMAL(10, 2),
                conveyence DECIMAL(10,2),
                professional_tax DECIMAL(10, 2),
                pf DECIMAL(10, 2),
                esic DECIMAL(10, 2),
                net_salary DECIMAL(10, 2),
                FOREIGN KEY (emp_code) REFERENCES employees(emp_code) ON DELETE CASCADE
            )
        ''')

        con.commit()
        con.close()


        self.root.geometry("1366x768+0+0")
        self.root.config(bg="#292826")
        title=tk.Label(self.root,text="Employee Payroll Management System",font=("times new roman",30,"bold"),bg="#292826",fg="white",anchor="w",padx=10)
        title.place(x=0,y=0,relwidth=1)
        button_emp=tk.Button(self.root,text="Emplopyee Salary",command=self.employee_salary_frame,font=("times new roman",13),bg="#292826",fg="white",activebackground="#efefef")
        button_emp.place(x=900,y=10,height=30,width=140)
        button_emp=tk.Button(self.root,text="All Employees",command=self.employee_frame,font=("times new roman",13),bg="#292826",fg="white",activebackground="#efefef")
        button_emp.place(x=1050,y=10,height=30,width=140)
        button_logout=tk.Button(self.root,text="Log Out",command=self.logout,font=("times new roman",13),bg="#292826",fg="white",activebackground="#efefef")
        button_logout.place(x=1200,y=10,height=30,width=140)
        
        ##-----------TTK Styling----------------##
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TCombobox', background = 'gray',foreground="black")
        style.map('TCombobox', fieldbackground=[('readonly','#292826')])
        style.configure("Treeview",background="#292826",foreground="White",fieldbackground="#292826")
        style.map('Treeview',background=[('selected',"#292826")],foreground=[('selected','#efefef')])
        
        ##------------------------------------Frame 1-------------#-----------------#
        #--------------Variables-----------------#
        self.var_emp_code=tk.StringVar()
        self.var_designation=tk.StringVar()
        self.var_name=tk.StringVar()
        self.var_email=tk.StringVar()
        self.var_department=tk.StringVar()
        self.var_dob=tk.StringVar()
        self.var_doj=tk.StringVar()
        self.var_contact=tk.StringVar()
        self.var_uan_no=tk.StringVar()
        self.var_bank_acc=tk.StringVar()
        self.var_pan_no=tk.StringVar()
        
        Frame1=tk.Frame(self.root,bd=3,relief=tk.RIDGE,bg="#292826")
        Frame1.place(x=10,y=70,width=750,height=430)
        
        title2=tk.Label(Frame1,text="Employee Details",font=("times new roman",20),bg="#292826",fg="#efefef",anchor="w",padx=10)
        title2.place(x=0,y=0,relwidth=1)
        
        lbl_code=tk.Label(Frame1,text="Employee Code*",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_code.place(x=10,y=38)
        self.txt_code=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_emp_code,bg="#292826",fg="White")
        self.txt_code.place(x=250,y=40,width=200)
        button_search=tk.Button(Frame1,text="Search",command=self.search,font=("times new roman",18),bg="#292826",fg="#efefef",activebackground="#efefef")
        button_search.place(x=480,y=40,height=30)
        
        #--------Row 1--------#
        lbl_designation=tk.Label(Frame1,text="Designation",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_designation.place(x=10,y=80)
        txt_designation=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_designation,bg="#292826",fg="White")
        txt_designation.place(x=170,y=80,width=200)
        
        lbl_dob=tk.Label(Frame1,text="D.O.B",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_dob.place(x=410,y=80)
        txt_dob=DateEntry(Frame1,font=("times  new roman",13),textvariable=self.var_dob,bg="#292826",fg="White",date_pattern="yyyy-mm-dd")
        txt_dob.place(x=520,y=80,width=200)
        
        #--------Row 2----------#
        lbl_name=tk.Label(Frame1,text="Name*",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_name.place(x=10,y=120)
        txt_name=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_name,bg="#292826",fg="White")
        txt_name.place(x=170,y=120,width=200)
        
        lbl_doj=tk.Label(Frame1,text="D.O.J",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_doj.place(x=410,y=120)
    
        doj_picker = DateEntry(
            Frame1,
            font=("times new roman", 13),
            textvariable=self.var_doj,
            bg="#454545",  # Change background color
            fg="white",    # Change text color
            date_pattern="yyyy-mm-dd"
        )
        doj_picker.place(x=520, y=120, width=200)
        
        
        #----------Row 3-------------#
        lbl_email=tk.Label(Frame1,text="Email*",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_email.place(x=10,y=160)
        txt_email=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_email,bg="#292826",fg="White")
        txt_email.place(x=170,y=160,width=200)
        
        lbl_contact=tk.Label(Frame1,text="Contact",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_contact.place(x=410,y=160)
        txt_contact=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_contact,bg="#292826",fg="White")
        txt_contact.place(x=520,y=160,width=200)
        
        #----------Row 4----------------#
        lbl_department=tk.Label(Frame1,text="Department",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_department.place(x=10,y=200)
        txt_department=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_department,bg="#292826",fg="White")
        txt_department.place(x=170,y=200,width=200)
        
        lbl_uan_no=tk.Label(Frame1,text="UAN",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_uan_no.place(x=410,y=200)
        txt_uan_no=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_uan_no,bg="#292826",fg="White")
        txt_uan_no.place(x=520,y=200,width=200)

        #----------Row 5----------------#
        lbl_bank_acc=tk.Label(Frame1,text="Bank Account No.",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_bank_acc.place(x=10,y=240)
        txt_bank_acc=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_bank_acc,bg="#292826",fg="White")
        txt_bank_acc.place(x=170,y=240,width=200)
        
        lbl_pan_no=tk.Label(Frame1,text="PAN No.",font=("times new roman",16),bg="#292826",fg="#efefef")
        lbl_pan_no.place(x=410,y=240)
        txt_pan_no=tk.Entry(Frame1,font=("times  new roman",13),textvariable=self.var_pan_no,bg="#292826",fg="White")
        txt_pan_no.place(x=520,y=240,width=200)

         #--------Row 6------------#
        self.button_save=tk.Button(Frame1,text="Save",command=self.save_emp_data,font=("times new roman",18),bg="#292826",fg="white",activebackground="#efefef")
        self.button_save.place(x=170,y=300,height=30,width=120)

        self.button_update=tk.Button(Frame1,text="Update",state=tk.DISABLED,command=self.update,font=("times new roman",18),bg="#292826",fg="white",activebackground="#efefef")
        self.button_update.place(x=310,y=300,height=30,width=120)
        
        self.button_delete=tk.Button(Frame1,text="Delete",state=tk.DISABLED,command=self.delete,font=("times new roman",18),bg="#292826",fg="White",activebackground="#efefef")
        self.button_delete.place(x=450,y=300,height=30,width=120)
        
        
        ##------------------------------Frame2---------------------------##
        #---------------Variables------------#
        self.var_month=tk.StringVar()
        self.var_year=tk.StringVar()
        self.var_absents=tk.StringVar()
        self.var_t_days=tk.StringVar()
        self.var_b_salary=tk.StringVar()
        self.var_medical=tk.StringVar()
        self.var_hra=tk.StringVar()
        self.var_standard_da=tk.StringVar()
        self.var_educational_allowance=tk.StringVar()
        self.var_conveyence=tk.StringVar()
        self.var_other_allowance =tk.StringVar()
        self.var_professional_tax=tk.StringVar()
        self.var_esic=tk.StringVar()
        self.var_pf=tk.StringVar()
        self.var_n_salary=tk.StringVar()

        Frame2=tk.Frame(self.root,bd=3,relief=tk.RIDGE,bg="#292826")
        Frame2.place(x=770,y=70,width=580,height=670)
        
        title3=tk.Label(Frame2,text="Employee Salary Details",font=("times new roman",20),bg="#292826",fg="#efefef",anchor="w",padx=10)
        title3.place(x=0,y=0,relwidth=1)
        
        lbl_month=tk.Label(Frame2,text="Month",font=("times new roman",17),bg="#292826",fg="#efefef")
        lbl_month.place(x=10,y=60)

        combo_month=ttk.Combobox(Frame2,textvariable=self.var_month,font=('times new roman',13,'bold'),state="readonly")
        combo_month['values']=("Select", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        combo_month.current(0)
        combo_month.place(x=95,y=64,width=100)
        
        lbl_year=tk.Label(Frame2,text="Year",font=("times new roman",17),bg="#292826",fg="#efefef")
        lbl_year.place(x=205,y=60)
        txt_year=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_year,bg="#292826",fg="White")
        txt_year.place(x=270,y=64,width=100)
        
        lbl_absents=tk.Label(Frame2,text="Absents",font=("times new roman",17),bg="#292826",fg="#efefef")
        lbl_absents.place(x=375,y=60)
        txt_absents=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_absents,bg="#292826",fg="White")
        txt_absents.place(x=470,y=64,width=100)

        lbl_days=tk.Label(Frame2,text="Total Days",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_days.place(x=10,y=100)
        txt_days=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_t_days,bg="#292826",fg="White")
        txt_days.place(x=160,y=100,width=100)
        
        
        #---------------Row 1-------------#
        lbl_add=tk.Label(Frame2,text="Additions",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_add.place(x=10,y=140)
        
        lbl_salary=tk.Label(Frame2,text="Basic Salary",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_salary.place(x=10,y=180)
        txt_salary=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_b_salary,bg="#292826",fg="White")
        txt_salary.place(x=160,y=180,width=120)
        
        #---------------Row 2--------------#
        lbl_medical=tk.Label(Frame2,text="Medical",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_medical.place(x=10,y=220)
        txt_medical=tk.Entry(Frame2,font=("times new roman",13),textvariable=self.var_medical,bg="#292826",fg="White")
        txt_medical.place(x=160,y=225,width=100)
        
        lbl_conveyence=tk.Label(Frame2,text="Conveyance",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_conveyence.place(x=280,y=220)
        txt_conveyence=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_conveyence,bg="#292826",fg="White")
        txt_conveyence.place(x=440,y=225,width=100)
        
         #---------------Row 3--------------#
        lbl_hra=tk.Label(Frame2,text="H.R.A",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_hra.place(x=10,y=260)
        txt_hra=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_hra,bg="#292826",fg="White")
        txt_hra.place(x=160,y=260,width=100)
        
        lbl_standard_da=tk.Label(Frame2,text="Standard  DA",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_standard_da.place(x=280,y=260)
        txt_standard_da=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_standard_da,bg="#292826",fg="White")
        txt_standard_da.place(x=440,y=260,width=100)

         #---------------Row 4--------------#
        lbl_educational_allowance=tk.Label(Frame2,text="Standard CCA",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_educational_allowance.place(x=10,y=300)
        txt_educational_allowance=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_educational_allowance,bg="#292826",fg="White")
        txt_educational_allowance.place(x=160,y=300,width=100)

        lbl_other_allowance=tk.Label(Frame2,text="Other Allowance",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_other_allowance.place(x=280,y=300)
        txt_other_allowance=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_other_allowance,bg="#292826",fg="White")
        txt_other_allowance.place(x=460,y=300,width=100)
        

        #---------------Row 5--------------#


        #---------------Row 6--------------#
        lbl_deduct=tk.Label(Frame2,text="Deduction",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_deduct.place(x=10,y=340)
    
        

         #---------------Row 7--------------#
        lbl_pf=tk.Label(Frame2,text="PF",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_pf.place(x=10,y=380)
        txt_pf=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_pf,bg="#292826",fg="White")
        txt_pf.place(x=160,y=380,width=100)
        
        lbl_professional_tax=tk.Label(Frame2,text="Professional Tax",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_professional_tax.place(x=280,y=380)
        txt_professional_tax=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_professional_tax,bg="#292826",fg="White")
        txt_professional_tax.place(x=460,y=380,width=100)

        lbl_esic=tk.Label(Frame2,text="ESIC",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_esic.place(x=10,y=420)
        txt_esic=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_esic,bg="#292826",fg="White")
        txt_esic.place(x=160,y=420,width=100)

        #---------------Row 8--------------#
        # lbl_tds=tk.Label(Frame2,text="T.D.S",font=("times new roman",18),bg="#292826",fg="#efefef")
        # lbl_tds.place(x=10,y=420)
        # txt_tds=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_tds,bg="#292826",fg="White")
        # txt_tds.place(x=160,y=420,width=100)
        
        lbl_netsalary=tk.Label(Frame2,text="Net Salary*",font=("times new roman",18),bg="#292826",fg="#efefef")
        lbl_netsalary.place(x=10,y=460)
        txt_netsalary=tk.Entry(Frame2,font=("times  new roman",13),textvariable=self.var_n_salary,bg="#292826",fg="White")
        txt_netsalary.place(x=160,y=460,width=120)

        
        ##--------Buttons----------##
        button_calculate=tk.Button(Frame2,text="Calculate",command=self.calculate,font=("times new roman",18),bg="#292826",fg="White",activebackground="#efefef")
        button_calculate.place(x=100,y=500,height=30,width=120)
        
        self.button_save=tk.Button(Frame2,text="Save",command=self.add,font=("times new roman",18),bg="#292826",fg="white",activebackground="#efefef")
        self.button_save.place(x=230,y=500,height=30,width=120)
        
        button_clear=tk.Button(Frame2,text="Clear",command=self.clear,font=("times new roman",18),bg="#292826",fg="White",activebackground="#efefef")
        button_clear.place(x=360,y=500,height=30,width=120)
        
        self.button_print=tk.Button(Frame2,text="Print",command=self.print,state=tk.DISABLED,font=("times new roman",18),bg="#292826",fg="White",activebackground="#efefef")
        self.button_print.place(x=100,y=540,height=30,width=110)

        
        ##----------------------------Frame3---------------------------------##  
        Frame3=tk.Frame(self.root,bd=3,relief=tk.RIDGE,bg="#292826")
        Frame3.place(x=10,y=450,width=750,height=320)
        
        #------------------Calculator Frame------------------------#
        self.var_txt=tk.StringVar()
        self.var_operator=''
        def btn_click(num):
            self.var_operator=self.var_operator+str(num)
            self.var_txt.set(self.var_operator)
            
        def result():
            res=str(eval(self.var_operator))
            self.var_txt.set(res)
            self.var_operator=''
            
        def clear_calc():
            self.var_txt.set('')
            self.var_operator=''
        
        cal_frame=tk.Frame(Frame3,bg="#292826",bd=2,relief=tk.RIDGE)
        cal_frame.place(x=5,y=5,width=247,height=295)
        
        txt_result=tk.Entry(cal_frame,bg='#292826',fg="White",textvariable=self.var_txt,font=("times new roman",20,"bold"),justify=tk.RIGHT)
        txt_result.place(x=0,y=0,relwidth=1,height=50)
        
        #-----------------------Row 1-------------------#
        btn_7=tk.Button(cal_frame,text='7',command=lambda:btn_click(7),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_7.place(x=0,y=52,w=60,h=60)
        btn_8=tk.Button(cal_frame,text='8',command=lambda:btn_click(8),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_8.place(x=61,y=52,w=60,h=60)
        btn_9=tk.Button(cal_frame,text='9',command=lambda:btn_click(9),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_9.place(x=122,y=52,w=60,h=60)
        btn_divide=tk.Button(cal_frame,text='/',command=lambda:btn_click("/"),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_divide.place(x=183,y=52,w=60,h=60)
        
        #-----------------------Row 2-------------------#
        btn_4=tk.Button(cal_frame,text='4',command=lambda:btn_click(4),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_4.place(x=0,y=112,w=60,h=60)
        btn_5=tk.Button(cal_frame,text='5',command=lambda:btn_click(5),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_5.place(x=61,y=112,w=60,h=60)
        btn_6=tk.Button(cal_frame,text='6',command=lambda:btn_click(6),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_6.place(x=122,y=112,w=60,h=60)
        btn_multiply=tk.Button(cal_frame,text='*',command=lambda:btn_click("*"),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_multiply.place(x=183,y=112,w=60,h=60)
        
        #-----------------------Row 3-------------------#
        btn_1=tk.Button(cal_frame,text='1',command=lambda:btn_click(1),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_1.place(x=0,y=172,w=60,h=60)
        btn_2=tk.Button(cal_frame,text='2',command=lambda:btn_click(2),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_2.place(x=61,y=172,w=60,h=60)
        btn_3=tk.Button(cal_frame,text='3',command=lambda:btn_click(3),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_3.place(x=122,y=172,w=60,h=60)
        btn_minus=tk.Button(cal_frame,text='-',command=lambda:btn_click("-"),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_minus.place(x=183,y=172,w=60,h=60)
        
        #-----------------------Row 4-------------------#
        btn_0=tk.Button(cal_frame,text='0',command=lambda:btn_click(0),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_0.place(x=0,y=233,w=60,h=60)
        btn_clear=tk.Button(cal_frame,text='C',command=clear_calc,font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_clear.place(x=61,y=233,w=60,h=60)
        btn_plus=tk.Button(cal_frame,text='+',command=lambda:btn_click("+"),font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_plus.place(x=122,y=233,w=60,h=60)
        btn_equalto=tk.Button(cal_frame,text='=',command=result,font=("times new roman",15,"bold"),bg="#292826",fg="#efefef",activebackground="#efefef")
        btn_equalto.place(x=183,y=233,w=60,h=60)
        

        
       
        self.check_connection()
    
    ##------------Functions----------##
    def search(self):
        try:
            con = sqlite3.connect('epm.db')
            cur = con.cursor()
            cur.execute("select * from employees where emp_code=?", (self.var_emp_code.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Employee ID, Please try with another ID", parent=self.root)
            else:
                self.var_emp_code.set(row[0])
                self.var_designation.set(row[1])
                self.var_name.set(row[2])
                self.var_email.set(row[3])
                self.var_department.set(row[4])
                self.var_dob.set(row[5])
                self.var_doj.set(row[6])
                self.var_contact.set(row[7])
                self.var_uan_no.set(row[8])
                self.var_bank_acc.set(row[9])
                self.var_pan_no.set(row[10])
                self.button_save.config(state=tk.NORMAL)
                self.button_update.config(state=tk.NORMAL)
                self.button_delete.config(state=tk.NORMAL)
                self.txt_code.config(state='readonly')
                self.button_print.config(state=tk.NORMAL)
        except Exception as ex:
            messagebox.showerror("Error", f'Error due to: {str(ex)}')
     

            
    def clear(self):
        self.button_save.config(state=tk.NORMAL)
        self.button_update.config(state=tk.DISABLED)
        self.button_delete.config(state=tk.DISABLED)
        self.button_print.config(state=tk.DISABLED)
        self.txt_code.config(state=tk.NORMAL)
        
        self.var_emp_code.set('') 
        self.var_designation.set('') 
        self.var_name.set('')
        self.var_email.set('') 
        self.var_department.set('') 
        self.var_dob.set('') 
        self.var_doj.set('') 
        self.var_contact.set('') 
        self.var_uan_no.set('') 
        self.var_bank_acc.set('') 
        self.var_pan_no.set('') 
        self.var_month.set('') 
        self.var_year.set('') 
        self.var_b_salary.set('') 
        self.var_t_days.set('') 
        self.var_absents.set('') 
        self.var_medical.set('') 
        self.var_hra.set('')
        self.var_conveyence.set('')
        self.var_educational_allowance.set('')
        self.var_professional_tax.set('')
        self.var_standard_da.set('')
        self.var_pf.set('') 
        self.var_n_salary.set('')

        
    def delete(self):
        if self.var_emp_code.get()=='':
            messagebox.showerror("Error","Employee ID is required")
        else:
            try:
                con=sqlite3.connect('epm.db')

                cur=con.cursor()
                cur.execute("select * from employees where emp_code=?",(self.var_emp_code.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID,Please try with another ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you want to Delete??")
                    if op:
                        # Check if there are dependent records in emp_salary
                        cur.execute("SELECT * FROM emp_salary WHERE emp_code=?", (self.var_emp_code.get(),))
                        salary_rows = cur.fetchall()

                        if salary_rows:
                            messagebox.showwarning("Warning", "Employee has salary records. Delete salary records first.", parent=self.root)
                        else:
                            # No salary records, proceed with deletion
                            cur.execute("DELETE FROM employees WHERE emp_code=?", (self.var_emp_code.get(),))
                            con.commit()
                            con.close()
                            messagebox.showinfo("Delete", "Employee Record Deleted Successfully", parent=self.root)
                            self.clear()
                    pass
            except Exception as ex:
                messagebox.showerror("Error",f'Error due to: {str(ex)}')

    def save_emp_data(self):
        if self.var_emp_code.get() == '' or self.var_name.get() == '':
            messagebox.showerror("Error", "Employee details are required")
        else:
            try:
                con = sqlite3.connect('epm.db')
                cur = con.cursor()

                cur.execute("SELECT * FROM employees WHERE emp_code=?", (self.var_emp_code.get(),))
                row = cur.fetchone()
                
                if row is not None:
                    messagebox.showerror("Error", "This employee id is already available in our record, try again with another id", parent=self.root)
                else:
                    cur.execute("INSERT INTO employees (emp_code, designation, name, email, department, dob, doj, contact, UAN, bank_account, pan_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (self.var_emp_code.get(), self.var_designation.get(), self.var_name.get(), self.var_email.get(),
                                self.var_department.get(), self.var_dob.get(), self.var_doj.get(),
                                self.var_contact.get(), self.var_uan_no.get(), self.var_bank_acc.get(), self.var_pan_no.get()))

                    con.commit()
                    con.close()

                    messagebox.showinfo("Success", "Record Added Successfully")
                    self.button_print.config(state=tk.NORMAL)
            except Exception as ex:
                messagebox.showerror("Error", f'Error due to: {str(ex)}')

                

        
    def add(self):
        if self.var_emp_code.get()=='' or self.var_name.get()=='':
            messagebox.showerror("Error","Employee details are required")
        else:
            try:
                con=sqlite3.connect('epm.db')

                cur=con.cursor()
                cur.execute("""
    INSERT INTO emp_salary (
        emp_code,
        month,
        year,
        absents,
        total_days,
        base_salary,
        medical,
        hra,
        conveyence,
        educational_allowance,
        std_da,
        other_allowance,
        esic,
        professional_tax,
        pf,
        net_salary
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    self.var_emp_code.get(),
    self.var_month.get(),
    self.var_year.get(),
    self.var_absents.get(),
    self.var_t_days.get(),
    self.var_b_salary.get(),
    self.var_medical.get(),
    self.var_hra.get(),
    self.var_conveyence.get(),  
    self.var_educational_allowance.get(),
    self.var_standard_da.get(),
    self.var_other_allowance.get(),
    self.var_esic.get(),  
    self.var_professional_tax.get(),
    self.var_pf.get(),
    self.var_n_salary.get()
))
                con.commit()
                con.close()
                messagebox.showinfo("Success","Record Added Successfully")
                self.button_print.config(state=tk.NORMAL)
            except Exception as ex:
                messagebox.showerror("Error",f'Error due to: {str(ex)}')
                
    def update(self):
        if self.var_emp_code.get()=='' or self.var_name.get()=='':
            messagebox.showerror("Error","Employee details are required")
        else:
            try:
                con=sqlite3.connect('epm.db')

                cur=con.cursor()
                cur.execute("select * from emp_salary where emp_code=?",(self.var_emp_code.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","This employee id is invalid,try again with valid id",parent=self.root)
                else:
                    cur.execute("UPDATE `employees` SET `designation`=?, `name`=?,`email`=?, `department`=?, `dob`=?, `doj`=?, `contact`=?, `UAN`=?, `bank_account`=?, `pan_number`=? WHERE `emp_code`=?",
                                            (self.var_designation.get(), self.var_name.get(), 
                                            self.var_email.get(), self.var_department.get(), self.var_dob.get(), self.var_doj.get(),
                                           self.var_contact.get(), self.var_uan_no.get(),self.var_bank_acc.get(),self.var_pan_no.get(),
                                            self.var_emp_code.get()))                    
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Record Updated Successfully")
            except Exception as ex:
                messagebox.showerror("Error",f'Error due to: {str(ex)}')
    def number_to_word(self,number):
        def get_word(n):
            words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
            if n<=20:
                return words[n]
            else:
                ones=n%10
                tens=n-ones
                return words[tens]+" "+words[ones]
                
        def get_all_word(n):
            d=[100,10,100,100]
            v=["","Hundred And","Thousand","lakh"]
            w=[]
            for i,x in zip(d,v):
                t=get_word(n%i)
                if t!="":
                    t+=" "+x
                w.append(t.rstrip(" "))
                n=n//i
            w.reverse()
            w=' '.join(w).strip()
            if w.endswith("And"):
                w=w[:-3]
            return w

        arr=str(number).split(".")
        number=int(arr[0])
        crore=number//10000000
        number=number%10000000
        word=""
        if crore>0:
            word+=get_all_word(crore)
            word+=" crore "
        word+=get_all_word(number).strip()+" Rupees"
        if len(arr)>1:
            if len(arr[1])==1:
                arr[1]+="0"
            word+=" and "+get_all_word(int(arr[1]))+" paisa"
        return word
                
    def calculate(self):
        if self.var_month.get()=='' or self.var_year.get()=='' or self.var_b_salary.get()=='' or self.var_absents.get()=='' or self.var_t_days.get()=='':
            messagebox.showerror('Error','All Fields are required')
        else:
            
            # Handle allowances
            medical = float(self.var_medical.get()) if self.var_medical.get() else 0
            hra = float(self.var_hra.get()) if self.var_hra.get() else 0
            standard_da = float(self.var_standard_da.get()) if self.var_standard_da.get() else 0
            educational_allowance = float(self.var_educational_allowance.get()) if self.var_educational_allowance.get() else 0
            conveyance = float(self.var_conveyence.get()) if self.var_conveyence.get() else 0
            other_allowance = float(self.var_other_allowance.get()) if self.var_other_allowance.get() else 0

            # Handle deductions
            pf = float(self.var_pf.get()) if self.var_pf.get() else 0
            professional_tax = float(self.var_professional_tax.get()) if self.var_professional_tax.get() else 0
            esic = float(self.var_esic.get()) if self.var_esic.get() else 0

            # Now perform the calculations:
            addition = medical + hra + standard_da + educational_allowance + conveyance + other_allowance
            per_day=(float(self.var_b_salary.get())+addition)/float(self.var_t_days.get())
            work_day=float(self.var_t_days.get())-float(self.var_absents.get())
            e_sal=per_day*work_day###Effective Salary
            deduct = pf + professional_tax + esic
            n_sal = e_sal - deduct
            self.var_n_salary.set(str(round(n_sal, 2)))
  
    def check_connection(self):
        try:
            con=sqlite3.connect('epm.db')

            cur=con.cursor()
            cur.execute("select * from emp_salary")
            self.row=cur.fetchall()
            #print(self.row)
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}')
            
    def show(self):
        try:
            con=sqlite3.connect('epm.db')

            cur=con.cursor()
            cur.execute("select * from employees")
            row=cur.fetchall()
            self.employee_tree.delete(*self.employee_tree.get_children())
            for x in row:
                self.employee_tree.insert('',tk.END,values=x)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error",f'Error due to: {str(ex)}')

    def show_salary_details(self):
        try:
            con = sqlite3.connect('epm.db')

            cur = con.cursor()
            cur.execute("select * from emp_salary")
            rows = cur.fetchall()
            self.employee_tree.delete(*self.employee_tree.get_children())

            self.selected_rows = []  # Store selected rows

            for x in rows:
                item_id = self.employee_tree.insert('', tk.END, values=x) 
        except Exception as ex:
            messagebox.showerror("Error", f'Error due to: {str(ex)}')


    def remove_many_employees(self):
        try:
            con = sqlite3.connect('epm.db')

            cur = con.cursor()
            selected_records = self.employee_tree.selection()
            op=messagebox.askyesno("Confirm","Do you want to Delete??")
            if op:
                for record in selected_records:
                    record_id = self.employee_tree.item(record, "values")[0]
                    print(record_id)
                    cur.execute("DELETE FROM employees WHERE emp_code=?", (record_id,))
                    self.employee_tree.delete(record)

            con.commit()
            con.close()
            self.show_salary_details()
        except Exception as ex:
            messagebox.showerror("Error", f'Error due to: {str(ex)}')

# -----fuction for employees salary----
    def remove_many_salary(self):
        try:
            con = sqlite3.connect('epm.db')

            cur = con.cursor()
            selected_records = self.employee_tree.selection()
            op=messagebox.askyesno("Confirm","Do you want to Delete??")
            if op:
                for record in selected_records:
                    record_id = self.employee_tree.item(record, "values")[0]
                    cur.execute("DELETE FROM emp_salary WHERE salary_id=?", (record_id,))
                    self.employee_tree.delete(record)

            con.commit()
            con.close()
            self.show_salary_details()
        except Exception as ex:
            messagebox.showerror("Error", f'Error due to: {str(ex)}')


    def print_record(self):
        try:
            con = sqlite3.connect('epm.db')
            cur = con.cursor()
            selected_records = self.employee_tree.selection()
            op = messagebox.askyesno("Confirm", "Do you want to save their payslips?")
            
            if op:
                for record in selected_records:
                    record_id = self.employee_tree.item(record, "values")[0]
                    cur.execute("SELECT * FROM emp_salary WHERE salary_id=?", (record_id,))
                    selected_record = cur.fetchone()

                    cur.execute("SELECT * FROM employees WHERE emp_code=?", (selected_record[1],))
                    selected_record_employee = cur.fetchone()
                    # Example: Print data to console
                    print("Selected Record:", selected_record)
                    print("Selected Record:", len(selected_record))
                    print("selected_record_employee:", selected_record_employee)
                    
                     # Replace missing values with None
                    selected_record = [None if val == '' else val for val in selected_record]
                    selected_record_employee = [None if val == '' else val for val in selected_record_employee]

                    medical = float(selected_record[9]) if selected_record[9] else 0
                    hra = float(selected_record[10]) if selected_record[10] else 0
                    standard_da = float(selected_record[8]) if selected_record[8] else 0
                    educational_allowance = float(selected_record[12]) if selected_record[12] else 0
                    conveyance = float(selected_record[13]) if selected_record[13] else 0
                    other_allowance = float(selected_record[10]) if selected_record[10] else 0

                    # Handle deductions
                    pf = float(selected_record[14]) if selected_record[14] else 0
                    professional_tax = float(selected_record[13]) if selected_record[13] else 0
                    esic = float(selected_record[15]) if selected_record[15] else 0

                    # Now perform the calculations:
                    addition = float(selected_record[7])+medical + hra + standard_da + educational_allowance + conveyance + other_allowance
                    
                    deduct = pf + professional_tax + esic
                    print("selected_record_employee:", selected_record_employee[0])
                    print("Length of selected_record_employee:", len(selected_record_employee))

                
                    word=self.number_to_word(selected_record[16])
                    data = {
                        'employee_name': selected_record_employee[2],
                        'month':selected_record[3],
                        'year':selected_record[4],
                        'basic_salary': selected_record[6],
                        'Designation': selected_record_employee[1],
                        'Department': selected_record_employee[4],
                        'uan_no':selected_record_employee[9],
                        'bank_acc':selected_record_employee[10],
                        'pan_no':selected_record_employee[10],
                        'conveyance':conveyance,
                        'doj': selected_record_employee[6],
                        'DaysPaid': float(selected_record[5]),
                        'DaysPresent': float(selected_record[5]) - float(selected_record[4]),
                        'DaysAbsent': selected_record[5],
                        'medical': medical,
                        'pt': professional_tax,
                        'hra':hra,
                        'pf': pf,
                        'std_da':standard_da,
                 
                        'ESIC':esic,
                        'otherAllowance': other_allowance,
                        'deductions': deduct,
                        'educational_allowance':educational_allowance,
                        'additions': addition,
                        'net_salary': selected_record[16],
                        'word':word,
                    }
                    print("Before print(data)")
                    print(data)
                    print("After print(data)")

                    # Example: Generate PDF using the selected record data
                    # Modify this part based on your PDF generation logic
                    pdf_data = {
                        'employee_name': selected_record_employee[1],  # Modify indices based on your table structure
                        'month': selected_record[2],
                        # Add other fields as needed
                    }
                    # self.generate_pdf(pdf_data)  # You need to implement the 'generate_pdf' method
                messagebox.showinfo("Success", "Payslip generated successfully!")
                    
            con.commit()
            con.close()
            self.show_salary_details()

        except Exception as ex:
            messagebox.showerror("Error", f'Error due to: {str(ex)}')

    def generate_pdf(self,pdf_data):
        try:
            
            # Handle allowances
            
            template_path = os.path.abspath('index.html')

            # Create a Jinja2 environment
            env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)), autoescape=True)

            # Load the template
            template = env.get_template(os.path.basename(template_path))

            # Render the template with dynamic data
            rendered_html = template.render(pdf_data)

            # Write the rendered HTML to a temporary file
            with open('temp.html', 'w') as html_file:
                html_file.write(rendered_html)

            # Convert HTML to PDF
            user_folder = f'C:/Users/Admin/Documents/Aetos_Digital/Pdf/{self.var_emp_code.get()}-{self.var_name.get()}'

            # Check if the directory exists, and create it if not
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            timestamp = time.strftime("%Y%m%H%M%S")
            pdf_file_path = f'{user_folder}/sample_{timestamp}.pdf'
            converter.convert(f'file:///{os.path.abspath("temp.html")}', pdf_file_path)

            

            # Open the generated PDF in the default PDF viewer
            webbrowser.open(pdf_file_path)
        except Exception as e:
            print(f"Error creating PDF: {str(e)}")
            messagebox.showerror("Error", f"Error creating PDF: {str(e)}")

            
    def logout(self):
        messagebox.showinfo("Success","Loged Out Successfully",parent=self.root)
        self.root.destroy()
        
    
    ##---------------------------All Employees Frame-------------------##
    def employee_frame(self):
        self.root2=tk.Toplevel(self.root)
        self.root2.title("All Employee Details")
        self.root2.geometry("950x550+130+100")
        self.root2.config(bg="#292826")
        title=tk.Label(self.root2,text="All Employee Details",font=("times new roman",30,"bold"),bg="#292826",fg="#efefef",anchor="w",padx=10)
        title.pack(side=tk.TOP,fill=tk.X)
        self.delete_selected_button = ttk.Button(self.root2, text="Delete Selected",command=self.remove_many_employees)
        self.delete_selected_button.pack(pady=10)

        self.root2.focus_force()
        
        scrolly=tk.Scrollbar(self.root2,orient=tk.VERTICAL,bg="#292826")
        scrollx=tk.Scrollbar(self.root2,orient=tk.HORIZONTAL,bg="#292826")
        scrollx.pack(side=tk.BOTTOM,fill=tk.X)
        scrolly.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.employee_tree=ttk.Treeview(self.root2,columns=('e_id', 'designation', 'name','email', 'department', 'dob', 'doj', 'contact', 'uan_no' ,'bank_acc','pan_no'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        self.employee_tree.heading('e_id',text='EID')
        self.employee_tree.heading('designation',text='Designation')
        self.employee_tree.heading('name',text='Name')
        self.employee_tree.heading('email',text='Email')
        self.employee_tree.heading('department',text='Department')
        self.employee_tree.heading('dob',text='DOB')
        self.employee_tree.heading('doj',text='DOJ')
        self.employee_tree.heading('contact',text='Contact')
        self.employee_tree.heading('uan_no',text='uan_no')
        self.employee_tree.heading('bank_acc',text='Bank Account')
        self.employee_tree.heading('pan_no',text='PAN No')

        self.employee_tree['show']='headings'
        
        self.employee_tree.column('e_id',width=50)
        self.employee_tree.column('designation',width=100)
        self.employee_tree.column('name',width=100)
        self.employee_tree.column('email',width=100)
        self.employee_tree.column('department',width=100)
        self.employee_tree.column('dob',width=100)
        self.employee_tree.column('doj',width=100)
        self.employee_tree.column('contact',width=100)
        self.employee_tree.column('uan_no',width=100)
        self.employee_tree.column('bank_acc',width=100)
        self.employee_tree.column('pan_no',width=100)

       
        scrollx.config(command=self.employee_tree.xview)
        scrolly.config(command=self.employee_tree.yview)
        self.employee_tree.pack(fill=tk.BOTH,expand=1)
        self.show()
    
        self.root2.mainloop()


# -------------- employee salary frame ------------------# 
    def employee_salary_frame(self):
        self.root2 = tk.Toplevel(self.root)
        self.root2.title("All Employee Details")
        self.root2.geometry("950x550+130+100")
        self.root2.config(bg="#292826")
        title = tk.Label(self.root2, text="Employees Salary", font=("times new roman", 30, "bold"), bg="#292826", fg="#efefef", anchor="w", padx=10)
        title.pack(side=tk.TOP, fill=tk.X)
        self.delete_selected_button = ttk.Button(self.root2, text="Delete Selected",command=self.remove_many_salary)
        self.delete_selected_button.pack(pady=10)
        self.delete_selected_button = ttk.Button(self.root2, text="Print Selected",command=self.print_record)
        self.delete_selected_button.pack(pady=10)



        self.root2.focus_force()

        scrolly = tk.Scrollbar(self.root2, orient=tk.VERTICAL, bg="#292826")
        scrollx = tk.Scrollbar(self.root2, orient=tk.HORIZONTAL, bg="#292826")
        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)

        self.employee_tree = ttk.Treeview(self.root2, columns=('SRN', 'e_id', 'month', 'year',  't-days', 'absent_days','basic_salary','std_da', 'medical', 'hra','other_allowance','educational_allowance','conveyence','professional_tax','pf', 'esi', 'net_salary', 'salary_receipt', 'print_button'), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        self.employee_tree.heading('SRN', text='SRN')
        self.employee_tree.heading('e_id', text='EID')
        self.employee_tree.heading('month', text='Month')
        self.employee_tree.heading('year', text='Year')
        self.employee_tree.heading('t-days', text='T.Days')
        self.employee_tree.heading('absent_days', text='Absents')
        self.employee_tree.heading('basic_salary', text='Basic Salary')
        self.employee_tree.heading('std_da', text='Standard DA')
        self.employee_tree.heading('medical', text='Medical')
        self.employee_tree.heading('hra', text='HRA')
        self.employee_tree.heading('other_allowance', text='Other Allowance')
        self.employee_tree.heading('educational_allowance', text='Educational Aallowance')
        self.employee_tree.heading('conveyence', text='Conveyence')
        self.employee_tree.heading('professional_tax', text='Professional Tax')
        self.employee_tree.heading('pf', text='PF')
        self.employee_tree.heading('esi', text='ESI')
        self.employee_tree.heading('net_salary', text='Net Salary')
        self.employee_tree.heading('salary_receipt', text='Salary Receipt')
        self.employee_tree.heading('print_button', text='Print')
        self.employee_tree['show'] = 'headings'

        self.employee_tree.column('SRN', width=50)
        self.employee_tree.column('e_id', width=50)
        self.employee_tree.column('month', width=100)
        self.employee_tree.column('year', width=100)
        self.employee_tree.column('basic_salary', width=100)
        self.employee_tree.column('t-days', width=70)
        self.employee_tree.column('absent_days', width=70)
        self.employee_tree.column('std_da', width=100)
        self.employee_tree.column('medical', width=100)
        self.employee_tree.column('hra', width=100)
        self.employee_tree.column('other_allowance', width=100)
        self.employee_tree.column('educational_allowance', width=100)
        self.employee_tree.column('conveyence', width=100)
        self.employee_tree.column('professional_tax', width=100)
        self.employee_tree.column('pf', width=100)
        self.employee_tree.column('esi', width=100)
        self.employee_tree.column('net_salary', width=100)
        self.employee_tree.column('salary_receipt', width=200)
        self.employee_tree.column('print_button', width=70)
        scrollx.config(command=self.employee_tree.xview)
        scrolly.config(command=self.employee_tree.yview)
        self.employee_tree.pack(fill=tk.BOTH, expand=1)
        self.show_salary_details()
        self.root2.mainloop()


    def print(self):
        try:
            
            # Handle allowances
            medical = float(self.var_medical.get()) if self.var_medical.get() else 0
            hra = float(self.var_hra.get()) if self.var_hra.get() else 0
            standard_da = float(self.var_standard_da.get()) if self.var_standard_da.get() else 0
            educational_allowance = float(self.var_educational_allowance.get()) if self.var_educational_allowance.get() else 0
            conveyance = float(self.var_conveyence.get()) if self.var_conveyence.get() else 0
            other_allowance = float(self.var_other_allowance.get()) if self.var_other_allowance.get() else 0

            # Handle deductions
            pf = float(self.var_pf.get()) if self.var_pf.get() else 0
            professional_tax = float(self.var_professional_tax.get()) if self.var_professional_tax.get() else 0
            esic = float(self.var_esic.get()) if self.var_esic.get() else 0

            # Now perform the calculations:
            addition = round(float(self.var_b_salary.get())+medical + hra + standard_da + educational_allowance + conveyance + other_allowance,2)
            
            deduct = round(pf + professional_tax + esic,2)
            
           
            word=self.number_to_word(self.var_n_salary.get())
            data = {
                'employee_name': self.var_name.get(),
                'month':self.var_month.get(),
                'year':self.var_year.get(),
                'basic_salary': self.var_b_salary.get(),
                'Designation': self.var_designation.get(),
                'Department': self.var_department.get(),
                'uan_no':self.var_uan_no.get(),
                'bank_acc':self.var_bank_acc.get(),
                'pan_no':self.var_pan_no.get(),
                'conveyance':self.var_conveyence.get(),
                'doj': self.var_doj.get(),
                'DaysPaid': float(self.var_t_days.get()),
                'DaysPresent': float(self.var_t_days.get()) - float(self.var_absents.get()),
                'DaysAbsent': self.var_absents.get(),
                'medical': self.var_medical.get(),
                'pt': self.var_professional_tax.get(),
                'hra': self.var_hra.get(),
                'pf': self.var_pf.get(),
                'std_da':self.var_standard_da.get(),
                'conveyence': self.var_conveyence.get(),
                'ESIC': self.var_esic.get(),
                'otherAllowance': self.var_other_allowance.get(),
                'deductions': deduct,
                'educational_allowance':self.var_educational_allowance.get(),
                'additions': addition,
                'net_salary': self.var_n_salary.get(),
                'word':word,
            }
            template_path = os.path.abspath('index.html')

            # Create a Jinja2 environment
            env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)), autoescape=True)

            # Load the template
            template = env.get_template(os.path.basename(template_path))

            # Render the template with dynamic data
            rendered_html = template.render(data)

            # Write the rendered HTML to a temporary file
            with open('temp.html', 'w') as html_file:
                html_file.write(rendered_html)

            # Convert HTML to PDF
            user_folder = f'C:/Users/Admin/Documents/Aetos_Digital/Pdf/{self.var_emp_code.get()}-{self.var_name.get()}'

            # Check if the directory exists, and create it if not
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            timestamp = time.strftime("%Y%m%H%M%S")
            pdf_file_path = f'{user_folder}/sample_{timestamp}.pdf'
            converter.convert(f'file:///{os.path.abspath("temp.html")}', pdf_file_path)

            messagebox.showinfo("Success", "Payslip generated successfully!")

            # Open the generated PDF in the default PDF viewer
            webbrowser.open(pdf_file_path)
        except Exception as e:
            print(f"Error creating PDF: {str(e)}")
            messagebox.showerror("Error", f"Error creating PDF: {str(e)}")

        
root=tk.Tk()
obj=EmployeeSystem(root)
root.mainloop()
