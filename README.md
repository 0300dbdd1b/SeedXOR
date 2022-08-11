# seedXOR

"The aim of this repo is to provide a way to split and recombine mnemonic phrases using the XOR operator in python"
</br>
</br>

##  Use :

--split will split your mnemonic phrase into n XOR backups
--deterministic will split your mnemonic phrase deterministically
--combine will combine n XOR backups to re-form a mnemonic phrase
```
 python3 SeedXOR.py --split "[your mnemonic]" [number of split]
 python3 SeedXOR.py --split --deterministic "[your mnemonic]" [number of split]
 python3 SeedXOR.py --combine "[your mnemonic spit1]" "[your mnemonic split2]" "[your mnemonic split n]"
```

 ##### Examples :
 `````
 python3 SeedXor.py --split "inmate stick assume lion demise drive foil fat party segment spare salad" 2
XOR Splitted Mnemonics :
1 :  industry blame wall intact cute end two bamboo play slender limb abandon

2 :  alter secret win waste artefact approve range door almost anchor faculty say

 `````

`````
python3 SeedXor.py --combine "industry blame wall intact cute end two bamboo play slender limb abandon" "alter secret win waste artefact approve range door almost anchor faculty say"
inmate stick assume lion demise drive foil fat party segment spare salad
`````


### Requierements :

- python3.x
- secrets : pip3 install secrets
- binascii : pip3 install binascii
