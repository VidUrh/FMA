import sqlite3
import sys
import pytest

sys.path.append("../src")

import parameters
from transaction import Transaction
from member import Member


@pytest.fixture()
def clean_database():
    conn = sqlite3.connect(parameters.databasePath)
    c = conn.cursor()

    # Check if the transaction already exists in the table
    c.execute("DELETE FROM members")
    c.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()

def test_save_member(clean_database):
    # Create a new member
    member = Member("John", "Doe", "M", True, "Section 1")

    # Save the member to the database
    member.save()

    # Retrieve the member from the database
    members = Member.select()

    # Check that the member was saved correctly
    assert len(members) == 1
    assert members[0].first_name == "John"
    assert members[0].last_name == "Doe"
    assert members[0].sex == "M"
    assert members[0].has_dress == True
    assert members[0].section == "Section 1"
    assert members[0].balance == 0.0

def test_update_member(clean_database):
    # Create a new member
    member = Member("John", "Doe", "M", True, "Section 1")
    member.save()

    # Update the member
    member.first_name = "Jane"
    member.has_dress = False
    member.save()

    # Retrieve the member from the database
    members = Member.select()

    # Check that the member was updated correctly
    assert len(members) == 1
    assert members[0].first_name == "Jane"
    assert members[0].has_dress == False

def test_save_transaction(clean_database):
    # Create two new members
    sender = Member("Jane", "Doe", "F", False, "Section 1")
    receiver = Member("John", "Doe", "M", True, "Section 1")
    
    sender.save()
    receiver.save()

    # Create a new transaction
    transaction = Transaction(sender.member_id, receiver.member_id, 100.0,"Test transaction","Test","2022-01-01")
    # Save the transaction to the database
    transaction.save()

    # Retrieve the transactions from the database
    transactions = Transaction.select()

    # Check that the transaction was saved correctly
    assert len(transactions) == 1
    assert transactions[0][1] == sender.member_id
    assert transactions[0][2] == receiver.member_id
    assert transactions[0][3] == 100.0
    assert transactions[0][4] == "Test transaction"
    assert transactions[0][5] == "Test"
    assert transactions[0][6] == "2022-01-01"

    # Check that the balances of the sender and receiver were updated correctly
    sender = Member.get_member_by_id(sender.member_id)
    receiver = Member.get_member_by_id(receiver.member_id)
    assert sender.balance == -100.0
    assert receiver.balance == 100.0
