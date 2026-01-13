A module for Bài cào — a Vietnamese basic card game

```py
>>> import baicao           # Imports the module, of course
>>> hand = baicao.BaiCao()  # Create a card pack
>>> hand.shuffle_pack()     # Shuffles the pack
>>> hand.deal()             # Deals a hand
>>> hand.calculate()        # Calculates the hand's point, result depends on your luck!
'Ba cào!!!'
```