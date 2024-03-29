import requests


def get_average_rating(business_name):
    url = f'http://localhost:8000/api/v1/reviews-ratings/average-rating/?business_name={busines_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']