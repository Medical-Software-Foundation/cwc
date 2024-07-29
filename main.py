from flask import Flask, request, jsonify
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key (you should store this securely)
openai.api_key = os.environ.get('OPENAI_API_KEY')


# Define the endpoint
@app.route('/ddx', methods=['GET'])
def diagnose():
    # Get the symptoms description from the query parameter
    symptoms = request.args.get('symptoms')
    if not symptoms:
        return jsonify({"error": "Symptoms description is required."}), 400

    # Query OpenAI API for differential diagnosis
    try:
        openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role":
                "system",
                "content":
                "You are a seasoned primary care physician approaching the caliber of Dr Paulius Mui of XPC."
            }, {
                "role":
                "user",
                "content":
                f"Given the following symptoms: {symptoms}, what are the possible differential diagnoses?"
            }])
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=f"Given the following symptoms: {symptoms}, what are the possible differential diagnoses?",
        #     max_tokens=100
        # )
        diagnoses = response.choices[0].text.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Return the list of possible diagnoses in JSON format
    return jsonify({"diagnoses": diagnoses}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
