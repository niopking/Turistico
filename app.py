from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import openrouteservice

app = Flask(__name__)

@app.route('/')
def home():
    return "nikola"


@app.route('/scrape')
def scrape():
    output = ""
    inputi = request.args.get('param', default="Nista", type=str)
    inputi.replace(" " , "+")
    search_terms = inputi.split(",")
    output = ""
    for term in search_terms:
        try:
            query = term.strip().replace('_', '+')
            url = f"https://www.bing.com/images/search?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch Bing search results for {term}. HTTP Status: {response.status_code}")
                continue

            # Parse the response HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the first image in the search results
            first_image = soup.find("img", {"class": "mimg"})
            if first_image and first_image.get("src"):
                image_url = first_image["src"]
                output += image_url + ","
        except Exception as e:
            print(f"Error while processing '{term}': {e}")
            continue

    return output

@app.route('/locate')
def locate():
    prompt = request.args.get('names', default="Nista", type=str)
    prompt = prompt.split("QQ")
    result  = []
    for p in prompt:
        try:
            geolocator = Nominatim(user_agent="coordinate_finder")
            location = geolocator.geocode(p)
            if location is not None:
                result.append(str(location.latitude))
                result.append(str(location.longitude))
        finally:
            pass

    return result



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
