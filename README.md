# ZeroLib Project

## Overview
ZeroLib is a desktop application designed to provide users with access to both a movie library and a university library. The application features advanced search capabilities, allowing users to filter their searches by various criteria such as title, actor, director, and genre for movies, as well as executing SPARQL queries for university-related information. Additionally, it leverages a language model (LLM) to generate queries and answer user questions.

## Features
- **Movie Library**: Search for movies using a title, actor, director, or genre filter.
- **University Library**: Execute SPARQL queries to retrieve information from a university database.
- **Query Generation**: Utilize a language model to generate SPARQL queries and provide answers to user prompts.
- **Responsive UI**: Built using PyQt5, providing a user-friendly interface.
- **Loading Indicators**: Displays loading messages while fetching data.
- **Error Handling**: User-friendly error messages in case of exceptions during data retrieval.

## Technologies Used
- **Python**: The core programming language for the application.
- **PyQt5**: Framework for building the GUI.
- **QWebEngine**: For displaying HTML content within the application.
- **HTMLBuilder**: Custom module for generating HTML content.
- **SparqlQueryHelper**: Custom module for executing SPARQL queries.
- **LLMClient**: Custom module for interacting with a language model to generate queries and responses.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Abduaws/ZeroLib.git
1. Navigate to Project Directory:
   ```bash
   cd ZeroLib
1. Install Dependencies:
   ```bash
   pip install -r requirements.txt
