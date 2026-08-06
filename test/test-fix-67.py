from key_multivalue_storage import Storage

db = Storage("top_lv_key", foo="bar")

dict1 = db.to_dict()

print(db)
print(isinstance(db, dict))
print(isinstance(db, Storage))
print('')
print(dict1)
print(isinstance(dict1, dict))
print(isinstance(dict1, Storage))
print('')
