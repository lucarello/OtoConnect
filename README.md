# OtoConnect v1.1

OtoConnect is a simple Python program designed to store audio and update Anki notes faster.

The script searches for notes that contain empty audio fields and automatically opens a web page (Forvo) so you can download the corresponding audio for the word.

**Note:** This tool was originally developed for personal use. While functional, it may contain specific customizations or edge-case bugs. Feedback is welcome!

## Prerequisites

### Option 1: Using the executable (.exe)
If you are using the `.exe` file, there are no technical prerequisites other than having your **Anki** app open while using the program.

### Option 2: Running from Source
If you prefer to run your script via Python (whether using a `.bat` file or not), ensure you have the following assets:

- **Python 3.x**.
- Updated **Anki** desktop app.
- **AnkiConnect** Anki add-on (Code: `2055492159`).
- Python `requests` library.

## Configuration

The script has a built-in **Configuration Wizard**.

You can configure the Anki deck and the audio or word fields you want to use.

When you first run the program and try to use it, the wizard will activate allowing you to set up:
- Target Anki Deck
- Field name for the Word (Source)
- Field name for the Audio (Destination)

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
3. The Workflow:
    - OtoConnect will open the browser searching for the word.
    - You *must* download the file **manually**.
    - **Drag and drop** the file into the terminal window.
    - Press **Enter**.
    - The program will update the note and move to the next one.
4. When there are no more notes with empty audio fields, the program will automatically close.

**NOTE:** You should NOT close Anki while using OtoConnect. This may and will cause errors.

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

Developed by Jub4rte - Luca Maciel Rello.