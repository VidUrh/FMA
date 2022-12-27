import customtkinter as ctk
from tkinter import ttk,Entry,Listbox
import tkinter as tk
from member import Member
from transaction import Transaction


class AutoCompleteEntry():
    def __init__(self, root, data):
        self.root = root
        self.allData = data
        self.data = [name for name in data]
        # creating list box
        """
        self.entry = ctk.CTkComboBox(root)
        self.entry.set("")
        self.entry.bind('<KeyRelease>', self.checkKeyPressed)
        """ 
        self.entryFrame = ctk.CTkFrame(self.root)
        
        #creating text box 
        self.entry = ctk.CTkEntry(self.entryFrame)
        self.entry.bind('<KeyRelease>', self.checkKeyPressed)
        self.entry.bind('<Down>',self.setFocusOnListBox)
        self.entry.grid(row=0,column=0,padx=10,pady=10)
        self.entryFrame.get = self.entry.get
        self.dropdown = Listbox(self.entryFrame, font=("Roboto", 10), background="#343638",
                     highlightcolor="#565b5e",
                     highlightbackground="#565b5e",
                     highlightthickness=2, fg="#d6d6d6")
        self.dropdown.bind('<<ListboxSelect>>', self.onSelect)
        self.dropdown.grid(row=1,column=0,padx=10,pady=10)
        #self.dropdown.configure(style="Custom.TEntry")
        self.selected = None
        self.update()

    def setFocusOnListBox(self,evt):
        self.dropdown.focus()
        self.dropdown.select_set(0)
        self.dropdown.event_generate('<<ListboxSelect>>')
        self.entry.focus()
    def onSelect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        if not w.curselection(): return  # Check if the tuple is not empty
        index = int(w.curselection()[0])
        value = w.get(index)
        self.selected = value
        member_id, *_ = value.split()
        self.entry.delete(0,100)
        self.entry.insert(0,value)

        self.update()

    def checkKeyPressed(self,event):
        value = self.entry.get()
        if value == '':
            self.data = [x for x in self.allData]
        else:
            self.data = []
            for item in self.allData:
                if value.lower() in item.lower():
                    self.data.append(item)
        self.update()

    def update(self):
        # clear previous data
        self.dropdown.delete(0, 'end')
    
        # put new data
        for index, item in enumerate(self.data):
            self.dropdown.insert('end', item)
            if item == self.selected:
                self.dropdown.select_set(index)


class MemberWindow:
    def __init__(self, root, memberView):
        # Create the main window
        self.window = root
        self.memberView = memberView
        # Create the widgets for the "Name" section
        self.name_label = ctk.CTkLabel(self.window, text="Name")
        self.first_name_entry = ctk.CTkEntry(self.window)
        self.last_name_entry = ctk.CTkEntry(self.window)

        # Create the widgets for the "Sex" section
        self.sex_label = ctk.CTkLabel(self.window, text="Sex")
        self.sex_entry = ctk.CTkEntry(self.window)

        # Create the widgets for the "Dress" section
        self.dress_label = ctk.CTkLabel(self.window, text="Dress")
        self.dress_checkbox = ctk.CTkCheckBox(self.window, text="Has Dress")

        # Create the widgets for the "Section" section
        self.section_label = ctk.CTkLabel(self.window, text="Section")
        self.section_entry = ctk.CTkEntry(self.window)

        # Create the "Add Member" button
        self.add_button = ctk.CTkButton(
            self.window, text="Add Member", command=self.add_member)

        # Place the widgets in the window using a grid layout
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.last_name_entry.grid(row=0, column=2, padx=10, pady=10)
        self.sex_label.grid(row=1, column=0, padx=10, pady=10)
        self.sex_entry.grid(row=1, column=1, padx=10, pady=10)
        self.dress_label.grid(row=2, column=0, padx=10, pady=10)
        self.dress_checkbox.grid(row=2, column=1, padx=10, pady=10)
        self.section_label.grid(row=3, column=0, padx=10, pady=10)
        self.section_entry.grid(row=3, column=1, padx=10, pady=10)
        self.add_button.grid(row=4, column=1, padx=10, pady=10)

    def add_member(self):
        # Get the values from the entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        sex = self.sex_entry.get()
        has_dress = bool(self.dress_checkbox.get())
        section = self.section_entry.get()

        # Create a new Member instance and save it to the database
        member = Member(first_name, last_name, sex, has_dress, section)
        member.save()
        self.memberView.load_members()


