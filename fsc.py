#! /bin/python3.9

from os import path
import sys
from sys import stdout, stderr, argv, exit
from getopt import getopt, GetoptError
from re import search
from time import time
from datetime import datetime

script_path: str = path.dirname(__file__)

if sys.platform in ('win32', 'cygwin'): SLASH: str = '\\'
else: SLASH: str = '/'

sys.path.append(script_path)

from fscLIB import fscFunction, fscIO, fscMJ, fsc_manual, fscModule

dsc: bool = True
coding: str = 'ISO-8859-1'
#            10485760
block: int = 10485760
#bench_out = stderr
bench_out = stdout


fsc_manual.path = script_path
fsc_manual.SLASH = SLASH
fscIO.coding_a = coding
fscFunction.coding_a = coding
fscIO.block = block
fscFunction.bench_out = bench_out
fscModule.bench_out = bench_out

short_opts = "edf:k:K:sE:Hi:o:qvbphtI"
long_opts = ['encrypt', 'decrypt', 'file=', 'read-file=', 'stdin', 'EOF=', 'hide-input',
             'inject=', 'output-file=',
             'quiet', 'verbose', 'benchmark', 'process', 'help',
             'ilv=', 'part=', 'prio=', 'sha256', 'sha512', 'sha224', 'hops=', 'key-file=', 'mk-key-file=',
             'mj',
             'sha0', 'sha-1']

def read_opt():
    global short_opts, long_opts
    global en_, de_, p_cache, iby, inj, ouf
    global ilv, ppl, sha, hps, kyf, mk_kyf
    global v, dsc, file_warn, jmr
    try:
        opts, args = getopt(argv[1:], short_opts, long_opts)
    except GetoptError as e:
        exit(f"\n [[ERR] {e}]\n -h     :list commands\n--help  :print help-page\n")

    for opt, arg in opts:
        if opt in ('-e', '--encrypt'): en_ = True
        elif opt in ('-d', '--decrypt'): p_cache = (False if de_ else True); de_ = True
        elif opt in ('-f', '--file'): iby = arg
        elif opt in ('-s', '--stdin'): iby = -1
        elif opt in ('-E', '--EOF'):iby, fscIO.EOF = -1, arg
        elif opt in ('-H', '--hide-input'): iby = -2
        elif opt in ('-i', '--inject'): inj = arg
        elif opt in ('-o', '--output-file'):
            ouf = arg
            if path.isdir(ouf): exit(f" [E] IsADirectoryError : '{ouf}'")
            elif path.isfile(ouf): file_warn = True
        elif opt in ('-q', '--quiet'): v = v.replace('p', '')
        elif opt in ('-v', '--verbose'): v += 'v'
        elif opt in ('-b', '--benchmark'): v += 'b'
        elif opt in ('-p', '--process'): v += 'P'
        elif opt == '-I': dsc = False
        elif opt in ('-h', '--help'): fsc_manual.FSC_MANUAL(opt)
        elif opt == "--ilv": ilv = (int(arg) if search("^[0-9]*$", arg)
                                    else exit(f" [E] ValueError --ilv : '{arg}'"))
        elif opt == '--part': ppl[0] = (int(arg) if arg in ('0', '1')
                                        else exit(f" [E] PartError : '{arg}' / 0|1"))
        elif opt == '--prio': ppl[1] = (int(arg) if search("^[1-9][0-9?]*$", arg)
                                        else exit(f" [E] PrioError : '{arg}' / n > 0"))
        elif opt in ('--sha256', '--sha512', '--sha224'): sha = opt[-3:]
        elif opt in ('--sha-1', '--sha0'): sha = opt
        elif opt == '--hops': hps = (int(arg) if search("^[1-9][0-9?]*$", arg)
                                     else exit(f" [E] HopError : '{arg}' / n > 0"))
        elif opt in ('-k', '--key-file'):kyf, mk_kyf = arg, False
        elif opt in ('-K', '--mk-key-file'):kyf, mk_kyf = arg, True
        elif opt == '--mj': jmr = True
        elif opt == '-t': v += 't'

v: str = "p"
en_: bool = False
de_: bool = False
p_cache:bool = True
iby: bytes = None
inj: str = None
ouf: str = None
vp1: bool = False
vb1: bool = False
ilv: int = 0
ppl: list[int, int] = [0, 1]
sha: str = '256'
hps: int = 3
kyf: str = None
mk_kyf: bool = False
jmr: bool = False
file_warn: bool = False

def enc_main():
    global iby, ouf, inj
    global ilv, ppl, sha, hps, kyf, mk_kyf
    global v, vp1, jmr
    if jmr:
        if vp1: print(" [*] run MemJammer", file=stdout)
        gen_ctl = fscMJ.GEN_CTL(len(iby) + 256 + ilv + 128 * hps)
        next(gen_ctl)
    if vp1: print(" [+] Hashing", file=stdout)
    o = fscModule.FStreamCipher(
        iby, (
            fscIO.pph(sha=sha) if not kyf else fscIO.multi_hash(kyf, mk=mk_kyf)
        ), ilv, ppl, hps, v=v
    ).encrypt()
    if inj:
        if vp1: print(" [f] Injecting", end="", file=stdout)
        fscIO.inject(inj, o)
        if vp1: print(" _DONE_", file=stdout)
    if ouf:
        if vp1: print(f" [f] WriteOut '{ouf}'")
        with open(ouf, "wb") as f:
            f.write(o)
    if not inj and not ouf:
        fscIO.to_stderr(o)
    if jmr:
        next(gen_ctl)
        if vp1: print(" [*] MemJammer stopped", file=stdout)
    exit(0)

