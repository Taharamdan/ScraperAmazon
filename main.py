from get_items_link import get_links
from amazon_scrapper import product_scrapper

links_getter=get_links("phone")
links=links_getter.grab_all_links()
filename = "output.txt"
with open(filename, 'w') as file:
    for item in links:
        file.write(f"{item}\n")
print(f"Data written to {filename}")

phone_prices=[]
i=0
for link in links:
    try:
        product_scrapp=product_scrapper(link)
        price=product_scrapp.get_price()
        print(i,price)
        i+=1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(i)
        print(links[i+1])
        break