class TransactionWindow:
    def __init__(self, root, memberView):
        # Create the main window
        self.window = root
        self.memberView = memberView
        # Create the widgets for the "Sender" section
        self.sender_amount_label = ctk.CTkLabel(self.window, text="Amount")
        self.sender_amount_entry = ctk.CTkEntry(self.window)
        
        memberValues = self.getMemberValues()
        self.sender_label = ctk.CTkLabel(self.window, text="Sender")
        self.sender_id_entry = AutoCompleteEntry(self.window, memberValues).entryFrame

        # Create the widgets for the "Receiver" section
        self.receiver_label = ctk.CTkLabel(self.window, text="Receiver")
        self.receiver_id_entry = AutoCompleteEntry(self.window, memberValues).entryFrame


        # Create the widgets for the "Description" section
        self.description_label = ctk.CTkLabel(self.window, text="Description")
        self.description_entry = ctk.CTkEntry(self.window)

        # Create the widgets for the "Category" section
        self.category_label = ctk.CTkLabel(self.window, text="Category")
        self.category_entry = ctk.CTkEntry(self.window)

        # Create the "Add Transaction" button
        self.add_button = ctk.CTkButton(
            self.window, text="Add Transaction", command=self.add_transaction)

        # Place the widgets in the window using a grid layout
        self.sender_amount_label.grid(row=0, column=0, padx=10, pady=10)
        self.sender_amount_entry.grid(row=0, column=1, padx=10, pady=10)
        self.sender_label.grid(row=1, column=0, padx=10, pady=10)
        self.sender_id_entry.grid(row=1, column=1, padx=10, pady=10,rowspan = 4)
        self.receiver_label.grid(row=1, column=2, padx=10, pady=10)
        self.receiver_id_entry.grid(row=1, column=3, padx=10, pady=10,rowspan = 4)
        self.category_label.grid(row=5, column=0, padx=10, pady=10)
        self.category_entry.grid(row=5, column=1, padx=10, pady=10)
        self.description_label.grid(row=6, column=0, padx=10, pady=10)
        self.description_entry.grid(row=6, column=1, padx=10, pady=10)
        self.add_button.grid(row=7, column=1, padx=10, pady=10)

    def add_transaction(self):
        # Get the values from the entry widgets
        sender_id = int(self.sender_id_entry.get().split()[0])
        amount = float(self.sender_amount_entry.get())
        receiver_id = int(self.receiver_id_entry.get().split()[0])
        description = self.description_entry.get()
        category = self.category_entry.get()

        # Create a new Transaction instance and save it to the database
        transaction = Transaction(
            sender_id, receiver_id, amount, description, category)
        transaction.save()
        self.memberView.load_members()

    def getMemberValues(self):
        members = []
        for member in Member.select():
            members.append(f"{member.member_id} {member.full_name()}")
        return members


class MemberView:
    def __init__(self, root):
        self.window = root

        # Create the Treeview widget
        self.tree = ttk.Treeview(self.window)
        self.tree["columns"] = (
            "member_id", "first_name", "last_name", "sex", "has_dress", "section", "balance")

        self.tree.column("#0", width=0, minwidth=0)
        self.tree.column("member_id", width=50, minwidth=50)
        self.tree.column("first_name", width=100, minwidth=100)
        self.tree.column("last_name", width=100, minwidth=100)
        self.tree.column("sex", width=50, minwidth=50)
        self.tree.column("has_dress", width=75, minwidth=75)
        self.tree.column("section", width=75, minwidth=75)
        self.tree.column("balance", width=75, minwidth=75)

        self.tree.heading("member_id", text="Member ID", anchor=ctk.W)
        self.tree.heading("first_name", text="First Name", anchor=ctk.W)
        self.tree.heading("last_name", text="Last Name", anchor=ctk.W)
        self.tree.heading("sex", text="Sex", anchor=ctk.W)
        self.tree.heading("has_dress", text="Has Dress", anchor=ctk.W)
        self.tree.heading("section", text="Section", anchor=ctk.W)
        self.tree.heading("balance", text="Balance", anchor=ctk.W)

        self.load_members()
        # Pack the Treeview widget and start the main loop
        self.tree.pack(expand=True, fill=ctk.BOTH)

    def load_members(self):
        self.tree.delete(*self.tree.get_children())
        members = Member.select()
        for member in members:
            self.tree.insert("", "end",
                             values=(
                                 member.member_id,
                                 member.first_name,
                                 member.last_name,
                                 member.sex,
                                 member.has_dress,
                                 member.section,
                                 member.balance
                             )
                             )


class TabWindow:
    def __init__(self, root):
        self.root = root
        self.tabview = ctk.CTkTabview(self.root, width=250)

        self.tabview.add("Transactions")
        self.tabview.add("Members")

        frameTransaction = ctk.CTkFrame(self.tabview.tab("Transactions"))
        frameMember = ctk.CTkFrame(self.tabview.tab("Members"))
        frameMemberView = ctk.CTkFrame(self.tabview.tab("Members"))

        self.memberView = MemberView(frameMemberView)
        self.transactionWindow = TransactionWindow(frameTransaction, self.memberView)
        self.memberWindow = MemberWindow(frameMember, self.memberView)

        self.transactionWindow.window.pack()
        self.memberWindow.window.pack()
        self.memberView.window.pack()

        self.tabview.pack()


class App():
    def __init__(self):
        # Create the main window
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Made with love for VAL")
        self.root.geometry("700*500")

        self.tabwindow = TabWindow(self.root)
        self.root.mainloop()


App()