def dec_main():
    global iby, ouf, inj
    global ilv, ppl, sha, hps, kyf, mk_kyf
    global v, vp1, jmr
    if inj:
        if vp1: print(" [+] Extracting", end="", file=stdout)
        iby = fscIO.extract(inj)
        if vp1: print(" _DONE_", file=stdout)
    if jmr:
        if vp1: print(" [*] run MemJammer", file=stdout)
        gen_ctl = fscMJ.GEN_CTL(len(iby))
        next(gen_ctl)
    if vp1: print(" [+] Hashing", file=stdout)
    o = fscModule.FStreamCipher(
        iby, (
            fscIO.pph(sha=sha) if not kyf else fscIO.multi_hash(kyf, mk=mk_kyf)
        ), ilv, ppl, hps, v=v
    ).decrypt(p_cache)
    if ouf:
        if vp1: print(f" [f] WriteOut '{ouf}'", file=stdout)
        with open(ouf, "wb") as f:
            f.write(o)
    else:
        fscIO.to_stderr(o)
    if jmr:
        next(gen_ctl)
        if vp1: print(" [*] MemJammer stopped", file=stdout)
    exit(0)


def i_main():
    global en_, de_, iby, ouf
    global ilv, ppl, sha, hps, kyf, mk_kyf
    global v, vp1, vb1, jmr
    gib = fscIO.gen_rb_file(vp1, (256 + ilv + 128 * hps if de_ else 0))
    if jmr:
        if vp1: print(" [*] run MemJammer", file=stdout)
        gen_ctl = fscMJ.GEN_CTL(block + 256 + ilv + 128 * hps)
        next(gen_ctl)
    if vp1: print(" [+] Hashing", file=stdout)
    hash_k = (fscIO.pph(sha=sha) if not kyf else fscIO.multi_hash(kyf, mk=mk_kyf))
    print(f" [i] Started {datetime.now()}", file=stdout)
    if vb1: t = time()

    try:
        if en_:
            while True:
                i_b = next(gib)
                o = fscModule.FStreamCipher(
                    i_b, hash_k, ilv, ppl, hps, v=v
                ).encrypt()
                with open(ouf, "ab") as f:
                    f.write(o)
                if vp1: print("\n· · · · · · · · · · · · · · · · ·", file=stdout)

        if de_:
            while True:
                i_b = next(gib)
                o = fscModule.FStreamCipher(
                    i_b, hash_k, ilv, ppl, hps, v=v
                ).decrypt(p_cache)
                with open(ouf, "ab") as f:
                    f.write(o)
                if vp1: print("\n· · · · · · · · · · · · · · · · ·", file=stdout)

    except StopIteration:
        if jmr:
            next(gen_ctl)
            if vp1: print(" [*] MemJammer stopped", file=stdout)
        if vb1: print(f"—————————————————————————————————\n"
                      f"—————————————————————————————————\n"
                      f"--$ {time() - t} s", file=bench_out)
        if vp1: print(f" [f] Writen : '{ouf}'", file=stdout)
        print(f" [i] Finished {datetime.now()}", file=stdout)
        exit(0)


def main():
    global en_, de_, p_cache, iby, ouf
    global v, vp1, vb1, file_warn, jmr, dsc

    read_opt()
    vp1 = (True if 'v' in v else False)
    vb1 = (True if 'b' in v else False)

    if dsc: fsc_manual.DISCLAIMER()

    if iby == -1: iby = fscIO.b_stdin()
    if iby == -2: iby = fscIO.hb_stdin()
    if type(iby) == str:
        iby = fscIO.rb_file(iby, (256 + ilv + 128 * hps if de_ else 0))

    if iby == -3 and (en_ or de_):
        print(" [i] Size_gt_10MiB", file=stdout)
        if jmr: print(" {!} CRITICAL : MemJammer activated", file=stdout)
        if 'P' in v: print(" [!] ResourceWarning : verbose process status", file=stdout)
        if 'p' in v: print(" [i] ResourceInfo : process isn't quiet", file=stdout)
        if de_ and p_cache: print(" {!} CRITICAL : cache positions", file=stdout)
        if file_warn: print(f" [!] AppendAt : '{ouf}'", file=stdout)
        if inj: exit(" [E] InjectError : Limit 10 MiB")
        elif not ouf: exit(" [E] NoOutputSpecification")
        i_main()

    if file_warn: print(f" [!] OverWrite :'{ouf}'", file=stdout)

    if (de_ or en_) and (not inj and not ouf) or (de_ and not ouf):
        print(" [!] return result to stderr? ", file=stdout, end="")
        if input() not in ('y', 'Y', 'yes', 'Yes', 'YES', 'ok', 'k', '1'): exit(" [i] exit")

    if en_:
        enc_main()

    if de_:
        dec_main()

    raise EOFError()


if __name__ == "__main__":
    try:
        print('\x1b[?25l', end="")
        main()
    except KeyboardInterrupt:
        exit('')
    except EOFError:
        fsc_manual.FSC_MANUAL('--help')
    except Exception as e:
        exit(f" [E -> MAIN] {e}")
    finally:
        print('\x1b[?25h', end="")
