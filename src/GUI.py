"""A module for creating and managing a GUI for a membership database.

This module contains classes for creating graphical user interface (GUI) windows
for adding and managing members and transactions in a membership database.
The `MemberWindow` class provides a GUI for adding new members to the database,
while the `TransactionWindow` class provides a GUI for adding new transactions between members.
"""

import customtkinter as tk
from member import Member
from transaction import Transaction


class MemberWindow:
    """A GUI window for adding new members to the database.

    The MemberWindow class provides a graphical user interface
    for adding new members to the database.
    It consists of several entry widgets for entering the member's:
        - name
        - sex
        - dress status
        - and section
    as well as a checkbox for indicating whether the member has a dress.
    The window also has a button for adding the new member to the database.
    """

    def __init__(self, root):
        """Initialize the member window and its widgets.

        :param root: The parent widget of the member window.
        """

        # Create the main window
        self.window = root

        # Create the widgets for the "Name" section
        self.name_label = tk.CTkLabel(self.window, text="Name")
        self.first_name_entry = tk.CTkEntry(self.window)
        self.first_name_entry.insert(0, "Enter First Name")
        self.last_name_entry = tk.CTkEntry(self.window)
        self.last_name_entry.insert(0, "Enter Last Name")

        # Create the widgets for the "Sex" section
        self.sex_label = tk.CTkLabel(self.window, text="Sex")
        self.sex_entry = tk.CTkEntry(self.window)
        self.sex_entry.insert(0, "Enter Sex")

        # Create the widgets for the "Dress" section
        self.dress_label = tk.CTkLabel(self.window, text="Dress")
        self.dress_checkbox = tk.CTkCheckBox(self.window, text="Has Dress")

        # Create the widgets for the "Section" section
        self.section_label = tk.CTkLabel(self.window, text="Section")
        self.section_entry = tk.CTkEntry(self.window)
        self.section_entry.insert(0, "Enter Section")

        # Create the "Add Member" button
        self.add_button = tk.CTkButton(
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

        self.window.pack()

    def add_member(self):
        """Add a new member to the database using the values entered in the entry widgets.

        :raises ValueError: If any of the required fields are empty.
        """
        # Get the values from the entry widgets
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        sex = self.sex_entry.get()
        has_dress = self.dress_checkbox.get()
        section = self.section_entry.get()

        # Create a new Member instance and save it to the database
        member = Member(first_name, last_name, sex, has_dress, section)
        member.save()


class TransactionWindow:
    """A GUI window for adding new transactions to the database.

    The TransactionWindow class provides a graphical user interface
    for adding new transactions to the database.
    It consists of several entry widgets for entering the:
        - sender's ID
        - receiver's ID
        - transaction amount
    as well as a text area for entering a description of the transaction.
    The window also has a button for adding the new transaction to the database.
    """

    def __init__(self, root):
        """Initialize the transaction window and its widgets.

        :param root: The parent widget of the transaction window.
        """
        # Create the main window
        self.window = root

        # Create the widgets for the "Sender" section
        self.sender_label = tk.CTkLabel(self.window, text="Sender")
        self.sender_id_entry = tk.CTkEntry(self.window)
        self.sender_id_entry.insert(0, "Enter Sender ID")
        self.sender_amount_entry = tk.CTkEntry(self.window)
        self.sender_amount_entry.insert(0, "Enter Amount")

        # Create the widgets for the "Receiver" section
        self.receiver_label = tk.CTkLabel(self.window, text="Receiver")
        self.receiver_id_entry = tk.CTkEntry(self.window)
        self.receiver_id_entry.insert(0, "Enter Receiver ID")

        # Create the widgets for the "Description" section
        self.description_label = tk.CTkLabel(self.window, text="Description")
        self.description_entry = tk.CTkEntry(self.window)
        self.description_entry.insert(0, "Enter Description")

        # Create the widgets for the "Category" section
        self.category_label = tk.CTkLabel(self.window, text="Category")
        self.category_entry = tk.CTkEntry(self.window)
        self.category_entry.insert(0, "Enter Category")

        # Create the "Add Transaction" button
        self.add_button = tk.CTkButton(
            self.window, text="Add Transaction", command=self.add_transaction)

        # Place the widgets in the window using a grid layout
        self.sender_label.grid(row=0, column=0, padx=10, pady=10)
        self.sender_id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.sender_amount_entry.grid(row=0, column=2, padx=10, pady=10)
        self.receiver_label.grid(row=1, column=0, padx=10, pady=10)
        self.receiver_id_entry.grid(row=1, column=1, padx=10, pady=10)
        self.description_label.grid(row=2, column=0, padx=10, pady=10)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)
        self.category_label.grid(row=3, column=0, padx=10, pady=10)
        self.category_entry.grid(row=3, column=1, padx=10, pady=10)
        self.add_button.grid(row=4, column=1, padx=10, pady=10)

        self.window.pack()

    def add_transaction(self):
        """Add a new transaction to the database using the values entered in the entry widgets.

        :raises ValueError: If any of the required fields are empty
        or if the transaction amount is not a valid number.
        :raises KeyError: If the sender or receiver ID does not match any member in the database.
        """
        # Get the values from the entry widgets
        sender_id = self.sender_id_entry.get()
        amount = self.sender_amount_entry.get()
        receiver_id = self.receiver_id_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()

        # Create a new Transaction instance and save it to the database
        transaction = Transaction(
            sender_id, receiver_id, amount, description, category)
        transaction.save()


class App():
    """The main application class for the membership database GUI.

    The App class manages the overall flow of the membership database GUI application.
    It creates and displays the main window and the member and transaction windows,
    and handles switching between them.
    """

    def __init__(self):
        # Create the main window
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme("dark-blue")

        self.root = tk.CTk()
        self.root.title("Made with love for VAL")
        self.root.geometry("700*500")

        self.tabview = tk.CTkTabview(self.root, width=250)
        self.tabview.add("Members")
        self.tabview.add("Transactions")

        frame_transaction = tk.CTkFrame(self.tabview.tab("Transactions"))
        frame_member = tk.CTkFrame(self.tabview.tab("Members"))

        TransactionWindow(frame_transaction)
        MemberWindow(frame_member)

        self.tabview.pack()
        self.root.mainloop()


App()
