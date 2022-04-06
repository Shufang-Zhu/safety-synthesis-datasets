#!/usr/bin/python

import sys, getopt
from pathlib import Path


def tlsf_gen_unreal_1(k):
    filename = 'unreal_1/unreal_scalable_1_'+str('{0:03}'.format(k+1))+'.tlsf'
    out = open(filename, 'w')
    # 'print INFO'
    print('INFO {', file=out)
    print('TITLE:       \"Scalable Unrealizable Benchmark n.'+str(k)+ '\"', file=out)
    print('DESCRIPTION: \"Scalable Unrealizable Benchmark n. for Ksy tool.\"', file=out)
    print('SEMANTICS:   Mealy', file=out)
    print('TARGET:      Mealy', file=out)
    print('}', file=out)
    # end 'print INFO'
    print('MAIN {', file=out)
    # 'print IN-OUT'
    print('\nINPUTS { ', file=out)
    for i in range(0,k+1):
        print('u',str(i), end = '', sep="", file=out);
        if(i<k):
            print(';', file=out)
        else:
            print(';\n}', file=out)
    print('\nOUTPUTS{\nc;\n}', file=out)
    # end 'print IN-OUT'
    # 'print GUARANTEE'
    print('\nGUARANTEE { \n', file=out)
    if(k<0):
        print('*** The index must be >= 0.');
        sys.exit()
    print('G( c ) && (', file=out)
    for i in range(0,k+1):
        print('G( ', end='', file=out)
        for j in range(0,i+1):
            if(j>0):
                print(' && ', end='', file=out)
            print('u'+str(j), end = '', file=out)
        if(i<k):
          print(' ) || ', file=out)
        else:
          print(') ', file=out)
    print(')', file=out)
    print('}\n}\n', file=out)
    # end 'print GUARANTEE'

def tlsf_gen_unreal_1_env(k):
    filename = 'unreal_1_env/unreal_scalable_1_'+str('{0:03}'.format(k+1))+'.tlsf'
    out = open(filename, 'w')
    # 'print INFO'
    print('INFO {', file=out)
    print('TITLE:       \"Scalable Unrealizable Benchmark n.'+str(k)+ '\"', file=out)
    print('DESCRIPTION: \"Scalable Unrealizable Benchmark n. for Ksy tool.\"', file=out)
    print('SEMANTICS:   Mealy', file=out)
    print('TARGET:      Mealy', file=out)
    print('}', file=out)
    # end 'print INFO'
    print('MAIN {', file=out)
    # 'print IN-OUT'
    print('\nINPUTS { ', file=out)
    for i in range(0,k+1):
        print('u',str(i), end = '', sep="", file=out);
        if(i<k):
            print(';', file=out)
        else:
            print(';\n}', file=out)
    print('\nOUTPUTS{\nc;\n}', file=out)
    # end 'print IN-OUT'
    # 'print GUARANTEE'
    print('\nGUARANTEE { \n', file=out)
    if(k<0):
        print('*** The index must be >= 0.');
        sys.exit()
    print('G( c ) && (', file=out)
    for i in range(0,k+1):
        print('G( ', end='', file=out)
        for j in range(0,i+1):
            if(j>0):
                print(' && ', end='', file=out)
            print('X(u'+str(j)+')', end = '', file=out)
        if(i<k):
          print(' ) || ', file=out)
        else:
          print(') ', file=out)
    print(')', file=out)
    print('}\n}\n', file=out)
    # end 'print GUARANTEE'

def smv_gen_unreal_1(k):
    filename = 'unreal_1_smv/unreal_scalable_1_'+str('{0:03}'.format(k+1))+'.smv'
    out = open(filename, 'w')
    if(k<0):
        print('*** The index must be >= 0.');
        sys.exit()
    print('G( c ) & (', file=out)
    for i in range(0,k+1):
        print('G( ', end='', file=out)
        for j in range(0,i+1):
            if(j>0):
                print(' & ', end='', file=out)
            print('u'+str(j), end = '', file=out)
        if(i<k):
          print(' ) | ', file=out)
        else:
          print(') ', file=out)
    print(')', file=out)

    print('\nINPUT : ', end = '', file=out)
    for i in range(0,k+1):
        print('u',str(i), end = '', sep="", file=out);
        if(i<k):
            print(', ', end = '', file=out)
    print('\nOUTPUT : c', file=out)
    print('\n-- UNREALIZABLE', file=out)




def main(argv):
    sindex = ''
    eindex = ''
    _format = ''
    try:
        opts, args = getopt.getopt(argv,"hf:s:e:",["ifile="])
    except getopt.GetoptError:
        print('test.py -f <format> -s <index_start> -e <index_end>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -f <format> -s <index_start> -e <index_end>')
            sys.exit()
        elif opt in ("-s", "--start"):
            sindex = arg
        elif opt in ("-e", "--end"):
            eindex = arg
        elif opt in ("-f", "--format"):
            _format = arg
    if(not sindex or not eindex):
        print('*** Please specify the indexes with -s <index_start> -e <index_end>')
        sys.exit()
    if((not _format) or (_format != "smv" and _format != "tlsf")):
        print('*** Please specify the format with -f <format>')
        sys.exit()

    save_tlsf = Path("unreal_1")
    save_tlsf.mkdir(parents=True, exist_ok=True)

    save_tlsf_env = Path("unreal_1_env")
    save_tlsf_env.mkdir(parents=True, exist_ok=True)

    # save_smv = Path("unreal_2_smv")
    # save_smv.mkdir(parents=True, exist_ok=True)
   
    for i in range(int(sindex),int(eindex)):
        if _format == "smv":
            print('Generating file unreal_scalable_1_', str('{0:03}'.format(i+1)), '.smv',sep='')
            smv_gen_unreal_1(i);
        elif _format == "tlsf":
            print('Generating file unreal_scalable_1_', str('{0:03}'.format(i+1)), '.tlsf',sep='')
            tlsf_gen_unreal_1(i);
            tlsf_gen_unreal_1_env(i);
        else:
            sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
