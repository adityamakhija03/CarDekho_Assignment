# CSV Data Insights Application

## Overview

CSV Data Insights is a powerful Gradio-based application that allows users to upload CSV files, ask natural language questions about the data, and generate visualizations - all within a clean, intuitive interface. The application leverages local Large Language Models (LLMs) through Ollama to provide intelligent answers and insights about your data without sending it to external APIs.

## Features

- **CSV File Upload**: Easily upload and analyze CSV files up to 25MB
- **Natural Language Querying**: Ask questions about your data in plain English
- **AI-Powered Insights**: Get intelligent answers powered by Llama 3.1
- **Data Visualization**: Generate and view charts and graphs without leaving the app
- **PDF Reports**: Export data insights and recommendations for stakeholders
- **Local Execution**: All processing happens on your machine for data privacy

## Screenshots
![Data Query](./Screenshot%202025-03-12%20220509.png)
![Sample Visualization](./Screenshot%202025-03-12%20220216.png)
![PDF Report interface](./Screenshot%202025-03-12%20215927.png)
![PDF Report Example](./Screenshot%202025-03-12%20220032.png)

## Installation

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- At least 8GB RAM for optimal performance

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adityamakhija03/CarDekho_Assignment.git
   cd csv-data-insights
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download and run the required Llama model with Ollama:
   ```bash
   ollama pull llama3.1-8b
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:7860`

3. Use the application:
   - Upload your CSV file using the file upload button
   - Wait for the data to load and process
   - Ask questions about your data in the question input field
   - Request visualizations or insights by specifying what you want to see
   - Generate PDF reports for stakeholder presentations

## Example Queries

Here are some example questions you can ask:

- "What is the average house price in this dataset?"
- "Show me the correlation between house size and price"
- "What are the top 5 most expensive properties and their locations?"
- "What insights can you give me about this housing market data?"
- "Create a report with recommendations for real estate investment based on this data"

## Project Structure

```
csv-data-insights/
│
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies            
│
├── modules/                # Application modules
│   ├── data_handler.py     # CSV handling and data processing
│   ├── model_handler.py    # Pydantic AI implementation for LLM interaction
│   ├── pdf_generator.py    # PDF report generation functionality
│   └── ui.py               # Gradio interface components
|
|---README.md

```

## Configuration

The application can be configured by modifying the following environment variables:

- `OLLAMA_HOST`: URL of Ollama API (default: http://localhost:11434)
- `MODEL_NAME`: LLM model to use (default: llama3.1-8b)
- `MAX_FILE_SIZE_MB`: Maximum CSV file size in MB (default: 25)
- `DEBUG_MODE`: Enable debug logging (default: False)

## Technical Details

- **Frontend**: Gradio 4.0+
- **LLM Integration**: Ollama with Llama 3.1 8B (Q4 quantization)
- **Agent Framework**: Pydantic AI for structured query processing
- **Visualization**: Matplotlib and Seaborn, embedded in Gradio
- **PDF Generation**: ReportLab

## Troubleshooting

**Q: The application is running slowly when processing large files.**  
A: Try using a smaller model or increasing the quantization level in `modules/llm_agent.py`.

**Q: I'm getting "Model not found" errors.**  
A: Ensure Ollama is running and that you've pulled the model with `ollama pull llama3.1-8b`.

**Q: Visualizations are not displaying properly.**  
A: Check that your CSV contains numerical data suitable for plotting. The app needs appropriate columns for X and Y axes.

**Q: The PDF generation is failing.**  
A: Ensure you have sufficient permissions to write to the output directory and that ReportLab is properly installed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Gradio](https://gradio.app) for the web interface framework
- [Ollama](https://ollama.ai) for local LLM infrastructure
- [Pydantic AI](https://docs.pydantic.dev/latest/integrations/ai/) for structured AI output
- [ReportLab](https://www.reportlab.com) for PDF generation