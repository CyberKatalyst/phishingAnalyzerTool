# Import required libraries and custom modules
import extract_email_info


def analyze_email():
    print("Your email is being analyzed...")
    extract_email_info.get_info("C:\\Users\\97258\\Downloads\\scam.eml")
    exit()


def report_request():
    print("The analysis report:")
    exit()


def menu_tab():
    while True:
        print("[1] - 🔍 Analyze the email\n"
              "[2] - 📄 Report the email\n"
              "[3] - ╰┈➤🚪 Exit")
        print("-" * 50)
        try:
            option = int(input("Enter your choice: "))
            if option == 1:
                analyze_email()
            elif option == 2:
                report_request()
            elif option == 3:
                print("Exiting the program.")
                exit()
            else:
                print("⚠️ Invalid choice. Please enter a number between 1 and 3.")
                print("-" * 50)
        except ValueError:
            print("⚠️ Invalid entry. Please enter a valid number.")
            print("-" * 50)

