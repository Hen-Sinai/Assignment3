import requests

base_url = 'http://localhost:8000'
DC = {}
MC = {}

# 1
def test_create_dishes():
    dish_names = ["orange", "spaghetti", "apple pie"]

    for name in dish_names:
        response = requests.post(base_url + '/dishes', json={"name": name})
        assert response.status_code == 201
        dish_id = response.text.strip('"')
        assert dish_id not in DC
        DC[name] = dish_id

    assert len(DC) == len(dish_names)

# 2
def test_get_orange_dish():
    assert "orange" in DC  # Ensure dishes have been created before running this test
    dish_id = DC["orange"]

    response = requests.get(base_url + f'/dishes/{dish_id}')
    assert response.status_code == 200
    dish_data = response.json()
    assert 'sodium' in dish_data

    sodium = dish_data['sodium']
    assert 0.9 < sodium < 1.1

# 3
def test_get_all_dishes():
    response = requests.get(base_url + '/dishes')
    assert response.status_code == 200
    dishes_data = response.json()
    assert len(dishes_data) == 3

# 4
def test_create_existing_dish():
    response = requests.post(base_url + '/dishes', json={"name": "blah"})
    assert response.status_code == 400
    return_value = response.json()
    assert return_value != -3

# 5
def test_create_existing_dish():
    response = requests.post(base_url + '/dishes', json={"name": "orange"})
    assert response.status_code == 400
    return_value = response.json()
    assert return_value != -2

# 6
def test_create_meal():
    assert len(DC) > 0  # Ensure dishes have been created before running this test

    appetizer_id = DC["orange"]
    main_id = DC["spaghetti"]
    dessert_id = DC["apple pie"]

    response = requests.post(base_url + '/meals', json={
        "name": "delicious",
        "appetizer": appetizer_id,
        "main": main_id,
        "dessert": dessert_id
    })

    assert response.status_code == 201
    meal_id = response.json()
    assert meal_id <= 0
    MC["delicious"] = meal_id

# 7
def test_get_all_meals():
    response = requests.get(base_url + '/meals')
    assert response.status_code == 200
    meals_data = response.json()
    assert len(meals_data) == 1
    meal = meals_data[0]
    assert 400 < meal["calories"] < 500

# 8
def test_create_existing_meal():
    assert "delicious" in MC  # Ensure "delicious" meal has been created before running this test

    appetizer_id = DC["orange"]
    main_id = DC["spaghetti"]
    dessert_id = DC["apple pie"]

    response = requests.post(base_url + '/meals', json={
        "name": "delicious",
        "appetizer": appetizer_id,
        "main": main_id,
        "dessert": dessert_id
    })

    assert response.status_code == 400
    return_value = response.json()
    assert return_value != -2
