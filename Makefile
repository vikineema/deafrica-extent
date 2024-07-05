get-natural-earth:
	curl -o data/ne_10m_admin_0_countries.zip https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip

extract-kenya-hull:
	python3 ./merge-africa.py

extract-mgrs-codes:
	python3 ./extract-mgrs.py

extract-pathrows:
	python3 ./extract-pathrows.py
