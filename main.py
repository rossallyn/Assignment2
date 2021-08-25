from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect('StudentsList.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS studentlist (name,idnum,gender,course_code,year_lvl)""")
c.execute("""CREATE TABLE IF NOT EXISTS courselist (course_code,course)""")


def mp():
    root2 = Tk()
    w = 995
    h = 500
    root2.geometry(f'{w}x{h}+{200}+{110}')
    root2.resizable(False, False)
    root2.configure(background="antiquewhite2")
    root2.title('STUDENT MANAGEMENT SYSTEM')

    c.execute("""SELECT name,idnum,gender,courselist.course_code,year_lvl,courselist.course  FROM studentlist  INNER JOIN courselist  ON courselist.course_code = studentlist.course_code; """)
    records = c.fetchall()

    f = Frame(root2, width=0, height=450, highlightbackground="antiquewhite2", highlightthickness=4, bg="#161618")
    f.place(x=400, y=0)

    f2 = Frame(root2, width=260, height=0, highlightbackground="antiquewhite2", highlightthickness=4, bg="#161618")
    f2.place(x=400, y=0)

    frm = Frame(root2)
    frm.pack(side=LEFT, padx=(0, 0), pady=(150, 0))

    tv = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=20)
    tv.pack()
    tv.heading(1, text="NAME", anchor=tk.CENTER)
    tv.column("1", minwidth=0, width=212)

    tv.heading(2, text="ID NUMBER", anchor=tk.CENTER)
    tv.column("2", minwidth=0, width=150)

    tv.heading(3, text="GENDER", anchor=tk.CENTER)
    tv.column("3", minwidth=0, width=150)

    tv.heading(6, text="COURSE", anchor=tk.CENTER)
    tv.column("6", minwidth=0, width=280)

    tv.heading(4, text="COURSE CODE", anchor=tk.CENTER)
    tv.column("4", minwidth=0, width=100)

    tv.heading(5, text="YEAR LEVEL", anchor=tk.CENTER)
    tv.column("5", minwidth=0, width=100)

    vsb = ttk.Scrollbar(root2, orient="vertical", command=tv.yview)
    vsb.place(x=782 + 190 + 4, y=158, height=340)


    for i in records:
        tv.insert('', 'end', value=i)

    def slc():
        name.delete(0, END)
        idnum.delete(0, END)
        gender.delete(0, END)
        course.delete(0, END)
        yr_lvl.delete(0, END)

        selected = tv.focus()
        values = tv.item(selected, 'values')

        name.insert(0, values[0])
        idnum.insert(0, values[1])
        gender.insert(0, values[2])
        course.insert(0, values[3])
        yr_lvl.insert(0, values[4])

    def delete():
        selected_item = tv.focus()

        if selected_item == "":
            messagebox.showerror("Delete Confirmation Error", "Please Select Record To Be Deleted")

        else:

            if messagebox.askyesno("Delete Confirmation", "Do you wanna Delete this Student") == False:
                return
            else:
                messagebox.showinfo("Delete Confirmation", "Successfully Deleted")
                conn = sqlite3.connect("StudentsList.db")
                c = conn.cursor()
                for selected_item in tv.selection():
                    c.execute("DELETE FROM studentlist WHERE idnum=?", (tv.set(selected_item, '#2'),))
                    conn.commit()
                    tv.delete(selected_item)
                conn.close()

    def update():
        if idnum.get() == '':
            return messagebox.showwarning("Warning!", "PLEASE SELECT A STUDENT")

        if messagebox.askyesno("Update", "Are you sure you want to update this student? ") == False:
            return
        else:
            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()
            messagebox.showinfo("Update Info", "Updated successfully!!!")
            data1 = name.get()
            data2 = idnum.get()
            data3 = gender.get()
            data4 = course.get()
            data5 = yr_lvl.get()

            selected = tv.selection()
            tv.item(selected, values=(data1, data2, data3, data4, data5))

            c.execute("UPDATE studentlist set  name=?, idnum=?, gender=?, course_code=?, year_lvl=?  WHERE idnum=? ", (data1, data2, data3, data4, data5, data2))

            conn.commit()
            conn.close()

            root2.destroy()
            mp()


    def register():
        root2.destroy()
        root1 = Tk()
        w = 400
        h = 400
        root1.geometry(f'{w}x{h}+{480}+{170}')
        root1.configure(background="lemonchiffon2")
        root1.resizable(False, False)
        root1.title('REGISTRATION')

        def registers():
            if name.get() == '':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")
            elif idnum.get() == '':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")
            elif gender.get() == 'Gender':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")
            elif course.get() == 'Course':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")
            elif course.get() == 'Year Level':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")


            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()

            c.execute("INSERT INTO studentlist VALUES(:name, :idnum, :gender, :course_code,:year_lvl)",
                      {
                          'name': name.get(),
                          'idnum': idnum.get(),
                          'gender': gender.get(),
                          'course_code': course.get(),
                          'year_lvl': yr_lvl.get()

                      })

            conn.commit()
            messagebox.showinfo("Register Confirmation", "Successfully Registered")
            conn.close()
            root1.destroy()
            mp()
        def back():
            root1.destroy()
            mp()

        name = Entry(root1, width=30)
        name.place(x=115, y=80)

        idnum = Entry(root1, width=30)
        idnum.place(x=115, y=110)

        gender = ttk.Combobox(root1, width=12)
        gender.set("Gender")
        gender['values'] = ("Male", "Female", "Other")
        gender.place(x=115, y=150)

        c.execute("SELECT course_code FROM courselist")
        cd = c.fetchall()

        course = ttk.Combobox(root1, width=12)
        course.set("Course Code")
        course['values'] = (cd)
        course.place(x=115, y=180)

        yr_lvl = ttk.Combobox(root1, width=12)
        yr_lvl.set("Year Level")
        yr_lvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
        yr_lvl.place(x=115, y=210)

        register_lbl = Label(root1, bg="lemonchiffon2", text="Student Registration", font=('Helvetica', 15, 'bold'), fg="black")
        register_lbl.place(x=115, y=15)

        name_lbl = Label(root1, bg="lemonchiffon2", fg='black', text="Complete Name:", font=('helvetica', 10))
        name_lbl.place(x=7, y=80)

        idnum_lbl = Label(root1, bg="lemonchiffon2", text="ID Number:", fg='black', font=('helvetica', 10))
        idnum_lbl.place(x=7, y=110)

        gender_lbl = Label(root1, bg="lemonchiffon2", text="Gender:", fg='black', font=('helvetica', 10))
        gender_lbl.place(x=7, y=150)

        course_lbl = Label(root1, bg="lemonchiffon2", text="Course Code:", fg='black', font=('helvetica', 10))
        course_lbl.place(x=7, y=180)

        year_lbl = Label(root1, bg="lemonchiffon2", text="Year Level:", fg='black', font=('helvetica', 10))
        year_lbl.place(x=7, y=210)

        register_btn = Button(root1, text="REGISTER", borderwidth=5, width=15,
                              activebackground="#161618", bg="white", command=registers)
        register_btn.place(x=151, y=250)

        b = Button(root1, text="Return", bg="wheat3",
                   borderwidth=1, activebackground="#161618", command=back)
        b.place(x=313, y=310)

        root1.mainloop()


    def course_reg():

        root5 = Tk()
        w = 400
        h = 200
        root5.geometry(f'{w}x{h}+{480}+{170}')
        root5.configure(background="lemonchiffon2")
        root5.resizable(False, False)

        root5.title('REGISTRATION')

        def register_c():

            if course_code.get() == '':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")

            elif courses.get() == '':
                return messagebox.showwarning("Warning!", "Fill the empty field!!")

            else:

                conn = sqlite3.connect('StudentsList.db')
                c = conn.cursor()

                c.execute("SELECT course_code FROM courselist")
                c_d = c.fetchall()

                for i in c_d:
                    if course_code.get() in i:
                        return messagebox.showwarning("Course Register Warning", "Course Already Register")

                else:
                    conn = sqlite3.connect('StudentsList.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO courselist VALUES(:course_code, :course)",
                              {
                                  'course_code': course_code.get(),
                                  'course': courses.get()

                              })
                    conn.commit()
                    conn.close()

                    course_code.delete(0, END)
                    courses.delete(0, END)

                    messagebox.showinfo("Register Confirmation", "Successfully Registered")

                    root2.destroy()
                    root5.destroy()
                    mp()


        course_code = Entry(root5, width=30)
        course_code.place(x=115, y=50)

        courses = Entry(root5, width=30)
        courses.place(x=115, y=80)

        register_lbl = Label(root5, bg="lemonchiffon2", text="Course Registration", font=('Helvetica', 15, 'bold'),fg="black")
        register_lbl.place(x=115, y=15)

        cc_lbl = Label(root5, bg="lemonchiffon2", fg='black', text="Course Code:", font=('helvetica', 10))
        cc_lbl.place(x=7, y=50)

        c_lbl = Label(root5, bg="lemonchiffon2", text="Course:", fg='black', font=('helvetica', 10))
        c_lbl.place(x=7, y=80)

        register_btn = Button(root5, text="Register Course", borderwidth=5, width=15,
                              activebackground="black", bg="beige", command=register_c)
        register_btn.place(x=151, y=120)
        root5.mainloop()

    def courses():
        root2.destroy()
        root4 = Tk()
        w = 400
        h = 300
        root4.geometry(f'{w}x{h}+{480}+{170}')
        root4.configure(background="lemonchiffon2")
        root4.resizable(False, False)
        root4.title("Course List")


        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()

        c.execute("SELECT * FROM courselist")
        records = c.fetchall()

        frm = Frame(root4)
        frm.pack(side=tk.LEFT, padx=5, pady=(110, 0))

        tv = ttk.Treeview(frm, columns=(1, 2), show="headings", height="8")
        tv.pack()

        tv.heading(1, text="Course Code", anchor=tk.CENTER)
        tv.column("1", minwidth=0, width=110)
        tv.heading(2, text="Course Name", anchor=tk.CENTER)
        tv.column("2", minwidth=0, width=277)

        for i in records:
            tv.insert('', 'end', value=i)

        def delete():
            selected_item = tv.focus()

            if selected_item == "":
                messagebox.showerror("Delete Confirmation Error", "Please Select Record To Be Deleted")
            else:

                if messagebox.askyesno("Delete Confirmation", "Do you wanna Delete this Course?") == False:
                    return
                else:
                    messagebox.showinfo("Delete Confirmation", "Successfully Deleted")
                    conn = sqlite3.connect("StudentsList.db")
                    c = conn.cursor()
                    for selected_item in tv.selection():
                        c.execute("DELETE FROM courselist WHERE course_code=?", (tv.set(selected_item, '#1'),))
                        conn.commit()
                        tv.delete(selected_item)
                    conn.close()

        def select():
            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()

            course_code.delete(0, END)
            courses.delete(0, END)

            selected = tv.focus()
            values = tv.item(selected, 'values')

            course_code.insert(0, values[0])
            courses.insert(0, values[1])

            conn.commit()
            conn.close()

        def updates():
            if course_code.get() == '':
                return messagebox.showwarning("Warning!", "PLEASE SELECT A COURSE")

            if messagebox.askyesno("Update", "Are you sure you want to update this course?") == False:
                return
            else:
                conn = sqlite3.connect('StudentsList.db')
                c = conn.cursor()
                messagebox.showinfo("Update Info", "Update successfully")
                data1 = course_code.get()
                data2 = courses.get()

                selected = tv.selection()
                tv.item(selected, values=(data1, data2))

                c.execute(
                    "UPDATE courselist set  course_code=?, course=? WHERE course_code=? ",
                    (data1, data2, data1))

                conn.commit()
                conn.close()

        def des1():
            root4.destroy()
            mp()

        delete_more_btn = Button(root4, bg="snow", text="DELETE", fg="black", width=9, command=delete)
        delete_more_btn.place(x=85, y=10)

        back_btn = Button(root4,bg="gray", text="BACK", fg="black", width=5,command=des1)
        back_btn.place(x=5, y=5)

        update_btn = Button(root4, bg="snow", text="UPDATE", fg="black", width=9, command=updates)
        update_btn.place(x=175, y=10)

        slc_btn = Button(root4, bg="snow", text="SELECT", fg="black", width=9, command=select)
        slc_btn.place(x=275, y=10)

        course_code = Entry(root4, width=10)
        course_code.place(x=100, y=55)

        courses = Entry(root4, width=30)
        courses.place(x=65, y=80)

        cc_lbl = Label(root4, bg="lemonchiffon2", fg='black', text="Course Code:", font=('helvetica', 10))
        cc_lbl.place(x=13, y=55)

        c_lbl = Label(root4, bg="lemonchiffon2", text="Course:", fg='black', font=('helvetica', 10))
        c_lbl.place(x=13, y=80)

        root4.mainloop()

    def search():
        root3 = Tk()
        w = 995
        h = 200
        root3.geometry(f'{w}x{h}+{280}+{200}')
        root3.title('Search Record')
        root3.resizable(False, False)
        root3.configure(background="snow")

        if srch_entry.get() == "":
            root3.destroy()
            messagebox.showwarning("Search Warning", "Please Input ID Number...")

        else:
            conn = sqlite3.connect('StudentsList.db')
            c = conn.cursor()

            c.execute("""SELECT name,idnum,gender,courselist.course_code,year_lvl,courselist.course 
                                      FROM studentlist 
                                      INNER JOIN courselist  ON courselist.course_code = studentlist.course_code WHERE idnum =?
                                       """, (srch_entry.get(),))
            records = c.fetchall()

            frm = Frame(root3)
            frm.pack(side=LEFT, padx=(0, 0), pady=(0, 0))

            tv = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5), show="headings", height=13)
            tv.pack()

            tv.heading(1, text="Name", anchor=CENTER)
            tv.heading(2, text="ID Number", anchor=CENTER)
            tv.heading(3, text="Gender", anchor=CENTER)
            tv.heading(4, text="Course", anchor=CENTER)
            tv.heading(5, text="Year Level", anchor=CENTER)

            for i in records:
                tv.insert('', 'end', value=i)

            if not records:
                root3.destroy()
                messagebox.showinfo("Search Information", "Student Doesn't Exist or Wrong Input")


        root3.mainloop()

    # delete button
    delete_more_btn = Button(root2, bg="RosyBrown3", text="DELETE", fg="black", width=9, command=delete)
    delete_more_btn.place(x=900, y=20)

    # Update button
    update_btn = Button(root2, bg="snow", text="UPDATE", fg="black", width=9, command=update)
    update_btn.place(x=800, y=20)

    # Select Button
    slc_btn = Button(root2, bg="SlateGray2", text="SELECT", fg="black", width=9, command=slc)
    slc_btn.place(x=700, y=20)

    def des():
        if messagebox.askyesno("EXIT INFO","ARE YOU SURE YOU WANT TO QUIT?") == False:
            return
        else:
            root2.destroy()

    #exit button
    ex_btn = Button(root2, text="EXIT", compound=CENTER, bg="red4", borderwidth=3, fg="white", activebackground="red", command=des)
    ex_btn.place(x=5, y=10)

    # search button
    search_btn = Button(root2, bg="snow", text="Search", fg="black", width=10, activebackground="#161618", command=search)
    search_btn.place(x=155, y=98)

    register_btn = Button(root2, text="Register Student", bg="beige", borderwidth=3, command=register)
    register_btn.place(x=60, y=10)

    registercourse_btn = Button(root2, text="Register Course", bg="lemonchiffon", borderwidth=3,fg="black",command=course_reg)
    registercourse_btn.place(x=170, y=10)

    course_btn = Button(root2, text="Courses", bg="bisque2", borderwidth=3, fg="black",command=courses)
    course_btn.place(x=275, y=10)

    # combobox Entry
    gender = ttk.Combobox(root2, width=12)
    gender.set("Gender")
    gender['values'] = ("Male", "Female", "Other")
    gender.place(x=890, y=60)

    yr_lvl = ttk.Combobox(root2, width=12)
    yr_lvl.set("Year Level")
    yr_lvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
    yr_lvl.place(x=890, y=90)

    c.execute("SELECT course_code FROM courselist")
    cd = c.fetchall()
    course = ttk.Combobox(root2, width=12)
    course.set("Course Code")
    course['values'] = (cd)
    course.place(x=790, y=120)

    name_lbl = Label(root2, bg="antiquewhite2", fg='black', text="Name:", font=('helvetica', 10))
    name_lbl.place(x=700, y=60)
    name = Entry(root2, width=20, borderwidth=3, bg="white")
    name.place(x=750, y=60)

    idnum_lbl = Label(root2, bg="antiquewhite2", text="ID Number:", fg='black', font=('helvetica', 10))
    idnum_lbl.place(x=680, y=90)
    idnum = Entry(root2, width=20, borderwidth=3, bg="white")
    idnum.place(x=750, y=90)

    srch_entry = Entry(root2, width=15, borderwidth=4)
    srch_entry.place(x=50, y=100)

    # label
    minse = Label(root2, text="Type ID Number to search", font=("Helvitica", 13, "bold"), bg="antiquewhite2", fg="black")
    minse.place(x=40, y=68)

    root2.mainloop()

mp()

