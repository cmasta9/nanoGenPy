#adapted from https://github.com/npy0/nanopy

import hashlib
import secrets
import binascii
import base64
import nanoED25519 as ed

import requests

url = 'https://rainstorm.city/api'

prefix = ['nano_','ban_']
encodix = b'13456789abcdefghijkmnopqrstuwxyz'

def getSeed():
    seedy = secrets.token_hex(32)
    return seedy

def getPriv(seed,index=0):
    assert len(seed) == 64
    blake = hashlib.blake2b(digest_size=32)
    blake.update(bytes.fromhex(seed)+index.to_bytes(4,byteorder='big'))
    return blake.hexdigest().upper()

def getPub(priv):
    return binascii.hexlify(ed.publickey(int(priv,16).to_bytes(32))).upper().decode()

def getAddr(pub,pre=prefix[0]):
    pub = bytes.fromhex(pub)
    check = hashlib.blake2b(pub,digest_size=5).digest()
    pub = b'\x00\x00\x00' + pub + check[::-1]
    addr = base64.b32encode(pub)
    addr = addr.translate(bytes.maketrans(base64._b32alphabet,encodix))[4:]
    return pre + addr.decode()

def gen():
    #seed = binascii.hexlify(int(1).to_bytes(32)).decode()
    seed = getSeed()
    print(f'seed: {seed}')
    priv = getPriv(seed,0)
    print(f'priv: {priv}')
    pub = getPub(priv)
    print(f'pub: {pub}')
    addy = getAddr(pub)
    print(f'addy: {addy}')
    return addy

def getBal(a):
    res = requests.post(url,json={'action': 'account_balance', 'account': a})
    print(res.text)

addy = gen()
#getBal(addy)