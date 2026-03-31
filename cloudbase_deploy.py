from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        # 启动浏览器（有界面模式）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 打开 CloudBase 控制台
        print("正在打开 CloudBase 控制台...")
        page.goto('https://console.cloud.tencent.com/tcb')
        
        print("\n请在新打开的浏览器窗口中扫码登录")
        print("登录成功后，回到这里按 Enter 键继续")
        input()
        
        # 等待页面加载
        page.wait_for_load_state('networkidle')
        time.sleep(2)
        
        print("正在截图查看当前状态...")
        page.screenshot(path='step1_login.png')
        
        # 1. 点击静态网站托管
        print("\n步骤1: 点击静态网站托管...")
        try:
            hosting_link = page.locator('text=静态网站托管').first
            if hosting_link.is_visible():
                hosting_link.click()
                print("✓ 已点击静态网站托管")
                time.sleep(3)
                page.screenshot(path='step2_hosting.png')
            else:
                print("未找到静态网站托管链接")
                return
        except Exception as e:
            print(f"点击静态网站托管失败: {e}")
            return
        
        # 2. 点击文件管理
        print("\n步骤2: 点击文件管理...")
        try:
            file_mgmt = page.locator('text=文件管理').first
            if file_mgmt.is_visible():
                file_mgmt.click()
                print("✓ 已点击文件管理")
                time.sleep(2)
                page.screenshot(path='step3_filemgmt.png')
            else:
                print("未找到文件管理标签")
        except Exception as e:
            print(f"点击文件管理失败: {e}")
        
        # 3. 上传文件
        print("\n步骤3: 准备上传 daywise.html...")
        print("文件路径: C:\\Users\\49592\\WorkBuddy\\20260320231952\\daywise.html")
        
        try:
            # 查找上传按钮
            upload_btn = page.locator('text=上传文件, text=上传, text=Upload').first
            if upload_btn.is_visible():
                upload_btn.click()
                print("✓ 已点击上传按钮")
                time.sleep(2)
                page.screenshot(path='step4_upload_dialog.png')
                
                # 处理文件选择对话框
                file_input = page.locator('input[type="file"]').first
                if file_input.is_visible():
                    file_input.set_input_files('C:\\Users\\49592\\WorkBuddy\\20260320231952\\daywise.html')
                    print("✓ 已选择文件 daywise.html")
                    time.sleep(3)
                    page.screenshot(path='step5_uploaded.png')
                else:
                    print("未找到文件输入框")
            else:
                print("未找到上传按钮")
        except Exception as e:
            print(f"上传文件失败: {e}")
            page.screenshot(path='error_upload.png')
        
        print("\n操作完成！")
        print("请查看截图了解操作结果")
        input("\n按 Enter 关闭浏览器...")
        browser.close()

if __name__ == '__main__':
    main()
