def encode(val):
    if val<=127:
        return [val]
    b=[]
    b.append(val&127)
    val=val>>7
    bs=128
    while val>127:
        b.append(bs|(val&127))
        val=val>>7
    b.append(bs|(val&127))
    b.reverse()
    return b

def decode(bar):
    i=0
    index=0
    fin=0
    for val in bar:
        if val>127:
            i=i<<(index*7)
            index=1
            i=i|(val&127)
        else:
            fin=val
            break
    i=i<<(index*7)
    i=i|(fin&127)
    return i

def check(ran):
    outt=ran//5
    for val in range(ran):
        enc=encode(val)
        if ran%outt==0:
            enc.append(999999)
        dec=decode(enc)
        if val!=dec:
            print("Mismatch val",val," Out",dec)
            return
        if val%outt==0:
            print(val,"==>",dec)
    print("Super")
