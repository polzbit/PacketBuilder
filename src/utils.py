from PyQt5.QtCore import QTimer, QEventLoop

def is_public(ip):
    octs = ip.strip().split(".")
    if int(octs[0]) == 10:
        return False
    elif int(octs[0]) == 172:
        if int(octs[1]) >= 16 and int(octs[1]) <= 31:
            return False
    elif int(octs[0]) == 192:
        if int(octs[1]) == 168:
            return False
    return True

def _sleep(msec):
    loop = QEventLoop()
    QTimer.singleShot(msec, loop.quit)
    loop.exec_()


def checksum(header_hex):
    results = 0
    for hexbyte in header_hex:
        results += hexbyte
        if results > 0xFFFF:
            # case add carry
            results = (results & 0xffff) + (results >> 16)
    # final step
    results = results + (results >> 16)
    return ~results & 0xffff

def typeCheck(num_str):
    numType = 'DEC'
    if num_str.__class__.__name__ == 'str' and num_str != '10':
        # hex check
        if '0x' in num_str:
            numType = 'HEX'
        else:
            # binary check
            isBin = True
            for char in num_str:
                if char not in '10':
                    isBin = False
                    break
            if isBin:
                numType = 'BIN'
    return numType

def numConvert(numString, to="DEC", toString=False):
    if numString == '':
        return None
    numType = typeCheck(numString)
    newNum = numString
    if numType == "DEC" and to == "HEX":
        newNum = hex(int(numString))
    elif numType == "DEC" and to == "BIN":
        newNum = format(int(numString), 'b')
    elif numType == "HEX" and to == "DEC":
        newNum = int(numString, 16)
    elif numType == "HEX" and to == "BIN":
        newNum = format(int(numString, 16), 'b')
    elif numType == "BIN" and to == "DEC":
        newNum = int(numString, 2)
    elif numType == "BIN" and to == "HEX":
        newNum = hex(int(numString, 2))
    if toString:
        newNum = str(newNum)
    elif to == 'DEC':
        newNum = int(newNum)
    return newNum
    

def ipConvert(ip, to="DEC"):
    if ip != '':
        data = ip.split('.')
        octs = []
        for d in data:
            octs.append(numConvert(d, to, toString=True))
        if len(octs):
            ip = ".".join(octs)
    return ip

#h = [0x4500, 0x003c, 0x1c46, 0x4000, 0x4006, 0x0000, 0xac10, 0x0a63, 0xac10, 0x0a0c]
#ip_checksum(h)
