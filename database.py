import sqlite3
import json
import logging
from datetime import datetime


# Set up logging
logging.basicConfig(
    filename="database_log.txt",  # Log file location
    level=logging.INFO,        # Log level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format with timestamp
)


# ------------------------------- EMAIL DataBase----------------------------------------
def create_email_db():
    try:
        # Connect to the email DB or create it if it doesn't exist
        connection = sqlite3.connect("email.db")
        cursor = connection.cursor()

        # Check if the "email" table exists, if not, create it
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS email (
            email_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            sender TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            urls TEXT,
            attachments TEXT
        );
        """)

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        logging.info("Email table created.")

    except sqlite3.Error as err:
        logging.info(f"An error occurred while creating email DB: {err}")


def add_to_table_email(email_date, email_sender, email_subject, email_body, email_urls, email_attachments):
    try:
        # Connect to the email DB
        connection = sqlite3.connect("email.db")
        cursor = connection.cursor()

        urls = json.dumps(email_urls)
        attachments = json.dumps(email_attachments)

        # Check if the domain already exists
        cursor.execute("SELECT 1 FROM email WHERE sender = ? and subject=? and body=?", (email_sender, email_subject, email_body))
        if cursor.fetchone():
            logging.info(f"{email_subject} email from {email_sender} already exists in the database. Skipping insertion.")
            connection.close()
            return

        # Insert new data into the email table
        cursor.execute("""
        INSERT INTO email (date, sender, subject, body, urls, attachments)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (email_date, email_sender, email_subject, email_body, urls, attachments))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        logging.info(f"Email from {email_sender} added successfully.")

    except sqlite3.Error as err:
        logging.error(f"An error occurred while adding data to email DB: {err}")


# ------------------------------- URL DataBase----------------------------------------
def create_url_db():
    try:
        # Connect to the email DB or create it if it doesn't exist
        connection = sqlite3.connect("url.db")
        cursor = connection.cursor()

        # Check if the "url" table exists, if not, create it
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS url (
            url_id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            virus_total TEXT
        );
        """)

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        logging.info("URL table created.")

    except sqlite3.Error as err:
        logging.info(f"An error occurred while creating URL DB: {err}")



def add_to_table_url(url, vt):
    try:
        # Connect to the email DB
        connection = sqlite3.connect("url.db")
        cursor = connection.cursor()

        # Check if the domain already exists
        cursor.execute("SELECT 1 FROM url WHERE url = ?", (url,))
        if cursor.fetchone():
            logging.info(f"{url} already exists in the database. Skipping insertion.")
            connection.close()
            return

        # Insert new data into the email table
        cursor.execute("""INSERT INTO url (url, virus_total)
        VALUES (?, ?);""",(url, vt))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        logging.info(f"{url} URL added successfully.")

    except sqlite3.Error as err:
        logging.error(f"An error occurred while adding data to URL DB: {err}")


# ------------------------------- Domain DataBase----------------------------------------
def create_domain_db():
    try:
        # Connect to the domain DB or create it if it doesn't exist
        connection = sqlite3.connect("domain.db")
        cursor = connection.cursor()

        # Check if the "url" table exists, if not, create it
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS domain(
            domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            virus_total TEXT
        );
        """)

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        logging.info("Domain table created.")

    except sqlite3.Error as err:
        logging.info(f"An error occurred while creating Domain DB: {err}")



def add_to_table_domain(domain, vt):
    try:
        # Connect to the domain DB
        connection = sqlite3.connect("domain.db")
        cursor = connection.cursor()

        # Check if the domain already exists
        cursor.execute("SELECT 1 FROM domain WHERE domain = ?", (domain,))
        if cursor.fetchone():
            logging.info(f"{domain} already exists in the database. Skipping insertion.")
            connection.close()
            return

        # Insert new data into the domain table
        cursor.execute("""
            INSERT INTO domain (domain, virus_total)
            VALUES (?, ?);
        """, (domain, vt))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        logging.info(f"{domain} added successfully.")

    except sqlite3.Error as err:
        logging.error(f"An error occurred while adding data to domain DB: {err}")


def read_all_emails():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('email.db')
        cursor = conn.cursor()

        # Fetch all rows from the "email" table
        cursor.execute("SELECT email_id, sender, subject, body FROM email")
        rows = cursor.fetchall()

        # Print the header row (columns) - fixed width with separators and centered headers
        print(f"{'ID':^5} | {'Sender':^30} | {'Subject':^50} | {'Body':^100}")
        print("="*185)  # Print a line separator to make it visually clean

        # Print each row with fixed width and separator
        for row in rows:
            email_id, sender, subject, body = row

            # Truncate content if it exceeds the width for each column
            sender = sender[:30]  # Truncate sender to 30 characters
            subject = subject[:30]  # Truncate subject to 50 characters
            body = body[:30]  # Truncate body to 100 characters

            # Print each row with fixed width and separators
            print(f"{email_id:^5} | {sender:^30} | {subject:^50} | {body:^100}")

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
