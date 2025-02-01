import requests
import sys

# api manager - can update the website via api calls with the right api key - designed to be used in commandline tool - probably would be better with a UI

API_KEY = 'tomspeed'
BASE_URL = 'http://localhost:8095'

def update_slots(new_slots):
    url = f'{BASE_URL}/update_slots'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {'available_slots': new_slots}
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully updated slots to {new_slots}')
        else:
            print(f'Failed to update slots: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print(f'Failed to update slots: Invalid response from server')

def update_pricing(plan, price):
    url = f'{BASE_URL}/update_pricing'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {'plan': plan, 'price': price}
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully updated pricing for {plan} to ${price}')
        else:
            print(f'Failed to update pricing: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print(f'Failed to update pricing: Invalid response from server')

def update_xp_gained(xp_gained):
    url = f'{BASE_URL}/update_xp_gained'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {'xp_gained': xp_gained}
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully updated XP gained to {xp_gained}')
        else:
            print(f'Failed to update XP: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print('Failed to update XP: Invalid response from server')

def update_hours_botted(hours_botted):
    url = f'{BASE_URL}/update_hours_botted'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {'hours_botted': hours_botted}
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully updated hours botted to {hours_botted}')
        else:
            print(f'Failed to update hours: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print('Failed to update hours: Invalid response from server')

def add_offering():
    print("\nAdd Offering")
    tag = input("Enter the tag (e.g., Skilling, Combat, etc.): ")
    image = input("Enter the image filename (e.g., script.png): ")
    title = input("Enter the title: ")
    description = input("Enter the description: ")
    image_path = f'/images/{image}'
    url = f'{BASE_URL}/add_offering'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {'tag': tag, 'image': image_path, 'title': title, 'description': description}
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully added offering with ID {response_data.get("id")}')
        else:
            print(f'Failed to add offering: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print('Failed to add offering: Invalid response from server')

def list_offerings():
    url = f'{BASE_URL}/offerings'
    try:
        response = requests.get(url)
        if not response.content.strip():
            print("No response received from server.")
            return []
        data = response.json()
        if 'error' in data:
            print(f"Server error: {data['error']}")
            return []
        offerings = data.get('offerings', [])
        if not offerings:
            print("No offerings found.")
            return []
        print("\nOfferings:")
        for offering in offerings:
            oid, tag, image, title, description = offering
            print(f"ID: {oid} - Title: {title} - Tag: {tag} - Image: {image} - Description: {description}")
        return offerings
    except Exception as e:
        print(f"Error fetching offerings: {e}\nResponse: {response.text if 'response' in locals() else 'No response'}")
        return []

def remove_offering():
    print("\nRemove Offering")
    offerings = list_offerings()
    if not offerings:
        return
    offering_id = input("Enter the ID of the offering to remove: ")
    url = f'{BASE_URL}/remove_offering'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {'id': offering_id}
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully removed offering with ID {response_data.get("removed_id")}')
        else:
            print(f'Failed to remove offering: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print('Failed to remove offering: Invalid response from server')

def edit_offering():
    print("\nEdit Offering")
    offerings = list_offerings()
    if not offerings:
        return
    offering_id = input("Enter the ID of the offering to edit: ")
    tag = input("Enter the new tag: ")
    image = input("Enter the new image filename: ")
    title = input("Enter the new title: ")
    description = input("Enter the new description: ")
    image_path = f'/images/{image}'
    url = f'{BASE_URL}/edit_offering'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {
        'id': offering_id,
        'tag': tag,
        'image': image_path,
        'title': title,
        'description': description
    }
    response = requests.post(url, json=data, headers=headers)
    try:
        response_data = response.json()
        if response.status_code == 200:
            print(f'Successfully edited offering with ID {response_data.get("edited_id")}')
        else:
            print(f'Failed to edit offering: {response_data}')
    except requests.exceptions.JSONDecodeError:
        print('Failed to edit offering: Invalid response from server')

def update_offerings_menu():
    while True:
        print("\nUpdate Offerings Menu")
        print("1. Add Offering")
        print("2. Remove Offering")
        print("3. Edit Offering")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_offering()
        elif choice == '2':
            remove_offering()
        elif choice == '3':
            edit_offering()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Update Slots/Status")
        print("2. Update Pricing")
        print("3. Update Offerings")
        print("4. Update XP Gained")
        print("5. Update Hours Botted")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_input = input("Enter the number of available slots or type 'maintenance': ")
            if new_input.strip().lower() == 'maintenance':
                update_slots("maintenance")
            else:
                try:
                    new_slots = int(new_input)
                    update_slots(new_slots)
                except ValueError:
                    print("Invalid input. Please enter a number or 'maintenance'.")
        elif choice == '2':
            print("\nUpdate Pricing")
            print("1. Monthly")
            print("2. 3 Months")
            print("3. Lifetime")
            tier_choice = input("Enter the tier to update: ")
            if tier_choice == '1':
                plan = "1 Month"
            elif tier_choice == '2':
                plan = "3 Months"
            elif tier_choice == '3':
                plan = "Lifetime"
            else:
                print("Invalid choice")
                continue
            price = int(input(f"Enter the new price for {plan}: "))
            update_pricing(plan, price)
        elif choice == '3':
            update_offerings_menu()
        elif choice == '4':
            xp_gained = int(input("Enter the new XP gained: "))
            update_xp_gained(xp_gained)
        elif choice == '5':
            hours_botted = int(input("Enter the new hours botted: "))
            update_hours_botted(hours_botted)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main_menu()
