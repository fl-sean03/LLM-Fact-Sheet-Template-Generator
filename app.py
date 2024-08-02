from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Load the fact sheet template
with open('factsheet_template.txt', 'r') as file:
    FACTSHEET_TEMPLATE = file.read()

api_key = #Insert your OpenAI API Key Here

client = OpenAI(
  api_key=api_key,
  )

def generate_fact_sheet(technology, template):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate a fact sheet, in a pretty html format, for the following technology based on the template:\n\nTemplate:\n{template}\n\nTechnology: {technology}\n\nFact Sheet:"}
        ]
    )
    return response.choices[0].message.content  

@app.route('/')
def index():
    return render_template('index.html', template=FACTSHEET_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    technology = request.form['technology']
    template = request.form['template']
    import re
    fact_sheet = generate_fact_sheet(technology, template).replace("```html", "").replace("```", "")
    fact_sheet = re.sub(r'\s+', ' ', fact_sheet).strip()

    return jsonify({'fact_sheet': fact_sheet})

if __name__ == '__main__':
    app.run(debug=True)
