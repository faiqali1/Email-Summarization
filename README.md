# Project Name

This project is a text processing and summarization application that utilizes the following technologies:

- [Sumy](https://github.com/miso-belica/sumy): A library for automatic text summarization.
- [Streamlit](https://www.streamlit.io/): A framework for building interactive UIs.
- [NLTK](https://www.nltk.org/): A natural language processing library.

## Installation

To run this application, you need to have Docker and Docker Compose installed on your machine. Follow the steps below to get started:

1. Clone this repository:
2. Navigate to the project directory
3. Build and run the Docker containers using Docker Compose: `docker-compose up`

## Setting Up Google API

To connect to the Gmail API, follow these steps to create a `credentials.json` file:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to the **API & Services** dashboard and enable the **Gmail API**.
4. Go to the **Credentials** section on the left menu.
5. Click on **Create Credentials** and select **OAuth 2.0 Client ID**.
6. Configure the OAuth consent screen by providing the necessary information.
7. Choose **Desktop app** as the application type and click **Create**.
8. Download the `credentials.json` file and save it in the project directory.

## Usage

Once the Docker containers are running, you can access the application by opening your web browser and navigating to `http://localhost:8501`. From there, you can interact with the UI to process and summarize text.

### Summarizing Emails

1. Click on the "Authenticate with Gmail" button.
2. Follow the instructions to authenticate with your Gmail account.
3. Select an email from the dropdown to see its summary.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.
