from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
from django.core.paginator import Paginator
from .models import Movie
def home_view(request):


    return render(request, "dashboard1.html")




def scrape_imdb_top_movies(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad response status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        movie_data = soup.findAll('div', attrs={'class': 'ipc-metadata-list-summary-item__tc'})
        images = soup.find_all('img', attrs={'class': 'ipc-image'})

        movie_info = []

        for data, img in zip(movie_data, images):
            name = data.a.h3.text
            year = data.find_all('span', class_='sc-be6f1408-8 fcCUPU cli-title-metadata-item')[0].text
            time = data.find_all('span', class_='sc-be6f1408-8 fcCUPU cli-title-metadata-item')[1].text
            rate = data.find('span', class_='sc-be6f1408-1 dbnleL').text.replace('Rate', '')
            rate = re.sub(r'\([^)]*\)', '', rate)
            vote = data.find('span', class_='sc-be6f1408-1 dbnleL').text.replace('Rate', '')
            vote = re.findall(r'\(([^)]*)\)', vote)[0]

            alt = img.get('alt')
            src = img.get('src')

            movie_info.append({
                'name': name,
                'year': year,
                'time': time,
                'rate': rate.strip(),
                'vote': vote.strip(),
                'alt_image': alt,
                'src_image': src
            })
        return movie_info

    except requests.exceptions.RequestException as e:
        print("An error occurred while making a request:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
# url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250&sort=popularity%2Casc'
# movie_info = scrape_imdb_top_movies(url)
# for movie in movie_info:
#     print(movie)

def top_movies(request):
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250&sort=popularity%2Casc'
    movie_info = scrape_imdb_top_movies(url)
    per_page = 12
    paginator = Paginator(movie_info, per_page)  # Split into pages with 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}

    return render(request,'topmovie.html',context)


from .models import Movie  # Assuming you have a Movie model defined in models.py

def save_movie_data(movie_info):
    for movie in movie_info:
        name = movie['name']
        year = movie['year']
        time = movie['time']
        rate = movie['rate']
        vote = movie['vote']
        alt_image = movie['alt_image']
        src_image = movie['src_image']

        # Check if the movie already exists in the database
        existing_movie = Movie.objects.filter(name=name).first()

        if existing_movie:
            # Update existing record
            existing_movie.year = year
            existing_movie.time = time
            existing_movie.rate = rate.strip()
            existing_movie.vote = vote.strip()
            existing_movie.alt_image = alt_image
            existing_movie.src_image = src_image
            existing_movie.save()
        else:
            # Create a new record
            Movie.objects.create(
                name=name,
                year=year,
                time=time,
                rate=rate.strip(),
                vote=vote.strip(),
                alt_image=alt_image,
                src_image=src_image
            )

