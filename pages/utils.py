import ollama
import re


import json 
import re
import streamlit as st
import ollama
import json
import re
import pymongo


# MongoDB Connection (Use your actual connection string)
MONGO_URI = "mongodb+srv://hack:ritika@hack.6nemp.mongodb.net/?retryWrites=true&w=majority&appName=Hack"
#MONGO_URI = 'mongodb%2Bsrv%3A%2F%2F%3Critika0204%3E%3A%3Critikakumar%3E%40hack.6nemp.mongodb.net%2F%3FretryWrites%3Dtrue%26w%3Dmajority%26appName%3DHackmongodb%2Bsrv%3A%2F%2F%3Critika0204%3E%3A%3Critikakumar%3E%40hack.6nemp.mongodb.net%2F%3FretryWrites%3Dtrue%26w%3Dmajority%26appName%3DHack'
client = pymongo.MongoClient(MONGO_URI)
db = client["mind_map_db"]  # Database Name
collection = db["summary"] 

# Load DeepSeek model
model = "deepseek-r1:14b"

# user_input = "How to learn Trignometry?"
# age = "12-18"
# Define your prompt
# teen_prompt =f"""
#     You are a AI tool for enhancing digital learning. Create a 2 sentence summary on the topic: {user_input}.
#     Also generate a enthusiastic motivation for a user who is of the age {age}.
#     Use GenZ language.

#     Example output:
#     The Solar System is like a giant cosmic neighborhood where the Sun is the boss, and eight planets—including Earth—orbit around it. It’s packed with cool stuff like moons, asteroids, and even icy comets zooming through space!

#     Yo, space is straight-up awesome! From Saturn’s blingy rings to Mars’ dusty red vibes, the universe is full of wild mysteries—so keep exploring, because who knows, you might be the next astronaut to step on another planet!

    
# """
# child_prompt =f"""
#     You are a AI tool for enhancing digital learning. Create a 2 sentence summary on the topic: {user_input}.
#     Also generate a enthusiastic motivation for a user who is of the age {age}.
#     Use GenZ language.

#     Example output:
#     The Solar System is like a giant cosmic neighborhood where the Sun is the boss, and eight planets—including Earth—orbit around it. It’s packed with cool stuff like moons, asteroids, and even icy comets zooming through space!

#     Yo, space is straight-up awesome! From Saturn’s blingy rings to Mars’ dusty red vibes, the universe is full of wild mysteries—so keep exploring, because who knows, you might be the next astronaut to step on another planet!

    
# """

def adult_summary_generate(user_input, collection, age='18+', model= "deepseek-r1:14b"):
    prompt =f"""
    You are a AI tool for enhancing digital learning. Create a 2 sentence summary on the topic: {user_input}.
    Also generate a enthusiastic motivation for a user who is of the age {age}.

    Example output:
    Summary: Data Science is the interdisciplinary field that leverages statistics, machine learning, and data-driven techniques to extract insights and make informed decisions from vast amounts of structured and unstructured data. It powers innovations across industries, from personalized recommendations to predictive analytics, shaping the future of technology and business.

Motivation: Dive into the world of Data Science and unlock the power of data to drive real-world impact! Whether you're predicting trends, building intelligent models, or uncovering hidden patterns, this field offers endless opportunities to innovate, solve problems, and shape the future—so start your journey today! 
"""
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input}
    ]
    # Call Ollama's chat API
    response = ollama.chat(model=model, messages=messages)
    response = response["message"]["content"]
    response = response.split('</think>')[1]
    response= re.sub(r"\*\*.*?\*\*\n?", "", response).strip()

    
    data = {
        'user_input': user_input,
        'age': age,
        'summary': response

    }

    collection.insert_one(data)
    return response


def teen_summary_generate(user_input, collection, age='12-18', model= "deepseek-r1:14b"):
    prompt =f"""
    You are a AI tool for enhancing digital learning. Create a 2 sentence summary on the topic: {user_input}.
    Also generate a enthusiastic motivation for a user who is of the age {age}.
    Use GenZ language.

    Example output:
    The Solar System is like a giant cosmic neighborhood where the Sun is the boss, and eight planets—including Earth—orbit around it. It’s packed with cool stuff like moons, asteroids, and even icy comets zooming through space!

    Yo, space is straight-up awesome! From Saturn’s blingy rings to Mars’ dusty red vibes, the universe is full of wild mysteries—so keep exploring, because who knows, you might be the next astronaut to step on another planet!
    """

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input}
    ]
    # Call Ollama's chat API
    response = ollama.chat(model=model, messages=messages)
    response = response["message"]["content"]
    response = response.split('</think>')[1]
    response= re.sub(r"\*\*.*?\*\*\n?", "", response).strip()

    
    data = {
        'user_input': user_input,
        'age': age,
        'summary': response

    }

    collection.insert_one(data)
    return response

def child_summary_generate(user_input, collection, age='8-12', model= "deepseek-r1:14b"):
    prompt =f"""
    You are a AI tool for enhancing digital learning. Create a 2 sentence summary on the topic: {user_input}.
    Also generate a enthusiastic motivation for a user who is of the age {age}.
    Please output like you are talking to a 8 year old.

    Example output:
    The Solar System is like a giant cosmic neighborhood where the Sun is the boss, and eight planets—including Earth—orbit around it. It’s packed with cool stuff like moons, asteroids, and even icy comets zooming through space!

    Yo, space is straight-up awesome! From Saturn’s blingy rings to Mars’ dusty red vibes, the universe is full of wild mysteries—so keep exploring, because who knows, you might be the next astronaut to step on another planet!
    """

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input}
    ]
    # Call Ollama's chat API
    response = ollama.chat(model=model, messages=messages)
    response = response["message"]["content"]
    response = response.split('</think>')[1]
    response= re.sub(r"\*\*.*?\*\*\n?", "", response).strip()

    
    data = {
        'user_input': user_input,
        'age': age,
        'summary': response

    }

    collection.insert_one(data)
    return response
