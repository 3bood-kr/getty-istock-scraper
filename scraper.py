import requests
from bs4 import BeautifulSoup
import os

def get_images_urls(term, max_images, choice, page=1):
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    images_urls = set()
    site = None
    if choice == "g":
       site = 'gettyimages.ae'
    else:
       site = 'istockphoto.com'

    url = f'https://{site}/search/2/image?phrase={term}&page={page}'

    while(max_images > len(images_urls) and page <= 100):
        # You Can Configure The Url To Scrap From Getty Images Also
        url.format(page=page)
        response = requests.get(url, headers=headers)      
        soup = BeautifulSoup(response.content, 'html.parser')

        for element in soup.find_all('picture'):
           link = element.find('img')['src']
           images_urls.add(link)

           if(max_images <= len(images_urls)):
              return images_urls
           
        page += 1

    return images_urls



term = input('Enter Search Term: ').strip().replace(" ", "%20")

max_images = None
while max_images is None:
    try:  
      max_images = int(input('Enter Max Images To Scrap: '))
    except ValueError:
      print('Please Enter A valid Number!')

choice = None 
while choice is None: # pick site to scrap (getty/istockphoto)
    choice = input('Scrap From GettyImages.com or iStockphoto.com?  (g/i): ')[0]
    if(choice != "g" and choice != "i"):
       choice = None

urls = get_images_urls(term, max_images, choice=choice) # Get URLs

if not os.path.isdir('images'): # Create Images Folder 
  os.mkdir('images')

i = 1
for url in urls: #Download Images From URLs
  response = requests.get(url)
  if response.status_code == 200:
    with open(f'images/image{i}.png', 'wb') as f:
        f.write(response.content)
        print(f'Image {i} Downloaded')
  i += 1     

