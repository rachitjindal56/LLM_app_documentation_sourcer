# Developer Personal Assistant

This Streamlit application serves as a Developer Personal Assistant, designed to assist users in finding documentation, extracting data from the open internet, and iterating over databases. Users can input queries or thoughts related to programming, and the assistant will provide relevant information.

This application is a LLM Personal Assistant Agent that involves use of OpenAI GPT-3.5-turbo capabilities and features like function calling and prompt engineering. The application has been designed to query the internet for information using Metaphor API and search for information realted to developer documentation, news, articles, general information, etc.

## Prerequisites

Before running the application, ensure that you have the necessary dependencies installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## How to Use

1. Run the Python script containing the provided code.

```bash
streamlit run streamlitapp.py
```

2. Access the application through your web browser. The application interface will allow you to input your query or thoughts related to programming.

```bash
Local URL: http://localhost:8501
Network URL: http://your-ip-address:8501
```

## Application Features

- **Query Input**: Enter your programming-related query or thoughts in the text area provided.
  
- **Submit Button**: Click the "Submit" button to initiate the query processing.

- **Result Display**:
  - If the query pertains to data, the application will display the input query as a subheading and the corresponding results below it.
  - If the query pertains to documentation, the application will display the code snippet or documentation, considering the specified programming language. If no language is specified, it will display the documentation without language-specific formatting.
  
- **Status Display**:
  - Before clicking the "Submit" button, the application will display a message indicating to press the button to start exploring.
  - After clicking the button, the application will process the query and display the results accordingly.

## Session State Variables

The application utilizes session state variables to manage user input and application status:

- `st.session_state.type`: Stores the type of information retrieved (data or documentation).
- `st.session_state.language`: Stores the programming language for formatting documentation.
- `st.session_state.status`: Stores the status of the application (True if the query has been submitted, False otherwise).

## Note

This application uses the Streamlit framework to create a user-friendly interface. Ensure that you have an active internet connection to access external resources if the queries involve internet-based data extraction.

Feel free to modify the code and customize the application according to your specific requirements. If you encounter any issues or have suggestions for improvements, please let us know.

[EmailID](rachitjindal56@gmail.com)