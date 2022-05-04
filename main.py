from spell_correct import generate_rank

lines = []
word_list=[]
with open('lexicon.txt') as f:
    lines = f.readlines()

for line in lines:
    word_list=word_list+(line.split())
word_list=sorted(list(set(word_list)))
query=input("Enter the query:")
print(generate_rank(query,word_list))