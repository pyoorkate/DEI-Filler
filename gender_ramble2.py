import random
from fpdf import FPDF

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

# Sample data for school districts in Republican states
school_districts = [
    {"name": "Lubbock Independent School District", "zip": "79401", "email": "info@lubbockisd.org"},
    {"name": "Tulsa Public Schools", "zip": "74103", "email": "contact@tulsaschools.org"},
    {"name": "Gilbert Public Schools", "zip": "85234", "email": "support@gilbertschools.net"},
    {"name": "Hamilton County Schools", "zip": "37402", "email": "info@hcde.org"},
    {"name": "Williamson County Schools", "zip": "37064", "email": "contact@wcs.edu"},
    {"name": "Forsyth County Schools", "zip": "30040", "email": "help@forsyth.k12.ga.us"},
    {"name": "Collier County Public Schools", "zip": "34102", "email": "info@collierschools.com"},
    {"name": "Greenville County Schools", "zip": "29601", "email": "support@greenville.k12.sc.us"},
    {"name": "Knox County Schools", "zip": "37902", "email": "contact@knoxschools.org"},
    {"name": "Montgomery Public Schools", "zip": "36104", "email": "info@mps.k12.al.us"},
]

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

def get_random_school_district():
    return random.choice(school_districts)

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
    # Get a random school district
    district = get_random_school_district()
    district_info = f"School District: {district['name']}\nZip Code: {district['zip']}\nEmail: {district['email']}\n\n"

    # Generate complaints text
    complaints = generate_complaints_text(word_count)

    # Combine district info and complaints
    full_text = district_info + complaints

    # Save to file
    with open(filename, "w") as file:
        file.write(full_text)
    print(f"Complaints text saved to '{filename}'.")

# Main program
if __name__ == "__main__":
    # Define the target file size in MB (9 MB)
    target_size_mb = 9

    # Define the output filenames
    pdf_filename = "gender_rambling.pdf"
    complaints_filename = "diversity_equity_complaints.txt"

    # Generate PDF with incoherent gender rambling
    generate_pdf(target_size_mb, pdf_filename)

    # Generate text file with vague complaints about diversity and equity
    save_complaints_to_file(complaints_filename, word_count=400)

    print("All files generated successfully.")