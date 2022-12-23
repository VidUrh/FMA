import sqlite3
import parameters


class Member:
    def __init__(self, first_name, last_name, sex, has_dress, section, balance=0.00):
        self.member_id = -1
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.has_dress = has_dress
        self.balance = balance
        self.section = section

    @classmethod
    def select(cls):
        members = []
        connection = sqlite3.connect(parameters.databasePath)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        for row in rows:
            member = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            member.member_id = row[0]
            members.append(member)
        connection.close()
        return members

    @classmethod
    def get_member_by_id(cls, member_id):
        connection = sqlite3.connect(parameters.databasePath)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members WHERE member_id=?", (member_id,))
        row = cursor.fetchone()
        if row:
            member = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            member.member_id = row[0]
            return member
        return None

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def pay(self, amount):
        self.balance -= amount

    def receive_payment(self, amount):
        self.balance += amount

    def save(self):
        # Connect to the database
        conn = sqlite3.connect(parameters.databasePath)
        cursor = conn.cursor()

        # Check if the member already exists in the table
        cursor.execute("SELECT * FROM members WHERE member_id=?", (self.member_id,))
        member = cursor.fetchone()

        if member:
            # Update the existing row
            cursor.execute(
                "UPDATE members SET first_name=?, last_name=?, sex=?, has_dress=?, balance=? WHERE member_id=?",
                (self.first_name, self.last_name, self.sex,
                 self.has_dress, self.balance, self.member_id)
            )
        else:
            # Insert a new row
            cursor.execute(
                "INSERT INTO members (first_name, last_name, sex, has_dress, balance, section) VALUES (?, ?, ?, ?, ?, ?)",
                (self.first_name, self.last_name,
                 self.sex, self.has_dress, self.balance, self.section)
            )
            self.member_id = cursor.lastrowid

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
