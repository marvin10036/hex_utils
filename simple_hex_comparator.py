import argparse

parser = argparse.ArgumentParser(description="Compare two hex files")

parser.add_argument('-n','--nol', type=int, help="Number of bytes per line", default=16)
parser.add_argument('-e', '--exclusive', type=bool, help="""Print only altered bytes, if this is True, it will ignore
                                         your -nol argument and print 1 byte per line""", default=False)
parser.add_argument('-ff', '--first', type=str, help="First file, the oldest version of the file probably")
parser.add_argument('-sf', '--second', type=str, help="Second file, the altered first file, or the newest version")

args = parser.parse_args()

 
def line_range(nol: int, address: int):
    for i in range(address, -1, -1):
        if i%nol == 0:
            lower_limit = i
            break

    upper_limit = lower_limit + nol
    return(lower_limit, upper_limit)

def hex_comparator(ff: str, sf: str, nol: int, e: bool):
    file1 = open(ff, 'rb')
    old = file1.read()
    file2 = open(sf, 'rb')
    new = file2.read()

    mapper = {}
    largest_size = max(len(old), len(new))
    address_counter = 0
    flag = False
    
    case0 = False
    if len(old)>len(new):
        case0 = True 

    #Filling the mapper
    try:
        for i in range(largest_size):
            if old[i] != new[i]:
                mapper[i] = [hex(old[i]), hex(new[i])]
            address_counter+=1
    except:
        if case0:
            for j in range(address_counter, largest_size):
                mapper[j] = [hex(old[j]), " "*4]
                address_counter+=1
        else:
            for j in range(address_counter, largest_size):
                mapper[j] = [" "*4, hex(new[j])]
                address_counter+=1

    left_side = list(mapper.keys())
    
    #two ways of printing it
    #only the altered bytes
    if e:
        #printing the info
        print("Address", end=" "*3)
        print("FF" + " " + "SF")
        print("-"*8 + " "*2 + "--" + " "+ "--")

        for i in range(len(left_side)):
            print(hex(left_side[i])[2:].rjust(8,"0"), end="  ")
            print(((mapper[left_side[i]])[0])[2:].rjust(2,"0"), end=" ")
            print(((mapper[left_side[i]])[1])[2:].rjust(2,"0"))
    
    #the lines of the altered bytes, who are shown with parenthesis
    else:

        #printing the info again
        print("Address", end=" "*3)
        for i in range(1,3):
            for lsB in range(nol):
                print(hex(lsB)[2:].rjust(2, "0"), end=" "*i)
            print(" "*4, end="")
        print("\n",end="")
        print("-"*8 + " "*2 + "-"*((3*nol)-1) + " "*4 + "-"*(4*nol))

        upper_limit = 0
        for address in left_side:
            if address > (upper_limit-1):
                lower_limit, upper_limit = line_range(nol, address)
                print(hex(lower_limit)[2:].rjust(8, "0"), end="  ")

                if upper_limit > largest_size:
                    upper_limit = largest_size
                    flag = True

                #first the old file and then the second, it may seem kind of redundant, but it's easier on my mind
                for line_address in range(lower_limit, upper_limit):                    
                    if line_address in(left_side):
                        print((((mapper[line_address][0])[2:]).rjust(2,"0")).upper(), end=" ")
                    else:
                        #weirdly the same indexing logic works for dict and list in these cases
                        print((hex(old[line_address])[2:].rjust(2, "0")).upper(), end=" ")

                if flag:
                    deviance = (lower_limit + nol) - (upper_limit)
                    print("   "*deviance, end="")
                print(" "*3, end="")

                for line_address in range(lower_limit, upper_limit):
                    if line_address in(left_side):
                        string = ((mapper[line_address][1])[2:].rjust(2, "0")).upper() #giving weird errors if i dint do it
                        print(f"({string})", end="")
                    else:
                        print((" "+ hex(new[line_address])[2:].rjust(2, "0")).upper(), end=" ")
                
                print("\n", end="")


    print()
    print("Number of altered bytes: ", len(left_side))

    file1.close()
    file2.close()


if __name__=="__main__":
    hex_comparator(args.first, args.second, args.nol, args.exclusive)
