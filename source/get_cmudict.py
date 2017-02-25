# import cmudict dictionary info

def read_cmudict():
    f = open('cmudict/cmudict', 'r')
    ret_dict = {}

    while True:
        line = f.readline()
        if line == '':
            break   # EOF
        else:
            line = line.split(' ')
            ret_dict[line[0]] = line[1:]

    f.close()

    return ret_dict