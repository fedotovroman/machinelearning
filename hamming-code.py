# Author: Fedotov Roman
# Coding date:  apr 2021

import numpy as np
#Коды Хэмминга - Лабораторная работа

# Функции, необходимые для преобразования текста в биты и обратно
def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), "big"))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding="utf-8", errors="surrogatepass"):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, "big").decode(encoding, errors) or "\0"


# Код Хэмминга
def emitterConverter(sizePar, data):
    if sizePar + len(data) <= 2 ** sizePar - (len(data) - 1):
        print("ERROR - size of parity don't match with size of data")
        exit(0)
    dataOut = []
    parity = []
    binPos = [bin(x)[2:] for x in range(1, sizePar + len(data) + 1)]
    dataOrd = []
    dataOutGab = []
    qtdBP = 0
    contData = 0
    for x in range(1, sizePar + len(data) + 1):
        if qtdBP < sizePar:
            if (np.log(x) / np.log(2)).is_integer():
                dataOutGab.append("P")
                qtdBP = qtdBP + 1
            else:
                dataOutGab.append("D")
        else:
            dataOutGab.append("D")
        if dataOutGab[-1] == "D":
            dataOrd.append(data[contData])
            contData += 1
        else:
            dataOrd.append(None)
    qtdBP = 0 
    for bp in range(1, sizePar + 1):
        contBO = 0
        contLoop = 0
        for x in dataOrd:
            if x is not None:
                try:
                    aux = (binPos[contLoop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1":
                    if x == "1":
                        contBO += 1
            contLoop += 1
        parity.append(contBO % 2)

        qtdBP += 1
    ContBP = 0  # parity bit counter
    for x in range(0, sizePar + len(data)):
        if dataOrd[x] is None:
            dataOut.append(str(parity[ContBP]))
            ContBP += 1
        else:
            dataOut.append(dataOrd[x])

    return dataOut


def receptorConverter(sizePar, data):
    dataOutGab = []
    qtdBP = 0
    contData = 0
    parityReceived = []
    dataOutput = []

    for x in range(1, len(data) + 1):
        if qtdBP < sizePar and (np.log(x) / np.log(2)).is_integer():
            dataOutGab.append("P")
            qtdBP = qtdBP + 1
        else:
            dataOutGab.append("D")
        if dataOutGab[-1] == "D":
            dataOutput.append(data[contData])
        else:
            parityReceived.append(data[contData])
        contData += 1
    dataOut = []
    parity = []
    binPos = [bin(x)[2:] for x in range(1, sizePar + len(dataOutput) + 1)]
    dataOrd = []
    dataOutGab = []
    qtdBP = 0
    contData = 0

    for x in range(1, sizePar + len(dataOutput) + 1):
        if qtdBP < sizePar and (np.log(x) / np.log(2)).is_integer():
            dataOutGab.append("P")
            qtdBP = qtdBP + 1
        else:
            dataOutGab.append("D")
        if dataOutGab[-1] == "D":
            dataOrd.append(dataOutput[contData])
            contData += 1
        else:
            dataOrd.append(None)

    qtdBP = 0  
    for bp in range(1, sizePar + 1):
        contBO = 0
        contLoop = 0
        for x in dataOrd:
            if x is not None:
                try:
                    aux = (binPos[contLoop])[-1 * (bp)]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    contBO += 1
            contLoop += 1
        parity.append(str(contBO % 2))

        qtdBP += 1
    ContBP = 0  
    for x in range(0, sizePar + len(dataOutput)):
        if dataOrd[x] is None:
            dataOut.append(str(parity[ContBP]))
            ContBP += 1
        else:
            dataOut.append(dataOrd[x])

    ack = parityReceived == parity
    return dataOutput, ack
