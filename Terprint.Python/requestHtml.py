from requests_html import HTMLSession

url="https://mete.labdrive.net/s/SfWBtnDxrN9qs2t/download/COA_2509CBR0194-005.pdf"
session = HTMLSession()
response = session.get(url)

# Render JavaScript (requires Chromium installed)
response.html.render()

print(response.html.html)