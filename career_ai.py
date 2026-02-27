import requests

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False


def get_user_data():
    name = input("Enter your name: ")
    interests = input("Enter your interests (comma separated): ")
    skills = input("Enter your skills (comma separated): ")
    subjects = input("Enter your subjects (comma separated): ")

    query = interests + " " + skills + " " + subjects
    return name, query


def search_jobs(query):
    print("\nSearching real job data from internet...\n")

    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY",  # Replace with your key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "num_pages": "1"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        print("Error fetching job data")
        return []


def show_results(name, jobs):
    print(f"\nHi {name}! Based on your profile, here are career options:\n")

    if not jobs:
        print("No jobs found. Try different skills.")
        return

    shown = set()

    for job in jobs[:10]:
        title = job.get("job_title", "Unknown")
        company = job.get("employer_name", "Unknown")

        if title not in shown:
            print(f"• {title} at {company}")
            shown.add(title)


# Main program
if __name__ == "__main__":
    print("=== AI Career Recommendation Tool ===")

    if not check_internet():
        print("No internet connection.")
    else:
        name, query = get_user_data()
        jobs = search_jobs(query)
        show_results(name, jobs)
