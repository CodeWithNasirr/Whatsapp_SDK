
def anagrams_logic(words):
    answser={}
    for word in words:
        sorted_word="".join(sorted(word))
        if not sorted_word in answser:
            answser[sorted_word]=[word]
        else:
            answser[sorted_word].append(word)
    return answser

words = ["listen", "silent", "enlist", "rat", "tar", "art", "dog", "god"]

x=anagrams_logic(words)
print(x)

