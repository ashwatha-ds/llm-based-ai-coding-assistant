# codemateAI – Multi-Language AI Coding Assistant & Mentor

## Live Demo

https://llm-based-ai-coding-assistant-zpwy3fax7yjxiul3pq32pz.streamlit.app/

---

## Overview

codemateAI is an AI-powered multi-language coding assistant and mentor built using Streamlit and Groq LLMs.  
The application helps users generate code, debug programs, explain concepts, and practice technical interviews through an interactive conversational interface.



---

## Key Features

### Multi-Language Coding Support

Supports multiple programming languages and domains including:

* Python
* Java
* C++
* SQL
* Data Analytics
* Data Science

---

### AI-Powered Coding Modes

#### General Coding Assistance

* Ask coding-related questions
* Get concept explanations and best practices
* Receive language-specific guidance

---

#### Code Generation

* Generate clean and structured code
* Produces well-formatted and commented outputs
* Supports multiple coding domains

---

#### Debug Code

* Detects bugs in user-provided code
* Explains issues clearly
* Provides corrected and optimized solutions

---

#### Explain Code

* Breaks down complex code into simple explanations
* Explains logic block-by-block
* Helps beginners understand programming concepts

---

#### Mock Interview Mode

* Simulates technical interview questions
* Evaluates user responses
* Provides feedback and improvement suggestions

---

## User Interface Highlights

* Clean and responsive Streamlit interface
* Multi-page application workflow
* Interactive chat-based experience
* Download generated code functionality
* Mode-based assistant interactions

---

## Technology Stack

* Python
* Streamlit
* Groq API
* llama-3.3-70b-versatile
* Prompt Engineering


---

## Project Structure

```bash
codemateAI/
│
├── codemateai.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Application Locally

1. Clone the repository

```bash
git clone <your-github-repo-link>
```

2. Navigate to the project directory

```bash
cd codemateAI
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add your Groq API key inside:

```bash
.streamlit/secrets.toml
```

Example:

```toml
GROQ_API_KEY = "your_api_key_here"
```

5. Run the application

```bash
streamlit run codemateai.py
```

---

## Model Information

* Uses Groq-hosted llama-3.3-70b-versatile model
* Context-aware conversational responses
* Language-specific prompt engineering
* Optimized for coding assistance and mentoring

---

## Future Enhancements

* Add support for more programming languages
* Integrate code execution environment
* Add voice-based interaction
* Implement chat history export
* Improve UI/UX with advanced customization
* Add authentication and user profiles

---

## Disclaimer

AI-generated responses may occasionally produce incorrect or incomplete code.  
Users are encouraged to review and test generated outputs before production use.

---

## Author

Ashwatha

