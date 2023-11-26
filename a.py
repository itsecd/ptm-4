with open('sentences.txt') as file:
    sentences = list(file)
print(sentences)

print('----------------')
f = open('sentences.txt').read()
sentences = f.split('\n')
print(sentences)