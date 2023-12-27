"""
Keyword Counter and Duplicate Checker
"""

# Import
import tkinter as tk
from tkinter import messagebox


def check_keywords():
    """
    Checks and removes duplicates from keywords then returns a unique
    keyword list along with it's count.

    Takes 'input_txt' and strips any leading or trailing spaces. Splits
    'input_txt' on ', ' and creates 'keyword_list'. If 'keyword_list' is
    empty it notifies that no keywords have been entered. Else it takes
    'keyword_list' and removes duplicates by turning 'keyword_list' into
    a set of dictionary keys with 'dict.fromkeys' and then casting it to
    list 'keywords_clean'. Checks the length of 'keyword_list' against
    that of 'keywords_clean'. If their lengths are not equal it loops
    through the words in 'keywords_clean' and counts how many times each
    word appears in 'keyword_list'. If the word appears more than once
    it is appended to the list 'duplicate_keywords'. When all the words
    in 'keywords_clean' have been looped through a message box is
    displayed telling the user duplicates have been found and displaying
    'duplicate_keywords', 'keywords_clean', and count of
    'keywords_clean'. Else it displays a message box saying
    'keyword_list' has no duplicates and providing count of
    'keyword_list'.
    """
    duplicate_keywords = []
    keyword_string = input_txt.get("1.0", tk.END)
    space_stripped_keyword_string = keyword_string.strip()
    comma_stripped_keyword_string = space_stripped_keyword_string.rstrip(",")
    keyword_list = comma_stripped_keyword_string.split(", ")
    if keyword_list == [""]:
        messagebox.showinfo(
            "No Keywords Detected",
            "Please enter your keyword list in the text box to proceed.",
        )
    else:
        keywords_clean = list(dict.fromkeys(keyword_list))
        if len(keyword_list) != len(keywords_clean):
            for word in keywords_clean:
                if keyword_list.count(word) > 1:
                    duplicate_keywords.append(word)
            messagebox.showinfo(
                "Duplicates Found",
                f"These keyword(s) have duplicates: {duplicate_keywords}\n\n"
                f"Here is your list with duplicates removed:\n\n"
                f"{', '.join(keywords_clean)}\n\n"
                f"Your unique keyword count is: {len(keywords_clean)}\n\n"
                f"The unique list has been copied to your clipboard for "
                f"convenience.",
            )
            root.clipboard_clear()
            root.clipboard_append(f"{', '.join(keywords_clean)}")

        else:
            messagebox.showinfo(
                "Clean List",
                f"Congratulations!\n\nThere are no duplicates in your list.\n"
                f"\nYour unique keyword count is: {len(keyword_list)}",
            )


# Root Window
root = tk.Tk()
root.title("Keyword Checker")

# Input and Output Frames
input_frm = tk.Frame(root)
button_frm = tk.Frame(root)
input_frm.pack(padx=10, pady=5)
button_frm.pack(padx=10, pady=5)

# Input Frame Widgets
input_lbl = tk.Label(
    input_frm,
    text="Enter your keyword list.\nEnsure all items are separated by a COMMA "
    "followed by a SINGLE space.",
)
input_txt = tk.Text(input_frm, height=20, wrap="word")
input_lbl.pack()
input_txt.pack()

# Button Frame Widgets
check_btn = tk.Button(
    button_frm, text="Check Keywords", command=check_keywords
)
check_btn.pack()

# Tkinter Loop
root.mainloop()
