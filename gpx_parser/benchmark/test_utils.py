from time import  strftime


def make_result_string(num:int, *args)->str:
    space = '   '
    result = [space, space]
    names = args[0]
    for i in range(num):
        result.extend([names[i],space,space])
    result.append('\n')

    length = len(args[1])
    for i in range(length):
        result.extend([space, space,space])
        for j in range(1,num+1):
            result.extend([str(round(args[j][i],2)), space, space, space])
        result.append('\n')
    return ''.join(result)


def get_time()->str:
    return strftime('%m.%d_%H:%M')