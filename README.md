# Console-Based Chatbot Using Gemini API

## Overview
This project provides a console-based chatbot that interacts with website content using the **Gemini API** from Google. It extracts relevant information from a given website, processes it, and uses the Gemini API to generate meaningful responses based on user inputs. The chatbot works directly in the command line (console), without the need for a frontend.

This guide will walk you through how to set up, install, and use the chatbot, even if you're new to programming.

## Features
- **Web Scraping**: The chatbot extracts relevant content from any given website.
- **Gemini API Integration**: Uses Google's **Gemini API** to generate conversational responses based on scraped data.
- **Console Interaction**: You can interact with the chatbot directly through the terminal/command line interface.
- **Environment Setup**: The project is designed to be easily set up with minimal configurations.

## Prerequisites
Before using this chatbot, ensure you have the following:
- **Python 3.8 or higher**: This project is built using Python, so make sure you have Python 3.8 or later installed on your machine.
- **Gemini API Key**: You need an API key from Google's Gemini service to allow the chatbot to generate responses.

If you don't have Python installed, visit [python.org](https://www.python.org/downloads/) to download and install it. For getting an API key, follow the instructions on the [Google Gemini documentation](https://gemini.com/).

## Installation Steps

### Step 1: Clone the Repository

To get started, clone the project repository to your local machine. Open your terminal (Command Prompt on Windows or Terminal on macOS/Linux) and run the following command:

git clone https://github.com/Kdar252/WebURL_ChatBot.git
cd WebURL_ChatBot

### Step 2: Install Dependencies

Install the necessary Python libraries by running this command:

pip install -r requirements.txt

### Step 3: Set Up Environment Variables

To securely store your Gemini API key, we use a .env file. Create a file named .env in the project directory (same level as main.py), and add the following line with your API key:

GEMINI_API_KEY=your_api_key_here

### Step 4: Running the Chatbot

Once everything is set up, you can run the chatbot by executing the following command:

python main.py


## Created requirements for the AI Engineer hiring process at Relinns Technologies


