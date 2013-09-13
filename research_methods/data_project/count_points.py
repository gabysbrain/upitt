import sys
import gzip

if __name__ == '__main__':
    counts = {}

    for file in sys.argv[1:]:
        f = gzip.open(file)
        for line in f:
            val = int(line)
            counts[val] = counts.get(val, 0) + 1
        f.close()
    for val, ct in counts.iteritems():
        print val, ct

