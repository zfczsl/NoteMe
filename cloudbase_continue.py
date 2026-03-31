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
        page.goto('https://console.cloud.tencent.com/tcb', timeout=60000)
        
        print("\n等待15秒让页面加载...")
        time.sleep(15)
        
        # 截图看当前状态
        page.screenshot(path='current_state.png')
        print("[OK] 已截图 current_state.png")
        
        # 1. 点击 noteme 环境卡片进入
        print("\n步骤1: 点击 noteme 环境...")
        try:
            # 找包含 noteme 的元素并点击
            noteme_card = page.locator('text=noteme').first
            if noteme_card.is_visible():
                noteme_card.click()
                print("[OK] 点击了 noteme 环境")
                time.sleep(3)
                page.screenshot(path='step1_env.png')
            else:
                print("未找到 noteme 环境")
        except Exception as e:
            print(f"点击环境失败: {e}")
        
        # 2. 找左侧菜单的静态网站托管
        print("\n步骤2: 找静态网站托管菜单...")
        time.sleep(3)
        
        try:
            # 列出所有可见的文本
            all_text = page.locator('text=/./').all()
            print(f"页面上的文本元素:")
            menu_items = []
            for el in all_text:
                try:
                    text = el.inner_text()
                    if text and len(text) < 50:
                        menu_items.append(text)
                except:
                    pass
            
            # 打印可能相关的菜单项
            for item in menu_items:
                if any(keyword in item for keyword in ['静态', '网站', '托管', '存储', '文件', '部署', 'hosting']):
                    print(f"  找到: {item}")
            
            # 尝试点击静态网站托管
            hosting = page.locator('text=静态网站托管').first
            if hosting.is_visible():
                hosting.click()
                print("[OK] 点击了静态网站托管")
                time.sleep(3)
                page.screenshot(path='step2_hosting.png')
            else:
                print("未找到静态网站托管，尝试找其他菜单...")
                # 尝试展开更多菜单
                expand_btn = page.locator('text=更多, text=展开, .expand-icon').first
                if expand_btn and expand_btn.is_visible():
                    expand_btn.click()
                    time.sleep(1)
        except Exception as e:
            print(f"找菜单失败: {e}")
        
        # 3. 找上传按钮
        print("\n步骤3: 找上传按钮...")
        time.sleep(2)
        
        try:
            # 列出所有按钮
            buttons = page.locator('button').all()
            print(f"找到 {len(buttons)} 个按钮:")
            for btn in buttons:
                try:
                    text = btn.inner_text()
                    if text:
                        print(f"  - {text[:40]}")
                        # 点击包含上传或文件的按钮
                        if any(kw in text for kw in ['上传', '文件', '部署', '新建']):
                            if btn.is_visible():
                                btn.click()
                                print(f"[OK] 点击了: {text}")
                                time.sleep(2)
                                page.screenshot(path='step3_clicked.png')
                                break
                except:
                    pass
        except Exception as e:
            print(f"找按钮失败: {e}")
        
        print("\n操作完成")
        print("浏览器将在60秒后关闭...")
        time.sleep(60)
        browser.close()

if __name__ == '__main__':
    main()
