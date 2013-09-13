import sys

outfile = sys.stdout

fieldids = None
fieldmap = {}

def findclasses(filename):
    fieldmap = {}
    fieldid = 0

    f = file(filename)
    f.readline() # first line is throwaway
    for line in f:
        c = line.strip().split("\t")[-1]
        if c not in fieldmap:
            fieldmap[c] = fieldid
            fieldid += 1
    f.close()
    return [str(x) for x in fieldmap.values()]

def convertdata(data, numattrs):
    def convertfield(field, fieldid, fieldmap):
        field = field.strip()
        if field == '': return '?'

        try:
            float(field)
            return field
        except ValueError:
            if field not in fieldmap:
                id = fieldid[0]
                fieldmap[field] = id
                fieldid[0] += 1
            return str(fieldmap[field])
    fieldids = [[0] for i in range(numattrs)]
    fieldmaps = [{} for i in range(numattrs)]

    for line in data:
        convline = line.strip().split("\t")
        convline = [convline[0]] + \
                   [''] * (numattrs-len(convline)) + \
                   convline[1:]
        tmp = [convertfield(f[0],f[1],f[2]) \
                 for f in zip(convline, fieldids, fieldmaps)]
        yield tmp

def printattributes(file, attrs, classes):
    for i in range(len(attrs)):
        attr = attrs[i]
        fixed_attr = attr.replace(" ", "_")
        fixed_attr = fixed_attr.replace("'", "")
        if i<len(attrs)-1:
            file.write("@ATTRIBUTE %s NUMERIC\n" % (fixed_attr))
        else:
            cstr = '{%s}' % (",".join(classes))
            file.write("@ATTRIBUTE %s %s\n" % (fixed_attr, cstr))

def printdata(file, datalist):
    file.write("%s\n" % (",".join(datalist)))

def printrelation(file, relname):
    file.write("@RELATION %s\n" % (relname))

if __name__ == '__main__':
    filename = sys.argv[1]
    f = file(filename)

    printrelation(outfile, "election")

    # first line is the header
    classes = findclasses(filename)
    attrs = f.readline().strip().split("\t")
    printattributes(outfile, attrs, classes)
    
    outfile.write("\n")
    outfile.write("@DATA\n")

    for datum in convertdata(f, len(attrs)):
        printdata(outfile, datum)
    
    f.close()

