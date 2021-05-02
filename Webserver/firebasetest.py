from firebase import firebase
import plot_room as p 


def get_most_recent_data():
    fb = firebase.FirebaseApplication("https://fyp-database-7e287-default-rtdb.europe-west1.firebasedatabase.app/",None)

    MapData = []

    db_entries = fb.get('/MapData/',None)
    db_entries = list(db_entries.values())
    db_entries.reverse()
    for entry in db_entries[0]:
        MapData.append(entry)
        

    return MapData

if __name__ == '__main__':
	MapData = get_most_recent_data()
    p.plot(MapData)


