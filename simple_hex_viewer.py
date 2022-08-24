import argparse

#1
parser = argparse.ArgumentParser()
#2
parser.add_argument("-f","--filename", type=str, help="The name of the file, if necessary the path should be included")
parser.add_argument("-s", "--size", type=int, help="Size per lines in terms of bytes")
#3
args = parser.parse_args()


def decode(filename, size):
    file_open = open(filename, 'rb')
    file = file_open.read()

    if len(file) % size != 0:
        number_of_bytes = len(file) // size + 1
    else:
        number_of_bytes = len(file) //size

    address_counter = 0

    #Essentially the first line of the table
    print("Address", end=" "*3)

    for lsB in range(size):
        hex_lsB = (hex(lsB)[2:]).rjust(2,"0")
        print(hex_lsB, end=" ")
    print(" "*3 +"ASCII")
    print("-"*8 + " "*2 + "-"*(size + (size*2)-1)+ " "*4 + "-"*5)

    #The table itself
    for i in range(number_of_bytes):
        flag = False
        upper_limit = address_counter + size
        if address_counter + size > len(file):
           upper_limit = len(file)
           flag = True
           space = size - (upper_limit - address_counter)

        current_address = (hex(address_counter)[2:]).rjust(8,"0")
        print("{}".format(current_address), end="  ")

        for i in range(address_counter, upper_limit):
            value = ((hex(file[i])[2:]).rjust(2,"0")).upper()
            print(value, end=" ")

        print("   ", end="")
        if flag:
            print("   "*space, end="")

        for i in range(address_counter, upper_limit):
            if file[i] > 32 and file[i] < 127:
                ascii_str = chr(file[i])
                print(ascii_str, end=" ")
            else:
                print(".", end=" ")

        print("\n", end="")
        address_counter +=size

        if flag:
            break

    file_open.close()


if __name__ == '__main__':
    decode(args.filename, args.size)
