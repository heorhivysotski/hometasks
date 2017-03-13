string = input()


def IsPalindrome(string):
    if (string == string[::-1]):
        print(string, " - Is palindrome")
    else:
        print(string, " - Not palindrome")

IsPalindrome(string)
