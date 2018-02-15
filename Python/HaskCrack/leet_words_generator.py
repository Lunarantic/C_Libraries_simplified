leet_dict = {'A': ['a', '4', '/-\\', '/_\\', '@', '/\\'],
'B': ['b', '8,|3', '13', '|}', '|:', '|8', '18', '6', '|B', '|8', 'lo', '|o', '|3'],
'C': ['c', '<', '{', '[', '('],
'D': ['d', '|)', '|}', '|]'],
'E': ['e', '3 '],
'F': ['f', '|=', 'ph', '|#', '|"'],
'G': ['g', '[', '-', '[+', '6'],
'H': ['h', '4', '|-|', '[-]', '{-}', '|=|', '[=]', '{=}'],
'I': ['i,1', '|', '!', '9'],
'J': ['j', '_|', '_/', '_7', '_)'],
'K': ['k', '|<', '1<', 'l<', '|{', 'l{'],
'L': ['l', '|_', '|', '1', ']['],
'M': ['m', '44', '|\\/|', '^^', '/\\/\\', '/X\\', '[]\\/][', '[]V[]', '][\\\\//][', '(V),//.', '.\\\\', 'N\\'],
'N': ['n', '|\\|', '/\\/', '/V', '][\\\\]['],
'O': ['o', '0', '()', '[]', '{}', '<> '],
'P': ['p', '|o', '|O', '|>', '|*', '|D', '/o'],
'Q': ['q', 'O_', '9', '(,)', '0'],
'R': ['r', '|2', '12', '.-', '|^', 'l2'],
'S': ['s', '5', '$'],
'T': ['t', '7', '+', '7`', "'|'"],
'U': ['u', '|_|', '\\_\\', '/_/', '\\_/', '(_)', '[_]', '{_}'],
'V': ['v', '\\/'],
'W': ['w', '\\/\\/', '(/\\)', '\\^/', '|/\\|', '\\X/', "\\\\'", "'//", 'VV'],
'X': ['x', '%', '*', '><', '}{', ')( '],
'Y': ['y', '`/'],
'Z': ['z', '2', '7_', '>_']}

def permute(dict_word):
    if len(dict_word) > 0:
        current_letter = dict_word[0]
        rest_of_word = dict_word[1:]

        if current_letter in leet_dict:
            substitutions = leet_dict[current_letter] + [current_letter]
        else:
            substitutions = [current_letter]

        if len(rest_of_word) > 0:
            perms = [s + p for s in substitutions for p in permute(rest_of_word)]
        else:
            perms = substitutions
        return perms


if __name__=="__main__":
    import sys

    if len(sys.argv) < 3:
        print "Usage : python leet_word_generator.py <input_file> <output_file>"
    
    try:
        lines = [line.strip('\n') for line in open(sys.argv[1],'r')]
    except:
        print "Check Input file"
        lines = None

    if lines:
        try:
            fw = open(sys.argv[2], 'w')
        except:
            print "Check Output file"
            fw = None

    if lines and fw:
        l = len(lines)
        i = 0
        for line in lines:
            perms = permute(line)
            if perms:
                for p in perms:
                    fw.write(p + '\n')
                    fw.flush()
            i += 1
            print('Done : ' + str(i) + '/' + str(l))
        fw.close()
