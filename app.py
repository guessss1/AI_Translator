from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Настройка OpenAI API
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

STYLE_PROMPTS = {
    'formal': "Переведите следующий текст формальным, профессиональным языком:",
    'informal': "Переведите следующий текст разговорным, повседневным языком:",
    'business_email': "Переведите следующий текст в формате делового письма с соответствующим приветствием и завершением:",
    'flirty': "Переведите следующий текст игривым, дружелюбным тоном:"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text')
        source_lang = data.get('source_lang')
        target_lang = data.get('target_lang')
        style = data.get('style')

        if not all([text, source_lang, target_lang, style]):
            return jsonify({'error': 'Missing required parameters'}), 400

        prompt = f"{STYLE_PROMPTS[style]}\n\nТекст: {text}\n\nПереведите с {source_lang} на {target_lang}."

        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "Вы - профессиональный переводчик."},
                {"role": "user", "content": prompt}
            ]
        )

        translated_text = response.choices[0].message.content

        return jsonify({'translation': translated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)