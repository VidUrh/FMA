import sqlite3
import parameters
import datetime
from member import Member

class Transaction:
    def __init__(self, sender_id, receiver_id, amount, description, category, date = None):
        self.transaction_id = 0
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.description = description
        self.category = category
        if date is None:
            self.date = datetime.datetime()
        else:
            self.date = date
    def save(self):
        # Connect to the database
        conn = sqlite3.connect(parameters.databasePath)
        c = conn.cursor()

        # Check if the transaction already exists in the table
        c.execute("SELECT * FROM transactions WHERE transaction_id=?",
                  (self.transaction_id,))
        transaction = c.fetchone()

        if transaction:
            # Update the existing row
            c.execute(
                "UPDATE transactions SET sender_id=?, receiver_id=?, amount=?, description=?, category=?, date=? WHERE transaction_id=?",
                (self.sender_id, self.receiver_id, self.amount,
                 self.description, self.category, self.date, self.transaction_id)
            )
        else:
            # Insert a new row
            c.execute(
                "INSERT INTO transactions (transaction_id, sender_id, receiver_id, amount, description, category, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                    self.transaction_id, self.sender_id, self.receiver_id, self.amount, self.description, self.category, self.date)
            )
            self.transaction_id = c.lastrowid
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()


        # Update the balance of the sender and receiver members
        sender = Member.get_member_by_id(self.sender_id)
        receiver = Member.get_member_by_id(self.receiver_id)
        if sender:
            sender.pay(self.amount)
            sender.save()
        else:
            raise Exception("Sender not in the member database")
        if receiver:
            receiver.receive_payment(self.amount)
            receiver.save()
        else:
            raise Exception("Receiver not in the member database")

        

    @classmethod
    def select(cls):
        # Connect to the database
        connection = sqlite3.connect(parameters.databasePath)
        cursor = connection.cursor()

        # Execute the SELECT statement
        cursor.execute("SELECT * FROM transactions")

        # Fetch all the rows
        rows = cursor.fetchall()

        # Close the connection
        connection.close()

        # Return the rows
        return rows
