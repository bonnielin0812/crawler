import os.path
import shutil
import configparser
import requests
from bs4 import BeautifulSoup
import urllib.request
import sys

# 獲取網頁HTML
def get_html_content(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            html_content = response.content  # 得到html的内容
            # print(html_content)
            return (html_content)
        else:
            print("failed to fetch")
    except Exception as e:
        print(f"爬取 {url} 時發生錯誤 {e}")

def get_html_content_urllib(url):
    try:
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        # print(html)
        return (html)
    except Exception as e:
        print(f"爬取 {url} 時發生錯誤 {e}")


# 從html内容中找pdfURL 和對應的名字
def get_pdf(htmlContent):
    # 解析HTML
    soup = BeautifulSoup(htmlContent, 'html.parser')
    pdf_link = []

    # 找 '.pdf'
    for link in soup.find_all('a', href=True):
        if '.pdf' in link['href']:
            pdf_link.append({"pdf_url": link['href'], "name": link.string})
    return pdf_link

def get_pdf1(htmlContent):
    # 解析HTML
    soup = BeautifulSoup(htmlContent, 'html.parser')
    pdf_link = []

    for table in soup.find_all('table', class_='transformable practice'):
        # 找 '.pdf'
        for link in table.find_all('a', href=True, class_='pdfIcon after'):
            if '.pdf' in link['href']:
                pdf_link.append({
                    "title": table.get('title'),
                    "pdf_url": link['href'],
                    "name": link.string})

    return pdf_link

# 清空文件夾
def clear_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        print(folder_path, "clear_folder success!")
    except:
        print(folder_path, "clear_folder 失敗!")

def check_move(temp_folder,target_folder):
    for filename in os.listdir(temp_folder):
        temp_file_path = os.path.join(temp_folder, filename)
        target_file_path = os.path.join(target_folder, filename)

        # 檢查文件是否為常規文件（非目錄）
        if os.path.isfile(temp_file_path):
            # 獲取臨時文件的大小
            temp_file_size = os.path.getsize(temp_file_path)

            # 檢查目標資料夾中是否存在同名文件
            if os.path.exists(target_file_path):
                # 獲取目標文件的大小
                target_file_size = os.path.getsize(target_file_path)

                # 比較文件名和大小
                if temp_file_size == target_file_size:
                    print(f"檔案 {filename} 已存在且大小相同，不移動。")
                    continue

            # 移動文件
            shutil.copy(temp_file_path, target_file_path)
            print(f"已移動檔案 {filename} 到目標資料夾。")

    # 刪除舊的文件
    temp_file = set(os.listdir(temp_folder))
    target_file = set(os.listdir(target_folder))

    # 找出 B 中有但 A 中沒有的文件
    files_to_delete = target_file - temp_file

    # 刪除這些文件
    for file_name in files_to_delete:
        file_path = os.path.join(target_folder, file_name)
        try:
            os.remove(file_path)
            print(f"已刪除文件: {file_path}")
        except Exception as e:
            print(f"無法刪除文件 {file_path}. 錯誤: {e}")

    print(f"共刪除了 {len(files_to_delete)} 個文件。")

    clear_folder(temp_folder)

def load_config():
    try:
        config = configparser.ConfigParser()
        exe_dir = os.getcwd()  # exe可执行文件所在位置
        path = os.path.join(exe_dir, "config.ini")  # 拼接上配置文件，形成全路径
        config.read(path)
        return config
    except Exception as e:
        print("加載配置文件時發生錯誤，找不到配置文件", e)

def check_paths(config):
    paths = config['Paths']
    for key, path in paths.items():
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"路徑 {path} 創建成功")
    print("所有路徑檢查通過。")

def create_folders(config):
    try:
        output_folder = config['Paths']['target_folder']
        temp_folder = config['Paths']['temp_folder']
    except KeyError as e:
        print(f"讀取配置文件時發生錯誤 {e}")
        input("按 Enter 鍵退出...")
        sys.exit(1)

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(temp_folder, exist_ok=True)

    return output_folder, temp_folder























































































