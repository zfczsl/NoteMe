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
        print("请在弹出的浏览器窗口中扫码登录")
        page.goto('https://console.cloud.tencent.com/tcb', timeout=60000)
        
        print("\n等待30秒让你登录...")
        time.sleep(30)
        
        print("继续操作...")
        time.sleep(3)
        
        # 截图看当前状态
        page.screenshot(path='step1_after_login.png')
        print("[OK] 已截图 step1_after_login.png")
        
        # 尝试点击静态网站托管
        print("\n尝试点击静态网站托管...")
        try:
            # 先尝试直接找文字
            elements = page.locator('text=静态网站托管').all()
            for el in elements:
                if el.is_visible():
                    el.click()
                    print("[OK] 点击了静态网站托管")
                    time.sleep(3)
                    page.screenshot(path='step2_hosting.png')
                    break
        except Exception as e:
            print(f"点击失败: {e}")
            page.screenshot(path='error_click.png')
        
        # 尝试找上传相关的按钮
        print("\n尝试找上传按钮...")
        try:
            time.sleep(2)
            
            # 列出所有按钮文字
            buttons = page.locator('button').all()
            print(f"找到 {len(buttons)} 个按钮")
            for i, btn in enumerate(buttons[:10]):  # 只显示前10个
                try:
                    text = btn.inner_text()
                    if text:
                        print(f"  按钮{i}: {text[:30]}")
                except:
                    pass
            
            # 尝试点击包含"上传"或"文件"的按钮
            for btn in buttons:
                try:
                    text = btn.inner_text()
                    if '上传' in text or '文件' in text or '部署' in text:
                        if btn.is_visible():
                            btn.click()
                            print(f"[OK] 点击了按钮: {text[:30]}")
                            time.sleep(2)
                            page.screenshot(path='step3_upload.png')
                            break
                except:
                    pass
                    
        except Exception as e:
            print(f"找按钮失败: {e}")
        
        print("\n操作完成，截图已保存")
        print("浏览器将在30秒后关闭...")
        time.sleep(30)
        browser.close()

if __name__ == '__main__':
    main()
