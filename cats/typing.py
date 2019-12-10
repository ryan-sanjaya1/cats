'"""Typing test implementation"""'

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    x = []
    for i in paragraphs:
        if select(i):
            x += [i]
    if k > (len(x)-1):
        return ''
    return x[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def finder(findee):
        status = False
        cleaned_findee = split(remove_punctuation(lower(findee)))
        for i in range(len(cleaned_findee)):
            for k in range(len(topic)):
                if cleaned_findee[i]==topic[k]:
                    status = True
        return status
    return finder
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct, incorrect = 0, 0
    if len(typed_words) == 0 or len(reference_words) == 0:
        return 0.0
    if len(typed_words) == 1 and len(reference_words) == 1:
        if typed_words == reference_words:
            return 100.0
        else:
            return 0.0
    i=0
    while i < min(len(typed_words),len(reference_words)):
        if typed_words[i] == reference_words[i]:
            correct += 1
        else:
            incorrect += 1
        i+= 1
    if len(typed_words)>len(reference_words):
        incorrect += abs((len(reference_words)-len(typed_words)))
    percentage = correct/(correct+incorrect)*100
    return percentage
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    words = len(typed)/5
    per_minute = 60/elapsed
    return per_minute*words
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    i, curr_no, autocorrected = 0, diff_function(user_word,valid_words[0],limit), valid_words[0]
    for i in range(len(valid_words)):
        each_word = valid_words[i]
        if user_word == each_word:
            return user_word
        elif diff_function(user_word,each_word,limit)<=limit:
            prev_no, curr_no = curr_no, min(diff_function(user_word,each_word,limit),curr_no)
            if curr_no != prev_no:
                autocorrected = each_word
    if diff_function(user_word,autocorrected,limit)>limit:
        return user_word    
    else:
        return autocorrected
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if limit < 0:
        return 0
    elif len(start)==0 or len(goal)==0:
        return max(len(start),len(goal))
    else:
        if start[0] != goal[0]:
            return 1 + swap_diff(start[1:],goal[1:],limit-1)
        else:
            return swap_diff(start[1:],goal[1:],limit)   
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    # BEGIN PROBLEM 7
    if limit < 0:
        return 0   
    elif len(start)==0 or len(goal)==0:
        return max(len(start),len(goal))
    else:
        add_diff = 1 + edit_diff(start,goal[1:],limit-1)
        remove_diff = 1 + edit_diff(start[1:],goal,limit-1)
        if start[0] != goal[0]:
            substitute_diff = 1 + edit_diff(start[1:],goal[1:],limit-1)
        else:
            substitute_diff = edit_diff(start[1:],goal[1:],limit)
        return min(add_diff,remove_diff,substitute_diff)
    # END PROBLEM 7

def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    # This is a lightly modified version of accuracy from question 3, which returns the accuracy as a float instead of a percentage
    def list_accuracy(typed_words,reference_words):
        correct, incorrect = 0, 0
        if not typed_words or not reference_words:
          return 0.0
        for i in range(min(len(typed_words),len(reference_words))):
            if typed_words[i] == reference_words[i]:
                correct += 1
            else:
                return correct/len(reference_words)
        if len(typed_words)!=len(reference_words):
            incorrect += abs((len(reference_words)-len(typed_words)))
        percentage = correct/(correct+incorrect)
        return percentage
    progress=list_accuracy(typed,prompt)
    send({'id': id, 'progress': progress})
    return progress
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9   
    shortest_times = []
    for player in range(n_players):
        #Creates empty lists for each player
        shortest_times += [[]]       
    for words in range(n_words):
        min_time = 9e99
        for player in range(n_players):
            word_time = elapsed_time(word_times[player][words+1])-elapsed_time(word_times[player][words])
            if word_time < min_time:
                min_time = word_time
        for player in range(n_players):
            word_time = elapsed_time(word_times[player][words+1])-elapsed_time(word_times[player][words])
            if word_time < min_time + margin:
                shortest_times[player].append(word(word_times[player][words+1]))         
    return shortest_times
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
