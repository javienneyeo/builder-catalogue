class CliHandler:
    def __init__(self):
        pass

    def get_input(self, prompt):
        print()
        return input(f"[bobby]: {prompt} ")
    
    def print_divider(self):
        print("=============================================")

    def print_guide(self, username):
        self.print_output("What would you like to do today?")
        print("======== Main Menu ========")
        print("1. See all users")
        print("2. See all available sets")
        print("3. Find buildable sets")
        print("4. Find collaborators to build a set")
        print("5. Find buildable sets without following color")
        print("6. Find pieces needed to build a set")
        print("7. How much of a set can I build") 
        print("8. Exit")
        choice = input(f"[{username}]: ")
        return choice
    
    def print_welcome_header(self):
        self.print_divider()
        print("WELCOME TO THE BUILDER CATALOGUE")
        print("Explore. Combine. Create your masterpiece!")
        self.print_divider()

    def print_error(self, error_message):
        print(f"[Error]: {error_message}")

    def print_output(self, message):
        print()
        print(f"[bobby]: {message}")

    def print_list(self, item_list):
        if len(item_list) > 0:
            for item in item_list:
                print(f"- {item}")
        else:
            print("<< No items found >>")

    def print_hello(self, username):
        self.print_output(f"Hello {username}!")