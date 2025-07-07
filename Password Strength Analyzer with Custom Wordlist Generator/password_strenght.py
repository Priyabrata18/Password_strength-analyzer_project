import argparse
import nltk
from zxcvbn import zxcvbn
import string
import os

# Download required NLTK resources
nltk.download('words')
from nltk.corpus import words

def analyze_password(password):
    result = zxcvbn(password)
    print(f"\nPassword Strength Score: {result['score']}/4")
    print(f"Estimated Guesses: {result['guesses']}")
    print(f"Feedback: {result['feedback']['warning'] or 'No warnings.'}")
    return result

def generate_wordlist(inputs, years=range(1990, 2031)):
    leet_subs = str.maketrans('aeios', '43105')
    wordlist = set()

    for word in inputs:
        wordlist.add(word.lower())
        wordlist.add(word.upper())
        wordlist.add(word.capitalize())
        wordlist.add(word.translate(leet_subs))
        for year in years:
            wordlist.add(f"{word}{year}")
            wordlist.add(f"{word.translate(leet_subs)}{year}")

    # Add common dictionary words (optional)
    common_words = [w for w in words.words() if len(w) <= 5]
    wordlist.update(common_words)
    return wordlist

def export_wordlist(wordlist, filename):
    with open(filename, 'w') as f:
        for word in sorted(wordlist):
            f.write(f"{word}\n")
    print(f"\nWordlist exported successfully to: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer & Custom Wordlist Generator")
    parser.add_argument('-p', '--password', type=str, required=True, help='Password to analyze')
    parser.add_argument('-i', '--inputs', nargs='+', required=True, help='Custom user inputs (name, pet, date)')
    parser.add_argument('-o', '--output', type=str, default='custom_wordlist.txt', help='Output wordlist filename')
    args = parser.parse_args()

    analyze_password(args.password)
    wordlist = generate_wordlist(args.inputs)
    export_wordlist(wordlist, args.output)

if __name__ == "__main__":
    main()
