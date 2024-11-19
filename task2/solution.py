import requests
import csv

# Constants
API_URL = "https://ru.wikipedia.org/w/api.php"
CATEGORY = "Категория:Животные по алфавиту"

def get_category_pages(category):
    """
    Gets all pages in the given category.
    """
    pages = []
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmtype": "page",
        "cmlimit": "max",
        "format": "json"
    }

    while True:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Check for successful request
        data = response.json()
        members = data.get("query", {}).get("categorymembers", [])
        for member in members:
            pages.append(member['title'])
        if 'continue' in data:
            params['cmcontinue'] = data['continue']['cmcontinue']
        else:
            break
    return pages

def count_animals_by_letter(titles):
    counts = {}
    for title in titles:
        # Get the first letter
        letter = title[0].upper()
        counts[letter] = counts.get(letter, 0) + 1
    return counts

def write_to_csv(counts, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])

def main():
    titles = get_category_pages(CATEGORY)
    counts = count_animals_by_letter(titles)
    write_to_csv(counts, 'beasts.csv')
    print("Data successfully written to 'beasts.csv'.")

if __name__ == "__main__":
    main()
