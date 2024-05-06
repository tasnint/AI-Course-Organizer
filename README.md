# AI-Course-Organizer
# Course Organizer Tool


## Description
This Python application automates the management and organization of course-related documents by monitoring a specified download directory. When new files matching specific course codes are detected, they are copied into dedicated, organized folders on the desktop. This tool is especially useful for students or educators who handle numerous documents and want to maintain an organized desktop.

## Features
- **Dynamic Course Addition:** Users can add new course codes at runtime, which the application will then monitor for document matches.
- **Automated File Organization:** Automatically sorts files into course-specific folders based on the course code present in the file name, with further organization by the date of addition.
- **Real-Time Monitoring:** Continuously monitors the download directory for new files, reducing manual sorting efforts.

## Technologies and Libraries Used
### Python Libraries
- **`os` and `shutil`**: Handle file system operations like reading directories and copying files.
- **`datetime`**: Manages date and time information, crucial for organizing files by the date they are processed.
- **`schedule`**: Allows the application to perform periodic checks of the directory to process and organize files.

### LangChain
LangChain is used for its powerful language processing capabilities, integrating seamlessly with OpenAI services. It provides an efficient way to work with large language models and implement complex language understanding tasks with less code and integration overhead.

## Installation
To run this application, you need Python installed on your system along with the necessary dependencies. Follow the steps below to set up and run the program:

### Clone the Repository
First, clone this repository to your local machine using:
git clone [URL-of-the-repository]
cd [repository-name]

### Install Dependencies which can be found in requirements.txt
Ensure that you have pip installed and then run:
pip install -r requirements.txt
This will install all the necessary Python packages including schedule, datetime, and other required libraries as listed in requirements.txt.

### Running the Application
To start the application, use the following command:
python main.py
The program will prompt you to add a course code. If you choose to add a course, it will start monitoring the specified downloads directory for files containing the course code in their names, copying them to a designated directory on the desktop.

### Configuration
Source Directory: Modify the source_dir variable in main.py to change the directory that the program monitors.

### Destination Directory: 
By default, the destination is set to the user's desktop. This can be changed by modifying the destination_dir path construction in the main() function.
