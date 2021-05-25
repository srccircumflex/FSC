# FSC

— script main —

- (encrypt / decrypt)
- (files / stdin / hidden stdin)
- (injection / extraction)
- 10 MiB block recursive encryption

— cipher module —
- hashing
- initializations vector's
- transposition
- stream-ciphering
- additional variable specifications*

**Performance**

Expenditure of time to encrypt is linear to mass of bytes, depending on the CPU ALU;
decryption needs approximate 18 % longer. 10 MiB takes 135 seconds for encrypt on
a "standard" system with a CORE i5 8th Gen. CPU load pick 12 %. 

**Encrypt process**

- hash passphrase [1]
- involve initialization vector [2]
- transposition [3]
- stream ciphering [4]

_additional variable specifications_*

[1] function can be specified; hash from passphrase can be ⊕ with hash from a file.
[2] expandable. [3] hops can be specified. 
[4] bit-part of the stream and his priority can be specified.  

****

~**Vulnerability (These)** _by Default settings_*

- Basically, encryption is as secure as the complexity of the passphrase

: worsts case++ scenario: algorithm, encrypted and origin file available

    It's impossible to extract the origin key, because of hashing.
    To extract the seed its impossible too, because not used for encryption.
    A part of the stream can be extracted, after solved fragmentation.
    
    Permutation = (128 != 3.8562048236258E+215) * bytes / 128
    
    After the fragmentation has been resolved, 
    and the initialization vector has been cut out of the encryption, 
    it is possible to ⊕ the cipher with the original bytes.
    The result is a stream of every second byte from the original stream, 
    minus the initialization vector's.

****
**Analysis**

The option sequence `-test` is intended for analysis.
On linux the output can be piped in a file.

Example: `fsc -vtest 2>> file`

****

_Platform: Linux_;
_Status: Experimental.1_
