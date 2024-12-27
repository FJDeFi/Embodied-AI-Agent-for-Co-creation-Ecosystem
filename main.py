import os
import openai
from transformers import pipeline
from typing import List
from enum import Enum


class Detail:
    def __init__(self, name: str, pronouns="Unspecified", description="", role="", stage_of_life="Unspecified",
                 alternative_names=None, hobbies=None, tags=None):
        self.name = name
        self.pronouns = pronouns
        self.description = description
        self.role = role
        self.stage_of_life = stage_of_life
        self.alternative_names = alternative_names if alternative_names else []
        self.hobbies = hobbies if hobbies else []
        self.tags = tags if tags else []


class LanguageStyle(Enum):
    BUSINESS_ABBREVIATIONS = "business abbreviations"
    COWBOY_LINGO = "cowboy lingo"
    HACKNEYED_CLICHES = "hackneyed cliches"
    INTERNET_MEME_SLANG = "Internet meme slang"
    MEDICAL_TERMINOLOGY = "medical terminology"
    MOVIE_QUOTES = "movie quotes"
    OBSCURE_IDIOMS = "obscure idioms"
    ORWELLIAN_NEWSPEAK = "Orwellian newspeak"
    SPORTS_METAPHORS = "sports metaphors"


class Colloquium:
    def __init__(self, style: LanguageStyle):
        if not isinstance(style, LanguageStyle):
            allowed_values = [e.value for e in LanguageStyle]
            # fmt: off
            raise ValueError(f"Invalid value for colloquium. Must be one of: {allowed_values}")
        self.style = style

    def set_style(self, style: LanguageStyle):
        if not isinstance(style, LanguageStyle):
            # fmt: off
            raise ValueError(f"Invalid value for colloquium. Must be one of: {[e.value for e in LanguageStyle]}")
        self.style = style

    def get_style(self):
        return self.style


class CharacterAdjective(Enum):
    ANXIOUS = "anxious"
    CONTEMPLATIVE = "contemplative"
    CURT = "curt"
    EXPRESSIVE = "expressive"
    HILARIOUS = "hilarious"
    INQUISITIVE = "inquisitive"
    INTENSE = "intense"
    MISCHIEVOUS = "mischievous"
    SNARKY = "snarky"


class Adjective:
    def __init__(self, adjective: CharacterAdjective):
        self.set_adjective(adjective)

    def set_adjective(self, adjective: CharacterAdjective):
        if not isinstance(adjective, CharacterAdjective):
            # fmt: off
            raise ValueError(f"Invalid adjective. Must be one of: {[e.value for e in CharacterAdjective]}")
        self.adjective = adjective

    def get_adjective(self):
        return self.adjective

    def __str__(self):
        return f"Adjective: {self.adjective.value}"


class DialogueStyle:
    def __init__(self, adjectives: List[Adjective], colloquium: Colloquium, example_dialogue: List[str]):
        if not all(isinstance(adj, Adjective) for adj in adjectives):
            raise ValueError(
                "All items in adjectives must be of type Adjective.")
        if not isinstance(colloquium, Colloquium):
            raise ValueError("Colloquium must be of type Colloquium.")
        if not all(isinstance(dialogue, str) for dialogue in example_dialogue):
            raise ValueError("All items in example_dialogue must be strings.")

        self.adjectives = adjectives
        self.colloquium = colloquium
        self.example_dialogue = example_dialogue


