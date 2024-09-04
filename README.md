# 成語典 《Dictionary of Chinese Idioms》

這是一款專為學習成語設計的應用程式。每次啟動時，程式會顯示當天的成語，並附有詳細的注音、釋義、書證以及近義詞和反義詞等資訊。使用者可以通過按鈕快速切換查看不同的成語。應用程式同時配有啟動畫面和音效，增添使用體驗。

## 功能特色
- **按鈕切換**：簡單操作切換前後成語。
- **自動保存進度**：關閉程式時自動保存目前查看的成語，重新開啟程式後，不會遺失進度。
- **啟動畫面與音效**：每次啟動時播放音效並顯示啟動畫面。

## 安裝與執行
使用者可下載 chengyudian.exe 直接運行；亦可下載 Python 程式碼後執行，在運行程式前，請確保已安裝相關依賴模組：
### bash
pip install pygame pandas xlrd Pillow

## 封裝應用程式
使用 PyInstaller 封裝程式：
### bash
pyinstaller --onefile --windowed --add-data "mnt/data/*;mnt/data" chengyudian.py

封裝完成後，可執行文件會位於 dist 文件夾中，雙擊即可運行應用程式。

## 系統需求
- **Windows 8 / Windows Server 2012以上 ( Windows NT 版本 6.2以上 )**
- **Python 3.6 或以上版本**
