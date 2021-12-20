from itertools import cycle
code = "0000D00343138881132611422165451197811827150410037302229143770132912276155641097002516170920341400026163441354315793140611099204518152091496911753197220008110215192690006210201188020012210163182990008910081172860012310029162490013010021149350009900004138610008910012128220004310000117450006300021109331004600011104930003500183131431242702142172740236515735172951195716898129381151305308154860384313091143321517012945182861022418247152281507101358151020276602791"

minussign = {1: {'a': False, 'b': False},
 2: {'a': False, 'b': False},
 3: {'a': True, 'b': False},
 4: {'a': True, 'b': False},
 5: {'a': False, 'b': True},
 6: {'a': True, 'b': True},
 7: {'a': False, 'b': True},
 8: {'a': False, 'b': False},
 9: {'a': False, 'b': False},
 10: { 'a': True, 'b': False},
 11: { 'a': True, 'b': False},
 12: { 'a': False, 'b': True},
 13: { 'a': True, 'b': False},
 14: { 'a': True, 'b': False},
 15: { 'a': True, 'b': False},
 16: { 'a': True, 'b': False},
 17: { 'a': False, 'b': False},
 18: { 'a': True, 'b': True},
 19: { 'a': True, 'b': False},
 20: { 'a': True, 'b': False},
 21: { 'a': True, 'b': False},
 22: { 'a': False, 'b': True},
 23: { 'a': True, 'b': False},
 24: { 'a': False, 'b': False},
 25: { 'a': False, 'b': True},
 26: { 'a': True, 'b': False},
 27: { 'a': False, 'b': False},
 28: { 'a': False, 'b': False},
 29: { 'a': False, 'b': True},
 30: { 'a': True, 'b': True}}

trailing_zeros = code[:4] 
serial_number = code[4:10]
number = code[11]
# sono dopo gruppi di 5 numeri
values_dict = {}
values = cycle(["L","a","b"])
patch = 0
for i in range(30*3):
    value = next(values)
    if value == "L":
        patch +=1
        values_dict[patch] = dict()
    values_dict[patch][value] = code[11+5*i:11+5*i+5]