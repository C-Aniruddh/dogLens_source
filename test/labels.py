file = open("retrained_labels.txt", "r")
lines = file.readlines()
print lines

new_lines = []
for x in lines:
	new_line = x.title()
	new_lines.append(new_line)

print new_lines

w_file = open("retrained.txt", "w")
for y in new_lines:
	w_file.write(y)
