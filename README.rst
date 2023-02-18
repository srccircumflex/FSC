Fragmented Stream Cipher
####


.. image:: ./experimental.png
    :align: left
    :width: 200
    :alt: experimental.png

.. image:: ./revision.png
    :align: left
    :width: 200
    :alt: experimental.png


FSC is an encryption algorithm written in Python. The encryption of data is based on a combination of transposition
of 128-byte blocks and 10-MiB block XOR operations. The encryption string is generated from an input passphrase,
according to its hash, and defines the transposition and XOR operation in a two-step process.
To disguise the beginning of the data, an initialization vector of random characters is prepended.

Additional Parameters
++++

The encryption process can be modified via additional parameters.

+------------------------+------------+----------+--------------------------------------------------------+
| Parameter              | Value      | Default  | Description                                            |
+========================+============+==========+========================================================+
| --ilv                  | integer    | 0        | extends the default initialization vector of 256 bytes |
+------------------------+------------+----------+--------------------------------------------------------+
| --part                 | 0 or 1     | 0        | defines the character of the generated pair which will |
|                        |            |          | be used for encryption considering the priority        |
+------------------------+------------+----------+--------------------------------------------------------+
| --prio                 | integer    | 1        | defines the priority with which the defined character  |
|                        |            |          | is used instead of the other one from the pair         |
|                        |            |          | (1 means every, 2 every second, 3 every third, ...)    |
+------------------------+------------+----------+--------------------------------------------------------+
| --hops                 | integer    | 3        | defines the jumps through the 128-byte blocks that are |
|                        |            |          | made during the transposition                          |
+------------------------+------------+----------+--------------------------------------------------------+
| --sha512               |            | sha256   | defines the hash function with which the seed is       |
|                        |            |          | created from the passphrase                            |
| --sha256               |            |          |                                                        |
|                        |            |          |                                                        |
| --sha224               |            |          |                                                        |
+------------------------+------------+----------+--------------------------------------------------------+


Performance
++++

The time expenditure for the encryption is linear to the mass of the bytes, depending on the CPU ALU;
decryption takes about 18% longer. 10 MiB need 135 seconds to encrypt on a "standard" system with a
CORE i5 8th Gen. CPU usage of 12 %.


Vulnerability thesis
++++

**Basically, encryption is as secure as the complexity of the passphrase**

In the worst case, if both the encrypted and decrypted files exist, it is theoretically possible
to obtain part of the encryption string from them.

The original passphrase cannot be obtained due to hashing. The seed can also not be obtained because
it is not used directly for the encryption. The fact that the encryption string is only partially used
for the XOR operations prevents a back calculation.

Before a purposeful XOR linking of the two files becomes possible, the transposition must be solved
(with a permutation of 3.8562048236258E+215 for each 128 byte block) and the initialization vector must
be removed.


****


**Analysis**

The option sequence ``-test`` (``-[v]test``) is intended for analysis.
On linux the output can be piped in a file.

``fsc -vtest 2>> file``
