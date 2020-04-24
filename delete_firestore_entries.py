from google.cloud import firestore
db = firestore.Client()

# Delete a collection content
# Whenever a collection is empty it is deleted
def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(u'Deleting doc {} => {}'.format(doc.id, doc.to_dict()))
        doc.reference.delete()
        deleted = deleted + 1
    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

collection_ref = db.collection('groups').document('bfmtv').collection('entries')
delete_collection(collection_ref, 1)
