
import pymongo
import yaml

db = pymongo.MongoClient().virtlab
config = yaml.load(open('/data/config.yml'), Loader=yaml.BaseLoader)

# create attrs collection
try:
    db.create_collection("attrs")
    print('Created attrs collection')
except pymongo.errors.CollectionInvalid:
    pass
else:
    db.attrs.insert_one({"_id": "last_count", "value": 0})

# create index_pool collection
try:
    db.create_collection("index_pool")
    print('Created index_pool collection')
except pymongo.errors.CollectionInvalid:
    pass

# fill the index_pool
last_count = db.attrs.find_one({"_id": "last_count"})['value']
user_count = int(config['USER_COUNT'])
if user_count > last_count:
    diff_count = user_count - last_count
    print('Adding {} more seats'.format(diff_count))
    new_members = range(last_count, user_count)
    db.index_pool.insert_many([{"value": x} for x in new_members])
    db.attrs.update_one({"_id": "last_count"}, {"$set": {"value": user_count}})

# create roster collection
try:
    db.create_collection("roster")
    print('Created roster collection')
except pymongo.errors.CollectionInvalid:
    pass
