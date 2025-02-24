import json
import os
import ollama
import random
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='mcq_generation.log', format='%(asctime)s - %(levelname)s - %(message)s')

# MongoDB connection setup
uri = "mongodb+srv://ritika0204:ritikakumar@hack.6nemp.mongodb.net/?retryWrites=true&w=majority&appName=Hack"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.mind_map_db  # Change 'mind_map_db' to your actual database name if different
collection = db.Hack

# Load subtopics from MongoDB
def load_subtopics():
    try:
        documents = collection.find({}, {"_id": 0, "mind_map.subtopics": 1})  # Adjust the projection as needed
        subtopics = []
        for doc in documents:
            for subtopic in doc['mind_map']['subtopics']:
                subtopics.append(subtopic['name'])
        return subtopics
    except Exception as e:
        logging.error(f"Failed to load subtopics from MongoDB: {e}")
        return []

# Generate MCQs using Ollama (Mistral model)
def generate_mcq(prompt):
    logging.info(f"Sending request to Ollama for prompt: {prompt}")
    try:
        response = ollama.generate(
            model="mistral:latest",
            prompt=prompt,
        )
        return response.response.strip() if response else None
    except Exception as e:
        logging.error(f"Error during Ollama API call: {e}")
        return None

# Generate four MCQs for each subtopic
def generate_questions_for_subtopics(subtopics):
    questions = []
    for subtopic in subtopics:
        for _ in range(4):  # Generate four questions per subtopic
            prompt = f"Generate an easy-level multiple-choice question (MCQ) on the topic of {subtopic}. The question should have 4 unique, distinct options and one correct answer."
            question = generate_mcq(prompt)
            if question:
                questions.append(question)
            else:
                logging.info(f"No questions generated for subtopic: {subtopic}")
    return questions

# Main function for terminal interaction
def main():
    subtopics = load_subtopics()
    if not subtopics:
        print("No subtopics found. Please check your database.")
        return

    print("\nGenerating MCQs for each subtopic...")
    questions = generate_questions_for_subtopics(subtopics)
    if questions:
        with open("mcqs.json", "w") as file:
            json.dump(questions, file, indent=4)
            logging.info("MCQs saved successfully to 'mcqs.json'")
        print("\nMCQs saved as `mcqs.json` 🎉")
    else:
        print("No questions generated. Please check the log for errors.")

if __name__ == "__main__":
    main()
