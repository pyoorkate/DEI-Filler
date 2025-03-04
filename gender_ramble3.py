import random
import csv
import os
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Word lists for incoherent rambling
subjects = ["Gender", "Pronouns", "Identity", "Society", "The patriarchy", "The binary", "The spectrum", "The void"]
verbs = ["is", "was", "will be", "could be", "might be", "should be", "must be", "isn't"]
adjectives = ["fluid", "rigid", "confusing", "liberating", "oppressive", "revolutionary", "nonexistent", "eternal"]
nouns = ["construct", "illusion", "reality", "dream", "nightmare", "journey", "destination", "paradox"]
connectors = ["because", "but", "however", "therefore", "meanwhile", "although", "unless", "since"]
random_phrases = ["like a cosmic joke", "in a sea of uncertainty", "on the edge of chaos", "in the shadow of the moon", "under the weight of expectations"]

# Word lists for vague complaints about diversity and equity
complaint_subjects = ["Diversity initiatives", "Equity programs", "The HR department", "Corporate policies", "The woke agenda", "Modern workplaces", "Inclusion efforts", "Social justice warriors"]
complaint_verbs = ["are", "were", "have become", "seem to be", "feel like", "are turning into", "are ruining", "are overshadowing"]
complaint_adjectives = ["overbearing", "misguided", "hypocritical", "excessive", "unfair", "divisive", "counterproductive", "performative"]
complaint_nouns = ["a checkbox exercise", "a waste of resources", "a source of resentment", "a distraction", "a political tool", "a band-aid solution", "a double standard", "a lost cause"]
complaint_phrases = ["without addressing the real issues", "while ignoring the root causes", "at the expense of common sense", "while alienating everyone", "without considering the consequences", "while creating more problems", "while pretending to care", "while making things worse"]

def load_school_districts(filename):
    districts = []
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            districts.append({"name": row[0], "zip": row[1], "email": f"info@{row[0].replace(' ', '').lower()}.org"})
    return districts

def generate_sentence():
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    connector = random.choice(connectors)
    phrase = random.choice(random_phrases)
    
    sentence = f"{subject} {verb} {adjective} {noun}, {connector} it's {phrase}."
    return sentence

def generate_paragraph():
    paragraph = ""
    for _ in range(random.randint(3, 6)):  # Each paragraph has 3-6 sentences
        paragraph += generate_sentence() + " "
    return paragraph.strip()

def generate_complaint_sentence():
    subject = random.choice(complaint_subjects)
    verb = random.choice(complaint_verbs)
    adjective = random.choice(complaint_adjectives)
    noun = random.choice(complaint_nouns)
    phrase = random.choice(complaint_phrases)
    
    sentence = f"{subject} {verb} {adjective} {noun}, {phrase}."
    return sentence

def generate_complaints_text(word_count=400):
    complaints = ""
    while len(complaints.split()) < word_count:
        sentence = generate_complaint_sentence()
        complaints += sentence + " "
    return complaints.strip()

def get_random_school_district(districts):
    return random.choice(districts)

def generate_pdf(target_size_mb, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    target_size_bytes = target_size_mb * 1024 * 1024  # Convert MB to bytes
    estimated_size_bytes = 0

    # Estimate size based on average paragraph size
    avg_paragraph_size = 500  # Approximate size of a paragraph in bytes
    while estimated_size_bytes < target_size_bytes:
        paragraph = generate_paragraph()
        pdf.multi_cell(0, 10, paragraph)  # Add paragraph to PDF
        pdf.ln(10)  # Add space between paragraphs
        estimated_size_bytes += avg_paragraph_size

    # Save the final PDF
    pdf.output(filename)
    print(f"PDF '{filename}' created with size approximately {target_size_mb} MB.")

def save_complaints_to_file(filename, word_count=400):
    # Load school districts from CSV
    districts = load_school_districts("school_districts_with_random_zipcodes.csv")

    # Get a random school district
    district = get_random_school_district(districts)

    # Generate complaints text
    complaints = generate_complaints_text(word_count)

    # Save to file (without district info)
    with open(filename, "w") as file:
        file.write(complaints)
    print(f"Complaints text saved to '{filename}'.")

    # Return the district name for PDF naming
    return district

def submit_form(district, complaints_text, pdf_filename):
    # Set up Selenium WebDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    service = Service(executable_path="/opt/homebrew/bin/chromedriver")  # Replace with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the form URL
        driver.get("https://enddei.ed.gov/")

        # Wait for the form to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "tipsForm"))
        )

        # Fill out the form
        # Email
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(district["email"])

        # School or school district
        school_field = driver.find_element(By.ID, "location")
        school_field.send_keys(district["name"])

        # ZIP Code
        zip_field = driver.find_element(By.ID, "zipcode")
        zip_field.send_keys(district["zip"])

        # Description
        description_field = driver.find_element(By.ID, "description")
        description_field.send_keys(complaints_text)

        # Attach the PDF file
        file_input = driver.find_element(By.ID, "file")
        absolute_pdf_path = os.path.abspath(pdf_filename)  # Convert to absolute path
        file_input.send_keys(absolute_pdf_path)  # Provide the full absolute path to the PDF file

        # Scroll the submit button into view
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "submitButton"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

        # Add a small delay to ensure the button is fully visible
        time.sleep(1)

        # Use JavaScript to click the button (bypassing potential overlays)
        driver.execute_script("arguments[0].click();", submit_button)

        # Wait for submission to complete
        WebDriverWait(driver, 20).until(
            EC.url_changes(driver.current_url)
        )
        print("Form submitted successfully!")
    except Exception as e:
        print(f"An error occurred while submitting the form: {e}")
    finally:
        driver.quit()

# Main program
if __name__ == "__main__":
    # Define the target file size in MB (9 MB)
    target_size_mb = 9

    # Generate text file with vague complaints about diversity and equity
    complaints_filename = "diversity_equity_complaints.txt"
    district = save_complaints_to_file(complaints_filename, word_count=400)

    # Generate PDF with incoherent gender rambling
    # Modify the PDF filename to match the school district name (without "gender_rambling")
    pdf_filename = f"{district['name'].replace(' ', '_')}.pdf"
    generate_pdf(target_size_mb, pdf_filename)

    # Submit the form with the generated data and attach the PDF
    with open(complaints_filename, "r") as file:
        complaints_text = file.read()
    submit_form(district, complaints_text, pdf_filename)

    print("All files generated and form submitted successfully.")
