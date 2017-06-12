import os
name = []

for dir in os.listdir("."):
	if os.path.isdir(dir):
		name.append(dir)

print name

new_names = []
for x in name:
	new_name = x[10:]
	new_names.append(new_name)

print new_names

sorted_names = []
for y in new_names:
	if '_' in y:
		y = y.replace('_', ' ')
	if '-' in y:
		y = y.replace('-', ' ')
	sorted_names.append(y)

print sorted_names

title_names = []

for z in sorted_names:
	z = z.title()
	title_names.append(z)

print title_names

#Rename

count = 0
for a in name:
	rename = title_names[count]
	command = 'mv "%s" "%s"' % (a, rename)
	print command
	os.system(command)
	count = count + 1
