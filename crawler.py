import requests
from bs4 import BeautifulSoup
import pandas as pd

domain_url = "https://careerguidance.unilearn.org.in/domain/"
career_url_base = "https://careerguidance.unilearn.org.in/career/"
parameters = [
    "bfsi", "defence", "design", "education", "engineering", "fine-arts",
    "fisheries", "general", "government", "health-wellness", "hospitality-tourism",
    "it", "language", "legal", "logistics", "management", "media", "science",
    "social-studies", "sports", "vocational"
]

def fetch_career_details(url):
    print(f"Fetching career details from URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to fetch details for {url} (status code: {response.status_code})"
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("article")
    details = ""
    for article in articles:
        details += article.text.strip() + "\n\n"
    return details.strip()

def fetch_career_links(url):
    print(f"Fetching career links from URL: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page for {url} (status code: {response.status_code})")
        return {}
    soup = BeautifulSoup(response.text, 'html.parser')
    career_links = {}
    for h2_tag in soup.find_all("h2"):
        link = h2_tag.find("a")
        if link:
            career_name = link.text.strip().replace(" ", "-").lower()  # Format career name
            career_links[link.text.strip()] = career_name
    return career_links

def extract_info(details):
    sections = [
        "NCS Code", "Personal Competencies", "Entry Pathway",
        "Where will you study?", "Fees, Scholarships & Loans", "Where will you work?",
        "Expected Income"
    ]
    extracted_info = {}
    current_section = None
    for line in details.split("\n"):
        if line.strip() in sections:
            current_section = line.strip()
        elif current_section:
            if current_section not in extracted_info:
                extracted_info[current_section] = ""
            extracted_info[current_section] += line.strip() + "\n"
    return extracted_info

def main():
    careers_data = []
    for parameter in parameters:
        url = domain_url + parameter
        print(f"Fetching career links for: {parameter}")
        career_links = fetch_career_links(url)
        if career_links:
            print(f"Found {len(career_links)} careers:")
            for career, career_name in career_links.items():
                career_url = career_url_base + career_name
                print(f"Career: {career}")
                print(f"URL: {career_url}")
                print("Fetching details...")
                career_details = fetch_career_details(career_url)
                print("Details:")
                print(career_details)
                print("-" * 50)
                extracted_info = extract_info(career_details)
                extracted_info["Career Name"] = career
                careers_data.append(extracted_info)
        else:
            print(f"No career links found for {parameter}")
        print("=" * 50)

    # Creating DataFrame from extracted data
    df = pd.DataFrame(careers_data)

    # Writing DataFrame to Excel file
    excel_filename = "career_details.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Career details have been saved to '{excel_filename}'.")

if __name__ == "__main__":
    main()
