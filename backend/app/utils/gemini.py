import google.generativeai as genai
import json
import time
import nltk
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.config import settings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

genai.configure(api_key=settings.gemini_api_key)

def get_chat_summary(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_name).first()
    if not user or not isinstance(user.summary_file, list):
        return []
    
    return [summary["summary"] for summary in user.summary_file if "summary" in summary]


def save_chat_summary(user_name: str, new_summary: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_name).first()
    if not user:
        return None

    if not isinstance(user.summary_file, list):
        user.summary_file = []

    user.summary_file.append(new_summary)
    db.commit()
    return user.summary_file

def generate_conversation_summary(user_name: str, chat_history: list, db: Session = Depends(get_db)):
    conversation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    model = genai.GenerativeModel(settings.gemini_model)

    response = model.generate_content(f"""
    You are an AI that summarizes conversations for a mental health chatbot.
    Here is the chat history: {chat_history}
    Please summarize the conversation, including key moments and emotions.
    Provide the summary concisely and include the time the conversation ended: {conversation_time}.
    """)

    summary_data = {
        "conversation_time": conversation_time,
        "summary": response.text.strip()
    }

    save_chat_summary(user_name, summary_data, db)
    delete_chat_history(user_name, db)

def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    return " ".join([word for word in words if word.lower() not in stop_words])

def update_chat_history(user_name: str, user_input: str, bot_response: str, emotion: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_name).first()
    if not user:
        return None

    if not isinstance(user.chat_history, dict):
        user.chat_history = {"user_info": {}, "chat_history": []}

    user.chat_history["chat_history"].append({
        "user_input": user_input,
        "bot_response": bot_response,
        "emotion": emotion
    })

    db.commit()
    return user.chat_history

def delete_chat_history(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_name).first()
    if not user:
        return None

    user.chat_history = {"user_info": {}, "chat_history": []}
    db.commit()
    return user.chat_history

def mental_health_chatbot(user_name: str, user_input: str, emotion: str, db: Session = Depends(get_db)):
    model = genai.GenerativeModel(settings.gemini_model)
    user = db.query(User).filter(User.username == user_name).first()

    if not user:
        return None

    chat_summary = get_chat_summary(user_name, db)
    chat_history = user.chat_history if isinstance(user.chat_history, dict) else {"user_info": {}, "chat_history": []}

    response = model.generate_content(f"""You are an empathetic mental health assistant.
    Remember the user's past conversations and provide meaningful responses.
    You have access to the following conversation history:
    Current Chat History: {chat_history}
    Previous Chat Summaries: {chat_summary}
    Where the current chat history is the conversation who are having right now and the previous chat history contains the summary of the chat you have had with that user previoulsy.
    Always provide supportive, uplifting, and kind responses based on the user input and their emotion which is given as input to you as seen on camera. If the any negative emotion is same for too long then try to tell quotes or suggest videos or music, or make a joke or play games to uplift the mood. If the person's emotion is happy or neutral for some time continuously, then ask questions to the person so you can learn more about them. You can use the JSON file to have conversation with the user (for example, if some happy moment is mentioned in the JSON file, then you can use that to talk if the person emotion is sad or remind the person about how they overcame a previous sad or negative situation). Refer the following text for more understanding:
    How the model should work:
    The model should understand the emotion of the user and reply to them in a way that makes them feel comfortable. The model can use the JSON file as reference to understand the user and give customised responses. For example, if the user is worried about some failure, is experiencing anxiety, and if the JSON file contains information from a previous chat that mentions how the user overcame his fear and achieved something, then the model can use it as a reference and mention that to inspire the user.
    Important Note: The model should remember the previous chat history to give proper replies.

    Refer to the following scenarios:
    The mood of the user is sad, if the mood of the user is sad for more than 4-8 replies then either get any one good memory from the good memory tag from the JSON file and tell it to the user and mention that things will get better or take any bad memory from the bad memory tag and tell how they’ve overcome that (if they did) and that they can overcome this also.
    If the mood is anxious then take any bad memory from the bad memory tag and tell how they’ve overcome that (if they did) and that they can overcome this also and that this is just a part of the process of something nice.

    Additional features to be used:
    The model can give a quote or ask if the user wants suggestions for videos, music, joke or games to uplift their mood if the person’s mood doesn’t get better even after 4-8 replies.
    The model can interact with fun text-based games to make the user engaging and happy.
    The model can tell jokes to make the user happy.
    The model can try to use sarcasm without hurting the feelings of the user.

    Rules:
    The model shouldn’t use offensive language.
    The model shouldn’t help in planning the user to sabotage any individual, organisation or self.
    The model shouldn’t prescribe any medication at any cost.
    Model should help the user seek medical/psychological assistance in case the user expresses suicidal/harmful actions.

    Output:
    For each reply from the user, the model should give the reply accordingly until the chat is completely ended with something similar to a bye.
    Always act like you are talking to the user like a person.
    Important Note: Don’t ask multiple questions in the same response, limit to maximum 2-3 and wait for the user’s response (preferably 1 question).
    Important: If the user specifies that they want to delete their data or some information that they hve mentioned to the chatbot before then return 'CLEAR' as the output, in this case you shouldn't return anything else.
    Important: If the user asks you forget something that they have mentioned earlier then return 'CLEAR' as the output, in this case you shouldn't return anything else.

    New input from user:
    User: {user_input} (Emotion: {emotion})

    AI:""")

    bot_response = response.text.strip()

    update_chat_history(user_name, user_input, bot_response, emotion, db)

    if user_input.lower() in ["bye", "exit", "quit", "see you", "talk to you later", "ttyl", "goodbye"]:
        generate_conversation_summary(user_name, chat_history, db)

    return bot_response
