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
    str1 = ""
    str2 = ""


if __name__ == "__main__":
    ex6()
