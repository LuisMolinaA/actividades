def gen():
    init ="q3"
    fin ="q2"
    num=["0","1","2","3","4","5","6","7","8","9"]
    alfab=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",]
    simbolos=["+","-","*","/"]
    for x in simbolos:
        print("('"+init+"', '"+x+"'): '"+fin+"',")

if __name__ == '__main__':
    gen()