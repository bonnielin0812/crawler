import requests
import os
import time

def download_pdf(link,directory):
    for item in link:
        filename = item["name"]
        # 確保文件名以.pdf結尾
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        # 確保文件名唯一
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(directory, filename)):
            filename = f"{base}_{counter}{extension}"
            counter += 1

        url = item["pdf_url"]

        response = requests.get(url,stream = True, verify=False)
        if response.status_code ==200:
            filepath = os.path.join(directory, filename)
            with open(filepath, 'wb') as pdf_object:
                pdf_object.write(response.content)
                print(f'{filename} was successfully saved!')
        else:
            print(f'Uh oh! Could not download {filename},')
            print(f'HTTP response status code: {response.status_code}')
        time.sleep(0.5)  # 暂停0.5s 防止過快






