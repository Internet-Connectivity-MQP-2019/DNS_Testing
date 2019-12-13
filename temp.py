import dig

if __name__ == "__main__":
    s = "\n"
    with open('out.txt') as f:
        for line in f:
            s += line + ""
    print(str(dig.DigResults.parse(s)))
