import requests
from SuperMarkdown import SuperMarkdown
import os

ignore = ['TiagoDanin.github.io', 'SendCH-Telegram']

def write_text(text, name):
	try:
		file = open('sites/{}/index.html'.format(name), 'w')
	except FileNotFoundError as error:
		return False
	file.write(text)
	file.close()
	return True

def github():
	url = 'https://api.github.com/users/TiagoDanin/repos'
	data = requests.get(url)
	data_json = data.json()
	for v in data_json:
		if v['language']:
			language = v['language']
		else:
			language = 'github'
		name = v['name']
		url_readme = 'https://raw.githubusercontent.com/TiagoDanin/{}/master/README.md'.format(name)
		description = v['description']

		if name in ignore:
			print('{} - {} - {}'.format(readme_data, name, 'IGNORE'))
		else:
			readme_data = requests.get(url_readme)
			readme = readme_data.text
			if readme != '404: Not Found':
				text = ''
				supermd = SuperMarkdown()
				supermd.add_content(text=readme)
				file = open('defaut.html', 'r')
				text = file.read()
				text = text.format(title=name,
									description=description,
									repo=name,
									html_text=supermd.build())
				status = write_text(text, name)
				if status:
					os.system('git add -A && git commit -S -m "Update GH-Pages"')
					print('{} - {} - {}'.format(readme_data, name, 'OK'))
				else:
					os.system('cd sites/{}/ git add -A && git commit -S -m "Update GH-Pages"'.format(name))
					status = write_text(text, name)
					if status:
						os.system('cd sites/{}/ git add -A && git commit -S -m "Update GH-Pages"'.format(name))
						print('{} - {} - {}'.format(readme_data, name, 'OK'))
					else:
						print('{} - {} - {}'.format(readme_data, name, 'No has git-repo'))
			else:
				print('{} - {} - {}'.format(readme_data, name, 'No has README file'))

github()
