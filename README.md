Keylogger Mini-Project

Project Overview
This mini project will show how the conceptual and practical functionality of a keylogger developed using software and implemented in Python works. It is a learning project wherein the functionality of capturing keyboard events at a system level and logging these events for analysis purposes will be comprehended.
The application contains a simple GUI, which helps the user initiate the key logging process while viewing how the keystroke information is stored in structured formats.

**Disclaimer: The development of this project is specifically for educational and awareness purposes and for defensive research only. Using a licensed keylogger is unethical and illegal.**

Objectives
For the study of handling keyboard events through the use of system-level listeners
In order to comprehend how keystroke information can be extracted, classified, and processed,
For the demonstration of multithreading for background execution of monitoring tasks
In consideration of possible security threats posed by keystroke tracking

Technologies Used
Programming Language: Python 3.11
GUI Framework: Tkinter
Event Listeners
To detect keystrokes

Data Storage:
Text file (logs.txt)
JSON file (logs.json)
Concurrency: Python threading module

Systems Architecture
GUI Layer (Tkinter)
It offers an easy interface consisting of the button to initiate the keylogger.
All executed on main thread.
Keylogger Engine (pyn)
Handles keyboard events such as key press, release, and holding.
It runs in a background daemon thread.
Data Logging Module
Stores sequential keystrokes in a text file.
Stores data of events (Pressed, Released, Signed, ReleasedWithOptionFlags, ReleasedWithUnicodeChar
Passed Coursework
Upon starting the application, a GUI window opens up.
Upon clicking "Start Keylogger", it triggers the start of the keyboard surveillance process through the creation of

It recognizes each keystroke event as:
-Pressed
Held
Released
"The data captured is: "
Appended to the logs.json file in a structured and human-readable format.
Recorded as a continuous stream in logs.txt.

Output Files
logs.json -
Stores key event logs for analysis and research.
logs.txt -
Carries a text data value of keystrokes captured.

Key Learning Outcomes
Understanding the interception of keyboard events at a low level
Applying the concept of multithreading to GUI programming
Safe handling and organized storage of gathered input information
Awareness of ethical implications and cybersecurity risks

