## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Tectonic

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone https://github.com/BadrKandri/meliodas_manus.git
   cd project
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv Myvenv
   Myvenv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Download Tectonic**
   ```
   1. visit this link https://github.com/tectonic-typesetting/tectonic/releases?page=2
   2. Under Asset download: tectonic-x86_64-pc-windows-msvc.zip
   3. Extract it somewhere permanent like: C:\tectonic\tectonic.exe
   4. Add that folder to your system PATH
   5. Check the instalation by runing this command ' C:\tectonic\tectonic.exe --version ' in your terminal
   6. You should see something like : tectonic 0.15.0Tectonic 0.15.0
   ```



## Usage
**Run this command in your terminal**
```bash
python Agent.py
```

The agent will start an interactive session where you can ask questions and request analysis.
