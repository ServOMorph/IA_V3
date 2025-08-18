import threading

def print_numbers(num):
    for i in range(num):
        print(i)

def main():
    thread1 = threading.Thread(target=print_numbers, args=(5,))
    thread2 = threading.Thread(target=print_numbers, args=(5,))
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    main()
