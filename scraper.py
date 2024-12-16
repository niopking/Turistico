from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "nikola"

# Route for the tourist attractions
@app.route('/scrape')
def scrape():
    output = ""
    inputi = request.args.get('param', default="Nista", type=str)

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, timeout=5, poll_frequency=1)

    search_term = inputi.split(",")
    for word in search_term:
        try:
            query = word.replace(' ', '+')
            url = f"https://www.google.com/search?q={query}&tbm=isch"

            driver.get(url)

            first_image = wait.until(EC.presence_of_element_located((By.XPATH,"//img[@class='YQ4gaf']")))
            first_image.click()

            large_image = wait.until(EC.presence_of_element_located((By.XPATH,"//a[@class='YsLeY']//img")))
            image_url = large_image.get_attribute("src")

            output+=image_url+","
        except Exception as e:
            print(f"Error: {e}")
        return output

    driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
