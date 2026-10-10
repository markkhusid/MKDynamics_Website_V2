# CSE543 Information Assurance and Security - Esper Cipher

Created with Grok Build

Esper, as used in this course, is a byte cipher with two steps. Each byte is rotated left by a small bit count, then exclusive-ored with a byte from a repeating key. Decryption exclusive-ors the same key byte and rotates right by the same count. Grokipedia has no article under this course's name for the cipher. The two operations are the [circular shift](https://grokipedia.com/page/Circular_shift) and the [XOR cipher](https://grokipedia.com/page/XOR_cipher). A repeating XOR key is a short keystream. The rotation only scrambles which bits meet which key bits. It does not add a new secret.

The submission decrypted a course ciphertext with a course key. Those two files stay off this page. The example uses a new seven-byte key and a new sentence.

## Rotate, then exclusive-or

```python
def rotl(byte, count):
    count = count & 7
    byte = byte & 0xFF
    if count == 0:
        return byte
    high = (byte << count) & 0xFF
    low = byte >> (8 - count)
    return high | low

def rotr(byte, count):
    count = count & 7
    if count == 0:
        return byte & 0xFF
    return rotl(byte, 8 - count)

def encrypt(data, key, count):
    out = bytearray()
    for index, byte in enumerate(data):
        mixed = rotl(byte, count) ^ key[index % len(key)]
        out.append(mixed)
    return bytes(out)

def decrypt(data, key, count):
    out = bytearray()
    for index, byte in enumerate(data):
        mixed = byte ^ key[index % len(key)]
        out.append(rotr(mixed, count))
    return bytes(out)
```

With key `Bright7` and a rotate of 3, `Public demo only` encrypts to the hex line `c0d97a04236f366159021c690f4421b9`. Decrypting with the same key and count returns the sentence.

## Why the order matters

Exclusive-or is its own inverse, and a right rotation undoes a left rotation. Swap the order, or use a different count, and the bytes stay scrambled. That is the whole cipher: two invertible steps, applied in a fixed order.
