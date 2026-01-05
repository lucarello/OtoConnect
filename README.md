# OtoConnect

OtoConnect is a simple Python program designed to store audio and update Anki cards faster.

The script searches for notes that contain empty audio fields, automatically opens a web page to download (manually) the corresponding audio for the word.

Since this program was made to help the creator, it has some self-personalized functionalities, which may (and probably will) cause problems during its execution. This is going to be updated in future versions.

## Prerequisites

This program requires the following assets installed:

- **Python 3.x**.
- Updated **Anki** desktop app.
- **AnkiConnect** Anki add-on (Code: `2055492159`).
- Python `requests` library.

## Configuration (Important!)

If you want to use this script for your own Anki decks, do the following:

1. Open `anki_utils.py`.
2. Locate the `get_notes()` function.
3. In the `payload`, inside `params`, locate `query`.
4. Change `'deck:"日本語::Main" ExpressionAudio:'` to `'deck:YOUR_DECK_NAME YOUR_AUDIO_FIELD_NAME:'`, following Anki's pattern.
5. Locate `update_audio()` function.
6. In the `payload`, inside `params`, then `note`, locate `fields`.
7. Change `'ExpressionAudio'` to `'YOUR_AUDIO_FIELD_NAME'`.
8. Save the changes.
9. Open `main.py`.
10. Locate the `main()` function.
11. Locate `for note in note_info:`
12. Locate `word = note['fields']['Expression']['value']`
13. Change `'Expression'` inside the brackets to `'YOUR_WORD_FIELD'`.
14. Save the changes.

## Usage

### Creating a .bat

To use this program, it's highly recommended for you to create a `.bat` file to run it.

Create a `.bat` file, and, in a text editor, paste the following:

```batch
@echo off
python "[YOUR_FOLDER_PATH]\main.py"
pause
```

### Actually using it

1. Open your Anki and be sure you're connected to the internet.
2. Run the `main.py` file (or the `.bat` file).
3. Download the audio at **Forvo** (the page will be automatically open).
4. Drag the file to the terminal or write its path.
5. Press **ENTER**.
6. Repeat until all of your notes are successfully updated.

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

Developed by Jub4rte - Luca Maciel Rello.