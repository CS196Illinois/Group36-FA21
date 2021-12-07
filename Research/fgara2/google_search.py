import requests

result = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyD8lesvuvvaM9NYaTipX2oDlDbMy1VKJbY&cx=017576662512468239146:omuauf_lfve&q=hospitals near me")

r = result.json()

for i in r['items']:
    print(i[title])
    print(i[link])
    print(i[snippet])
    print('\n')