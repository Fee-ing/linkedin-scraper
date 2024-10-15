arr = [{'name': 'Joe Wall', 'link': 'https://www.linkedin.com/in/joe-wall-980766273?miniProfileUrn=urn%3Ali%3Afsd_profile%3AACoAAELal_ABKCmZr-dp7KQHb0DKUlNEtB_HF9M', 'recent': '5h • \n '}]

bb = []
for data in arr:
  print(data['link'])
  bb.append({**data, **{'cc': "aa"}})

print(bb)