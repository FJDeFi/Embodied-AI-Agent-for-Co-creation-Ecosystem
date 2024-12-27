# Project: Inworld Avatar Personality and Emotion Analysis

This project provides tools to create and manage detailed character profiles, simulate emotions, and analyze text-based interactions. The system utilizes Python-based machine learning libraries, including Hugging Face Transformers and OpenAI GPT, for emotion and intent analysis.

---

## Features
- **Character Profiles:** Define detailed attributes for avatars, such as traits, emotions, and motivations.
- **Emotion Analysis:** Use a pretrained model to analyze text and generate emotion vectors.
- **Intent Recognition:** Identify user intents from text interactions with zero-shot classification.
- **Personality Updates:** Dynamically adjust avatar personality traits based on user input.
- **Dialogue Generation:** Generate detailed character descriptions using OpenAI GPT.

---

## Prerequisites
To run this project, ensure your environment meets the following requirements:

1. Python 3.8 or above.
2. Required libraries installed (see below).
3. A valid OpenAI API key for GPT integration.

---

## Installation Steps

### Step 1: Clone the Repository
Clone this project repository to your local machine:
```bash
git clone <repository_url>
cd <repository_directory>
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### Step 3: Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, manually install the libraries:
```bash
pip install transformers openai
```

### Step 4: Set Up OpenAI API Key
Ensure your OpenAI API key is set up in your environment. You can either:
- Add it directly to the script: `openai.api_key = "<your_api_key>"`
- Or, set it as an environment variable:
```bash
export OPENAI_API_KEY=<your_api_key>     # For macOS/Linux
set OPENAI_API_KEY=<your_api_key>       # For Windows
```

---

## Running the Project

### Initialize the Script
Run the main Python script:
```bash
python main.py
```
## Expected Output

When you run `main.py`, the program will create an avatar, display its default personality, then execute emotion analysis on two sample user input, detect their intent, and updates the avatar personality accordingly. Below is a detailed explanation of each step and its corresponding output that will appear in the terminal:

---

### 1. **Avatar Creation**
- **Command:**
  ```python
  avatar = Avatar(detail, coreDescription, motivations, flaws, dialogueStyle, personality)
  ```
- **Behavior:**
  Initializes an `Avatar` object with the provided attributes such as details, motivations, flaws, dialogue style, and personality traits.
- **Output:**
  No output is directly printed during initialization.

---

### 2. **Displaying Avatar Personality**
- **Command:**
  ```python
  avatar.display_personality()
  ```
- **Behavior:**
  Prints the avatar’s details, dialogue style, and key personality traits to the terminal.
- **Sample Output:**
  ```
  === Avatar Details ===
  Name: John Doe
  Description: A brave adventurer.
  Role: Hero
  Core Description: An adventurous and courageous hero.
  Motivations: Save the world, Protect the weak
  Flaws: Impulsive, Overconfident
  === Dialogue Style ===
  Adjectives: expressive, hilarious
  Colloquium: cowboy lingo
  Example Dialogues: Howdy!, Let's ride.
  === Personality ===
  Sadness: 0.50, Joy: 0.50
  Anger: 0.50, Fear: 0.50
  Disgust: 0.50, Trust: 0.50
  Anticipation: 0.50, Surprise: 0.50
  Static: 0.50, Dynamic: 0.50
  Negative: 0.50, Positive: 0.50
  Aggressive: 0.50, Peaceful: 0.50
  Cautious: 0.50, Open: 0.50
  Introvert: 0.50, Extravert: 0.50
  Insecure: 0.50, Confident: 0.50
  ```

---

### 3. **Loading Emotion Analyzer Pipeline**
- **Command:**
  ```python
  emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
  ```
- **Behavior:**
  Downloads and loads the `emotion-english-distilroberta-base` model for analyzing emotions in text.
- **Output:**
  A confirmation that the model has been loaded successfully, such as:
  ```
  Downloading: 100% [Model Files]
  Model 'emotion-english-distilroberta-base' loaded successfully.
  ```

---

### 4. **Emotion Vector Extraction**
- **Command:**
  ```python
  get_emotion_vector("You can be more open")
  ```
- **Behavior:**
  Analyzes the given input text to extract emotion scores using the loaded emotion analyzer pipeline.
- **Sample Output:**
  ```
  Emotion Vector:
  {'joy': 0.45, 'sadness': 0.15, 'anger': 0.10, 'surprise': 0.30}
  ```

---

### 5. **Loading Zero-Shot Classifier**
- **Command:**
  ```python
  classifier = pipeline("zero-shot-classification")
  ```
- **Behavior:**
  Loads a zero-shot classification pipeline, which will be used to identify intent from user input.
- **Output:**
  Confirmation of model loading:
  ```
  Zero-shot classification pipeline loaded successfully.
  ```

---

### 6. **Intent Detection**
- **Command:**
  ```python
  main_intent, intent_score = get_intent("You can be more open")
  ```
- **Behavior:**
  Determines the main intent of the input text along with its confidence score.
- **Sample Output:**
  ```
  Detected Intent: encourage_character
  Intent Score: 0.85
  ```

---

### 7. **Updating Avatar Emotion and Personality**
- **Command:**
  ```python
  update_avatar_emotion_and_personality(avatar, "I feel really inspired by your actions!")
  ```
- **Behavior:**
  Updates the avatar's emotion traits based on the input text's emotion vector and intent.
- **Sample Output:**
  ```
  Emotion Vector: {'joy': 0.70, 'sadness': 0.05}
  Detected Intent: praise_character
  Intent Score: 0.90
  Updating Joy: 0.50 -> 0.65
  Updating Positive: 0.50 -> 0.75
  ```

---

### 8. **Displaying Updated Avatar Personality**
- **Command:**
  ```python
  avatar.display_personality()
  ```
- **Behavior:**
  Prints the updated personality traits of the avatar.
- **Sample Output:**
  ```
  === Personality ===
  Sadness: 0.35, Joy: 0.65
  Negative: 0.25, Positive: 0.75
  Aggressive: 0.50, Peaceful: 0.50
  ```

---

### 9. **Generating Character Description**
- **Command:**
  ```python
  character_description = generate_character_description(avatar)
  ```
- **Behavior:**
  Constructs a prompt based on the avatar’s attributes and calls the OpenAI `gpt-3.5-turbo` model to generate a character description.
- **Sample Output:**
  ```
  Generated Character Description:
  "John Doe is a brave adventurer, driven by a deep desire to save the world and protect the weak. Despite his impulsive and overconfident nature, he remains courageous and full of life."
  ```

