word = list(input())
word[0] = word[0].lower()

for i, item in enumerate(word):
    if item.isupper():
        item = item.lower()
        word.insert(i, "_")
    
        
s = ""
print(s.join(word))