class Personality:
    def __init__(self, traits=None):

        if traits is None:
            # Default 10 trait pairs
            traits = {
                "Sadness-Joy": (0.5, 0.5),
                "Anger-Fear": (0.5, 0.5),
                "Disgust-Trust": (0.5, 0.5),
                "Anticipation-Surprise": (0.5, 0.5),
                "Static-Dynamic": (0.5, 0.5),
                "Negative-Positive": (0.5, 0.5),
                "Aggressive-Peaceful": (0.5, 0.5),
                "Cautious-Open": (0.5, 0.5),
                "Introvert-Extravert": (0.5, 0.5),
                "Insecure-Confident": (0.5, 0.5)
            }
        self.traits = {key: self._normalize_pair(
            value) for key, value in traits.items()}

    @staticmethod
    def _normalize_pair(pair):
        total = sum(pair)
        if total == 0:
            return 0.5, 0.5  # Avoid division by 0
        return pair[0] / total, pair[1] / total

    def update_trait_pair(self, trait_pair: str, value1: float):
        if trait_pair not in self.traits:
            raise ValueError(f"{trait_pair} is not a valid trait pair.")
        if not 0.0 <= value1 <= 1.0:
            raise ValueError("Value must be between 0.0 and 1.0.")
        value2 = 1.0 - value1
        self.traits[trait_pair] = (value1, value2)

    def get_trait_value(self, trait_pair: str):
        if trait_pair not in self.traits:
            raise ValueError(f"{trait_pair} is not a valid trait pair.")
        return self.traits[trait_pair]

    def display_traits(self):
        print("\033[33m=== Personality ===\033[0m")
        for trait_pair, values in self.traits.items():
            trait1, trait2 = trait_pair.split("-")
            print(f"{trait1}: {values[0]:.2f}, {trait2}: {values[1]:.2f}")


class Avatar:
    def __init__(self, detail: Detail, coreDescription: str, motivations: List[str], flaws: List[str],
                 dialogueStyle: DialogueStyle, personality: Personality):
        self.detail = detail
        self.coreDescription = coreDescription
        self.motivations = motivations
        self.flaws = flaws
        self.dialogueStyle = dialogueStyle
        self.personality = personality

    def greet(self):
        if hasattr(self.detail, "name"):
            print(f"Hello, my name is {self.detail.name}.")
        else:
            print("Hello, I am an Avatar.")

    def display_personality(self):
        print("\033[33m=== Avatar Details ===\033[0m")
        if hasattr(self.detail, "name"):
            print(f"Name: {self.detail.name}")
        if hasattr(self.detail, "description"):
            print(f"Description: {self.detail.description}")
        if hasattr(self.detail, "role"):
            print(f"Role: {self.detail.role}")
        print(f"Core Description: {self.coreDescription}")
        print(f"Motivations: {', '.join(self.motivations)}")
        print(f"Flaws: {', '.join(self.flaws)}")
        print("\033[33m=== Dialogue Style ===\033[0m")
        # fmt: off
        print(f"Adjectives: {[adj.get_adjective().value for adj in self.dialogueStyle.adjectives]}")
        print(f"Colloquium: {self.dialogueStyle.colloquium.get_style().value}")
        # fmt: off
        print(f"Example Dialogues: {', '.join(self.dialogueStyle.example_dialogue)}")
        print("\033[33m=== Personality ===\033[0m")
        self.personality.display_traits()


detail = Detail(name="John Doe", pronouns="He/Him",
                description="A brave adventurer.", role="Hero")
dialogue_style = DialogueStyle(
    adjectives=[Adjective(CharacterAdjective.EXPRESSIVE),
                Adjective(CharacterAdjective.HILARIOUS)],
    colloquium=Colloquium(LanguageStyle.COWBOY_LINGO),
    example_dialogue=["Howdy!", "Let's ride."]
)
personality = Personality()

avatar = Avatar(
    detail=detail,
    coreDescription="An adventurous and courageous hero.",
    motivations=["Save the world", "Protect the weak"],
    flaws=["Impulsive", "Overconfident"],
    dialogueStyle=dialogue_style,
    personality=personality
)

avatar.display_personality()


