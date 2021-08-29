# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 23:15:06 2021

@author: kazuk
"""

"""
dp[i][lst][less][more] := 順列のi番目まで確定していて、最後の要素がlst、それより小さい要素がless個、大きい要素がmore個あるとする組み合わせ
dp[i][lst][less][more]からの遷移を考えると、

次の要素との関係が'<'ならば、more通りの遷移先がある
次の要素との関係が'>'ならば、less通りの遷移先がある
ここで、問題として遷移先のDPのlstをどうするかという問題があるが、遷移を見てみると、lstは特に使っていない。
つまり、最後の要素に対して小さい数、大きい数がどれだけ残っているかが重要になる。
そのため、lstを削ってみる。
　
dp[i][less][more] := 順列のi番目まで確定していて、最後の要素より小さい要素がless個、大きい要素がmore個あるとする組み合わせ
dp[i][less][more]からの遷移を考えると、

次の要素との関係が'<'ならば、more通りの遷移先がある
次の要素との関係が'>'ならば、less通りの遷移先がある
はしっかり行える。
次の要素との関係が'<'で、more通りの中で小さい方から2番目に遷移したとすると、遷移先はdp[i+1][less+1][more-2]のようにかける。
これで状態O(N^3)、遷移O(N)となり、O(N^4)を達成できる。
ここから、まずは、状態を削減できる。

dp[i][less] := 順列のi番目まで確定していて、最後の要素より小さい要素がless個である組み合わせ
moreを削ったのだが、i番目まで確定ということは未確定要素はN-i-1個となる。
（N-i-1の-1はiを0-indexedで考えているため）
よって、lessがわかれば、more=N-i-1-lessなので、状態として分けて保存しなくてもいい。
dp[i][less]からの遷移を考えると、

次の要素との関係が'<'ならば、N-i-1-less通りの遷移先がある
次の要素との関係が'>'ならば、less通りの遷移先がある
となり、変わらない。
これで状態O(N^2)、遷移O(N)
最後に遷移を最適化する。　
　
DPの最適化でよくあるテクだが、配るDPを貰うDPに変換する。
今までは遷移元から遷移先を考えていたが、逆に遷移先から遷移元を考える。
dp[i][less]への遷移元について考えてみると、

前の要素との関係が'<'ならば、dp[i-1][0], dp[i-1][1], ..., dp[i-1][less]
次の要素との関係が'>'ならば、dp[i-1][less+1], dp[i-1][less+2], ..., dp[i-1][N-1]
となる。
これは区間和になっているので、1つ前の桁のDPをBITにしておけば高速に取得できる。
"""

from itertools import accumulate
n = int(input())
s = [0] + list(input())
mod = 10**9+7

#dp[i][less] := 順列のi番目まで確定していて、最後の要素より小さい要素がless個である組み合わせ
#moreを削ったのだが、i番目まで確定ということは未確定要素はN-i-1個となる。
#（N-i-1の-1はiを0-indexedで考えているため）
dp = [[0] * n for _ in range(n)]

#一つ目は何をおいてもよい
#ある要素を置くとそれに応じてjも変化するはずで各々一通りある(初期化)
for j in range(n):
    dp[0][j] = 1
dp_now = list(accumulate(dp[0]))
for i in range(1, n):
    dp_prev = dp_now
    dp_now = [0] * n
    for j in range(n - i):
        #前の要素が小さいならば、そのどれからも自分に対して遷移する可能性がある
        if s[i] == "<":
            dp[i][j] = dp_prev[j]%mod
            #for k in range(j+1):
                #dp[i][j] += dp[i-1][k]
        #前の要素が自分より大きいならば、そのどれからも自分に遷移する可能性がある
        else:
            dp[i][j] = (dp_prev[n - i] - dp_prev[j])%mod
            #for k in range(n-i-j, n-i+1):
                #dp[i][j] += dp[i-1][k]
        if j == 0:
            dp_now[j] = dp[i][j]
        else:
            dp_now[j] += (dp_now[j-1] + dp[i][j])%mod

print(dp[-1][0]%mod)

                