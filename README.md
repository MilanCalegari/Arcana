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

2. Navigate to the project folder:

   ```bash
   cd Arcana
   ```

3. Create a virtual environment:

   ```bash
   python -m venv env
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     env\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source env/bin/activate
     ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Deployed Version on Hugging Face Spaces

Access the deployed version of Arcana on Hugging Face Spaces: [Arcana on Hugging Face Spaces](https://huggingface.co/spaces/rmcalegari/Arcana)

## Usage

1. Ensure the virtual environment is active.

2. Export your Hugging Face token:

   - On Windows:

     ```bash
     SET HF_TOKEN="YOUR_TOKEN_HERE"
     ```

   - On macOS/Linux:

     ```bash
     export HF_TOKEN="YOUR_TOKEN_HERE"
     ```

3. Run the application:

   ```bash
   streamlit run app.py
   ```

4. Access the application in your browser at `http://localhost:8501`.

## Future Features

- [ ] Handle Multiple Languages
- [ ] Local Version using Ollama
- [ ] Add More Reading Methods

## License

This project is licensed under the MIT License.

**Note:** Ensure you replace `"YOUR_TOKEN_HERE"` with your actual Hugging Face token.
