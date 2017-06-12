file = open("retrained.txt", "r")
lines = file.readlines()
print lines 

new_lines = []

for x in lines:
	new_line = x[:-1]
	new_lines.append(new_line)

print new_lines

items = []

for y in new_lines:
	new_string = '<item>%s</item>\n' % y
	items.append(new_string)

print items

w_file = open("retrained_items.txt", "w")
for z in items:
        w_file.write(z)
