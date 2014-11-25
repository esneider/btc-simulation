#!/usr/bin/env python
import math
import json
import sys
import os

def choose(n, k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

# def func(q, n, lam, beta):
#     ret = 1
#     P =    beta / (q * lam + beta)
#     Q = q * lam / (q * lam + beta)
#     for m in range(n + 1):
#
#         ret -= choose(n + m - 1, m) * (P**n * Q**m - P**m * Q**n)
#     return ret

def func(q, n, lam, beta):
    ret = 1
    P =    beta / (q * lam + beta)
    Q = q * lam / (q * lam + beta)
    for m in range(n + 1):
        LAM = n * Q / P
        num = (LAM ** m) * math.exp(-LAM) * (1 - (Q / P) ** (n - m))
        for k in range(1, m + 1):
            num /= k
        ret -= num
    return ret

with open('output.csv', 'w') as output:
    for fname in sys.argv[1:]:
        with open(fname) as f:
            data = json.load(f)
            output.write('%d,%d,%d,%d,%g,%g,%g,%g' % (
                data['size'],
                data['time'],
                data['nodes'],
                data['connections'],
                data['lambda'],
                data['alpha_mean'],
                data['beta_mean'],
                data['tps']
            ))
            for q in range(5, 40, 5):
                N = 0
                for n in range(100):
                    N = n
                    val = func(q / 100.0, n, data['lambda'], data['beta_mean'])
                    if val <= 0.001:
                        break
                output.write(',%d' % (N))
            output.write('\n')
