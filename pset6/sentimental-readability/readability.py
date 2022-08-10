# TODO
from cs50 import get_string
# counting letters, words , sentences


def count_letters_words_sentences(text):
    letters = 0.0
    words = 1.0
    sentences = 0.0
    for c in text:

        if c.isalpha():
            letters = letters + 1
        if c.isspace():
            words = words + 1
        if c == "." or c == "!" or c == "?":
            sentences = sentences + 1

    return letters, words, sentences


# main
def main():
    text = get_string("Text: ")
    # tuple destructuring
    letters, words, sentences = count_letters_words_sentences(text)
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    if (index > 16):

        print("Grade 16+")

    elif (index < 1):

        print("Before Grade 1")

    else:

        print(f"Grade {index}",)


# calling main
if __name__ == "__main__":
    main()