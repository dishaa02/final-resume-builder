from flask import Flask, request
import docx2txt
import enchant

app = Flask(__name__)

# Initialize Enchant dictionary for English
english_dict = enchant.Dict("en_US")

def check_grammar(text):
    """Check grammar in the given text."""
    errors = []
    words = text.split()
    for word in words:
        if not english_dict.check(word):
            errors.append(word)
    return errors

@app.route('/')
def upload_file():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume Grammar and Document Correction</title>
    </head>
    <body>
        <div class="container">
            <h1>Check Grammar and Document Correction</h1>
            <div class="upload-box">
                <i class="icon fas fa-file-word"></i><br>
                <form action="/check_grammar" method="post" enctype="multipart/form-data">
                    <label for="resume-file" class="file-input-label">Choose File</label>
                    <input type="file" id="resume-file" name="resume" accept=".docx"><br>
                    <button class="button" type="submit">Check Grammar</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/check_grammar', methods=['POST'])
def check_grammar_route():
    if 'resume' not in request.files:
        return "Please upload a resume file."

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return "Please select a resume file."

    resume_text = docx2txt.process(resume_file)
    grammar_errors = check_grammar(resume_text)

    if grammar_errors:
        return f"Grammar errors found: {', '.join(grammar_errors)}"
    else:
        return "No grammar errors found."

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Change the port number as needed
