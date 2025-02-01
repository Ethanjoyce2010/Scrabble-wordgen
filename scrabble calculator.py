import urllib.request
import ssl
from time import time
import sys
import os

# Scrabble configurations for different languages
LANGUAGE_CONFIGS = {
    "English": {
        "name": "English",
        "dict_url": "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt",
        "letter_values": {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
            'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
            'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
        },
        "tile_distribution": {
            'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2, 'I': 9,
            'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6, 'O': 8, 'P': 2, 'Q': 1, 'R': 6,
            'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1, 'Y': 2, 'Z': 1
        }
    },
    "French": {
        "name": "French",
        "dict_url": "https://raw.githubusercontent.com/Taknok/French-Wordlist/refs/heads/master/francais.txt",
        "letter_values": {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
            'J': 8, 'K': 10, 'L': 1, 'M': 2, 'N': 1, 'O': 1, 'P': 3, 'Q': 8, 'R': 1,
            'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 10, 'X': 10, 'Y': 10, 'Z': 10,
            'É': 1, 'È': 1, 'Ê': 1, 'Ë': 1, 'Â': 1, 'Î': 1, 'Ô': 1, 'Û': 1, 'À': 1
        },
        "tile_distribution": {
            'A': 9, 'B': 2, 'C': 2, 'D': 3, 'E': 15, 'F': 2, 'G': 2, 'H': 2, 'I': 8,
            'J': 1, 'K': 1, 'L': 5, 'M': 3, 'N': 6, 'O': 6, 'P': 2, 'Q': 1, 'R': 6,
            'S': 6, 'T': 6, 'U': 6, 'V': 2, 'W': 1, 'X': 1, 'Y': 1, 'Z': 1,
            'É': 2, 'È': 1, 'Ê': 1, 'Ë': 1, 'Â': 1, 'Î': 1, 'Ô': 1, 'Û': 1, 'À': 1
        }
    },
    "Spanish": {
        "name": "Spanish",
        "dict_url": "https://raw.githubusercontent.com/ManiacDC/TypingAid/refs/heads/master/Wordlists/Wordlist%20Spanish.txt",
        "letter_values": {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
            'J': 8, 'K': 8, 'L': 1, 'M': 3, 'N': 1, 'Ñ': 8, 'O': 1, 'P': 3, 'Q': 5,
            'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 8, 'X': 8, 'Y': 4, 'Z': 10,
            'Á': 1, 'É': 1, 'Í': 1, 'Ó': 1, 'Ú': 1, 'Ü': 1
        },
        "tile_distribution": {
            'A': 12, 'B': 2, 'C': 4, 'D': 5, 'E': 12, 'F': 1, 'G': 2, 'H': 2, 'I': 6,
            'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 5, 'Ñ': 1, 'O': 9, 'P': 2, 'Q': 1,
            'R': 5, 'S': 6, 'T': 4, 'U': 5, 'V': 1, 'W': 1, 'X': 1, 'Y': 1, 'Z': 1,
            'Á': 1, 'É': 1, 'Í': 1, 'Ó': 1, 'Ú': 1, 'Ü': 1
        }
    }
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu(title, options):
    """Print a formatted menu with options."""
    clear_screen()
    print(f"🎲 {title} 🎲")
    print("=" * 50)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("=" * 50)

def get_menu_choice(max_choice):
    """Get a valid menu choice from the user."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-" + str(max_choice) + "): "))
            if 1 <= choice <= max_choice:
                return choice
            print(f"Please enter a number between 1 and {max_choice}")
        except ValueError:
            print("Please enter a valid number")

def print_progress(count, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """Print a progress bar."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (count / float(total)))
    filled_length = int(length * count // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if count == total:
        print()

def download_dictionary(language_config):
    """Download a word list for the specified language."""
    print(f"\n📚 Downloading {language_config['name']} dictionary...")
    context = ssl._create_unverified_context()
    
    try:
        response = urllib.request.urlopen(language_config['dict_url'], context=context)
        words = response.read().decode('utf-8', errors='ignore').upper().split('\n')
        valid_words = {word.strip() for word in words if word.strip().isalpha()}
        print(f"✅ Successfully downloaded {len(valid_words):,} words")
        return valid_words
    except:
        print(f"❌ Could not download dictionary. Using sample words...")
        return {f"SAMPLE{i}" for i in range(10)}

def calculate_max_score(word, letter_values, letter_multipliers=None, word_multiplier=1):
    """Calculate the maximum possible score for a word."""
    if letter_multipliers is None:
        letter_multipliers = [1] * len(word)
    
    base_score = sum(letter_values.get(letter, 0) * multiplier 
                    for letter, multiplier in zip(word, letter_multipliers))
    
    return base_score * word_multiplier

def find_best_placement(word, config):
    """Find the best possible score for a word."""
    max_score = 0
    best_letter_multipliers = None
    best_word_multiplier = 1
    
    for triple_word in [True, False]:
        for double_word in [True, False]:
            word_mult = (3 if triple_word else 1) * (2 if double_word else 1)
            letter_mults = [1] * len(word)
            
            letter_values = [(config['letter_values'].get(c, 0), i) for i, c in enumerate(word)]
            letter_values.sort(reverse=True)
            
            if len(word) >= 1:
                letter_mults[letter_values[0][1]] = 3
            if len(word) >= 2:
                letter_mults[letter_values[1][1]] = 2
            
            score = calculate_max_score(word, config['letter_values'], letter_mults, word_mult)
            
            if score > max_score:
                max_score = score
                best_letter_multipliers = letter_mults
                best_word_multiplier = word_mult
    
    return max_score, best_letter_multipliers, best_word_multiplier

def is_word_possible(word, config):
    """Check if a word can be formed with the available tiles."""
    available_tiles = config['tile_distribution'].copy()
    
    for letter in word:
        if letter not in available_tiles or available_tiles[letter] <= 0:
            return False
        available_tiles[letter] -= 1
    return True

def find_highest_scoring_words(dictionary, config, num_results=10):
    """Find the highest scoring possible words."""
    print(f"\n🔍 Analyzing possible words in {config['name']}...")
    word_scores = []
    start_time = time()
    
    valid_words = [word for word in dictionary if len(word) <= 15]
    print(f"📊 Found {len(valid_words):,} words of valid length (≤15 letters)")
    
    print("\n⚙️ Calculating scores for each word...")
    for i, word in enumerate(valid_words):
        if i % 1000 == 0:
            print_progress(i, len(valid_words), 
                         prefix='Progress:', 
                         suffix=f'({i:,}/{len(valid_words):,} words)')
        
        if is_word_possible(word, config):
            score, letter_mults, word_mult = find_best_placement(word, config)
            word_scores.append((score, word, letter_mults, word_mult))
    
    print(f"\n✅ Analysis complete! Time taken: {time() - start_time:.2f} seconds")
    return sorted(word_scores, reverse=True)[:num_results]

def print_score_breakdown(word, config, letter_multipliers, word_multiplier):
    """Print a detailed breakdown of the score calculation."""
    print(f"\nScore breakdown for '{word}':")
    print("-" * 50)
    
    base_scores = []
    for letter, multiplier in zip(word, letter_multipliers):
        base_score = config['letter_values'].get(letter, 0)
        final_score = base_score * multiplier
        multiplier_text = f"(×{multiplier})" if multiplier > 1 else ""
        base_scores.append(final_score)
        print(f"Letter {letter}: {base_score} points {multiplier_text} = {final_score}")
    
    subtotal = sum(base_scores)
    print("-" * 50)
    print(f"Subtotal: {subtotal} points")
    
    if word_multiplier > 1:
        print(f"Word multiplier: ×{word_multiplier}")
        print(f"Final score: {subtotal * word_multiplier} points")

def main():
    while True:
        # Display language selection menu
        languages = list(LANGUAGE_CONFIGS.keys())
        print_menu("MULTILINGUAL SCRABBLE MAXIMUM SCORE CALCULATOR",
                  languages + ["Exit"])
        
        choice = get_menu_choice(len(languages) + 1)
        
        if choice == len(languages) + 1:
            print("\n👋 Thanks for using the Multilingual Scrabble Calculator!")
            break
        
        # Get selected language configuration
        selected_language = languages[choice - 1]
        config = LANGUAGE_CONFIGS[selected_language]
        
        # Download dictionary and find highest scoring words
        dictionary = download_dictionary(config)
        top_words = find_highest_scoring_words(dictionary, config)
        
        # Display results
        print(f"\n🏆 TOP 10 HIGHEST SCORING POSSIBLE WORDS IN {config['name'].upper()} SCRABBLE:")
        print("=" * 50)
        for i, (score, word, letter_mults, word_mult) in enumerate(top_words, 1):
            print(f"\n{i}. {word}: {score} points")
            print_score_breakdown(word, config, letter_mults, word_mult)
        
        input("\nPress Enter to return to the language menu...")

if __name__ == "__main__":
    main()