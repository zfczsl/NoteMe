from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # 启动浏览器（有界面模式）
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # 打开 CloudBase 控制台
    page.goto('https://console.cloud.tencent.com/tcb')
    
    print("浏览器已打开，请扫码登录...")
    print("登录后按 Enter 键继续")
    input()
    
    # 等待用户登录完成
    time.sleep(2)
    
    # 截图查看当前状态
    page.screenshot(path='cloudbase_status.png')
    print("已截图保存为 cloudbase_status.png")
    
    # 保持浏览器打开
    print("浏览器保持打开状态，请告诉我下一步操作")
    input("按 Enter 关闭浏览器")
    
    browser.close()
