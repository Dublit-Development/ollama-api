import subprocess

models = {
    '1': 'neural-chat',
    '2': 'starling-lm',
    '3': 'mistral',
    '4': 'llama2',
    '5': 'codellama',
    '6': 'llama2-uncensored',
    '7': 'llama2:13b',
    '8': 'llama2:70b',
    '9': 'orca-mini',
    '10': 'vicuna'
}

def install_model(model_name):
    subprocess.run(["ollama", "pull", model_name])

def install_ollama():
    # Define the command
    curl_command = "curl https://ollama.ai/install.sh | sh"

    subprocess.run(curl_command, shell=True)

def model_selection():
    while True:
        print("Choose a model to install:")
        for key, value in models.items():
            print(f"{key}. Install {value}")

        user_choice = input("Enter the number of the model to install (or 'exit' to exit): ")

        if user_choice.lower() == 'exit':
            print("Exiting the script.")
            break

        model_name = models.get(user_choice)
        if model_name:
            install_model(model_name)
            install_another = input("Do you want to install another model? (yes/no): ").lower()
            if install_another != 'yes':
                print("Exiting the script.")
                break
        else:
            print("Invalid choice. Please enter a valid option.")

def print_menu():
    print("1. Install Ollama")
    print("2. Install a Model")
    print("3. Exit")

def execute_task(task_number):
    if task_number == 1:
        install_ollama()
    elif task_number == 2:
        model_selection()
    else:
        print("Invalid value. Please enter a valid option.")
 
while True:
    print_menu()
    user_choice = input("Welcome to the Ollama-API! Enter the number of the task you want to execute (or 3 to exit): ")

    if user_choice.isdigit():
        task_number = int(user_choice)
        if task_number == 3:
            break
        else:
            execute_task(task_number)
    else:
        print("Invalid input. Please enter a number.")
