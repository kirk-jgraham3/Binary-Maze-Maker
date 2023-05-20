import binGenDFS
import binGenKruskal
import binPlay
import binAStar
import os

os.system('cls')
while True:
    alg = input("DFS (d) or Kruskal (k)?")
    if alg in ['d','k','D','K']:
        break
if alg in ['d', 'D']:
    binGenDFS.main()
if alg in ['k', 'K']:
    binGenKruskal.main()
    
print()

while True:
    a_star = input("AI solution? (y/n)")
    if a_star in ['y','n','N','Y']:
        break
if a_star in ['y','Y']:
    binAStar.main()

while True:
    play = input("Play it yourself? (y/n)")
    if play in ['y','n','N','Y']:
        break

if play in ['y','Y']:
    binPlay.main()