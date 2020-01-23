import connexion
import requests
from connexion import NoContent

STORE_SERVICE_ITEM_URL = "http://localhost:8090/items"
STORE_SERVICE_WISHLIST_ITEM_URL = "http://localhost:8090/wishlistItems"
HEADERS = { "content-type": "application/json"}

def addItem(body):
    response = requests.post(STORE_SERVICE_ITEM_URL, json=body, headers=HEADERS)
    return NoContent, response.status_code

# def updateItem(body):
#     print(body)
#     return 'Successful!', 200

def addWishListItem(body):
    response = requests.post(STORE_SERVICE_WISHLIST_ITEM_URL, json=body, headers=HEADERS)
    return NoContent, response.status_code

# def updateWishlistItem(body):
#     print(body)
#     return 'Successful!', 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)