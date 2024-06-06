import random
import math
import string
import json
from tqdm import tqdm
from bigram import *
def generate_cipher(cypher:str) -> str:
    char_count = {x:0 for x in string.ascii_uppercase}
    for c in cypher:
        if c not in string.ascii_uppercase:
            continue
        if c in char_count:
            char_count[c]+=1
        else:
            char_count[c]=1
    sorted_char_count = sorted(char_count.items(),key=lambda x:x[1],reverse=True)
    common_chars = "EARIOTNSLCUDPMHGBFYWKVXZJQ"
    char_pairs = list(zip(common_chars,sorted_char_count))
    sorted_char_pair = sorted(char_pairs,key=lambda x:x[1][0])
    return ''.join([x[0] for x in sorted_char_pair])
def apply_key(text:str,key:str) -> str:
    u = text.upper()
    return ''.join([key[string.ascii_uppercase.index(c)] if c in string.ascii_uppercase else c for c in u])

def check_dict(text:str,key:str,words:list[str]) -> float:
    s = apply_key(text,key)
    score = 0
    w = s.split()
    n = len(w)
    for word in w:
        if word.lower() in words:
            score += 1
    return score/n
def swap(cipher:str) -> str:
    i = random.randint(0,25)
    j = random.randint(0,25)
    new_cipher = list(cipher)
    if i != j:
        new_cipher[i],new_cipher[j] = new_cipher[j],new_cipher[i]
    return ''.join(new_cipher)

class MCMC_sub:
    def __init__(self,text) -> None:
        self.bigram_scores = load_bigram()
        self.cipher = generate_cipher(text)
        self.text = text
        self.words = open("google-10000-english.txt").read().split("\n")
        
    def decrypt(self,text:str,iterations:int=10000) -> str:
        best_score = -float('inf')
        best_text = ""
        for i in tqdm(range(iterations)):
            ori_cipher = self.cipher
            new_cipher = swap(self.cipher)
            new_text = apply_key(text,new_cipher)
            score = grade(new_text,self.bigram_scores)
            if score > best_score or random.random() < math.exp((score - best_score) / 1.0):
                best_score = score
                best_text = new_text
                self.cipher = new_cipher
            if random.uniform(0,1) < 0.004:
                self.cipher = ori_cipher
            if i % 1000 == 0:
                if check_dict(best_text,self.cipher,self.words) > 0.5:
                    print(f"New best score: {best_score}, Text: {best_text}")
                
        return best_text

if __name__ == "__main__":
    text = "Of zit itqkz gy q rtflt ygktlz, rqhhstr lxfsouiz hotketr zit zioea eqfghn, eqlzofu q dglqoe gy souiz qfr liqrgv gf zit ygktlz ysggk. Q utfzst wkttmt violhtktr zikgxui zit stqctl, eqkknofu vozi oz zit letfz gy vosrysgvtkl qfr rqdh tqkzi. Wokrl eiokhtr dtsgrogxlsn ykgd iorrtf htkeitl, qrrofu zg zit ltktft lndhigfn gy fqzxkt. Qdorlz ziol zkqfjxos ltzzofu, q ldqss, exkogxl ygb hgatr ozl itqr ykgd wtiofr q wxli, ozl wkouiz tntl leqffofu zit lxkkgxfroful vozi q dob gy eqxzogf qfr vgfrtk. Ql oz ctfzxktr yxkzitk, zit kxlzst gy ozl lzthl dofustr vozi zit lgyz lgxfrl gy zit ygktlz, ektqzofu q htqetyxs iqkdgfn vozi zit vosrtkftll."
    text = text.upper()
    tt = ""
    for c in filter_plaintext(text):
        tt += c
    mcmcsub = MCMC_sub(tt)
    print(mcmcsub.decrypt(tt))