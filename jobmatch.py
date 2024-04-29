from flask import Flask, request, redirect, url_for
import docx2txt
from difflib import SequenceMatcher
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Download NLTK resources (only needed once)
nltk.download('stopwords')
nltk.download('punkt')

def preprocess_text(text):
    """Preprocess text by removing punctuation and stopwords, and converting to lowercase."""
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def calculate_similarity(text1, text2):
    """Calculate similarity percentage between two preprocessed texts."""
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)
    matcher = SequenceMatcher(None, preprocessed_text1, preprocessed_text2)
    similarity_ratio = matcher.ratio()
    similarity_percentage = round(similarity_ratio * 100, 2)
    return similarity_percentage

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # If it's a POST request, redirect to the '/match' route
        return redirect(url_for('match_resume'))
    else:
        # If it's a GET request, serve the HTML form
        return '''
               <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Description Matching</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        background-image: url(images/hero-bg.png);
    }
    .container {
        width: 80%;
        margin: 50px auto;
        text-align: center;
    }
    .box {
        display: inline-block;
        width: 45%;
        padding: 20px;
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
        margin-bottom: 20px;
    }
    .box h2 {
        color: #007bff;
        margin-bottom: 20px;
    }
    .button {
        padding: 10px 20px;
        font-size: 16px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .button:hover {
        background-color: #0056b3;
    }
    /* Hide the default file input button */
    input[type="file"] {
        display: none;
    }
    /* Style the custom upload button */
    .upload-button {
        padding: 10px 20px;
        font-size: 16px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .upload-button:hover {
        background-color: #0056b3;
    }
    h2{
        color:black
    }
</style>
</head>
<body>

<div class="container">
    <h2>Job Description Matching</h2>
    <form action="/match" method="post" enctype="multipart/form-data">
        <div class="box">
            <h2>Submit Your Resume</h2>
            <label for="resume-upload" class="upload-button">Upload Resume</label>
            <input type="file" id="resume-upload" name="resume" accept=".docx">
            <span id="resume-file-name" class="file-name"></span> <!-- Add this span for displaying file name -->
        </div>
        <div class="box">
            <h2>Submit Your Job Description</h2>
            <label for="job-description-upload" class="upload-button">Upload Job Description</label>
            <input type="file" id="job-description-upload" name="job_description" accept=".docx">
            <span id="job-description-file-name" class="file-name"></span> <!-- Add this span for displaying file name -->
        </div>
        <button class="button" type="submit">Match Your Resume</button>
    </form>
</div>

<script>
document.getElementById('resume-upload').addEventListener('change', function() {
    document.getElementById('resume-file-name').textContent = this.files[0] ? this.files[0].name : 'No file chosen';
});

document.getElementById('job-description-upload').addEventListener('change', function() {
    document.getElementById('job-description-file-name').textContent = this.files[0] ? this.files[0].name : 'No file chosen';
});
</script>

</body>
</html>

        '''


@app.route('/match', methods=['POST'])
def match_resume():
    if 'resume' not in request.files or 'job_description' not in request.files:
        return "Please upload both resume and job description files."

    resume_file = request.files['resume']
    job_description_file = request.files['job_description']

    if resume_file.filename == '' or job_description_file.filename == '':
        return "Please select both resume and job description files."

    resume_text = docx2txt.process(resume_file)
    job_description_text = docx2txt.process(job_description_file)

    similarity_percentage = calculate_similarity(resume_text, job_description_text)

    return f"Similarity Percentage: {similarity_percentage:.2f}%"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

