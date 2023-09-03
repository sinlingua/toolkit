import os
from flask import Flask, render_template, request, jsonify
from sinlingua.singlish.rulebased_transliterator import RuleBasedTransliterator
from sinlingua.grammar_rule.grammar_main import GrammarMain
# from sinlingua.summarizer.faster_longformer import FLongformerTextSummarizer
from sinlingua.sinhala_audio.audio_to_text import conversion
from flaskwebgui import FlaskUI, close_application

app = Flask(__name__, template_folder="templates")
# ui = FlaskUI(app, width=800, height=500)


@app.route('/', methods=['GET', 'POST'])
def index():
    processed_result = None

    if request.method == 'POST':
        input_text = request.form.get('input_text')
        audio_input = request.files.get('audio_input')

        if input_text:
            # Perform text processing on input_text
            processed_result = f"Processed: {input_text}"  # Example text processing
        elif audio_input:
            # Perform audio processing
            processed_result = "Audio Collected"

    return render_template('index.html', processed_result=processed_result)


@app.route('/singlish', methods=['GET', 'POST'])
def singlish():
    return render_template('singlish.html')


@app.route('/grammar', methods=['GET', 'POST'])
def grammar():
    return render_template('grammar.html')


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    return render_template('summarize.html')


@app.route("/close", methods=["GET"])
def close_window():
    close_application()


@app.route('/process', methods=['POST'])
def process():
    input_text, audio_input = None, None
    checkbox1, checkbox2, checkbox3, checkbox4 = None, None, None, None

    input_text = request.form.get('input_text')
    audio_input = request.files.get('audio_input')

    checkbox1 = request.form.get('checkbox1') == 'true'
    checkbox2 = request.form.get('checkbox2') == 'true'
    checkbox3 = request.form.get('checkbox3') == 'true'
    checkbox4 = request.form.get('checkbox4') == 'true'

    if input_text and checkbox1:
        obj = RuleBasedTransliterator()
        # Perform text processing on input_text
        out = obj.transliterator(text=input_text)
        processed_result = f"{out}"  # Example text processing
    elif audio_input and checkbox2:
        # Save the uploaded file to a specific directory
        upload_dir = 'src'
        os.makedirs(upload_dir, exist_ok=True)
        audio_path = os.path.join(upload_dir, audio_input.filename)
        audio_input.save(audio_path)
        # Perform audio processing
        out = conversion(path=audio_path)
        processed_result = f"{out}"
    else:
        processed_result = input_text

    if checkbox3:
        obj2 = GrammarMain()
        paragraphs = processed_result.split('\n')

        processed_paragraphs = []
        for paragraph in paragraphs:
            # Step 2: Split paragraphs into sentences using periods (.) as delimiter
            sentences = paragraph.split('.')

            processed_sentences = []
            for sentence in sentences:
                # Remove leading and trailing whitespaces from the sentence
                sentence = sentence.strip()
                # Step 3: Process each sentence
                processed_sentence = obj2.mapper(sentence)
                processed_sentences.append(processed_sentence)

            # Step 4: Join processed sentences to form paragraph
            processed_paragraph = ' '.join(processed_sentences)
            processed_paragraphs.append(processed_paragraph)

        # Join processed paragraphs to form final processed text
        processed_result = '\n'.join(processed_paragraphs)

    # if checkbox4 == "true":
    #     obj3 = FLongformerTextSummarizer()
    #     processed_result = obj3.refined_summarize_by_word_count(processed_result)

    return jsonify({'processed_result': processed_result})


if __name__ == '__main__':
    app.run()
