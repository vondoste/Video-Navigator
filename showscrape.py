"""
Scraping show episode information from my personal web server
"""
# Import the `requests` package
import requests

# Import `BeautifulSoup` from the `bs4` package
from bs4 import BeautifulSoup

import pandas as pd

def main():
    NUMBER_OF_SEASONS = 10
    BECKER = 1
    CHEERS = 2
    CHOSEN = 3
    FRASIER = 4
    FRIENDS = 5
    QUEST = 6
    KOQ = 7
    OFFICE = 8
    SANDFORD = 9
    STARWARS = 11
    RAYMOND = 14
    
    SHOWS = [BECKER, CHEERS, CHOSEN, FRASIER, FRIENDS, QUEST, KOQ, OFFICE, SANDFORD, STARWARS, RAYMOND]
    SEASONS = {BECKER: 6, CHEERS: 10, CHOSEN: 2, RAYMOND: 9, FRASIER: 11, FRIENDS: 10, 
             QUEST: 1, KOQ: 9, OFFICE: 9, SANDFORD: 6, STARWARS: 1}
    URLS = {BECKER: ("Becker","Becker"),
            CHEERS: ("Cheers","Cheers"),
            CHOSEN: ("The Chosen","Chosen"),
            RAYMOND: ("Raymond","Raymond"),
            FRASIER: ("Frasier","Frasier"),
            FRIENDS: ("Friends","Friends"),
            QUEST: ("Johnny Quest","Johnny Quest"),
            KOQ: ("King of Queens","KOQ"),
            OFFICE: ("the office","Office"),
            SANDFORD: ("Sanford and Son","Sanford"),
            STARWARS: ("Movies","star wars")
            }

    rows = [] # this will hold out rows for the df
    final_data_list = []
    for series in SHOWS:
        if SEASONS[series] > 1:
            for i in range(1,SEASONS[series] + 1):
                temp = URLS[series]
                url = f"http://192.168.1.250/Video/{temp[0]}/Season {i}/{temp[1]}-season{i}.html"
                # print(url)
                rows.append(buildRows(url,series))
                # print(rows)
        else:
            # print('else clause')
            temp = URLS[series]
            url = f"http://192.168.1.250/Video/{temp[0]}/{temp[1]}.html"
            rows.append(buildRows(url,series))


    for row in rows:
        for item in row:
            # print(item)
            final_data_list.append(item)
    df = pd.DataFrame.from_dict(final_data_list)
    



    df.to_csv("episodes.csv",header=False,mode='a')


        
def buildRows(url: str, SeriesID: int)->list[dict]:
    # print(url)
    # Get data from the URL
    data = requests.get(url)
    # print(data)
    # Find data text (the HTML!) 
    html = data.text
    # Parse data using the HTML that we extracted using the `html.parser`, and save output to soup.
    soup = BeautifulSoup(html, 'html.parser')
    # Now, let's print out the "prettified" version of that HTML!
    #print(soup.prettify())
    # Find all table elements on the page
    tables = soup.find_all("ol")
    #print("Number of tables: " + str(len(tables)))
    #print("Tables:")
    #print(tables)
    # Select the table
    table = tables[0]
    # Find all rows in the table
    rows = table.find_all("li")
    """
    for i in range(0,5):
        print(rows[i])
        print("\n")
    """
    # Print out prettified HTML for row 2 (index 1)
    # print(rows[1].prettify())
    # Find all <td> elements in the row
    tds = rows[1].find_all("a")
    '''
    # Iterate over all <td> elements and print them out
    for td in tds:
        print(td)
    '''
    # Determine column headers
    # column_headers = ["ename", "SeriesID", "season", "episode", "url"]

    #Create list to store final data
    final_data_list = []

    # Iterate over every other row...
    for index, row in enumerate(rows):
        
        row_data = {}
        
        # Find all <td> elements in the row
        tds = row.find_all("a")

        row_data["ename"] = tds[0].text

        row_data["SeriesID"] = SeriesID

        temp = soup.find_all("title")
        temp2 = temp[0].text.split()
        if temp2[0] == "Johnny":
            row_data["season"] = 1
        elif temp2[0] == "Star":
            row_data["season"] = 1
        else:
            row_data["season"] = int(temp2[len(temp2)-1])

        row_data["episode"] = index + 1

        temp = str(tds[0]).split('"')
        row_data["url"] = temp[1]
        # Add data to final list    
        final_data_list.append(row_data)
    return final_data_list

if __name__ == "__main__":
    main()
