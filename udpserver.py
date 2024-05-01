import socket

# Decimal Operation Function, simple math operations on decimal numbers

def perform_decimal_operation(operation, numbers):
    if operation == "divide" and 0 in numbers[1:]:
        return "Error: Division by zero"
    if operation == "add":
        return sum(numbers)
    elif operation == "subtract":
        return numbers[0] - sum(numbers[1:])
    elif operation == "multiply":
        result = 1
        for num in numbers:
            result *= num
        return result
    elif operation == "divide":
        result = numbers[0]
        for num in numbers[1:]:
            if num == 0:
                return "Error: Division by zero"
            result /= num
        return result
    elif operation == "exponent":
        return numbers[0] ** numbers[1]
    elif operation == "modulo":
        return numbers[0] % numbers[1]

# Binary Operation Function, binary addition and subtraction

def perform_binary_operation(operation, numbers):
    max_length = max(len(num) for num in numbers)  # Find max length of the binary numbers
    integers = [int(num, 2) for num in numbers]  # Convert binary strings to integers
    
    # Option Choice -> Operation

    if operation == "add":
        result = sum(integers)
    elif operation == "unsigned_subtract":
        result = max(integers[0] - integers[1], 0)  # Prevent negative result in unsigned operation
    elif operation == "signed_subtract":
        # Convert to two's complement, perform subtraction, and convert back
        a, b = integers
        two_comp_b = (~b + 1) & ((1 << max_length) - 1)  # Compute two's complement of b 
        result = (a + two_comp_b) & ((1 << max_length) - 1)

    return bin(result)[2:].zfill(max_length)  # Return the result as a binary string, padded to maintain length

def handle_support_session(addr):
    # Send initial support session start message
    welcome_message = "Support session started. Type 'exit' to end support."
    server_socket.sendto(welcome_message.encode(), addr)
    
    while True:
        # Server waits for client message
        data, addr = server_socket.recvfrom(1024)
        client_message = data.decode()
        if client_message.lower() == "exit":
            goodbye_message = "Support session ended."
            server_socket.sendto(goodbye_message.encode(), addr)
            break
        
        # Display the client's message on the server's console for the server operator
        print(f"Client: {client_message}")
        server_response = input("Reply to client: ")  # Server types a response here
        server_socket.sendto(server_response.encode(), addr)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "10.228.91.53"
port = 15000
server_socket.bind((ip, port))

# Python Socket Initialization

try:
    while True:
        data, addr = server_socket.recvfrom(1024)
        choice = data.decode()
        
        # Choice Handling

        if choice == "support":
            handle_support_session(addr)
        else:
            data, addr = server_socket.recvfrom(1024)
            operation, numbers = data.decode().split(':')
            numbers = numbers.strip().split()

            if choice == "decimal":
                result = perform_decimal_operation(operation, list(map(int, numbers)))
            elif choice == "binary":
                result = perform_binary_operation(operation, numbers)
            
            server_socket.sendto(str(result).encode(), addr)

except KeyboardInterrupt:
    print("\nServer is shutting down.")
finally:
    server_socket.close()
