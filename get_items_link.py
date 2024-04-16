from bs4 import BeautifulSoup
import requests



class get_links():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.140", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    def _init_(self,product_name):
        self.product=product_name
        self.name=str(self.product)
        self.url="https://www.amazon.fr/s?k="+self.name+"&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3TP3EBVC6R45W&sprefix="+self.name+"%2Caps%2C128&ref=nb_sb_noss_1"
        self.page=requests.get(self.url,headers=self.headers)
        self.soup=BeautifulSoup(self.page.content,"html.parser")
        self.soup=BeautifulSoup(self.soup.prettify(),"html.parser")

    def _next_page(self):
        span=self.soup.find(class_="a-section a-text-center s-pagination-container")
        href=span.find(class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
        if href:
            href=href['href'].strip()
            self.url="https://amazon.fr/"+href
            self.page=requests.get(self.url,headers=self.headers)
            self.soup=BeautifulSoup(self.page.content,"html.parser")
            href=self.url
            return href
        return None
        
    
    def _grab_links(self):
        hrefs=[]
        page=requests.get(self.url,headers=self.headers)
        soup=BeautifulSoup(page.content,"html.parser")
        products=soup.find_all(class_="sg-col-inner")
        for product in products:
            href=product.find(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
            if href:
                href=href['href'].strip()
                href="https://amazon.fr/"+href
                hrefs.append(href)
        
        return hrefs
  
    def grab_all_links(self):
        all_links=[]
        all_links+=self._grab_links()
        href=self._next_page()
        while href:
            
            
            page_links=self._grab_links()
            all_links+=page_links
            href=self._next_page()
        return all_links


links_getter=get_links("computer")
print(len(links_getter.grab_all_links()))