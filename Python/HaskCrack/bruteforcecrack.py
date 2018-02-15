import hashlib
import itertools
import string
from multiprocessing.dummy import Pool as ThreadPool

def crack_hash(in_str):
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
    
    for pglen in xrange(3,7):
        for pguess in itertools.product(chars, repeat=pglen):
            pguess = ''.join(pguess)
            h = hashlib.sha256(pguess).hexdigest()
            if h == in_str:
                return pguess
    
    return None

lines = [line for line in open('passwords_nosalt.txt', 'r')]

def crack_line(line):
    l = line.split(':')
    if len(l[4]) >= 64:
        p = crack_hash(l[4][:64])
        if p:
            print l[4][:64] + "\t" + p
    else:
        print "Error >> " + str(l)

pool = ThreadPool(2)

results = pool.map(crack_line, lines)

pool.close()
pool.join()

