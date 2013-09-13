import os

if __name__=='__main__':
    for i in range(100):
        for puzztype in ['i', 'm', 'e']:
            cmd = "gen_puzzle 24 %s" % (i)
            cmd += "| sed -e 's/ //g'"
            cmd += ("| sed -e 's/^/%s /'" % (puzztype))
            os.system(cmd)
