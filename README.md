# Excel Analysis AI Agent

An autonomous AI agent designed to analyze Excel files, extract charts and images, and generate comprehensive reports using advanced AI capabilities.

## Overview

This project implements an intelligent Excel analysis system that combines multiple technologies to provide deep insights into Excel files. The agent can parse Excel data, extract embedded charts and images, analyze visual content using AI vision models, and generate detailed reports.

## Features

### 🔍 **Excel Analysis**
- **Sheet Structure Analysis**: Automatically analyzes Excel worksheets, including row/column counts, data types, and column headers
- **Data Quality Assessment**: Identifies missing values, duplicate rows, invalid entries, and data consistency issues
- **Statistical Analysis**: Calculates comprehensive statistics including mean, median, quartiles, standard deviation, and outlier detection
- **Sample Data Extraction**: Provides representative data samples for quick understanding

### 📊 **Chart Extraction & Analysis**
- **Advanced Chart Extraction**: Uses Spire.XLS library for reliable chart extraction from Excel files
- **AI-Powered Chart Analysis**: Leverages OpenAI's GPT-4 Vision to analyze extracted charts and provide insights
- **Multiple Chart Types**: Supports all Excel chart types (bar, line, pie, scatter, etc.)
- **Detailed Chart Insights**: Extracts trends, patterns, data values, and key takeaways from visual content

### 🖼️ **Image Processing**
- **Embedded Image Extraction**: Extracts all embedded images from Excel files using ZIP-based extraction
- **Vision AI Analysis**: Analyzes extracted images using OpenAI's vision capabilities
- **Content Description**: Provides detailed descriptions of image content, objects, and visual elements

### 🤖 **AI Agent Capabilities**
- **Interactive Interface**: Command-line interface for real-time interaction with the agent
- **Comprehensive Reporting**: Generates structured JSON reports with detailed analysis
- **Error Handling**: Robust error handling and logging for reliable operation
- **Reasoning Tools**: Enhanced with reasoning capabilities for complex analysis tasks

### 🛠️ **Additional Tools**
- **Python Code Execution**: Can execute Python code for custom analysis
- **File Operations**: File manipulation and management capabilities
- **LaTeX Compilation**: Support for generating PDF reports from LaTeX templates
- **Text Processing**: Advanced text processing and escaping functions

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
   python -m venv myvenv
   myvenv\Scripts\activate  # On Windows
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


## Dependencies

The project relies on the following key libraries:

- **agno**: AI agent framework for building intelligent agents
- **openai**: OpenAI API client for GPT-4 and vision capabilities
- **pandas**: Data manipulation and analysis
- **Spire.XLS**: Excel file processing and chart extraction
- **python-dotenv**: Environment variable management
- **pillow**: Image processing
- **requests**: HTTP client for API calls

## Usage

### Starting the Agent

Run the main agent script:

```bash
python Agent.py
```

The agent will start an interactive session where you can ask questions and request analysis.

### Example Commands

```
what do you want from the agent? : Analyze the Excel file food.xlsx
what do you want from the agent? : Extract and analyze all charts from the spreadsheet
what do you want from the agent? : Generate a comprehensive report of the data quality
what do you want from the agent? : exit
```

### Sample Analysis Output

The agent generates structured JSON reports with detailed information:

```json
{
  "file_summary": {
    "file_size": "2.5 MB",
    "total_sheets": "3 sheets",
    "total_charts": "12 charts",
    "total_images": "5 images",
    "extraction_status": "success"
  },
  "sheets": {
    "Sheet1": {
      "rows_count": "150 rows",
      "columns_count": "8 columns",
      "column_names": ["Date", "Product", "Sales", "Region"],
      "data_types": {
        "Date": "date",
        "Product": "string",
        "Sales": "numeric",
        "Region": "string"
      },
      "statistics": {
        "Sales": {
          "mean": 1250.5,
          "median": 1100.0,
          "min": 200,
          "max": 5000,
          "quartiles": [800, 1100, 1600]
        }
      }
    }
  },
  "chart_analyses": [
    {
      "chart_file": "Sheet1_Chart_1.png",
      "analysis": "This bar chart shows sales trends over time...",
      "insights": "Notable upward trend in Q3..."
    }
  ]
}
```

## Project Structure

```
project/
├── Agent.py              # Main agent script
├── tools.py              # Custom tools and functions
├── prompt.txt            # Agent instructions and prompts
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .env                 # Environment variables (create this)
├── myvenv/              # Virtual environment
├── charts/              # Extracted chart images
└── extracted_images/    # Extracted embedded images
```

## Key Components

### Agent.py
The main entry point that initializes the AI agent with OpenAI's GPT-4 model and custom tools.

### tools.py
Contains specialized tools for:
- Excel parsing and analysis
- Chart extraction using Spire.XLS
- Image extraction and analysis
- Vision AI integration
- LaTeX compilation

### prompt.txt
Detailed instructions for the agent, defining the expected output format and analysis approach.

## Features in Detail

### Excel Data Analysis
- **Comprehensive Structure Analysis**: Analyzes sheet structure, data types, and relationships
- **Data Quality Metrics**: Identifies missing values, duplicates, and inconsistencies
- **Statistical Insights**: Provides descriptive statistics and outlier detection
- **Performance Tracking**: Monitors extraction time and success rates

### Visual Content Analysis
- **Chart Intelligence**: Understands chart types, trends, and data relationships
- **Image Recognition**: Analyzes embedded images for content and context
- **AI-Powered Insights**: Uses GPT-4 Vision for detailed visual analysis
- **Automated Reporting**: Generates structured reports with key findings

### Advanced Capabilities
- **Multi-Sheet Support**: Handles complex Excel files with multiple worksheets
- **Error Recovery**: Robust error handling with detailed logging
- **Extensible Architecture**: Easy to add new analysis tools and capabilities
- **Performance Optimization**: Efficient processing of large Excel files

## Configuration

The agent behavior can be customized by modifying:

1. **prompt.txt**: Adjust analysis instructions and output format
2. **tools.py**: Add or modify analysis functions
3. **Agent.py**: Change model parameters or add new tools

## Troubleshooting

### Common Issues

1. **Spire.XLS Import Error**
   ```
   pip install Spire.XLS
   ```

2. **OpenAI API Key Not Found**
   - Ensure `.env` file contains valid `OPENAI_API_KEY`
   - Check that the key has sufficient credits

3. **Chart Extraction Fails**
   - Verify Excel file is not corrupted
   - Check if file contains actual charts

4. **Memory Issues with Large Files**
   - Process files in smaller chunks
   - Increase available system memory

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For questions, issues, or feature requests, please create an issue in the repository or contact the development team.

## Changelog

### Latest Version
- Enhanced chart extraction with Spire.XLS
- Added GPT-4 Vision for visual content analysis
- Improved error handling and logging
- Added comprehensive data quality assessment
- Enhanced statistical analysis capabilities

---

**Note**: This agent requires an active OpenAI API key for full functionality. Chart extraction requires the Spire.XLS library which may have licensing considerations for commercial use.
