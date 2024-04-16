from bs4 import BeautifulSoup
import requests
import datetime
import re


class product_scrapper():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.140", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    def __init__(self,url) :
        self.url=url
        self.page=requests.get(url,headers=self.headers)
        self.soup=BeautifulSoup(self.page.content,"html.parser")
        self.soup=BeautifulSoup(self.soup.prettify(),"html.parser")
    
    def get_title(self):
        title=self.soup.find(id="productTitle").get_text()
        return title.strip()
    
    def get_price(self):
            price_int=self.soup.find(class_="a-price-whole").get_text().replace(",","").strip()
            try:
                price_int=int(price_int)
                price_decimal=self.soup.find(class_="a-price-fraction").get_text().strip()
                price_decimal=int(price_decimal)/100
                price=price_int+price_decimal
                return price
            except Exception as e:
                price_int=re.sub(r'[^\d]','',price_int)
                price_int=int(price_int)
                price_decimal=self.soup.find(class_="a-price-fraction").get_text().strip()
                price_decimal=int(price_decimal)/100
                price=price_int+price_decimal
                return price
        
    def get_saving_pourcentage(self):
        saving_pourcentage=self.soup.find(class_="a-size-large a-color-base savingPriceOverrideEdlpT2 aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage")
        if saving_pourcentage:
            saving_pourcentage=saving_pourcentage.get_text().strip()
            return saving_pourcentage
    
    def get_main_image_url(self):
        image_url=self.soup.find('img',id="landingImage")
        if image_url:
            image_url=image_url['src']
            return image_url.strip()
    
    def get_stock_availability(self):
        stock=self.soup.find(id="availability")
        if stock:
            stock=stock.find('span').get_text()
            return stock.strip()

    def get_rating(self):
        rating=self.soup.find(id="averageCustomerReviews").find(class_="a-size-base a-color-base")
        if rating:
            rating=rating.get_text()
            rating=rating.strip().replace(',','.')
            return float(rating)
    
    def get_num_evaluations(self):
        num_evaluations=self.soup.find(id="acrCustomerReviewText")
        if num_evaluations:
            num_evaluations=num_evaluations.get_text()
            return num_evaluations.strip()
    
    def get_html_about_product(self):
        about_product=self.soup.find(id="feature-bullets")
        if about_product:
            about_product=about_product.find_all(class_="a-list-item")
            return about_product
    
    def get_paiment_method(self):
        countainer=self.soup.find(id="issuancePriceblockAmabot_feature_div")
        paiment=countainer.find('span')
        if paiment:
            paiment=paiment.get_text()
            if ':' not in paiment:
                return paiment.strip()
            else:
                spans=countainer.find_all('span')
                return spans[1].get_text().strip() + spans[2].get_text().strip()
    
    def get_time(self):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%d-%m-%Y")
        hour=current_datetime.strftime("%H")
        return formatted_datetime , hour
    
    def get_related_items(self):
        items_url=[]
        items=self.soup.find_all(class_="a-carousel-card")
        n=len(items)
        for i in range(n):
            link_normal=items[i].find(class_="a-link-normal")
            if link_normal :
                url=link_normal['href'].strip()
                if url[:5]=='https':
                    
                    pass
                else:
                    url='https://www.amazon.fr'+url
                    items_url.append(url)
        return items_url
    

url="https://www.amazon.fr/dp/B07GBWQDNW/ref=vp_d_cpf-substitute-widget_pd?_encoding=UTF8&pf_rd_p=aeba322b-e44b-4628-b6d2-3c9277ed0694&pf_rd_r=24YXMBC2SXEFVH9M8V4X&pd_rd_wg=Z5ZTg&pd_rd_i=B07GBWQDNW&pd_rd_w=E3Khx&content-id=amzn1.sym.aeba322b-e44b-4628-b6d2-3c9277ed0694&pd_rd_r=2edd0cca-efe6-4e4e-b72e-5d9a1f2eb0f4&psc=1"
scrapper=product_scrapper(url)
print(scrapper.get_price())
