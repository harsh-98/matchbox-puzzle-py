# Matchbox puzzle v1

## Cmd to run
```
python game.py -x   2974341663658 -y -197967556159255  -l 4
```


## Test 
Go to goerli.voyager.online. Find any valid submission tx to this puzzle_v1 game. Copy the xhr response from api/txn endpoint. Store that in json file locally and copy the args to `submit_move_for_level` from explorer. Using this you can verify game.py is working as intended. Some example txs that I have downloaded and tested are below: 

```
python game.py -x   2974341663658 -y -197967556159255  -l 4 -t example/b.json
python game.py -x   90000000000000 -y -125000000000000  -l 3 -t example/a.json
```

## Use case

- For testing locally if the velocity x,y coordinates for given level are a valid solution. This is much faster than sending a tx to starknet goerli and waiting for the result.
- For bruteforcing the solutions.
