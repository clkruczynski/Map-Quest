import urllib.parse
import requests

# Simple user authentication system
users = {}
user_preferences = {}  # To store traffic preferences per user

def register(username, password):
    if username in users:
        return 'Username already exists. Please choose another one.'
    else:
        users[username] = password
        return 'Registration successful!'

def login(username, password):
    if username in users and users[username] == password:
        return f'Login successful! Welcome, {username}!'
    else:
        return 'Invalid username or password.'

def validate_location(location):
    if not location.strip():
        print("Location cannot be empty. Please try again.")
        return False
    return True

def get_weather(location):
    # OpenWeatherMap API key and URL
    weather_api_key = "bd5e378503939ddaee76f12ad7a97608"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"

    try:
        response = requests.get(weather_url)
        data = response.json()

        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            if "rain" in weather_description.lower():
                return f"Weather at {location}: {weather_description}. It looks like it's raining."
            else:
                return f"Weather at {location}: {weather_description}. No rain expected."
        else:
            return f"Unable to fetch weather for {location}. Please try again later."
    except Exception as e:
        return f"Error getting weather data: {e}"

def get_user_preference(username, change_preferences=False):
    if username in user_preferences and not change_preferences:
        print(f"\nYour saved traffic preference is: {user_preferences[username]}")
        use_saved = input("Do you want to use this preference? (yes/no): ").lower()
        if use_saved == 'yes':
            return user_preferences[username]

    print("\nSet Traffic Preferences:")
    print("1. Fastest Route")
    print("2. Shortest Distance")
    preference = input("Choose your preference (1/2): ")

    if preference == '1':
        user_preferences[username] = {"routeType": "fastest"}
    elif preference == '2':
        user_preferences[username] = {"routeType": "shortest"}
    else:
        print("Invalid preference. Defaulting to fastest route.")
        user_preferences[username] = {"routeType": "fastest"}

    return user_preferences[username]


def route_finder(username):
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = "wMz7DsbJzW5VjP5iOmrXqKMrOISKfgaY"

    while True:
        print("\n=== ROUTE FINDER ===")
        while True:
            orig = input("Starting Location: ")
            if validate_location(orig):
                break

        while True:
            dest = input("Destination: ")
            if validate_location(dest):
                break

        # Check weather at destination
        print(f"\nChecking weather at your destination: {dest}")
        weather_result = get_weather(dest)
        print(weather_result)

        # Check and allow changing user preferences
        print("\nTraffic Preferences Options:")
        print("1. Use Current Preferences")
        print("2. Update Preferences")
        pref_choice = input("Choose your option (1/2): ")

        if pref_choice == '2':
            preference = get_user_preference(username, change_preferences=True)
        else:
            preference = get_user_preference(username)

        route_type = preference["routeType"]

        # Building the URL with route type
        url_params = {
            "key": key,
            "from": orig,
            "to": dest,
            "routeType": route_type
        }

        # Make the API request
        url = main_api + urllib.parse.urlencode(url_params)
        print("\nFetching route...")
        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]

        if json_status == 0:
            print("\nAPI Status: " + str(json_status) + " = A successful route call.")
            print("=============================================")
            print("Directions from " + orig + " to " + dest)
            print("Trip Duration:   " + json_data["route"]["formattedTime"])

            # Accurate kilometers conversion
            kilometers = json_data["route"]["distance"] * 1.60934
            print("Kilometers:      " + str("{:.2f}".format(kilometers)))
            print("=============================================")

            for each in json_data["route"]["legs"][0]["maneuvers"]:
                maneuver_km = each["distance"] * 1.60934
                print(each["narrative"] + " (" + str("{:.2f}".format(maneuver_km)) + " km)")

            print("=============================================\n")

            # Ask if the user wants to find another route
            while True:
                choice = input("Do you want to find another route? (yes/no): ").lower()
                if choice == "yes":
                    break
                elif choice == "no":
                    print("Returning to the main menu...\n")
                    return
                else:
                    print("Invalid choice. Please enter 'yes' or 'no'.")

        elif json_status == 402:
            print("\nStatus Code: " + str(json_status) + "; Invalid user inputs for one or both locations.\n")
        elif json_status == 611:
            print("\nStatus Code: " + str(json_status) + "; Missing an entry for one or both locations.\n")
        else:
            print("\nFor Status Code: " + str(json_status) + "; Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes\n")

def main():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            result = register(username, password)
            print(result)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            result = login(username, password)
            print(result)
            if "Login successful" in result:
                route_finder(username)
        elif choice == '3':
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
