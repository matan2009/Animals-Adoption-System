import requests

# url = 'http://localhost:5000/signup'
# response = requests.post(url, json={"username": "my_usr", "password": "my_pass", "auth_password": "my_pass"})
# print(response.status_code)
# print(response.text)


url = 'http://localhost:5000/login'
response = requests.post(url, json={"username": "my_usr", "password": "my_pass"})
print(response.status_code)
print(response.text)
token = response.text

url = 'http://localhost:5000/animal_for_adoption'
response = requests.post(url, json={"category": "dog", "age": 3, "weight": 20, "owner_name": "Israel Israeli",
                                    "owner_phone_number": "1234567890"},
                         headers={"Authorization": "Bearer {}".format(token)})
print(response.status_code)
print(response.text)

