file1 = open("org.txt", "r",encoding="utf8")
file2 = open("input_asli.txt","a",encoding="utf8")
for line in file1:
	input_sentences = list(line.split())
	if(len(input_sentences) >= 6):
		file2.write(line)
file2.close()
file1.close()