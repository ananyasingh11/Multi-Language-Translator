# AI Language Translator

This project is a powerful AI-based language translator capable of translating English text into **Hindi, Italian, Portuguese, French, and Spanish**. It utilizes a fine-tuned version of Facebook's **mBART-50** model to deliver high-quality translations.

The application features a user-friendly interface built with **Streamlit**.

## 🚀 Features

- **Multi-Language Support**: Translate English to 5 different languages.
- **State-of-the-Art Model**: Powered by `facebook/mbart-large-50-many-to-many-mmt`.
- **User-Friendly UI**: Simple and intuitive web interface using Streamlit.
- **Auto-Model Assembly**: Automatically combines split model files on the first run, ensuring easy distribution.
- **Easy Setup**: Simple commands to get up and running quickly.

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Git (optional)

### Setup Steps

1.  **Clone the Repository** (if applicable) or navigate to the project directory.

2.  **Create and Activate Virtual Environment**
    It's recommended to use a virtual environment to manage dependencies.

    ```powershell
    # Create venv
    python -m venv venv

    # Activate venv (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Install the required Python packages using `requirements.txt`.

    ```powershell
    pip install -r requirements.txt
    ```

    _Dependencies include: `transformers`, `torch`, `sentencepiece`, `streamlit`, `protobuf`_

## 🖥️ Usage

Run the application using the following command:

```powershell
streamlit run app.py
```

_or explicitly with python:_

```powershell
python -m streamlit run app.py
```

**Note on First Run:**
The model files are split into smaller parts (24 parts) for easier handling. The application includes a self-healing mechanism that will **automatically combine these parts** into the full `model.safetensors` file (~2.4GB) the first time you run the app. This process may take 1-2 minutes.

Once running, open your browser to the URL shown (usually `http://localhost:8501`).

## 📂 Project Structure

```
ai lang translator/
├── model/                  # Contains split model parts (and combined model after run)
│   ├── model.safetensors.part1...24
│   └── ...config files
├── venv/                   # Virtual environment directory
├── app.py                  # Main application & model combination logic
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🤖 Model Details

- **Base Model**: mBART-50 (Multilingual Denoising Pre-training for Neural Machine Translation)
- **Fine-tuning**: Optimized for translation from English to the target set (Hi, It, Pt, Fr, Es).

## ⚠️ Troubleshooting

- **"Failed to fetch dynamically imported module"**: If you see this in the browser, try a Hard Refresh (`Ctrl+F5`) or clear your browser cache.
- **Module not found**: Ensure you have activated the virtual environment (`.\venv\Scripts\activate`) before running the app.
