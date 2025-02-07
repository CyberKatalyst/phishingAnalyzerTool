# Import required libraries and custom modules
import email_functions
from tabulate import tabulate
import suspicion_check


def analyze_email():
    try:
        date, sender, subject, body, urls, attachments = email_functions.extract_info("C:\\Users\\97258\\Downloads\\suspicious.eml")
        domain = email_functions.extract_domain(sender)

        # Prepare data in a list of lists or tuples
        data = [["Date", date], ["Sender", sender], ["Sender Domain", domain], ["Subject", subject], ["Body", body], ["URLs", urls], ["Attachments", attachments]]

        # Using tabulate to format the output with "plain" table format (no extra spaces)
        print(tabulate(data, tablefmt="grid"))

    except Exception as e:
        # Catch any error and print it
        print(f"⚠️ Error during email analysis: {e}")

    print("\nEmail information has been extracted.\n")
    answer = input("Do you want to process and analyze the email [y/n] ?  ")
    print("\n📊 Analysis report")
    print("-" * 50)
    if answer.lower() == "y":
        suspicion_check.url_check(urls)
        print("-" * 50)
        suspicion_check.domain_check(domain)
        print("-" * 50)
        suspicion_check.body_check(body)
        print("-"*50)
    elif answer.lower() == "n":
        exit()
    else:
        print("⚠️ Invalid choice. Please enter a number between 1 and 3.")
        print("-" * 50)


def report_request():
    print("The analysis report:")


def general_menu_tab():
    while True:
        print("[1] - 🔍 Analyze the email\n"
              "[2] - 📄 Report the email\n"
              "[3] - ╰┈➤🚪 Exit")
        print("-" * 50)
        try:
            option = int(input("Enter your choice: "))
            if option == 1:
                analyze_email()
                break
            elif option == 2:
                report_request()
                break
            elif option == 3:
                print("\nExiting the program.")
                exit()
            else:
                print("⚠️ Invalid choice. Please enter a number between 1 and 3.")
                print("-" * 50)
        except ValueError:
            print("⚠️ Invalid entry. Please enter a valid number.")
            print("-" * 50)

