from fastapi import FastAPI
import pickle
import re


app = FastAPI(
    title="Arabic Dialect Classification API",
    description="A simple API that use NLP model to predict the dialect of arabic text",
)

# load the model
# with open(
#     join(dirname(realpath(__file__)), "models/sentiment_model_pipeline.pkl"), "rb"
# ) as f:
#     model = joblib.load(f)

with open('models\LR_model.pkl', 'rb') as f:
            model = pickle.load(f)

# Data cleaning
def clean_text(text):
    """
    Receive a text and clean it
    :param text:
    :return: text
    """
    # remove mentions from text
    text = re.sub(r'@\w+', '', text)

    # remove emojis from text
    EMOJI_PATTERN = re.compile(
        "(["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U0001F1F2"
        "\U0001F1F4"
        "\U0001F620"
        "\u200d"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # Dingbats
        "\u3030"
        "\U00002500-\U00002BEF"  # Chinese char
        "\U00010000-\U0010ffff"
        "])"
    )

    text = re.sub(EMOJI_PATTERN, '', text)

    # remove digits from text
    text = re.sub(r'\d+', '', text)

    # remove URLs from text
    text = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', '', text)
    
    # remove english words
    text = re.sub(r'[a-zA-Z0-9]+', '', text)

    # remove the MSA relative pronouns ( الذي , التي , الذين ) and the dialectal relative pronoun ( اللى ) since they don't affect the dialect identification
    pattern = '|'.join([' الذي ', ' الذى ', ' التى ', ' التي ', ' الذين ', ' اللي ', ' اللى ', ' إللي ', ' إللى '])
    text = re.sub(pattern, '', text)

    # replace punctuations with space
    text = re.sub(r'[…“” ̮+=\-–—ـــ()*&^%$@!‘÷×؛<>\":/،\[\]؟ـــــ.,’{}~]+', ' ', text)

    # replace ( # ) and ( _ ) in hashtags with space
    text = re.sub(r'(#|_)+', ' ', text)

    # remove the laughing words (هههه..إلخ) since they don't affect the dialect identification
    text = re.sub(r'ههه+', ' ', text)
        
    return text


@app.get("/predict")
def predict(text: str):
    """
    Receive a text and predict the dialect
    :param text:
    :return: prediction
    """
    # clean text
    text_cleaned = clean_text(text)
    
    # perform prediction
    prediction = model.predict([text_cleaned])

    # show result
    result = {"predicted dialect" : prediction[0]}
    return result