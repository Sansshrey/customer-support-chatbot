# Customer Support Chatbot

An AI-powered Customer Support Chatbot built using **Python, Flask, and Natural Language Processing (NLP)** to automate customer queries and provide relevant responses through a web-based chat interface.

The chatbot uses an intent-based approach to understand user messages and generate appropriate responses, simulating a real-world customer support assistant.

---

## Overview

Customer support teams often handle repetitive queries related to products, services, and general information. This project aims to automate such interactions by creating a chatbot capable of understanding user intents and providing instant responses.

The chatbot is designed with a customizable intent and response structure, allowing new conversations and use cases to be added easily.

---

## Features

- Intent-based query classification
- Automated response generation
- Web-based chatbot interface
- Customizable intents and responses using JSON
- Flask-based backend application
- NLP-based text processing
- Unit testing support

---

## Technology Stack

### Programming Language
- Python

### Backend Framework
- Flask

### Natural Language Processing
- NLP
- Intent Classification
- Text Processing

### Frontend
- HTML
- CSS
- JavaScript

### Data Storage
- JSON

### Testing
- Python Unit Testing

---

## Project Structure

```
CustomerSupportChatbot/
│
├── app.py                  # Flask application entry point
├── chatbot.py              # Chatbot logic and NLP processing
├── intents.json            # Intent patterns and chatbot responses
├── test_chatbot.py         # Test cases
├── requirements.txt        # Project dependencies
│
├── templates/
│   └── index.html          # Chatbot user interface
│
├── README.md               # Project documentation
└── .gitignore              # Ignored files
```

---

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/Sansshrey/customer-support-chatbot.git
```

### Navigate to Project Directory

```bash
cd customer-support-chatbot
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Run the Application

```bash
python app.py
```

Open the application in your browser:

```
http://127.0.0.1:5000/
```

---

## Example Interaction

User:

```
Hello
```

Chatbot:

```
Hi! How can I help you today?
```

---

User:

```
I need help with my order
```

Chatbot:

```
Sure, I can help you with your order-related query.
```

---

## Testing

Run the test cases using:

```bash
python test_chatbot.py
```

The test suite validates chatbot functionality and response handling.

---

## Future Enhancements

- Implement machine learning-based intent classification
- Add database integration for customer information
- Add voice-based chatbot capabilities
- Deploy the application on cloud platforms
- Maintain user conversation history
- Integrate advanced AI models for better responses

---

## Applications

This chatbot can be used for:

- Customer support automation
- FAQ assistance
- E-commerce support systems
- Helpdesk automation
- Business query handling

---

## Author

**Sanskriti Shrey**

Computer Science Engineer

Interests:
- Artificial Intelligence
- Natural Language Processing
- Conversational AI
- Software Development

---

## License

This project is developed for learning and demonstration purposes.
