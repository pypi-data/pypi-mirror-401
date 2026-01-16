#!/usr/bin/env python3
"""
Phone Agent Usage Examples / Phone Agent 使用示例

Demonstrates how to use Phone Agent for phone automation tasks via Python API.
演示如何通过 Python API 使用 Phone Agent 进行手机自动化任务。
"""
import json
from datetime import datetime

from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.config import get_messages
from phone_agent.model import ModelConfig

from xhs_note_extractor.login_propmt import phone_agent_protocol_v3_t1, phone_agent_protocol_v3_t3
from xhs_note_extractor.sms_verification import get_verification_code_sync

def do_login(device_id:str, lang: str = "cn", phone_number:str = "19163152334"):
    """Basic task example / 基础任务示例"""
    # Configure model endpoint
    model_config = ModelConfig(
        model_name="ZhipuAI/AutoGLM-Phone-9B",
        temperature=0.1,
        api_key="ms-ed9ed848-d630-4192-a688-37ebbf985246",
        base_url="https://api-inference.modelscope.cn/v1"
    )

    # Configure Agent behavior
    agent_config = AgentConfig(
        max_steps=50,
        verbose=True,
        lang=lang,
        device_id=device_id,
    )

    # Create Agent
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )
    cur_date_time = datetime.now()
    print(f'phone_number:{phone_number}')
    # 从文件加载协议内容
    prompt_task1 = phone_agent_protocol_v3_t1.format(phone_number)
    result = agent.run(prompt_task1)
    print(f"prompt_task1: {result}")
    
    # 解析JSON结果
    try:
        result_json = json.loads(result)
        print(f"result_json: {result_json}")
        # 检查任务1是否成功
        if result_json.get("status") != "success":
            # 特别检查是否为图片验证码错误
            if result_json.get("code") == "CAPTCHA_DETECTED":
                print(f"检测到图片验证码，立即终止登录: {result_json.get('message')}")
                # 在遇到图片验证码时，不仅返回False，还设置一个特殊的环境变量或全局标记
                # 由于Python没有全局变量，我们通过抛出异常来传递这个特殊情况
                raise RuntimeError("CAPTCHA_DETECTED")
            else:
                print(f"验证码触发失败: {result_json.get('message')}")
            return False
    except json.JSONDecodeError:
        print(f"result error: {result}")
        # 如果不是JSON格式，尝试兼容旧格式
        
        # 检查是否包含图片验证码相关内容（更全面的关键词列表）
        image_captcha_keywords = [
            "图片验证码", "点击文字", "旋转图片", "滑块", "拼图", "拖拽", "文字验证",
            "验证图片", "点击验证", "滑动验证", "拖动验证", "旋转验证",
            "点击图片上的文字", "图片上的文字", "验证码图片"
        ]
        has_image_captcha = any(keyword in result for keyword in image_captcha_keywords)
        
        if has_image_captcha:
            print("检测到图片验证码，立即终止登录")
            # 在遇到图片验证码时，抛出异常以确保任务被完全终止
            raise RuntimeError("CAPTCHA_DETECTED")
            return False
        
        # 原始的旧格式检查逻辑
        if (not "验证码已触发" in result and not "验证码已成功发送" in result and "任务已完成" not in result ) and ("图片验证码界面" in result):
            print("检测到图片验证码，验证码触发失败")
            # 在遇到图片验证码时，抛出异常以确保任务被完全终止
            raise RuntimeError("CAPTCHA_DETECTED")
            return False
    # 3. 自定义重试参数
    print(f"\n获取手机号 {phone_number} 的验证码（3次尝试，每次间隔3秒）...")
    code = get_verification_code_sync(
        phone_number,
        send_time=cur_date_time,
        max_retries=3,
        retry_interval=3
    )
    print(f"手机号: {phone_number}, 验证码: {code}")
    prompt_task3 = phone_agent_protocol_v3_t3.format(phone_number, code)
    result = agent.run(prompt_task3)
    print(f"prompt_task3: {result}")
    
    # 解析JSON结果
    try:
        result_json = json.loads(result)
        # 检查任务3是否成功
        return result_json.get("status") == "success"
    except json.JSONDecodeError:
        # 如果不是JSON格式，尝试兼容旧格式
        return "登录成功" in result

