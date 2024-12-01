# Import required libraries and custom modules
import pyfiglet
import menu


def main():
    Title = pyfiglet.figlet_format("Email Analyzer")
    print(Title)
    menu.menu_tab()


if __name__ == "__main__":
    main()
