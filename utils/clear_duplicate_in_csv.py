
with open(r"C:\Users\pasho\Downloads\main_entries.csv",'r',encoding='utf-8') as in_file, open('main_entries.csv','w',encoding='utf-8') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)