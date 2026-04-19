# OtoConnect

OtoConnect is a simple tool designed to automate the process of attaching native audio to Anki flashcards, integrating with the **AnkiConnect API**.

It uses a **SQLite** database to track processed **Anki** note data and prevent duplicate processing of notes.

The script searches for notes with empty audio fields and automatically opens a Forvo page so the user can download the corresponding pronunciation audio.

**Note:** This tool was originally designed for personal use. While functional, it may contain specific customizations or edge-case bugs. Feedback is welcome!

## Features

- Automatic SQLite database initialization.
- Automatic Anki app initialization.
- Integration with Anki through AnkiConnect API.
- HTTP-based communication with Anki.
- Assisted audio download and storage workflow.
- Persistent note tracking with database.
- Simple SQLite database queries for stored notes.

## Requirements

- **Python 3.12+**.
- Updated **Anki** desktop app.
- **AnkiConnect** Anki add-on (Code: `2055492159`).
- Python `requests` library.
- Python `tabulate` library.
- Python `watchdog` library.

## Installation

### Installing from `.whl`

1. Download the `.whl` file from the latest release.
2. Open your **Command Prompt or Terminal** and navigate to the folder where the `.whl` file is located.
```bash
cd C:\your\path
```
(Replace `C:\your\path` with the actual path)
3. Run the `pip` command:
```bash
pip install file.whl
```
(Replace `file` with the actual file name)

**Note:** You might use `pipx` as well.

### Installing from Source

1. Cloning the repository:
Open **Git Bash** in the desired folder and run the following command:
```bash
git clone https://github.com/lucarello/OtoConnect.git
```

2. Installing library dependencies:
Open your **Command Prompt or Terminal** in the cloned repository folder and run the following command:
```python
pip install -e .
```

3. Installing Anki dependencies:
    - Open your **Anki** app.
    - Click on **Tools**, and then **Add-ons** (or just press **Ctrl+Shift+A**).
    - Click on **Get Add-ons...** and paste the **AnkiConnect** code (`2055492159`).
    - Click on **Ok** and restart your **Anki**.

**Note:** While it is recommended to use a virtual environment to install the dependencies, you might either install them globally as well.

## Configuration

### Anki Startup
When first running the program, it will ask if the user wants to open Anki during OtoConnect startup.

### Anki Configuration

The script has a built-in **Configuration Wizard**.

The user can configure the Anki deck and the audio or word fields they want to use.

When running the program for the first time, the wizard will activate allowing you to set up:
- Target Anki Deck.
- Field name for the Word (Source).
- Field name for the Audio (Destination).

**Tip:** If you are running the source code, avoid manually editing the `config.json` to prevent format errors. Use the built-in wizard.

### Changing the Search URL (Source Code Only)
By default, the program redirects to **Forvo** with the **Japanese** search tag enabled.
This is currently hardcoded. If you are running from the source and want to change the language (e.g., to French or Spanish), do the following steps:

1. Inside `src/cli/` folder Open `main.py` in your text editor.
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

If you installed OtoConnect through the `.whl` file, you can run `otoconnect` command on your **Command Prompt or Terminal** to start the program. 

**NOTE:** If you are using a **venv**, ensure it is active before trying to run `otoconnect`.

1. Open the Anki app and ensure you are connected to the internet.
2. Run OtoConnect and choose your mode:
    - Use: to start the audio updating process.
    - Configuration: to change the deck/field settings.
    - Data: to check database entries. 
3. The Workflow:
    - OtoConnect will open your browser and search for the word.
    - You *must* download the file **manually**.
    - The program will automatically identify the downloaded file, update the note, and move to the next one.
4. When there are no more notes with empty audio fields, the program will automatically close.

**NOTE 2:** You should not close Anki while using OtoConnect as this will cause errors.

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

- [ ] Remove magic numbers.
- [ ] Add the option to quit during configuration updates.
- [ ] Improve watchdog implementation.
- [ ] Correct `config.json` and `oto_connect_data.db` file location, that made the program inoperable.
- [X] Add `watchdog` library to eliminate the audio file **drag and drop**.

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

Developed by Jub4rte - Luca Maciel Rello.