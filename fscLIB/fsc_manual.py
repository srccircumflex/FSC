from sys import stdout, exit

SLASH: str = '/'
path: str = ':NONE:'
folder: str = f'{SLASH}fscLIB'

def manual_print(string:str=None, file:str=None,
                     companion:str=None, split_arg:str='#' * 90, companions:tuple=('--help', '-h', '-I'),
                     exiting:bool=False):

    if file:
        with open(file, "r") as f:
            if companion:
                fl = f.read().split(split_arg)
                for i in range(len(fl)):
                    if companion == companions[i]: print(fl[i][1:], file=stdout)
            else:
                print(f.read(), file=stdout)
    if string:
        print(string, file=stdout)
    if exiting: exit()


def FSC_MANUAL(comp): manual_print(file=f'{path}{folder}{SLASH}fsc_manpage', companion=comp, exiting=True)
def DISCLAIMER(): manual_print(file=f'{path}{folder}{SLASH}fsc_manpage', companion='-I', exiting=False)
