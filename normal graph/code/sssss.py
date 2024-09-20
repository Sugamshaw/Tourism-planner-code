import pandas as pd
places_data = pd.read_csv("places.csv", index_col="PLACES")
places = list(places_data.index)
total_ratings=0
for i in range(len(places)-1):
    total_ratings += places_data.at[places[i+1], "RATINGS"]
    
print(total_ratings)