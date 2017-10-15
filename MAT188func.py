from sympy import *
from wxpy import *

def msgdiff(msg):
    msg = msg.replace('／', '/');
    msg = msg.replace('？', '?');
    msg = msg.replace('。', '.');
    msg = msg.replace('，', ',');
    msg = msg.replace('；', ';');
    x = Symbol("x")
    s = msg
    return(str(diff(s, x)))

def msgrref(msg):
    msg = msg.replace('／', '/');
    msg = msg.replace('？', '?');
    msg = msg.replace('。', '.');
    msg = msg.replace('，', ',');
    msg = msg.replace('；',';');
    msg = msg.replace(' ', '');

    middle = []
    tmp = []
    flag = 0

    while msg.find(';') != -1 or flag == 1:
        tmp = []
        tempstr = msg[0:msg.find(';')]
        if msg.find(';') == -1:
            tempstr = msg[0:len(msg)]
        while tempstr.find(',') != -1:
            tmp.append(int(tempstr[0:tempstr.find(',')]))
            tempstr = tempstr[tempstr.find(',') + 1:len(tempstr)]
        tmp.append(int(tempstr[0:len(tempstr)]))
        middle.append(tmp)
        msg = msg[msg.find(';') + 1:len(msg)]
        if flag == 1:
            flag += 1
        if msg.find(';') == -1 and flag == 0:
            flag += 1

    M = Matrix(middle)
    rref = M.rref()
    result = ""
    for i in range(0, M.rows):
        for j in range(0, M.cols):
            if j != M.cols - 1:
                result += str(list(rref[0])[i * M.cols + j]) + ','
            else:
                result += str(list(rref[0])[i * M.cols + j])
        result += '\n'
    result += 'with leading term on col: '
    for i in range(0, len(list(rref[1]))):
        if i != len(list(rref[1])) - 1:
            result += str(rref[1][i]+1) + ','
        else:
            result += str(rref[1][i]+1) + '.'
    return result

embed()