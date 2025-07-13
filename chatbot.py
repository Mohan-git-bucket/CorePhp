# chatbot.py
import sys

# Sample backend data
backend_data = {
    "login": "To login, click the login button and enter your credentials.",
    "register": "To register, fill out the registration form and submit.",
    "reset password": "Click 'Forgot Password' and follow the instructions.",
    "profile update": "Go to your profile page and click 'Edit Profile'."
}

def search_backend(query):
    results = []
    for key, value in backend_data.items():
        if query.lower() in key:
            results.append(f"{key.title()}: {value}")
    return results

def main():
    print("Welcome to the Chatbot! Type your search query:")
    for line in sys.stdin:
        query = line.strip()
        if not query:
            continue
        results = search_backend(query)
        if results:
            for res in results:
                print(res)
        else:
            print("No results found. Try another keyword.")
        print("\nType your search query:")

if __name__ == "__main__":
    main()