def example_with_callbacks(lang: str = "cn"):
    """Task example with callbacks / 带回调的任务示例"""
    msgs = get_messages(lang)

    def my_confirmation(message: str) -> bool:
        """Sensitive operation confirmation callback / 敏感操作确认回调"""
        print(f"\n[{msgs['confirmation_required']}] {message}")
        response = input(f"{msgs['continue_prompt']}: ")
        return response.lower() in ("yes", "y", "是")

    def my_takeover(message: str) -> None:
        """Manual takeover callback / 人工接管回调"""
        print(f"\n[{msgs['manual_operation_required']}] {message}")
        print(msgs["manual_operation_hint"])
        input(f"{msgs['press_enter_when_done']}: ")

    # Create Agent with custom callbacks
    agent_config = AgentConfig(lang=lang)
    agent = PhoneAgent(
        agent_config=agent_config,
        confirmation_callback=my_confirmation,
        takeover_callback=my_takeover,
    )

    # Execute task that may require confirmation
    result = agent.run("打开淘宝搜索无线耳机并加入购物车")
    print(f"{msgs['task_result']}: {result}")


def example_step_by_step(lang: str = "cn"):
    """Step-by-step execution example (for debugging) / 单步执行示例（用于调试）"""
    msgs = get_messages(lang)

    agent_config = AgentConfig(lang=lang)
    agent = PhoneAgent(agent_config=agent_config)

    # Initialize task
    result = agent.step("打开美团搜索附近的火锅店")
    print(f"{msgs['step']} 1: {result.action}")

    # Continue if not finished
    while not result.finished and agent.step_count < 10:
        result = agent.step()
        print(f"{msgs['step']} {agent.step_count}: {result.action}")
        print(f"  {msgs['thinking']}: {result.thinking[:100]}...")

    print(f"\n{msgs['final_result']}: {result.message}")


def example_multiple_tasks(lang: str = "cn"):
    """Batch task example / 批量任务示例"""
    msgs = get_messages(lang)

    agent_config = AgentConfig(lang=lang)
    agent = PhoneAgent(agent_config=agent_config)

    tasks = [
        "打开高德地图查看实时路况",
        "打开大众点评搜索附近的咖啡店",
        "打开bilibili搜索Python教程",
    ]

    for task in tasks:
        print(f"\n{'=' * 50}")
        print(f"{msgs['task']}: {task}")
        print("=" * 50)

        result = agent.run(task)
        print(f"{msgs['result']}: {result}")

        # Reset Agent state
        agent.reset()


def example_remote_device(lang: str = "cn"):
    """Remote device example / 远程设备示例"""
    from phone_agent.adb import ADBConnection

    msgs = get_messages(lang)

    # Create connection manager
    conn = ADBConnection()

    # Connect to remote device
    success, message = conn.connect("192.168.1.100:5555")
    if not success:
        print(f"{msgs['connection_failed']}: {message}")
        return

    print(f"{msgs['connection_successful']}: {message}")

    # Create Agent with device specified
    agent_config = AgentConfig(
        device_id="192.168.1.100:5555",
        verbose=True,
        lang=lang,
    )

    agent = PhoneAgent(agent_config=agent_config)

    # Execute task
    result = agent.run("打开微信查看消息")
    print(f"{msgs['task_result']}: {result}")

    # Disconnect
    conn.disconnect("192.168.1.100:5555")



def check_adb_devices():
    """Check if any ADB devices are connected / 检查是否有 ADB 设备连接"""
    import subprocess
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:] # Skip header
        devices = [line for line in lines if line.strip()]
        if not devices:
            print("\nError: No Android devices connected via ADB.")
            print("错误: 未通过 ADB 连接任何 Android 设备。")
            print("Please connect a device or start an emulator.")
            print("请连接设备或启动模拟器。")
            return False
        return True
    except FileNotFoundError:
        print("\nError: 'adb' command not found. Please install Android Platform Tools.")
        print("错误: 未找到 'adb' 命令。请安装 Android Platform Tools。")
        return False
#
# if __name__ == "__main__":
#     if not check_adb_devices():
#         exit(1)
#
#     import argparse
#
#     parser = argparse.ArgumentParser(description="Phone Agent Usage Examples")
#     parser.add_argument(
#         "--lang",
#         type=str,
#         default="cn",
#         choices=["cn", "en"],
#         help="Language for UI messages (cn=Chinese, en=English)",
#     )
#     args = parser.parse_args()
#
#     msgs = get_messages(args.lang)
#
#     print("Phone Agent Usage Examples")
#     print("=" * 50)
#
#     # Run basic example
#     print(f"\n1. Basic Task Example")
#     print("-" * 30)
#     do_login(args.lang)
#
#     # Uncomment to run other examples
#     # print(f"\n2. Task Example with Callbacks")
#     # print("-" * 30)
#     # example_with_callbacks(args.lang)
#
#     # print(f"\n3. Step-by-step Example")
#     # print("-" * 30)
#     # example_step_by_step(args.lang)
#
#     # print(f"\n4. Batch Task Example")
#     # print("-" * 30)
#     # example_multiple_tasks(args.lang)
#
#     # print(f"\n5. Remote Device Example")
#     # print("-" * 30)
#     # example_remote_device(args.lang)
