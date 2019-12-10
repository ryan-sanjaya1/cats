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
    curr_no = diff_function(user_word,valid_words[0],limit)
    i = 0
    while i < len(valid_words):
        if i == 0:
            autocorrected = valid_words[0]
        each_word = valid_words[i]
        if user_word == valid_words[i]:
            return user_word
        if diff_function(user_word,each_word,limit)<=limit:
            prev_no = curr_no
            curr_no = min(diff_function(user_word,each_word,limit),prev_no)
            if curr_no != prev_no:
                autocorrected = each_word
        elif i == len(valid_words)-1 and autocorrected==valid_words[0] and diff_function(user_word,autocorrected,limit)>limit:
            return user_word
        elif i == len(valid_words)-1 and autocorrected==valid_words[0]:
            return autocorrected
        i+=1
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
    if len(start) == 1 and len(goal) == 1:
        if start != goal:
            return 1
        else:
            return 0
    elif len(start) == 1 or len(goal) == 1:
        if start[0] != goal[0]:
            return 1 + abs(len(start)-len(goal))
        else:
            return 0 + abs(len(start)-len(goal))
    else:
        if start[0] != goal[0]:
            return 1 + swap_diff(start[1:],goal[1:],limit-1)
        else:
            return 0 + swap_diff(start[1:],goal[1:],limit)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    """assert False, 'Remove this line'

    if ______________: # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END

    elif ___________: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END

    else:
        add_diff = ...  # Fill in these lines
        remove_diff = ...
        substitute_diff = ...
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END

    """
    if limit < 0:
        return 0
    if len(start) == 1 and len(goal) == 1:
        if start != goal:
            return 1
        else:
            return 0
    elif len(start) == 1 or len(goal) == 1: #Check if either start or goal is down to the last letter
        if start[-1] == goal[-1]: #Check if the last letter of the longer string is equal to the shorter string
            return 0 + abs(len(start)-len(goal))
        if start[0] != goal[0]:
            if len(start)>1: #if len(start) is greater than 1, that means goal is the one remaining letter, so we check if this letter is ever in any of the remaining characters of start
                for i in range(len(start)):
                    if start[i]==goal:
                        return abs(len(start)-len(goal)) #if this case is ever true, that means we consider this a swap, and the remaining letters needed to be added in
                return 1 + abs(len(start)-len(goal)) #otherwise, it will hit this case
            if len(goal)>1: #if len(start) is greater than 1, that means goal is the one remaining letter, so we check if this letter is ever in any of the remaining characters of start
                for i in range(len(goal)):
                    if goal[i]==start:
                        return abs(len(goal)-len(start))
                return 1 + abs(len(start)-len(goal))
        else:
            return abs(len(start)-len(goal))
    else:
        if start[0] != goal[0]:
            if len(start)>2 and start[1] == goal[0]: #Check if there is an off-by-one difference that we can add a letter to
                if goal[1] == start[0]: #Check if the first and second letters can be swapped, which would only be 1 operation
                    return min(1 + edit_diff(start[2:],goal[2:],limit-1),1 + edit_diff(start[2:],goal[1:],limit-1)) #Check if it is more efficient to swap or not
                else:
                    return 1 + min(edit_diff(start[2:],goal[1:],limit-1),edit_diff(start[1:],goal[1:],limit)) #Check if it is more efficient to edit this letter now or later
            elif len(goal)>2 and start[0] == goal[1]: #Check if there is an off-by-one difference that we can remove a letter from
                return 1 + min(edit_diff(start[1:],goal[2:],limit-1),edit_diff(start[1:],goal[1:],limit))
            elif len(start)>3 and start[2] == goal[0]: #Check if there is an off-by-two difference
                if start[1] == goal[1]: #Check if the letters in between this off-by-two are the same
                    return 1 + edit_diff(start[3:],goal[1:],limit-1)
                else:
                    return 2 + min(edit_diff(start[3:],goal[1:],limit-2),edit_diff(start[2:],goal[1:],limit-1)) #Check if it is more efficient to edit 2 letters at once, or just one.
            elif len(goal)>3 and start[0] == goal[2]:
                if start[1] == goal[1]:
                    return 1 + edit_diff(start[1:],goal[3:],limit-1)
                else:
                    return 2 + min(edit_diff(start[1:],goal[3:],limit-2),edit_diff(start[1:],goal[2:],limit-1))
            else: #Once we get here, we are sure the most efficient way to fix the difference is by just swapping it with a different letter
                return 1 + edit_diff(start[1:],goal[1:],limit-1)
        else: #There was no error, move on
            return 0 + edit_diff(start[1:],goal[1:],limit)



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    def list_accuracy(typed_words,reference_words):
        correct, incorrect = 0, 0
        if len(typed_words) == 0 or len(reference_words) == 0:
          return 0.0
        if len(typed_words) == 1 and len(reference_words) == 1:
            if typed_words == reference_words:
                return 1.0
            else:
                return 0.0
        i=0
        while i < min(len(typed_words),len(reference_words)):
            if typed_words[i] == reference_words[i]:
                correct += 1
            else:
                return correct/len(reference_words)
            i+= 1
        if len(typed_words)>len(reference_words) or len(reference_words)>len(typed_words):
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
    result = []
    flattened = []
    for x in range(len(word_times[0])):
        flattened += word_times[0][x]


    word_list = []
    for k in range(len(flattened)):
        if k % 2 == 0:
            word_list += [flattened[k]]
    word_list = word_list[1:]

    y=[]
    for i in range(len(word_list)):
        y +=[[(word_list[i]),(flattened[2*i+3])]]


    y = [[y[0][0],y[0][1]]]+[[y[i][0],y[i][1]-y[i-1][1]] for i in range(1,len(y))]

    dict_temp = []
    dict_temp += [{z[0]: z[1] for z in y}]
    result = [[i for i in dict_temp[0]]]


    for aq in range(1,len(word_times)):
        result += [[]]
        flattened = []
        for x in range(len(word_times[aq])):
            flattened += word_times[aq][x]


        word_list = []
        for k in range(len(flattened)):
            if k % 2 == 0:
                word_list += [flattened[k]]
        word_list = word_list[1:]

        y=[]
        for i in range(len(word_list)):
            y +=[[(word_list[i]),(flattened[2*i+3])]]
        '''
        def rational(n, d):
            """A representation of the rational number N/D."""
            g = gcd(n, d)
            n, d = n//g, d//g
            def select(name):
                if name == 'n':
                    return n
                elif name == 'd':
                    return d
            return select

        def numer(x):
            """Return the numerator of rational number X in lowest terms and having
            the sign of X."""
            return x('n')

        def denom(x):
            """Return the denominator of rational number X in lowest terms and positive."""
            return x('d')'''
        a = round(y[0][1],2)
        b = round(y[1][1],2)
        print(round(b-a))
        y = [[y[0][0],y[0][1]]]+[[y[i][0],y[i][1]-y[i-1][1]] for i in range(1,len(y))]

        dict_temp += [{z[0]: z[1] for z in y}]
        for x in range(len(result)-1):
            for j in dict_temp[aq]:
                print(dict_temp)
                if dict_temp[x][j] == dict_temp[aq][j]:
                    print(j, dict_temp[x][j], dict_temp[aq][j])
                    for i in result[aq]:
                        if i != j:
                            result[aq] += [j]
                elif dict_temp[x][j] < dict_temp[aq][j]:
                    for i in result[aq]:
                        if (i == j):
                            result[aq] = result[aq][:-1]
                else:
                    result[x].remove(j)
    return result
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
