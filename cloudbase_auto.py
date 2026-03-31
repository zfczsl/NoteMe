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
        print("30秒后自动继续...")
        
        # 等待30秒让用户登录
        for i in range(30, 0, -1):
            print(f"倒计时: {i}秒", end='\r')
            time.sleep(1)
        print("\n继续操作...")
        
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
                print("未找到静态网站托管链接，尝试查找菜单...")
                # 尝试点击展开菜单
                menu_items = page.locator('text=静态网站托管, text=托管').all()
                for item in menu_items:
                    if item.is_visible():
                        item.click()
                        print("✓ 已点击菜单项")
                        break
                time.sleep(3)
                page.screenshot(path='step2_hosting.png')
        except Exception as e:
            print(f"点击静态网站托管失败: {e}")
            page.screenshot(path='error_hosting.png')
        
        # 2. 查找上传入口
        print("\n步骤2: 查找上传入口...")
        try:
            # 等待页面稳定
            time.sleep(3)
            
            # 查找上传按钮（可能是"上传文件"、"上传"、"+"等）
            upload_selectors = [
                'text=上传文件',
                'text=上传',
                'button:has-text("上传")',
                '[class*="upload"]',
                'text=部署',
                'text=文件管理'
            ]
            
            for selector in upload_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        print(f"✓ 找到元素: {selector}")
                        element.click()
                        print(f"✓ 已点击: {selector}")
                        time.sleep(2)
                        page.screenshot(path='step3_clicked.png')
                        break
                except:
                    continue
            else:
                print("未找到上传按钮，截图查看当前页面...")
                page.screenshot(path='step3_no_upload.png')
                
        except Exception as e:
            print(f"查找上传入口失败: {e}")
            page.screenshot(path='error_upload.png')
        
        # 3. 尝试上传文件
        print("\n步骤3: 准备上传 daywise.html...")
        print("文件路径: C:\\Users\\49592\\WorkBuddy\\20260320231952\\daywise.html")
        
        try:
            # 查找文件输入框
            file_input = page.locator('input[type="file"]').first
            if file_input.count() > 0 and file_input.is_visible():
                file_input.set_input_files('C:\\Users\\49592\\WorkBuddy\\20260320231952\\daywise.html')
                print("✓ 已选择文件 daywise.html")
                time.sleep(3)
                page.screenshot(path='step4_file_selected.png')
                
                # 查找确认/上传按钮
                confirm_btn = page.locator('button:has-text("确定"), button:has-text("上传"), button:has-text("确认")').first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    print("✓ 已点击确认上传")
                    time.sleep(5)
                    page.screenshot(path='step5_upload_complete.png')
            else:
                print("未找到文件输入框，可能需要手动点击上传按钮")
                page.screenshot(path='step4_manual.png')
                
        except Exception as e:
            print(f"上传文件失败: {e}")
            page.screenshot(path='error_file.png')
        
        print("\n操作完成！")
        print("请查看截图了解操作结果")
        
        # 保持浏览器打开，让用户查看结果
        print("\n浏览器保持打开，60秒后自动关闭...")
        time.sleep(60)
        browser.close()

if __name__ == '__main__':
    main()
