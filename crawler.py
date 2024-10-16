from bs4 import BeautifulSoup
import os
import time
import sys
sys.path.append('./dist/_lib')
import service
import downloadPDF

def getPdfUrl():
    link = []
    link.append({
        "pdf_url": 'https://www.elegislation.gov.hk/hk/cap123Q!en-zh-Hant-HK.pdf',
        "name": 'Building Regulation'})

    # 1####################################################################################################################################
    url = 'https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/index.html'

    html_content = service.get_html_content(url)

    pdf_link = service.get_pdf1(html_content)

    # 篩選出需要的link
    need_link = []
    for item in pdf_link:
        if (item['title'] == 'Planning and Construction'):
            if (('Code of Practice for Fire Safety in Buildings 2011' in item['name']) or (
                    'fs_code2011' in item['pdf_url'])):
                need_link.append({
                    "pdf_url": item['pdf_url'],
                    "name": item['name']})
        if (item['title'] == 'Site and Building Works' or item['title'] == 'Structure'):
            need_link.append({
                "pdf_url": item['pdf_url'],
                "name": item['name']})
    for item in need_link:
        item['pdf_url'] = item['pdf_url'].replace('../../../../', 'https://www.bd.gov.hk/')
        link.append({
            "pdf_url": item['pdf_url'],
            "name": item['name']})

    # 2####################################################################################################################################

    # 獲取網頁内容
    url = 'https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnap.html'

    html_content = service.get_html_content(url)

    pdf_link = service.get_pdf(html_content)

    for item in pdf_link:
        if (('ADM' in item['name']) or ('APP' in item['name']) or ('ADV' in item['name'])):
            need_link.append({
                "pdf_url": item['pdf_url'],
                "name": item['name']})

    for item in need_link:
        item['pdf_url'] = item['pdf_url'].replace('../../../../', 'https://www.bd.gov.hk/')
        link.append({
            "pdf_url": item['pdf_url'],
            "name": item['name']})

    # 3####################################################################################################################################

    # 獲取網頁内容
    url = 'https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnrc.html'

    html_content = service.get_html_content(url)

    pdf_link = service.get_pdf(html_content)

    # 篩選出需要的link
    need_link = []
    for item in pdf_link:
        if ('PNRC' in item['name']):
            need_link.append({
                "pdf_url": item['pdf_url'],
                "name": item['name']})

    for item in need_link:
        item['pdf_url'] = item['pdf_url'].replace('../../../../', 'https://www.bd.gov.hk/')
        link.append({
            "pdf_url": item['pdf_url'],
            "name": item['name']})

    # 4####################################################################################################################################

    # 獲取網頁内容
    url = 'https://www.cedd.gov.hk/eng/publications/standards-spec-handbooks-cost/stan-cs1-2010/index.html'

    html_content = service.get_html_content_urllib(url)

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到標題為 "Continuously Updated Version with Amendments" 的 h2 標籤
        target_h2 = soup.find('h2', string='Continuously Updated Version with Amendments')

        # 如果找到了目標 h2 標籤，獲取其後面的表格
        if target_h2:
            table = target_h2.find_next('table', class_='colorTable pdfTable')

        pdf_link = []

        for item in table.find_all('a', href=True):
            if '.pdf' in item['href']:
                pdf_link.append({
                    'title': 'Continuously Updated Version with Amendments',
                    "pdf_url": item['href'],
                    "name": item.string})
    except Exception as e:
        print(f"爬取 {url} 時發生錯誤 {e}")

    need_link = []
    for item in pdf_link:
        if ('Construction Standard' in item['name']):
            need_link.append({
                "pdf_url": item['pdf_url'],
                "name": item['name']})

    for item in need_link:
        item['pdf_url'] = 'https://www.cedd.gov.hk/' + item['pdf_url']
        link.append({
            "pdf_url": item['pdf_url'],
            "name": os.path.basename(item['pdf_url'])})

    # 5#########################################################################################################
    # 獲取網頁内容
    url = 'https://www.cedd.gov.hk/eng/publications/standards-spec-handbooks-cost/stan-cs2-2012/index.html'

    try:
        html_content = service.get_html_content_urllib(url)

        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到標題為 "Continuously Updated Version with Amendments" 的 h2 標籤
        target_h2 = soup.find('h2', string='Continuously Updated Version with Amendments')

        # 如果找到了目標 h2 標籤，獲取其後面的表格
        if target_h2:
            table = target_h2.find_next('table', class_='colorTable pdfTable')

        pdf_link = []

        # 遍歷表格中的所有行
        for item in table.find_all('a', href=True):
            if '.pdf' in item['href']:
                pdf_link.append({
                    'title': 'Continuously Updated Version with Amendments',
                    "pdf_url": item['href'],
                    "name": item.string})
    except Exception as e:
        print(f"爬取 {url} 時發生錯誤 {e}")

    need_link = []
    for item in pdf_link:
        if ('Construction Standard' in item['name']):
            need_link.append({
                "pdf_url": item['pdf_url'],
                "name": item['name']})

    for item in need_link:
        item['pdf_url'] = 'https://www.cedd.gov.hk' + item['pdf_url']
        link.append({
            "pdf_url": item['pdf_url'],
            "name": os.path.basename(item['pdf_url'])})
    return link


def getPdf():
    # for item in link:
    #     print(item)
    # 先將PDF存進臨時區
    # 讀取配置文件
    config = service.load_config()
    # 獲取目標資料夾路徑
    service.check_paths(config)
    target_folder, temp_folder = service.create_folders(config)
    # 清空臨時文件夾
    service.clear_folder(temp_folder)
    directory = temp_folder
    link = getPdfUrl()
    downloadPDF.download_pdf(link, directory)

    # 對比后move到存放區
    service.check_move(temp_folder, target_folder)

    print("處理完成。程序將在5秒後自動關閉...")
    time.sleep(5)
    # 關閉窗口
    sys.exit()


