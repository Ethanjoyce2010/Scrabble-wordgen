# Multilingual Scrabble Maximum Score Calculator

This Python script calculates the maximum possible score for words in Scrabble across multiple languages, including English, French, and Spanish. It downloads word lists from online sources, checks for valid words, and applies Scrabble scoring rules to find the highest-scoring words possible.

## Features
- Supports **English, French, and Spanish** Scrabble configurations
- Downloads word lists from online sources
- Uses letter values and tile distributions specific to each language
- Calculates the maximum possible score for words
- Displays detailed score breakdowns
- User-friendly menu for selecting a language and viewing results

## Requirements
- Python 3.x
- Internet connection (for downloading dictionaries)

## Installation
Download the.py

## Usage
Run the script using Python:
```sh
python scrabble-calculator.py
```
Follow the on-screen prompts to select a language and view the highest-scoring words.

## How It Works
1. The script presents a **menu** for selecting a language.
2. It downloads the word list from the specified **online dictionary**.
3. It **validates words** based on available Scrabble tiles.
4. It calculates the **maximum possible score** for each word.
5. It **sorts and displays** the top 10 highest-scoring words.
6. Users can view a **detailed breakdown** of how the score is calculated.

## Example Output
```
🏆 TOP 10 HIGHEST SCORING POSSIBLE WORDS IN ENGLISH SCRABBLE:
==================================================
1. EXAMPLE: 50 points
   Letter breakdown: E(1), X(8), A(1), M(3), P(3), L(1), E(1)
   Word multiplier: x2
   Final score: 100 points
```

## Contributing
Feel free to fork the repository and submit pull requests for improvements or additional language support.

## License
This project is licensed under the MIT License.

## Author
[Your Name] - [Your GitHub Profile]

