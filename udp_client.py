import socket

# Output Menu to the Console

def display_main_menu():
    print("\nChoose type of operations:")
    print("1. Decimal")
    print("2. Binary")
    print("3. Support")
    print("4. Exit")

def display_decimal_menu():
    print("\nDecimal operations:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exponent")
    print("6. Modulo")
    print("7. Back to main menu")

def display_binary_menu():
    print("\nBinary operations:")
    print("1. Add")
    print("2. Unsigned Subtract")
    print("3. Signed Subtract")
    print("4. Back to main menu")

# Menu Tree

def get_operation_choice(menu_type):
    if menu_type == "decimal":
        display_decimal_menu()
    elif menu_type == "binary":
        display_binary_menu()

    choice = int(input("Select operation: "))
    if menu_type == "decimal":
        operations = ["add", "subtract", "multiply", "divide", "exponent", "modulo"]
    elif menu_type == "binary":
        operations = ["add", "unsigned_subtract", "signed_subtract"]
    
    if choice == len(operations) + 1:
        return "back"
    else:
        return operations[choice - 1]

def initiate_support_session(s, serverAddr):
    # The client waits for the initial welcome message from the server
    data, _ = s.recvfrom(1024)
    print("Server:", data.decode())

    # Support Initialization

    while True:
        message = input("Enter message (type 'exit' to end support): ")
        s.sendto(message.encode(), serverAddr)
        if message.lower() == "exit":
            break

        # Client waits for a response from the server
        response, _ = s.recvfrom(1024)
        print("Server:", response.decode())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 15000
serverAddr = ('10.228.211.87', port)

# Python Socket Initialization

try:
    while True:
        # User Selection
        display_main_menu()
        menu_choice = int(input("Enter your choice (1-4): "))
        
        if menu_choice == 4:
            print("Exiting the client.")
            break
        
        if menu_choice == 3:
            s.sendto("support".encode(), serverAddr)
            initiate_support_session(s, serverAddr)
            continue

        # Decimal vs Binary Selection
        choice = "decimal" if menu_choice == 1 else "binary" if menu_choice == 2 else None
        if choice:
            s.sendto(choice.encode(), serverAddr)
            while True:
                operation = get_operation_choice(choice)
                if operation == "back":
                    break
                
                numbers = input("Enter numbers (binary numbers for binary operations, separated by space): ")
                s.sendto(f"{operation}:{numbers}".encode(), serverAddr)
                
                # Receive and print result
                result, _ = s.recvfrom(1024)
                print("Result:", result.decode())

except KeyboardInterrupt:
    print("\nExiting the client.")
finally:
    print("Closing the socket.")
    s.close()
