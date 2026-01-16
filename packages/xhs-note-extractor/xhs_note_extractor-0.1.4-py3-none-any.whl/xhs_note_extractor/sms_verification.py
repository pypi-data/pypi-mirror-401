import asyncio
import os
import re
from datetime import datetime
from playwright.async_api import async_playwright

# 从环境变量获取配置，允许用户自定义
SMS_SYSTEM_URL = os.getenv('SMS_SYSTEM_URL', 'https://smssystem.dicbs.com/admin/smsrecord')

async def parse_sms_table(page, phone_number, send_time):
    """
    解析短信记录表格，提取符合条件的验证码
    
    Args:
        page: Playwright页面对象
        phone_number: 目标手机号
        send_time: 发送时间，只返回在此时间之后的验证码
        
    Returns:
        str: 符合条件的6位数字验证码，如果没有找到则返回None
    """
    try:
        # 查找表格元素 - 使用更通用的选择器
        table_selectors = [
            'tbody',       # 尝试tbody元素
            '#dataList tbody',  # 尝试特定ID下的tbody
            'table tbody',      # 尝试任何表格下的tbody
        ]
        
        tbody = None
        for selector in table_selectors:
            try:
                tbody = await page.wait_for_selector(selector, timeout=3000)
                print(f'使用选择器 {selector} 找到表格')
                break
            except:
                continue
        
        if not tbody:
            print('未找到表格元素，使用替代方案提取验证码')
            return await extract_codes_from_text(page, send_time)
        
        # 获取所有行
        rows = await tbody.query_selector_all('tr')
        print(f'找到表格行数量: {len(rows)}')
        
        # 只处理第一条数据行（最新的记录）
        if len(rows) > 0:
            row = rows[0]
            try:
                # 获取行内所有单元格
                cells = await row.query_selector_all('td')
                
                if len(cells) < 5:  # 确保有足够的单元格（根据截图，表格有5列）
                    print(f'单元格数量不足（实际: {len(cells)}），跳过该行')
                    return await extract_codes_from_text(page, send_time)
                
                # 根据截图调整列索引：
                # 第0列：ID
                # 第1列：短信内容
                # 第2列：发送号码
                # 第3列：接收号码
                # 第4列：创建时间
                
                # 获取手机号（第4列）
                phone_cell = cells[3]
                phone_text = await phone_cell.inner_text()
                print(f'检查手机号: {phone_text}')
                
                # 检查是否是目标手机号
                if phone_number not in phone_text:
                    print('手机号不匹配，尝试从页面文本提取')
                    return await extract_codes_from_text(page, send_time)
                
                # 获取短信内容（第2列）
                content_cell = cells[1]
                content_text = await content_cell.inner_text()
                print(f'短信内容: {content_text}')
                
                # 查找6位数字验证码
                codes = re.findall(r'\d{6}', content_text)
                if not codes:
                    print('未找到6位验证码，尝试从页面文本提取')
                    return await extract_codes_from_text(page, send_time)
                
                # 获取发送时间（第5列）
                time_cell = cells[4]
                time_text = await time_cell.inner_text()
                print(f'发送时间: {time_text}')
                
                # 解析时间格式
                try:
                    sms_time = datetime.strptime(time_text, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(f'无法解析时间格式: {time_text}')
                    return await extract_codes_from_text(page, send_time)
                
                # 检查时间是否在发送时间之后
                if sms_time > send_time:
                    print(f'找到符合条件的验证码: {codes[0]} (时间: {time_text})')
                    return codes[0]
                else:
                    print(f'验证码时间 {time_text} 早于发送时间 {send_time.strftime("%Y-%m-%d %H:%M:%S")}')
                    return await extract_codes_from_text(page, send_time)
                    
            except Exception as e:
                print(f'解析表格行失败: {e}')
                return await extract_codes_from_text(page, send_time)
        
        print('表格中未找到符合条件的验证码，尝试从页面文本提取')
        # 如果表格中没有找到，尝试从整个页面文本提取
        return await extract_codes_from_text(page, send_time)
        
    except Exception as e:
        print(f'解析表格失败: {e}')
        # 失败时回退到文本提取
        return await extract_codes_from_text(page, send_time)

async def extract_codes_from_text(page, send_time):
    """
    从页面文本中提取验证码的备用方案
    
    Args:
        page: Playwright页面对象
        send_time: 发送时间
        
    Returns:
        str: 符合条件的验证码，如果没有找到则返回None
    """
    try:
        # 提取所有文本内容
        all_text = await page.inner_text('body')
        print(f'页面文本内容长度: {len(all_text)} 字符')
        
        # 查找所有6位数字验证码
        all_codes = re.findall(r'\d{6}', all_text)
        print(f'找到验证码数量: {len(all_codes)} 个')
        
        if all_codes:
            # 返回最新的验证码（页面上的最后一个）
            verification_code = all_codes[-1]
            print(f'获取到验证码：[{verification_code}]')
            return verification_code
        else:
            return None
            
    except Exception as e:
        print(f'从文本提取验证码失败: {e}')
        return None

async def get_verification_code(phone_number, send_time=None, max_retries=5, retry_interval=5):
    """
    获取指定手机号的最新验证码
    
    Args:
        phone_number (str): 目标手机号
        send_time (datetime, optional): 发送时间，只返回在此时间之后的验证码
            默认使用当前时间
        max_retries (int, optional): 最大重试次数，默认5次
        retry_interval (int, optional): 重试间隔时间（秒），默认5秒
        
    Returns:
        str: 6位数字验证码
        
    Raises:
        Exception: 如果经过多次尝试后仍未找到验证码
    """
    # 如果未指定发送时间，使用当前时间
    if send_time is None:
        send_time = datetime.now()
        print(f'未指定发送时间，默认使用: {send_time.strftime("%Y-%m-%d %H:%M:%S")}')
    
    for retry in range(max_retries):
        try:
            print(f'\n=== 第 {retry + 1}/{max_retries} 次尝试 ===')
            # 启动Playwright
            async with async_playwright() as p:
                # 启动浏览器
                browser = await p.chromium.launch(
                    headless=False,
                    args=['--no-sandbox', '--disable-setuid-sandbox'],
                    timeout=60000
                )
                
                # 创建页面
                page = await browser.new_page()
                
                # 访问登录页面
                await page.goto('https://smssystem.dicbs.com/admin/user/login', 
                              wait_until='domcontentloaded', timeout=60000)
                
                print(f'当前页面: {page.url}')
                
                # 检查是否需要登录
                if 'login' in page.url:
                    print('检测到未登录状态，开始登录...')
                    
                    # 输入账号密码
                    await page.fill('input[name="username"]', '京东xhs')
                    await page.fill('input[name="password"]', '123456')
                    await page.fill('input[name="captcha"]', '1234')
                    
                    # 点击登录按钮
                    await page.click('button')
                    await page.wait_for_load_state('domcontentloaded', timeout=30000)
                    
                    # 检查是否登录成功
                    if 'login' not in page.url:
                        print('登录成功！')
                    else:
                        print('登录失败，可能是验证码错误，但继续尝试...')
                
                # 确保在目标页面
                if SMS_SYSTEM_URL not in page.url:
                    await page.goto(SMS_SYSTEM_URL, wait_until='domcontentloaded', timeout=60000)
                
                # 尝试搜索手机号
                print(f'尝试搜索手机号：{phone_number}...')
                try:
                    # 查找搜索输入框
                    search_box = await page.wait_for_selector('input[name*="receiver"], input[id*="receiver"]', timeout=10000)
                    if search_box:
                        await search_box.fill(phone_number)
                        await page.click('#memberSearch')
                        await page.wait_for_load_state('domcontentloaded', timeout=15000)
                        print('搜索完成')
                    else:
                        print('未找到搜索框，直接提取表格内容')
                except Exception as e:
                    print(f'搜索失败: {e}')
                
                # 解析表格内容
                print('解析表格内容...')
                verification_code = await parse_sms_table(page, phone_number, send_time)
                
                if verification_code:
                    await browser.close()
                    return verification_code
                else:
                    print('未找到符合条件的验证码')
                    await browser.close()
            
        except Exception as e:
            print(f'获取验证码失败: {type(e).__name__}: {str(e)}')
            
        # 如果不是最后一次尝试，等待一段时间后重试
        if retry < max_retries - 1:
            print(f'等待 {retry_interval} 秒后重试...')
            await asyncio.sleep(retry_interval)
    
    raise Exception(f'经过 {max_retries} 次尝试后仍未找到符合条件的验证码')


def get_verification_code_sync(phone_number, send_time=None, max_retries=5, retry_interval=5):
    """
    同步版本的获取验证码函数
    
    Args:
        phone_number (str): 目标手机号
        send_time (datetime, optional): 发送时间，只返回在此时间之后的验证码
            默认使用当前时间
        max_retries (int, optional): 最大重试次数，默认5次
        retry_interval (int, optional): 重试间隔时间（秒），默认5秒
        
    Returns:
        str: 6位数字验证码
        
    Raises:
        Exception: 如果经过多次尝试后仍未找到验证码
    """
    return asyncio.run(get_verification_code(
        phone_number=phone_number,
        send_time=send_time,
        max_retries=max_retries,
        retry_interval=retry_interval
    ))


if __name__ == '__main__':
    """
    示例用法
    """
    import sys
    
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('用法: python sms_verification.py <手机号> [<发送时间>]')
        print('发送时间格式: YYYY-MM-DD HH:MM:SS')
        sys.exit(1)
    
    phone_number = sys.argv[1]
    
    if len(sys.argv) == 3:
        try:
            send_time = datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print('发送时间格式错误，请使用YYYY-MM-DD HH:MM:SS格式')
            sys.exit(1)
    else:
        send_time = None
    
    try:
        # 使用同步版本调用
        code = get_verification_code_sync(phone_number, send_time)
        print(f'\n最终结果：获取到验证码：[{code}]')
    except Exception as e:
        print(f'\n执行失败: {str(e)}')
        sys.exit(1)
