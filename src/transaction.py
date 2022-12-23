import sqlite3
import datetime
import parameters
from member import Member


class Transaction:
    def __init__(self, sender_id, receiver_id, amount, description, category, date=None):
        self.transaction_id = 0
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = float(amount)
        self.description = description
        self.category = category
        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = date

    def save(self):
        """
        This method doesn't take paramaters. It doesn't return anything.
        It saves (or updates) the current Transaction object into the database.
        It also modifies the sender's and recipient's balance by the transaction budget and saves
        them to database.
        """

        # Connect to the database
        conn = sqlite3.connect(parameters.databasePath)
        cursor = conn.cursor()

        # Check if the transaction already exists in the table
        cursor.execute("SELECT * FROM transactions WHERE transaction_id=?",
                       (self.transaction_id,))
        transaction = cursor.fetchone()

        if transaction:
            # Update the existing row
            cursor.execute(
                "UPDATE transactions SET sender_id=?, receiver_id=?, amount=?, description=?, category=?, date=? WHERE transaction_id=?",
                (self.sender_id, self.receiver_id, self.amount,
                 self.description, self.category, self.date, self.transaction_id)
            )
        else:
            # Insert a new row
            cursor.execute(
                "INSERT INTO transactions (transaction_id, sender_id, receiver_id, amount, description, category, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                    self.transaction_id, self.sender_id, self.receiver_id, self.amount, self.description, self.category, self.date)
            )
            self.transaction_id = cursor.lastrowid

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
        """
        This classmethod takes one parameter cls, which is always Transaction class in this case.
        It queries the database for all rows of this class.

        Parameters:
        - cls (className): A required class parameter (Example: Transaction.select()).

        Returns:
        - rows: array of all the rows from database, presented as a tuple.
        """
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
