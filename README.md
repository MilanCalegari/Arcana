---
title: Arcana
emoji: 🔮
colorFrom: gray
colorTo: purple
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: false
license: mit
short_description: Your AI fortune teller 🔮
---

# Arcana

![MIT License](https://img.shields.io/badge/license-MIT-green)

## Description

Arcana is an artificial intelligence application that acts as your personal fortune teller, providing personalized predictions and insights.

## Features

- Personalized AI-based predictions
- Interactive and user-friendly interface
- Real-time updates

## Technologies Used

- Python
- Streamlit 1.41.1
- Hugging Face

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MilanCalegari/Arcana.git
   ```

2. Navigate to project folder:
  ```bash
  cd Arcana 
  ```

3. Create a virtual environment:
  
  ```bash
  python -m venv env
  ```

4. Activate virtual enviroment:
  * On Windows: 
  ```bash
  env\Scripts\activate
  ```
  
  * On macOS/Linux:
  ```bash
  source env/bin/activate
  ```

5. Install dependencies:
  ````bash
  pip install -r requirements.txt
  ```

## Deployed version available on Hugging Spaces
[Deployed Arcana](https://huggingface.co/spaces/rmcalegari/Arcana)


## Usage
1. Ensure the virtual environment is activate
  
2. Export your huggingface token:
  * On Windows
  ```
  SET HF_TOKEN="YOUR_TOKEN_HERE"
  ```
  * On macOS/Linux

  ```bash
  export HF_TOKEN="YOUR_TOKEN_HERE"
  ```
  
3. Run the application:
  ```bash
  streamlit run app.py
  ```

4. Acess the application in your browser at http://localhost:8501

## Future Features
- [ ] Handle Multiple Languages
- [ ] Local Version using Ollama
- [ ] Add more reading methods


## License
This project is licensed under the MIT License.

