import requests
from bs4 import BeautifulSoup
import csv

class RightmoveScraper:
    results = []    
    
    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url)
        print(' | Status code: %s' % response.status_code)
        
        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        
        titles = [title.text.strip() for title in content.findAll('h2', {'class': 'propertyCard-title'})]
        addresses = [address['content'] for address in content.findAll('meta', {'itemprop': 'streetAddress'})]
        descriptions = [description.text for description in content.findAll('span', {'data-test': 'property-description'})]
        prices = [price.text.strip() for price in content.findAll('span', {'class': 'propertyCard-priceValue'})]
        dates = [date.text.split(' ')[-1] for date in content.findAll('span', {'class': 'propertyCard-branchSummary-addedOrReduced'})]
        sellers = [seller.text.split('by')[-1].strip() for seller in content.findAll('span', {'class': 'propertyCard-branchSummary-branchName'})]
        images = [image['src'] for image in content.findAll('img', {'itemprop': 'image'})]
        
        for index in range(0, len(titles)):
            self.results.append({
                'title': titles[index],
                'address': addresses[index],
                'price': prices[index],
                'description': descriptions[index],
                'date': dates[index],
                'seller': sellers[index],
                'image': images[index],
            })
    
    def to_csv(self):
        with open('rightmove.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
            
            print('Stored results to "rightmove.csv"')

    def run(self):
        url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE^2520&minBedrooms=2&maxPrice=1800&radius=1.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
        
        response = self.fetch(url)
        self.parse(response.text)

        self.to_csv()

if __name__ == '__main__':
    scraper = RightmoveScraper()
    scraper.run()