from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        # 启动浏览器（有界面模式）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 打开静态网站托管页面
        print("正在打开静态网站托管页面...")
        page.goto('https://tcb.cloud.tencent.com/dev?envId=noteme-4g46b2fz98b36db3#/static-hosting', timeout=60000)
        
        # 等待20秒让页面加载
        print("\n等待20秒让页面加载...")
        time.sleep(20)
        
        # 截图让二维码出现
        print("\n[截图] 刷新出二维码...")
        page.screenshot(path='qrcode_trigger.png')
        print("[OK] 已截图，二维码应该出现了")
        
        # 等待用户登录（60秒倒计时）
        print("\n请扫码登录...")
        print("60秒后自动继续...")
        for i in range(60, 0, -1):
            if i % 10 == 0:
                print(f"倒计时: {i}秒")
            time.sleep(1)
        print("\n继续操作...")
        
        time.sleep(2)
        
        # 截图看当前状态
        try:
            page.screenshot(path='hosting_page.png')
            print("[OK] 已截图 hosting_page.png")
        except Exception as e:
            print(f"截图失败: {e}")
        
        # 1. 点击本地项目上传
        print("\n步骤1: 点击本地项目上传...")
        try:
            # 找本地项目上传区域
            local_upload = page.locator('text=本地项目上传').first
            if local_upload.is_visible():
                local_upload.click()
                print("[OK] 点击了本地项目上传")
                time.sleep(3)
                page.screenshot(path='step1_upload.png')
            else:
                print("未找到本地项目上传，尝试其他方式...")
                # 尝试找包含上传的按钮
                upload_btn = page.locator('button:has-text("上传"), a:has-text("上传")').first
                if upload_btn and upload_btn.is_visible():
                    upload_btn.click()
                    print("[OK] 点击了上传按钮")
                    time.sleep(3)
                    page.screenshot(path='step1_upload.png')
        except Exception as e:
            print(f"点击上传失败: {e}")
            try:
                page.screenshot(path='error_upload_click.png')
            except:
                pass
        
        # 2. 等待上传对话框出现
        print("\n步骤2: 等待上传对话框...")
        time.sleep(3)
        try:
            page.screenshot(path='step2_dialog.png')
        except:
            pass
        
        # 3. 找文件输入框
        print("\n步骤3: 找文件输入框...")
        try:
            # 找文件选择输入框
            file_input = page.locator('input[type="file"]').first
            if file_input.count() > 0:
                print(f"找到 {file_input.count()} 个文件输入框")
                # 上传 daywise.html
                file_path = 'C:\\Users\\49592\\WorkBuddy\\20260320231952\\daywise.html'
                file_input.set_input_files(file_path)
                print(f"[OK] 已选择文件: {file_path}")
                time.sleep(3)
                page.screenshot(path='step3_file_selected.png')
                
                # 4. 找确认/上传按钮
                print("\n步骤4: 找确认按钮...")
                confirm_btn = page.locator('button:has-text("确定"), button:has-text("上传"), button:has-text("部署"), button:has-text("确认")').first
                if confirm_btn and confirm_btn.is_visible():
                    confirm_btn.click()
                    print("[OK] 点击了确认按钮")
                    time.sleep(5)
                    page.screenshot(path='step4_deploying.png')
                else:
                    print("未找到确认按钮，列出所有按钮:")
                    buttons = page.locator('button').all()
                    for btn in buttons:
                        try:
                            text = btn.inner_text()
                            if text:
                                print(f"  - {text[:40]}")
                        except:
                            pass
            else:
                print("未找到文件输入框")
                # 尝试找拖拽上传区域
                drop_zone = page.locator('text=拖拽文件到此处, text=点击上传').first
                if drop_zone and drop_zone.is_visible():
                    print("找到拖拽上传区域")
                    drop_zone.click()
                    time.sleep(2)
                    page.screenshot(path='step2_dropzone.png')
        except Exception as e:
            print(f"上传文件失败: {e}")
            try:
                page.screenshot(path='error_file_upload.png')
            except:
                pass
        
        print("\n操作完成")
        print("浏览器将在60秒后关闭...")
        time.sleep(60)
        browser.close()

if __name__ == '__main__':
    main()
