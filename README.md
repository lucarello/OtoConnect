# OtoConnect

OtoConnect is a simple tool designed to automate the process of attaching native audio to Anki flashcards, integrating with the **AnkiConnect API**.

It uses a **SQLite** database to track processed **Anki** note data and prevent duplicate processing of notes.

The script searches for notes with empty audio fields and automatically opens a Forvo page so the user can download the corresponding pronunciation audio.

**Note:** This tool was originally designed for personal use. While functional, it may contain specific customizations or edge-case bugs. Feedback is welcome!

**New in 1.1.3:** Simple **SQLite** database queries were implemented, allowing the user to check stored data about their Anki notes. Also, the code became more modular, optimizing it.

## Features

- Automatic SQLite database initialization.
- Integration with Anki through AnkiConnect API.
- HTTP-based communication with Anki.
- Assisted audio download and storage workflow.
- Persistent note tracking with database.
- Simple SQLite database queries for stored notes.

## Requirements

### Option 1: Using the executable (.exe)
If you are using the `.exe` file, there are no technical requirements other than having your **Anki** app open while using the program.

### Option 2: Running from Source
If you prefer to run your script via Python (whether using a `.bat` file or not), ensure you have the following assets:

- **Python 3.x**.
- Updated **Anki** desktop app.
- **AnkiConnect** Anki add-on (Code: `2055492159`).
- Python `requests` library.
- Python `tabulate` library.

## Installation

**Note 1:** The first two steps consider you are a source-code user. If you are using the `.exe` file, you may skip them.

1. Cloning the repository:
Open **Git Bash** in the desired folder and run the following command:
```git
git clone https://github.com/lucarello/OtoConnect.git
```

2. Installing library dependencies:
Open your **Command Terminal** in the cloned repository folder and run the following command:
```python
pip install -r requirements.txt
```

3. Installing Anki dependencies:
    - Open your **Anki** app.
    - Click on **Tools**, and then **Add-ons** (or just press **Ctrl+Shift+A**).
    - Click on **Get Add-ons...** and paste the **AnkiConnect** code (`2055492159`).
    - Click on **Ok** and restart your **Anki**.


**Note 2:** If you're not using **Git Bash** to clone the repository, search for the correct installation process for your tool.

**Note 3:** While it is recommended to use a virtual environment to install the dependencies, you might install them globally as well.

## Configuration

The script has a built-in **Configuration Wizard**.

You can configure the Anki deck and the audio or word fields you want to use.

When you first run the program and try to use it, the wizard will activate allowing you to set up:
- Target Anki Deck.
- Field name for the Word (Source).
- Field name for the Audio (Destination).

**Tip:** If you are running the source code, avoid manually editing the `config.json` to prevent format errors. Use the built-in wizard.

### Changing the Search URL (Source Code Only)
By default, the program redirects to **Forvo** with the **Japanese** search tag enabled.
This is currently hardcoded. If you are running from the source and want to change the language (e.g., to French or Spanish), do the following steps:

1. Open `main.py` in your text editor.
2. Search for the line
```python 
webbrowser.open_new_tab(f'https://forvo.com/word/{word}/#ja')
```
3. Change the language code from `#ja` to your preferred one.
4. Save the changes and close `main.py`

You may also want to change the website. To do so, you must change the line
```python 
'https://forvo.com/word/{word}/#ja'
```
to your preferred website.
**NOTE:** Ensure `{word}` is still present in the code so you can correctly search for it.

## Usage

1. Open the Anki app and ensure you are connected to the internet.
2. Run OtoConnect and choose your mode:
    - Use: to start the audio updating process.
    - Configuration: to change the deck/field settings.
    - Data: to check database entries. 
3. The Workflow:
    - OtoConnect will open the browser searching for the word.
    - You *must* download the file **manually**.
    - **Drag and drop** the file into the terminal window.
    - Press **Enter**.
    - The program will update the note and move to the next one.
4. When there are no more notes with empty audio fields, the program will automatically close.

**NOTE:** You should NOT close Anki while using OtoConnect. This may and will cause errors.

## Database

OtoConnect uses a **SQLite database** to persist information about processed Anki notes.

The database and table are created during first execution if they do not exist. Also, if an Anki note is already stored in the database, it won't be stored again.

Stored data includes:

- Note ID. -> **Primary Key**
- Word.
- Audio file name.
- Audio update date.
- Note status (**audioless** or **updated**).

## Future Improvements

- Code refactoring.
- Add the option to automatically open Anki when opening the program.
- Add the option to quit during configuration updates.
- Make connection errors stop execution if Anki is not open, instead of trying to connect until it is open. 
- Add `watchdog` library to eliminate the audio file **drag and drop**.


## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

Developed by Jub4rte - Luca Maciel Rello.