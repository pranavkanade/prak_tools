if __name__ == "__main__":
    inptl = []
    outptl = []
    with open('test', 'r') as inpfp:
        inptl = inpfp.readlines()

    for line in inptl:
        toks = line.split()
        if "NL" not in toks:
            outptl.append(line)

    with open('test', 'w') as outfp:
        outfp.writelines(outptl)
# the output was created using `python -m tokenize pyClass.py > test`
