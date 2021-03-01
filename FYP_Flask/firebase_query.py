from firebase import firebase

def get_most_recent_data():
    fb = firebase.FirebaseApplication("https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/",None)

    most_recent_entries = []

    db_entries = fb.get('/MockedData/',None)
    db_entries = list(db_entries.values())
    db_entries.reverse()
    for entry in db_entries:
        most_recent_entries.append(entry)
        if len(most_recent_entries) > 60:
            break

    return most_recent_entries

print(get_most_recent_data())

