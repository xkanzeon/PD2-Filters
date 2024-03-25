# Rebased onto Mewtiny's master list creation
# Mostly just added the batch download for this repo

import urllib.request as req, json
from pathlib import Path

pd2FilterListUrl = "https://raw.githubusercontent.com/Project-Diablo-2/LootFilters/main/filters.json"
masterFilterList = {}

with req.urlopen(pd2FilterListUrl) as url:
    authorsData = json.load(url)

if authorsData:
    for d in authorsData:
        authorName  = d["author"]
        displayName = d["name"]
        authorUrl   = d["url"]

        masterFilterList[authorName] = {}
        
        masterFilterList[authorName]["info"] = d
        masterFilterList[authorName]["filters"] = []

        with req.urlopen(authorUrl) as url:
            filterData = json.load(url)
        
        if filterData:
            for f in filterData:
                if f['name'].endswith('.filter'):
                    masterFilterList[authorName]["filters"].append({
                        "name": f["name"],
                        "url": f["url"],
                        "download_url": f["download_url"]
                    })

                    with req.urlopen(f["download_url"]) as url:
                        url.headers.set_param("charset", "cp1252")
                        filterText = url.read()
                    
                    filterName = f["name"].replace(".filter", "")
                    Path(Path(__file__).parent / "filters" / authorName / filterName).mkdir(parents=True, exist_ok=True)
                    with open(Path(__file__).parent / "filters" / authorName / filterName / "loot.filter", "wb") as filter:
                        filter.write(filterText)

    jsonData = json.dumps(sorted(masterFilterList.items()), indent=4)
    with open("pd2_filters.json", "w") as j:
        j.write(jsonData)
