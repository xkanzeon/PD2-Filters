import requests
import json
from pathlib import Path

authorListJson = json.loads(requests.get('https://raw.githubusercontent.com/Project-Diablo-2/LootFilters/main/filters.json').text)
for author in authorListJson:
    authorFolder = Path(__file__).parent / 'filters' / author['author']
    Path(authorFolder).mkdir(parents=True, exist_ok=True)

    authorContentsJson = requests.get(author['url']).json()
    if 'message' in authorContentsJson:
        print(authorContentsJson['message'])
        break
    for file in authorContentsJson:
        try:
            if file['name'].endswith('.filter'):
                filterName = file['name'].replace('.filter', '')
                print(f"Downloading {author['author']}/{filterName}...")
                Path(authorFolder / filterName).mkdir(parents=True, exist_ok=True)
                with open(Path(authorFolder) / filterName / 'loot.filter', 'wb') as filter:
                    filterResponse = requests.get(file['download_url'])
                    filterResponse.encoding = 'cp1252'
                    if 'message' in filterResponse:
                        print(filterResponse['message'])
                        break
                    filter.write(filterResponse.content)
        except Exception as e:
          print(f"Error writing file [{file['name']}]: {e}")
          continue
