#csv functions
def opencsv(fname, headerlines=0, footerlines=0):
    with open(fname, 'r') as fin:
        data = [l.strip().split(',') for l in fin if l.strip()]
    return data[headerlines: -footerlines if footerlines else None]

def writecsv(fname, data, header=()):
    with open(fname, 'w') as fout:
        if header:
            fout.write(','.join(map(str, elem)) + '\n')
        for line in data:
            fout.write('\n' + ','.join([(str(elem) if elem != None else '') for elem in line]))
