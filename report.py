#!/usr/bin/python3
f=open("salary30k","rb")
print("Header of the file:")
print("<Header String>: ", f.read(16).decode("utf-8"))
pagesize=int.from_bytes(f.read(2), "big")
print("<Page Size>: ", pagesize)
print("<Write version>: ", int.from_bytes(f.read(1), "big"))
print("<Read version>: ", int.from_bytes(f.read(1), "big"))
print("<Bytes of unused>: ", int.from_bytes(f.read(1), "big"))
print("<Max embedded payload fraction>: ", int.from_bytes(f.read(1), "big"))
print("<Min embedded payload fraction>: ", int.from_bytes(f.read(1), "big"))
print("<Leaf payload fraction>: ", int.from_bytes(f.read(1), "big"))
print("<File change counter>: ", int.from_bytes(f.read(4), "big"))
noofpages=int.from_bytes(f.read(4), "big")
print("<Size of db file in pages>: ", noofpages)
print("<Page no. of first freelist trunk page>: ", int.from_bytes(f.read(4), "big"))
print("<Total number of freelist pages>: ", int.from_bytes(f.read(4), "big"))
print("<Schema cookie>: ", int.from_bytes(f.read(4), "big"))
print("<Schema format number>: ", int.from_bytes(f.read(4), "big"))
print("<Default page cache size>: ", int.from_bytes(f.read(4), "big"))
print("<Page no. of largest root btree>: ", int.from_bytes(f.read(4), "big"))
print("<Database text encoding>: ", int.from_bytes(f.read(4), "big"))
print("<User version>: ", int.from_bytes(f.read(4), "big"))
print("<Incremental vacuum mode (True or False)>: ", int.from_bytes(f.read(4), "big"))
print("<Application Id>: ", int.from_bytes(f.read(4), "big"))
print("<Reserved for expansion (must be 0)>: ", int.from_bytes(f.read(20), "big"))
print("<Version valid for>: ", int.from_bytes(f.read(4), "big"))
print("<Sqlite version number>: ", int.from_bytes(f.read(4), "big"))
filesize=pagesize*noofpages
if filesize<=1073741824:
    print("File has no lock byte page")
else:
    print("File has 1 lock byte page")
print("Read bytes: ", f.tell())

from varint import *
def getvarint():
    b=[]
    while True:
        val=int.from_bytes(f.read(1),"big")
        if val>127:
            b.append(val)
        else:
            b.append(val)
            break
    return(decode(b))

def printpg(startfrom,pgn):
    print("\n\n\nStart from: ", startfrom)
    print("pgn :", pgn)
    f.seek(startfrom)
    print("Currently seeking from : ", f.tell())
    print("Page header : ",pgn)
    pgty=int.from_bytes(f.read(1), "big")
    pg=None
    print("pgty = ",pgty)
    if pgty == 2:
        pg="interior index b-tree page"
    elif pgty == 5:
        pg="interior table b-tree page"
    elif pgty == 10:
        pg="leaf index b-tree page"
    elif pgty == 13:
        pg="leaf table b-tree page"
    print("b-tree page type: ",pg)
    print("Start of the first free block on the page: ",int.from_bytes(f.read(2), "big"))
    nocells=int.from_bytes(f.read(2), "big")
    print("Number of cells on the page: ",nocells)
    print("Start of the cell content area: ",int.from_bytes(f.read(2), "big"))
    print("Number of fragmented free bytes within cell content area: ",int.from_bytes(f.read(1), "big"))
    if pgty == 2 or pgty == 5:
        print("Right most pointer: ",int.from_bytes(f.read(4), "big"))
    print("The cell pointer arrays are as follows")
    i=nocells
    keys=[]
    ind=0
    while i>=1:
        keys.append(int.from_bytes(f.read(2), "big"))
        print("Key :",keys[ind])
        i-=1
        ind+=1
    for key in keys:
        seekval=(pgn-1)*pagesize + key 
        print("seekval=",seekval)
        f.seek(seekval)
        if pgty==13:
            loadsize=getvarint()
            print("Number of bytes of payload at key ", key, ": ", loadsize)
            print("Rowid at key ", key, ": ",getvarint() )
            header=getvarint()
            print("Header size:", header)
            coltypes=[]
            for hd in range(1, header):
                coltypes.append(getvarint())
            coltdict={0:"NULL",
                      1:"8 bit 2s complement integer",
                      2:"Value is a big-endian 16-bit twos-complement integer",
                      3:"Value is a big-endian 24-bit twos-complement integer",
                      4:"Value is a big-endian 32-bit twos-complement integer",
                      5:"Value is a big-endian 48-bit twos-complement integer",
                      6:"Value is a big-endian 64-bit twos-complement integer",
                      7:"Value is a big-endian IEEE 754-2008 64-bit floating point number",
                      8:"Value is the integer 0",
                      9:"Value is the integer 1",
                      10:"Not used. Reserved for expansion",
                      11:"Not used. Reserved for expansion"}
            o=0
            for col in coltypes:
                o+=1
                if col >=13 and col%2==1:
                    print("Col:",o, " : Text string of size ", (col-13)/2)
                else:
                    print("Col:",o, " : ", coltdict[col])

            o=0
            for col in coltypes:
                o+=1
                if col >=13 and col%2==1:
                    print("Col val:",o, " : ",f.read( (col-13)//2))
                elif col>=1 and col<=4:
                    print("Col val:",o, " : ",int.from_bytes(f.read(col),"big"))







printpg(100,1)

print("Current offset: ", f.tell())
for i in range(2,noofpages+1):
    printpg((i-1)*pagesize,i)
    print("Current offset: ", f.tell())
f.close()
print("================================")
