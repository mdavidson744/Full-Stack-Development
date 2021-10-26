fin = open("words.txt", "r")

letter = input("please enter a letter: ")

fout = open("letters.txt", "w")
for line in fin:
    word = line.strip()
    if letter == word:
        output = word + "\n"
        fout.write(output)
        print(word)

fin.close()
fout.close()