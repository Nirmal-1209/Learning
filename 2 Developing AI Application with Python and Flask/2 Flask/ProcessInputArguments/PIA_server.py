from flask import Flask, make_response, request

app = Flask(__name__)

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]


@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message" : f"Data of length {len(data)} found"}
        else:
            return {"message" : "Data is empty"}, 500
    except NameError:
        return {"message" : "Data not Found"}, 404


@app.route("/name_search")
def name_search():
    """Find a person in the database.

    Returns:
        json: Person if found, with status of 200
        404: If not found
        400: If argument 'q' is missing
        422: If argument 'q' is present but invalid
    """
    # Get the argument 'q' from the query parameters of the request
    query = request.args.get('q')

    # Check if the query parameter 'q' is missing
    if query is None:
        return {"message": "Query parameter 'q' is missing"}, 400

    # Check if the query parameter is present but invalid (e.g., empty or numeric)
    if query.strip() == "" or query.isdigit():
        return {"message": "Invalid input parameter"}, 422

    # Iterate through the 'data' list to look for the person whose first name matches the query
    for person in data:
        if query.lower() in person["first_name"].lower():
            # If a match is found, return the person as a JSON response with a 200 OK status code
            return person, 200

    # If no match is found, return a JSON response with a message indicating the person was not found and a 404 Not Found status code
    return {"message": "Person not found"}, 404



# @app.get("/count")
@app.route("/count", methods=['GET'])
def count():
    try:
        if data and len(data) > 0 :
            return {"data count " : len(data)}, 200
        else:
            return {"message":"data is empty"}, 500
    except NameError:
        return {"message" : "data not found"}, 404


@app.route("/person/<unique_identifier>", methods=['GET'])
def find_by_uuid(unique_identifier):
    for person in data:
        if person["id"] == str(unique_identifier):
            return person, 200
    return {"message" : "Person not found"}, 404


@app.route("/person/<uuid:unique_identifier>", methods=['DELETE'])
def delete_person(unique_identifier):
    for person in data:
        if person["id"] == str(unique_identifier):
            # Remove the person from the data list
            data.remove(person)
            # Return a JSON response with a message and HTTP status code 200 (OK)
            return {"message": "Person with ID deleted"}, 200
    # If no person with the given ID is found, return a JSON response with a message and HTTP status code 404 (Not Found)
    return {"message": "Person not found"}, 404


@app.route("/person", methods=['POST'])
def add_by_uuid():
    # Get the JSON data from the incoming request
    new_person = request.get_json()

    # Check if the JSON data is empty or None
    if not new_person:
        # Return a JSON response indicating that the request data is invalid
        # with a status code of 422 (Unprocessable Entity)
        return {"message" : "Invalid input, no data provided"}, 422
    
    # Proceed with further processing of 'new_person', such as adding it to a database
    # or validating its contents before saving it
    try:
        data.append(new_person)
    except NameError:
        return {"message":"Data not defined"}, 500
    
    # Assuming the processing is successful, return a success message with status code 200 (Created)
    return {"message": f"Person with id {new_person['id']} added"}, 200


@app.errorhandler(404)
def api_not_found(error):
    # This function is a custom error handler for 404 Not Found errors
    # It is triggered whenever a 404 error occurs within the Flask application
    return{"message" : "API not found"}, 404


# This tells Flask to catch any unhandled Exception raised anywhere in your app and route it to this handler, returning a 500 Internal Server Error response with the error message.
@app.errorhandler(Exception)
def handle_exception(e):
    return {"message": str(e)}, 500



# curl -X POST -i -w '\n' \
#   --url http://localhost:5000/person \
#   --header 'Content-Type: application/json' \
#   --data '{
#         "id": "4e1e61b4-8a27-11ed-a1eb-0242ac120002",
#         "first_name": "John",
#         "last_name": "Horne",
#         "graduation_year": 2001,
#         "address": "1 hill drive",
#         "city": "Atlanta",
#         "zip": "30339",
#         "country": "United States",
#         "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff"
# }'

# You can also test the case where you send an empty JSON to the enpoint by using the following command:
# curl -X POST -i -w '\n' \
#   --url http://localhost:5000/person \
#   --header 'Content-Type: application/json' \
#   --data '{}'