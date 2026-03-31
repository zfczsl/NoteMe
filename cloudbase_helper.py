from playwright.sync_api import sync_playwright
import time
import sys

def main():
    with sync_playwright() as p:
        # 启动浏览器（有界面模式，方便扫码）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 打开 CloudBase 控制台
        print("正在打开 CloudBase 控制台...")
        page.goto('https://console.cloud.tencent.com/tcb')
        
        print("\n" + "="*50)
        print("请在新打开的浏览器窗口中扫码登录")
        print("登录成功后，回到这里输入 'ok' 继续")
        print("="*50 + "\n")
        
        while True:
            user_input = input("输入 'ok' 继续，或 'exit' 退出: ").strip().lower()
            if user_input == 'ok':
                break
            elif user_input == 'exit':
                browser.close()
                return
        
        # 登录完成，进入静态网站托管
        print("正在进入静态网站托管...")
        
        # 尝试点击左侧菜单的静态网站托管
        try:
            # 等待页面加载
            page.wait_for_load_state('networkidle')
            time.sleep(2)
            
            # 截图查看当前状态
            page.screenshot(path='cloudbase_logged_in.png')
            print("已截图保存当前状态")
            
            # 查找并点击静态网站托管
            hosting_link = page.locator('text=静态网站托管').first
            if hosting_link.is_visible():
                hosting_link.click()
                print("已点击静态网站托管")
                time.sleep(2)
                page.screenshot(path='hosting_page.png')
                print("已截图静态网站托管页面")
            else:
                print("未找到静态网站托管链接，请手动点击")
                input("手动点击后按 Enter 继续...")
                page.screenshot(path='hosting_page.png')
            
            print("\n现在你可以告诉我下一步要做什么：")
            print("1. 上传文件")
            print("2. 配置域名")
            print("3. 其他操作")
            
        except Exception as e:
            print(f"出错: {e}")
            page.screenshot(path='error.png')
        
        input("\n按 Enter 关闭浏览器...")
        browser.close()

if __name__ == '__main__':
    main()
