# facebook-auto-post
Auto Post in your Marketplace for Facebook.

## Description
Auto Post in your Marketplace for Facebook is an automated tool that allows you to seamlessly post and manage your products and services on Facebook Marketplace. This application utilizes Python with Selenium to automate the posting process and retrieves the necessary data from your locally stored SQLite database.

![🤖_Facebook_Auto_Post_Marketplace_para_No_TécnicosExpress](https://github.com/eselejuanito/facebook-auto-post/assets/10732249/3e31e3d7-8d2b-475d-ac54-d09c9a91bf3a)

## Video Tutorial
Spanish
[Full Video with explanation](https://youtu.be/OKwrIdM0lrY)
[Short Video about the Project](https://youtube.com/shorts/o9EwFgHPKBY?feature=share)

English
[Full Video with explanation](https://youtu.be/UNWULh6jlZc)
[Short Video about the Project](https://youtube.com/shorts/Knio3G8qBa8?feature=share)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [Contact](#contact)

## Features

- Automated posting of products and services on Facebook Marketplace.
- Retrieve data from your locally stored SQLite database for seamless posting.
- Add tags and emojis for your posts.

## Prerequisites

Before using this tool, ensure that you have the following:

- Python installed on your system.
- Selenium library installed.
- SQLite database with the necessary data for your Marketplace posts.
- Firefox
- geckodriver.exe

## Installation
   
1. Clone the repository:

   ```bash
   git clone https://github.com/eselejuanito/facebook-auto-post.git
   ```

2. Navigate to the project directory:

   ```bash
   cd auto-post-facebook-marketplace
   ```

3. Create an virtual enviroment 

   ```bash
   python -m venv env
   ```
   
   Then acvivate it.
   
   ```bash
   env\Scripts\activate
   ```
   
4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
5. Make a copy and rename config_example.ini to config.ini. Change your user, password and right path of your post's photos.

6. Run python create_database.py and add your data in the table name 'post'. 
   ```bash
   python create_database.py
   ```
   
7. Run python app.py
   ```bash
   python app.py
   ```


## Usage

1. Configure your SQLite database with the necessary product/service data.
2. Run the tool:

   ```bash
   python app.py
   ```

   The tool will automate the posting process.

## Contribution

Contributions are welcome! If you have any suggestions, enhancements, or bug fixes, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## Contact

For any questions, suggestions, or feedback, please feel free to contact me at [eselejuanito](https://linktr.ee/eselejuanito).

For help me 💰:
paypal.me/eselejuanito