# Load multi-emotion analyzer (e.g., RoBERTa pre-trained model)
emotion_analyzer = pipeline(
    "text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

# Analyze emotion and output the emotion vector
def get_emotion_vector(text):
    # Get emotion analysis results
    emotion_results = emotion_analyzer(text)[0]
    # Convert results to emotion vector
    emotion_vector = {res['label']: res['score'] for res in emotion_results}

    return emotion_vector


# Test function
text = "You can be more open"
emotion_vector = get_emotion_vector(text)

print("Emotion Vector:", emotion_vector)

# Load zero-shot classifier for intent recognition
classifier = pipeline("zero-shot-classification")

# Intent labels affecting emotions
intent_labels_emotion = [
    "express_emotion_towards_character",  # User expresses emotions towards the character, such as liking or disappointment
    "seek_emotional_support",             # User seeks emotional support, expecting comfort from the character
    "praise_character",                   # User praises the character, boosting the character's positive emotions
    "criticize_character",                # User criticizes the character, causing negative emotions
    "share_personal_emotion",             # User shares personal emotions, affecting the character's empathetic response
    "encourage_character",                # User encourages the character, enhancing confidence or positive emotions
    "blame_character",                    # User blames the character, potentially causing guilt or unease
    "show_sympathy_for_character"         # User shows sympathy for the character, triggering an emotional response
]

# Intent labels affecting personality
intent_labels_personality = [
    "challenge_character_belief",         # User challenges or questions character beliefs, influencing openness
    "suggest_personality_change",         # User suggests character changes, such as becoming more confident or kind
    "reinforce_character_trait",          # User supports or encourages existing character traits
    "request_character_reflection",       # User requests character self-reflection, driving personality change
    "encourage_personal_growth",          # User encourages growth, affecting conscientiousness and agreeableness
    "highlight_flaws_in_character",       # User points out character flaws, pushing for improvement
    "propose_new_interest",               # User suggests new interests or activities, enhancing openness
]

# Intent labels with no emotional or personality impact
intent_labels_neutral = [
    "ask_about_character_background",     # User asks about character backstory
    "request_factual_information",        # User requests factual information, e.g., "What is your name?"
    "confirm_character_action",           # User confirms whether the character completed a task
    "ask_for_progress_update",            # User asks about task progress
    "seek_instruction",                   # User requests guidance or suggestions from the character
    "inquire_about_preferences",          # User asks about preferences or likes
    "ask_for_story_continuation",         # User requests continuation of a story or scenario
    "explore_hypothetical_scenario"       # User proposes a hypothetical scenario without emotional or personality changes
]

# Comprehensive intent label table
intent_labels = intent_labels_emotion + \
    intent_labels_personality + intent_labels_neutral

# Analyze text intent
def get_intent(text):
    # Use zero-shot classifier to identify intent
    intent_result = classifier(text, intent_labels)
    # Extract the most probable intent label
    main_intent = intent_result['labels'][0]  # Most probable intent category
    intent_score = intent_result['scores'][0]  # Confidence score for the intent

    return main_intent, intent_score


# Test function
text = "You can be more open"
main_intent, intent_score = get_intent(text)

print("Detected Intent:", main_intent)
print("Intent Score:", intent_score)


def calculate_change(current_value, base_change):
    return base_change * (1 - current_value)  # The closer to 1, the smaller the change


def update_avatar_emotion_and_personality(avatar, user_input: str):
    """
    Directly update Avatar's emotional and personality states based on user input.
    """
    # Get emotion vector from user input
    emotion_vector = get_emotion_vector(user_input)
    print("Emotion Vector:", emotion_vector)

    # Get main intent and confidence score from user input
    main_intent, intent_score = get_intent(user_input)
    print("Detected Intent:", main_intent)
    print("Intent Score:", intent_score)

    # Update Avatar's emotional traits
    if main_intent in intent_labels_emotion:
        # Define emotion trait mapping
        emotion_trait_mapping = {
            "Sadness-Joy": "joy",
            "Anger-Fear": "anger",
            "Disgust-Trust": "disgust",
            "Anticipation-Surprise": "surprise",
            "Static-Dynamic": "neutral",  # Special handling for Static-Dynamic
        }

        # Iterate through mapping and update
        for trait_pair, emotion in emotion_trait_mapping.items():
            if emotion in emotion_vector:
                # Special handling for Static-Dynamic
                if trait_pair == "Static-Dynamic" and emotion == "neutral":
                    trait_value = avatar.personality.get_trait_value(
                        trait_pair)
                    # Update Static value (higher neutral -> increase Static, reduce Dynamic)
                    updated_value = trait_value[0] + calculate_change(
                        trait_value[0], intent_score * emotion_vector[emotion])
                    avatar.personality.update_trait_pair(
                        trait_pair, updated_value)
                    # fmt: off
                    print(f"Updating Static: {trait_value[0]:.2f} -> {updated_value:.2f}")
                else:
                    # Get values for the trait pair
                    trait1, trait2 = trait_pair.split("-")
                    trait_value = avatar.personality.get_trait_value(
                        trait_pair)

                    # Check keyword direction
                    if emotion.lower() == trait1.lower():
                        # Update the first trait
                        updated_value = trait_value[0] + calculate_change(
                            trait_value[0], intent_score * emotion_vector[emotion])
                        avatar.personality.update_trait_pair(
                            trait_pair, updated_value)
                        # fmt: off
                        print(f"Updating {trait1}: {trait_value[0]:.2f} -> {updated_value:.2f}")
                    elif emotion.lower() == trait2.lower():
                        # Update the second trait
                        updated_value = trait_value[0] - calculate_change(
                            trait_value[1], intent_score * emotion_vector[emotion])
                        avatar.personality.update_trait_pair(
                            trait_pair, updated_value)
                        # fmt: off
                        print(f"Updating {trait1}: {trait_value[0]:.2f} -> {updated_value:.2f}")

    # Update Avatar's personality traits
    elif main_intent in intent_labels_personality:
        # Define personality trait mapping
        personality_trait_mapping = {
            "Negative-Positive": "positive",
            "Aggressive-Peaceful": "peaceful",
            "Cautious-Open": "open",
            "Introvert-Extravert": "extravert",
            "Insecure-Confident": "confident",
        }

        for trait_pair, personality_trait in personality_trait_mapping.items():
            if personality_trait:
                trait1, trait2 = trait_pair.split("-")
                trait_value = avatar.personality.get_trait_value(trait_pair)

                # Check keyword direction
                if personality_trait.lower() == trait1.lower():
                    # Update the first trait
                    updated_value = trait_value[0] + \
                        calculate_change(trait_value[0], intent_score)
                    avatar.personality.update_trait_pair(
                        trait_pair, updated_value)
                    # fmt: off
                    print(f"Updating {trait1}: {trait_value[0]:.2f} -> {updated_value:.2f}")
                elif personality_trait.lower() == trait2.lower():
                    # Update the second trait
                    updated_value = trait_value[0] - \
                        calculate_change(trait_value[1], intent_score)
                    avatar.personality.update_trait_pair(
                        trait_pair, updated_value)
                    # fmt: off
                    print(f"Updating {trait1}: {trait_value[0]:.2f} -> {updated_value:.2f}")


# User input example
user_input = "I feel really inspired by your actions!"

# Assume avatar is initialized and contains a complete personality attribute
update_avatar_emotion_and_personality(avatar, user_input)

# Print updated emotion and personality state
avatar.display_personality()


# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")  # Update with your OpenAI API key

# Initialize sentiment analysis pipeline using Hugging Face Transformers
sentiment_analyzer = pipeline("sentiment-analysis")


def generate_character_description(avatar):
    """
    Generate a detailed character description using OpenAI's GPT-3.5 model.
    avatar: Avatar object containing character details.
    return: Generated character description.
    """
    # Base prompt for generating character description
    base_prompt = (
        f"Generate a detailed description of a character with the following attributes:\n"
        f"Name: {avatar.detail.name}\n"
        f"Description: {avatar.detail.description}\n"
        f"Role: {avatar.detail.role}\n"
        f"Core Description: {avatar.coreDescription}\n"
        f"Motivations: {', '.join(avatar.motivations)}\n"
        f"Flaws: {', '.join(avatar.flaws)}\n"
        # fmt: off
        f"Dialogue Style Adjectives: {', '.join([adj.adjective.value for adj in avatar.dialogueStyle.adjectives])}\n"
        f"Colloquium: {avatar.dialogueStyle.colloquium.style.value}\n"
    )

    # Use OpenAI GPT model to generate character description
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative assistant helping generate character descriptions."},
                {"role": "user", "content": base_prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        description = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        description = "Failed to generate description using OpenAI API."

    return description


character_description = generate_character_description(avatar)
print("Character Description:", character_description)
