import string


def main():
    return 0


def ex1():
    a = int(input("Enter a number: "))
    b = int(input("Enter a number: "))
    if a*b > 1000:
        print(a+b)
    else:
        print(a*b)


def ex2():
    a = int(input("Enter a number: "))
    b = int(input("Enter a number: "))
    for i in range(a, b):
        print(i+i+1)


def ex3(number_list):
    # number_list = [1, 20, 3, 2, 1]
    if number_list[0] == number_list[-1]:
        return True
    else:
        return False


def ex4(number_list):
    # number_list = [10, 20, 3, 24, 125]
    for num in number_list:
        if num % 5 == 0:
            print(num)


def ex5():
    str1 = "Emma is a good developer. Emma is also a writer"
    x = 0
    for word in str1.split():
        if word == "Emma":
            x += 1
    print(x)
    return x


def ex6():
    list1 = [23, 20, 3, 24, 125]
    list2 = [1, 44, 3, 24, 125]
    list3 = []
    for i in list1:
        if i % 2 == 1:
            list3.append(i)
    for i in list2:
        if i % 2 == 0:
            list3.append(i)
    print(list3)


def ex7():
    str1 = "Hello programmer ! This is python"
    str2 = "What is this again ?"
    first_half = str1[:int(len(str1)/2)]
    second_half = str1[int(len(str1)/2):]
    str3 = first_half + str2 + second_half
    print(str3)


def ex8():
    str1 = "Hello programmer ! This is python"
    str2 = "What is this again ?"
    final = "" + str1[0] + str1[int(len(str1)/2)] + str1[-1] + str2[0] + str2[int(len(str1)/2)] + str2[-1]
    print(final)


def ex9():
    str1 = "Hello programmer ! This is python"
    lower, upper, special = 0, 0, 0
    for i in str1:
        if i.islower():
            lower += 1
        elif i.isupper():
            upper += 1
        else:
            special += 1
    print(f"There are {upper} Upper case letters,\n"
          f"{lower} lower case letters \n"
          f"and {special} special symbols (counting spaces)")


def ex10():
    str1 = "USA"
    str2 = "The Usa is the U S and A usa USA"
    count = 0
    for word in str2.split():
        if word.upper() == str1:
            count += 1
    print(f"The string USA appears {count} times")


def ex11():
    str1 = "uo4T7iTiP3E6JN6pzOmn"
    sum_numbers = 0
    for i in str1:
        if i.isnumeric():
            sum_numbers += int(i)
    print(f"The sum is {sum_numbers}")


def ex12():
    d = dict.fromkeys(string.ascii_lowercase, 0)
    str1 = "JKDeRGkFfBnWZoCBGvLq"
    for i in str1:
        if i.isalpha():
            d[i.lower()] += 1
    print(d)


if __name__ == "__main__":
    ex12()
