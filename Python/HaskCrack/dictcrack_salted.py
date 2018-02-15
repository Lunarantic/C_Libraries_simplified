import hashlib
from multiprocessing.dummy import Pool as ThreadPool

def crack_hash(in_str, salt):
    for pguess in open('rockyou.txt', 'r'):
        pguess = pguess.strip('\n')
        h = hashlib.sha256(pguess+salt).hexdigest()
        if h == in_str:
            return pguess
    
    return None

def crack_line(line):
    l = line.split(':')
    if len(l[4]) >= 64:
        p = crack_hash(l[4][:64], l[2])
        if p:
            print l[4][:64] + "\t" + p
        else:
            print l[4][:64] + "\t<<::>>CDC"
    else:
        print "Error >> " + str(l)


if __name__=='__main__':
    lines = [line for line in open('passwords_salt.txt', 'r')]
    pool = ThreadPool(20)

    results = pool.map(crack_line, lines)

    pool.close()
    pool.join()
