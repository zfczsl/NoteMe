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
        print("[OK] 已截图")
        
        # 等待用户登录（60秒倒计时）
        print("\n请扫码登录...")
        print("60秒后自动继续...")
        for i in range(60, 0, -1):
            if i % 10 == 0:
                print(f"倒计时: {i}秒")
            time.sleep(1)
        print("\n继续操作...")
        
        time.sleep(2)
        
        # 1. 点击本地项目上传
        print("\n步骤1: 点击本地项目上传...")
        try:
            local_upload = page.locator('text=本地项目上传').first
            if local_upload.is_visible():
                local_upload.click()
                print("[OK] 点击了本地项目上传")
                time.sleep(3)
        except Exception as e:
            print(f"点击失败: {e}")
        
        # 2. 等待上传对话框并选择文件夹
        print("\n步骤2: 选择文件夹...")
        time.sleep(3)
        try:
            file_input = page.locator('input[type="file"]').first
            if file_input.count() > 0:
                folder_path = 'C:\\Users\\49592\\WorkBuddy\\20260320231952'
                file_input.set_input_files(folder_path)
                print("[OK] 已选择文件夹")
                time.sleep(3)
        except Exception as e:
            print(f"选择文件夹失败: {e}")
        
        # 3. 填写项目名称
        print("\n步骤3: 填写项目名称...")
        try:
            # 找项目名称输入框
            name_input = page.locator('input[placeholder*="项目名称"]').first
            if name_input and name_input.is_visible():
                name_input.fill("notemyday")
                print("[OK] 填写项目名称: notemyday")
                time.sleep(1)
            else:
                # 尝试找所有输入框
                inputs = page.locator('input').all()
                for inp in inputs:
                    try:
                        placeholder = inp.get_attribute('placeholder') or ''
                        if '项目' in placeholder or '名称' in placeholder:
                            inp.fill("notemyday")
                            print(f"[OK] 填写项目名称到: {placeholder}")
                            time.sleep(1)
                            break
                    except:
                        pass
        except Exception as e:
            print(f"填写项目名称失败: {e}")
        
        # 4. 修改项目框架为「其他」
        print("\n步骤4: 修改项目框架为其他...")
        try:
            # 找项目框架下拉框（包含 React 的）
            framework_select = page.locator('.tea-select').first
            if framework_select and framework_select.is_visible():
                framework_select.click()
                print("[OK] 点击了框架下拉框")
                time.sleep(1)
                
                # 选择「其他」
                other_option = page.locator('text=其他').first
                if other_option and other_option.is_visible():
                    other_option.click()
                    print("[OK] 选择了其他")
                    time.sleep(1)
        except Exception as e:
            print(f"修改框架失败: {e}")
        
        # 5. 点击部署
        print("\n步骤5: 点击部署...")
        try:
            # 截图看当前状态
            page.screenshot(path='before_deploy.png')
            
            # 找部署按钮
            deploy_btn = page.locator('button', has_text='部署').first
            if deploy_btn and deploy_btn.is_visible():
                deploy_btn.click()
                print("[OK] 点击了部署")
                time.sleep(5)
                page.screenshot(path='deploy_result.png')
            else:
                # 尝试找包含部署文字的按钮
                buttons = page.locator('button').all()
                for btn in buttons:
                    try:
                        text = btn.inner_text()
                        if '部署' in text or '确认' in text:
                            btn.click()
                            print(f"[OK] 点击了按钮: {text}")
                            time.sleep(5)
                            page.screenshot(path='deploy_result.png')
                            break
                    except:
                        pass
                else:
                    print("未找到部署按钮")
        except Exception as e:
            print(f"点击部署失败: {e}")
            page.screenshot(path='error_deploy.png')
        
        print("\n操作完成")
        print("浏览器将在60秒后关闭...")
        time.sleep(60)
        browser.close()

if __name__ == '__main__':
    main()
