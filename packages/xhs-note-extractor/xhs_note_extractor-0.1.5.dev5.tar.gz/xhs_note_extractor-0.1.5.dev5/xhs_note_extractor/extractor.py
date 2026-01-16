"""
小红书笔记提取器模块

该模块提供了从小红书URL中提取笔记信息的功能，包括：
- URL解析和转换
- 设备连接和页面跳转
- 笔记内容提取（正文、图片、点赞数等）
- 结构化数据返回

作者: JoyCode Agent
版本: 1.0.0
"""

import uiautomator2 as u2
import time
import re
import requests
import logging
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse, parse_qs
import xml.etree.ElementTree as ET

# 延迟加载agent_login模块以避免不必要的依赖
from .date_desc_utils import parse_time_to_timestamp_ms
from .number_utils import parse_count_to_int

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XHSNoteExtractor:
    """
    小红书笔记提取器类
    
    提供了从小红书URL中提取笔记信息的完整功能，
    包括URL解析、设备连接、页面跳转和笔记内容提取。
    """
    
    def __init__(self, devices:dict = None):
        """
        初始化小红书笔记提取器
        
        Args:
            devices (dict, optional): 设备信息字典，包含设备序列号和对应小红书账号可选手机号
            {
                "b520805": ["13800000000"]
            }
        
        Raises:
            ValueError: 当设备信息为空或无效时抛出异常
        """
        if not devices:
            raise ValueError("设备信息必须从外部传入")
        
        self.device = None # 当前设备
        self.next_phone = None # 下一个手机号
        self.devices_info = devices  # 存储设备信息字典
        self.problematic_devices = []  # 存储无法获取笔记的设备信息
        self.enable_time_logging = True  # 默认启用耗时打印
        self.phone_last_attempt = {}  # 记录每个手机号的最后尝试时间
        self.phone_cooldown_time = 300  # 手机号冷却时间（秒），默认5分钟
        
        # 日志记录设备信息
        logger.info(f"已配置设备信息: {self.devices_info}")
        logger.info(f"手机号冷却时间: {self.phone_cooldown_time}秒")
        logger.info("设备将在需要时连接")
    
    def _get_next_phone_number(self, device_serial: str) -> Optional[str]:
        """
        获取指定设备的下一个手机号（循环）
        
        Args:
            device_serial (str): 设备序列号
            
        Returns:
            str: 下一个手机号，如果没有则返回None
        """
        if device_serial not in self.devices_info:
            return None
        
        phone_list = self.devices_info[device_serial]
        if not phone_list:
            return None
        
        # 如果当前没有设置下一个手机号，返回第一个
        if not self.next_phone:
            self.next_phone = phone_list[0]
            return self.next_phone
        
        # 找到当前手机号在列表中的索引
        try:
            current_index = phone_list.index(self.next_phone)
            # 循环到下一个
            next_index = (current_index + 1) % len(phone_list)
            self.next_phone =  phone_list[next_index]
        except ValueError:
            # 如果当前手机号不在列表中，返回第一个
            self.next_phone = phone_list[0]
        return self.next_phone
    def _time_method(self, method_name, start_time):
        """
        记录方法执行时间
        
        Args:
            method_name (str): 方法名称
            start_time (float): 开始时间
        """
        if self.enable_time_logging:
            elapsed_time = time.time() - start_time
            if elapsed_time < 1:
                logger.info(f"⏱️  [{method_name}] 耗时: {elapsed_time*1000:.0f}ms")
            else:
                logger.info(f"⏱️  [{method_name}] 耗时: {elapsed_time:.2f}s")
    

    
    def connect_device(self, device_serial: Optional[str] = None) -> bool:
        """
        连接设备
        
        Args:
            device_serial (str, optional): 指定设备序列号，如果为None则使用devices_info中的第一个设备
            
        Returns:
            bool: 是否成功连接设备
        """
        start_time = time.time()
        
        # 如果指定了设备序列号，则使用指定的设备
        target_device = device_serial
        
        # 如果没有指定设备序列号，尝试使用devices_info中的第一个设备
        if not target_device and self.devices_info:
            target_device = next(iter(self.devices_info.keys()))
        
        try:
            if not target_device:
                logger.error("✗ 设备连接失败: 无法确定设备序列号")
                self._time_method("connect_device", start_time)
                return False
            
            self.device = u2.connect(target_device)
            logger.info(f"✓ 已连接设备: {self.device.serial}")
            self._time_method("connect_device", start_time)
            # 重启小红书应用以确保登录状态
            logger.info("🔄 重启小红书应用...")
            self.device.app_stop("com.xingin.xhs")
            time.sleep(1)
            self.device.app_start("com.xingin.xhs")
            time.sleep(3)
            # 获取下一个手机号
            self.next_phone = self._get_next_phone_number(target_device)
            logger.warning(f'next_phone:{self.next_phone}')
            return True
        except Exception as e:
            logger.error(f"✗ 设备连接失败: {e}")
            self._time_method("connect_device", start_time)
            return False
    
    def switch_to_next_device(self) -> bool:
        """
        切换到下一个可用设备
        
        Returns:
            bool: 是否成功切换到下一个设备
        """
        self.next_phone = None # 重置下一个手机号为None
        if not self.devices_info or len(self.devices_info) <= 1:
            logger.warning("没有更多可用设备可以切换")
            return False
        
        # 获取当前设备的序列号
        current_serial = self.device.serial if self.device else None
        logger.info(f"当前设备: {current_serial}")
        # 转换为列表以便切换
        device_serials = list(self.devices_info.keys())
        logger.info(f"device_serials: {device_serials}")
        # 找到当前设备的索引
        current_index = device_serials.index(current_serial) if current_serial in device_serials else -1
        logger.info(f"current_index: {current_index}")
        
        # 如果当前设备不在列表中，并且有尝试过的设备记录，则从尝试过的设备之后开始
        attempted_serials = [d['serial'] for d in self.problematic_devices]
        if current_index == -1 and attempted_serials:
            # 找到最后一个尝试过的设备的索引
            last_attempted = attempted_serials[-1]
            if last_attempted in device_serials:
                current_index = device_serials.index(last_attempted)
        
        # 移动到下一个设备
        next_index = (current_index + 1) % len(device_serials)
        next_device_serial = device_serials[next_index]
        logger.info(f"next_device_serial: {next_device_serial}")
        logger.info(f"尝试切换到设备: {next_device_serial}")
        return self.connect_device(next_device_serial)
    def is_device_connected(self) -> bool:
        """
        检查设备是否仍然连接
        
        Returns:
            bool: 设备是否连接
        """
        if not self.device:
            return False
        try:
            # 通过获取设备信息来验证连接
            self.device.info
            return True
        except:
            return False
    
    def get_problematic_devices(self) -> List[Dict[str, Union[str, float]]]:
        """
        获取无法获取笔记的设备列表
        
        Returns:
            List[Dict[str, Union[str, float]]]: 包含有问题设备信息的列表，每个设备信息包括：
                - serial: 设备序列号
                - reason: 问题原因
                - note_id: 尝试提取的笔记ID
                - timestamp: 记录时间戳
        """
        return self.problematic_devices
    
    def clear_problematic_devices(self) -> None:
        """
        清空有问题的设备列表
        """
        self.problematic_devices.clear()
    # 清除缓存并重启APP
    def clear_login_state(self, device_serial=None):
        import uiautomator2 as u2
        import time

        # 连接设备
        d = u2.connect(device_serial)

        # 彻底杀掉APP进程（使用两种方式确保完全终止）
        d.app_stop('com.xingin.xhs')
        d.shell('am force-stop com.xingin.xhs')
        time.sleep(2)  # 等待进程完全终止
        
        # 启动APP
        d.app_start('com.xingin.xhs')
        time.sleep(3)  # 等待APP完全启动
        try:
            if not d(text='我').exists():
                print("已退出登录，无需退出登录")
                return
                
            # 点击我的/个人中心按钮
            d(description='我').click()
            time.sleep(2)

            if d(text='微信登录').exists() or d(text='手机号登录').exists():
                print("已登录，无需退出登录")
                return

            # 点击设置按钮
            d(description='设置').click()
            time.sleep(2)
            
            # 滚动到退出登录选项
            d.swipe_ext('up', scale=0.5)
            time.sleep(1)
            
            # 点击退出登录
            d(text='退出登录').click()
            time.sleep(1)
            
            # 确认退出
            d(text='退出登录').click()
            time.sleep(2)
            
            print("退出登录成功")
        except Exception as e:
            print(f"退出登录失败: {e}")
    
    @staticmethod
    def parse_xhs_url(url: str) -> Dict[str, str]:
        """
        解析小红书URL，提取note_id和xsec_token
        
        Args:
            url (str): 小红书URL，支持标准格式或xhsdiscover协议格式
            
        Returns:
            Dict[str, str]: 包含note_id和xsec_token的字典
            
        Raises:
            ValueError: 当URL格式不正确时抛出异常
        """
        start_time = time.time()
        # 处理xhsdiscover协议格式
        if url.startswith("xhsdiscover://"):
            # 提取note_id
            note_id_match = re.search(r'item/([^?]+)', url)
            if not note_id_match:
                raise ValueError("无法从xhsdiscover URL中提取note_id")
            
            note_id = note_id_match.group(1)
            
            # 尝试从open_url参数中提取原始URL
            open_url_match = re.search(r'open_url=([^&]+)', url)
            xsec_token = ""
            if open_url_match:
                open_url = open_url_match.group(1)
                # 解码URL
                import urllib.parse
                decoded_url = urllib.parse.unquote(open_url)
                # 从原始URL中提取xsec_token
                token_match = re.search(r'xsec_token=([^&]+)', decoded_url)
                if token_match:
                    xsec_token = token_match.group(1)
            
            return {
                "note_id": note_id,
                "xsec_token": xsec_token,
                "original_url": url
            }
        
        # 处理标准URL格式
        elif "xiaohongshu.com" in url:
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # 查找explore部分和note_id
            if 'explore' in path_parts:
                explore_index = path_parts.index('explore')
                if explore_index + 1 < len(path_parts):
                    note_id = path_parts[explore_index + 1]
                else:
                    raise ValueError("URL中缺少note_id")
            # 兼容 /discovery/item/ 格式
            elif 'discovery' in path_parts and 'item' in path_parts:
                item_index = path_parts.index('item')
                if item_index + 1 < len(path_parts):
                    note_id = path_parts[item_index + 1]
                else:
                    raise ValueError("URL中缺少note_id")
            else:
                raise ValueError("URL格式不正确，缺少/explore/或/discovery/item/路径")
            
            # 提取查询参数中的xsec_token
            query_params = parse_qs(parsed_url.query)
            xsec_token = query_params.get('xsec_token', [''])[0]
            
            elapsed_time = time.time() - start_time
            logger.info(f"[parse_xhs_url] 耗时: {elapsed_time:.3f}秒")
            return {
                "note_id": note_id,
                "xsec_token": xsec_token,
                "original_url": url
            }
        
        else:
            elapsed_time = time.time() - start_time
            logger.info(f"[parse_xhs_url] 耗时: {elapsed_time:.3f}秒")
            raise ValueError("不支持的URL格式")
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        验证URL是否是有效的小红书URL
        
        Args:
            url (str): 要验证的URL
            
        Returns:
            bool: URL是否有效
        """
        try:
            XHSNoteExtractor.parse_xhs_url(url)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def convert_to_xhsdiscover_format(note_id: str, xsec_token: str = "") -> str:
        """
        将note_id和xsec_token转换为xhsdiscover协议格式
        
        Args:
            note_id (str): 笔记ID
            xsec_token (str): xsec_token参数
            
        Returns:
            str: xhsdiscover协议格式的URL
        """
        start_time = time.time()
        result = ""
        if xsec_token:
            original_url = f"http://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_feed"
            encoded_url = requests.utils.quote(original_url)
            result = f"xhsdiscover://item/{note_id}?open_url={encoded_url}"
        else:
            result = f"xhsdiscover://item/{note_id}"
        
        elapsed_time = time.time() - start_time
        logger.info(f"[convert_to_xhsdiscover_format] 耗时: {elapsed_time:.3f}秒")
        return result
    
    def extract_note_data(self, url: Optional[str] = None, note_id: Optional[str] = None,
                         xsec_token: Optional[str] = None) -> Optional[Dict[str, Union[str, List[str]]]]:
        """
        从小红书笔记中提取数据，支持设备重试机制
        
        Args:
            url (str, optional): 小红书URL，如果提供则会解析其中的note_id和xsec_token
            note_id (str, optional): 笔记ID，如果提供则直接使用
            xsec_token (str, optional): xsec_token参数
            
        Returns:
            Optional[Dict[str, Union[str, List[str]]]]: 包含笔记数据的字典，如果没有成功则返回None
            
        Raises:
            Exception: 当提取过程中出现错误时抛出异常
            RuntimeError: 当检测到图片验证码时抛出此异常
        """
        start_time = time.time()
        # 如果提供了URL，则先解析它（验证URL有效性）
        if url:
            parsed_data = self.parse_xhs_url(url)
            note_id = parsed_data["note_id"]
            xsec_token = parsed_data["xsec_token"]
        
        max_retries = len(self.devices_info) if self.devices_info else 1
        attempted_devices = []
        
        for attempt in range(max_retries):
            logger.info(f"尝试第 {attempt + 1}/{max_retries} 次提取笔记: {note_id}")
            
            # 检查设备是否连接，如果没有则尝试连接
            if self.device is None:
                if not self.connect_device():
                    logger.warning("设备连接失败，尝试下一个设备")
                    # 记录连接失败的设备
                    device_serials = list(self.devices_info.keys())
                    if device_serials and attempt < len(device_serials):
                        failed_device = device_serials[attempt]
                        if failed_device not in [d['serial'] for d in self.problematic_devices]:
                            self.problematic_devices.append({
                                'serial': failed_device,
                                'reason': '设备连接失败',
                                'note_id': note_id,
                                'timestamp': time.time()
                            })
                    if self.switch_to_next_device():
                        continue
                    else:
                        break
            
            # 构建跳转URL
            jump_url = self.convert_to_xhsdiscover_format(note_id, xsec_token)
            
            logger.info(f"正在尝试跳转至笔记: {note_id} (设备: {self.device.serial if self.device else '未知'})")
            
            try:
                # # 在跳转链接前重启APP
                # logger.info(f"🔄 准备跳转至笔记 {note_id}，正在重启APP...")
                # self.restart_xhs_app()
                
                # 发起跳转
                self.device.open_url(jump_url)
                logger.info("✓ 已发送跳转指令，等待页面加载...")
                need_retry = False
                # 使用现有的xhs_utils功能提取数据
                data = self._get_detail_data(jump_url)
                # 如果返回None，说明需要登录，尝试下一个设备
                if data is None:
                    logger.warning(f"当前设备{self.device.serial}需要登录，尝试切换到下一个设备")
                    attempted_devices.append(self.device.serial if self.device else "未知设备")
                    # 尝试重新登录
                    # 触发退出登录
                    
                    # 触发登录
                    try:
                        # 延迟加载agent_login模块以避免不必要的依赖
                        from .agent_login import do_login
                        
                        # 获取当前设备的所有手机号列表
                        phone_list = self.devices_info.get(self.device.serial, [])
                        if not phone_list:
                            logger.warning(f"设备{self.device.serial}没有配置手机号")
                            attempted_devices.append(self.device.serial)  # 记录尝试过的设备
                            failed_device_serial = self.device.serial
                            self.device = None
                        else:
                            # 找到当前手机号在列表中的索引
                            current_phone = self.next_phone
                            current_index = phone_list.index(current_phone) if current_phone in phone_list else -1
                            
                            # 从下一个手机号开始循环尝试，不包括当前手机号
                            phone_count = len(phone_list)
                            login_success = False
                            
                            # 如果当前手机号在列表中，从下一个开始尝试；否则从第一个开始
                            start_index = (current_index + 1) % phone_count if current_index != -1 else 0
                            
                            # 尝试当前手机号之后的所有手机号（循环一次）
                            for i in range(phone_count):
                                # 计算当前要尝试的手机号索引
                                next_index = (start_index + i) % phone_count
                                self.next_phone = phone_list[next_index]
                                
                                # 如果已经尝试过所有手机号，或者回到了当前手机号（如果当前手机号在列表中），则停止
                                if current_index != -1 and next_index == current_index:
                                    break
                                    
                                logger.warning(f'attempting phone:{self.next_phone}')
                                
                                # 检查手机号是否在冷却期内
                                current_time = time.time()
                                last_attempt = self.phone_last_attempt.get(self.next_phone, 0)
                                if current_time - last_attempt < self.phone_cooldown_time:
                                    remaining_time = self.phone_cooldown_time - (current_time - last_attempt)
                                    logger.warning(f'手机号{self.next_phone}正在冷却中，剩余{int(remaining_time)}秒，跳过尝试')
                                    continue
                                    
                                try:
                                    self.clear_login_state(self.device.serial)
                                    # 尝试登录
                                    login_result = do_login(phone_number=self.next_phone, device_id=self.device.serial)
                                    
                                    # 记录手机号的最后尝试时间
                                    self.phone_last_attempt[self.next_phone] = current_time
                                    
                                    if login_result:
                                        logger.info(f"✓ 设备{self.device.serial}使用手机号{self.next_phone}登录成功")
                                        login_success = True
                                        break
                                    else:
                                        logger.warning(f"✗ 设备{self.device.serial}使用手机号{self.next_phone}登录失败")
                                except RuntimeError as e:
                                    if str(e) == "CAPTCHA_DETECTED":
                                        logger.error("✗ 检测到图片验证码，完全终止当前任务")
                                        # 在遇到图片验证码时，完全终止当前任务，不再尝试任何其他设备或手机号
                                        # 通过抛出异常来终止整个extract_note_data方法
                                        raise RuntimeError("CAPTCHA_DETECTED")
                                    elif str(e) == "SMS_LIMIT_EXCEEDED":
                                        logger.error("✗ 短信发送次数已达上限，完全终止当前任务")
                                        # 在遇到发送次数限制时，同样完全终止当前任务，不再尝试任何其他设备或手机号
                                        # 通过抛出异常来终止整个extract_note_data方法
                                        raise RuntimeError("SMS_LIMIT_EXCEEDED")
                                    else:
                                        # 其他RuntimeError异常，继续尝试下一个手机号
                                        logger.warning(f"✗ 登录过程中出现异常: {e}")
                                        continue
                            
                            if login_success:
                                need_retry = True
                                break
                            else:
                                logger.warning(f"✗ 设备{self.device.serial}尝试所有手机号均登录失败")
                                attempted_devices.append(self.device.serial)  # 记录尝试过的设备
                                failed_device_serial = self.device.serial
                                self.device = None
                            
                            # 手动记录失败的设备信息
                            if failed_device_serial not in [d['serial'] for d in self.problematic_devices]:
                                self.problematic_devices.append({
                                    'serial': failed_device_serial,
                                    'reason': '设备登录失败',
                                    'note_id': note_id,
                                    'timestamp': time.time()
                                })
                            
                            # 尝试切换到下一个设备
                            if not self.switch_to_next_device():
                                logger.error("没有更多可用设备，提取失败")
                                self._time_method("extract_note_data", start_time)
                                return {}
                            need_retry = True
                    except ImportError as e:
                        logger.warning(f"无法导入登录模块: {e}")
                        logger.warning("将尝试跳过登录步骤，继续使用当前设备")
                        continue
                if need_retry:
                    logger.warning("完成再次登录或切换设备，重试采集笔记数据")
                    continue
                logger.info(f"✓ 成功提取笔记数据，点赞数: {data['likes']}, 图片数: {len(data['image_urls'])}")
                self._time_method("extract_note_data", start_time)
                return data
                
            except Exception as e:
                logger.error(f"✗ 提取笔记数据失败: {e}")
                attempted_devices.append(self.device.serial if self.device else "未知设备")
                
                # 记录有问题的设备
                if self.device and self.device.serial not in [d['serial'] for d in self.problematic_devices]:
                    self.problematic_devices.append({
                        'serial': self.device.serial,
                        'reason': f'提取异常: {str(e)}',
                        'note_id': note_id,
                        'timestamp': time.time()
                    })
                
                # 如果还有设备可用，尝试下一个
                if attempt < max_retries - 1 and self.switch_to_next_device():
                    continue
                else:
                    logger.error("所有设备尝试完毕，提取失败")
                    self._time_method("extract_note_data", start_time)
        logger.error(f"所有设备尝试完毕，提取失败。尝试过的设备: {attempted_devices}")
        self._time_method("extract_note_data", start_time)
        return {}
    
    def _get_detail_data(self, jump_url: str) -> Dict[str, Union[str, List[str]]]:
        """
        从当前已经打开的小红书详情页提取完整正文、图片和点赞数。
        优化版本: 使用 dump_hierarchy 替代遍历，大幅提升速度。
        
        Args:
            jump_url (str): 笔记的跳转URL，用于白屏时重新加载
            
        Returns:
            Dict[str, Union[str, List[str]]]: 包含笔记数据的字典
        """
        start_time = time.time()
        logger.info("🔍 进入深度提取模式 (XML优化版)...")
        
        # 1. 验证是否进入详情页 & 展开全文
        detail_loaded = False
        try:
            if self.device(text="展开").exists:
                self.device(text="展开").click()
        except: pass

        # 超快速检查 - 只等0.2秒
        time.sleep(0.2)
        
        # 快速检查登录状态
        if self.device(textContains="其他登录方式").exists or self.device(textContains="微信登录").exists or self.device(textContains="登录发现更多精彩").exists:
            logger.error("✗ 需要登录才能查看详情页内容，提取终止")
            return None
        
        # 极简检查 - 只检查一次
        time.sleep(0.3)
        detail_count = 5
        detail_loaded = False
        while(detail_count > 0):
            if not self.device(textContains="关注").exists:
                detail_count -= 1
                time.sleep(0.1)
                continue
            detail_loaded = True
            break    
        
        if not detail_loaded:
            logger.warning("⚠ 警告:详情页特征未发现,提取可能不完整")

        # 智能滚动 - 确保看到发布时间和评论区 (优化速度版)
        scroll_phase_start = time.time()
        try:
            # 定义需要查找的目标元素 (正则匹配)
            target_pattern = re.compile(r"条评论|留下你的想法吧")
            
            # 最多滚动6次，单次距离加大
            for i in range(6):
                # 向下滚动
                swipe_start = time.time()
                self.device.swipe(540, 1600, 540, 600, 0.1)
                self._time_method(f"scroll_swipe_{i+1}", swipe_start)
                
                # 核心优化：只 dump 一次，在字符串中搜索，避免多次 exists() 调用的开销
                dump_start = time.time()
                xml_temp = self.device.dump_hierarchy()
                self._time_method(f"scroll_dump_{i+1}", dump_start)
                
                if target_pattern.search(xml_temp):
                    logger.info(f"✓ 已检测到目标元素 (第 {i+1} 次滚动)")
                    break
                
                # 极短间隔
                time.sleep(0.1)
            
            time.sleep(0.3)  # 稳定时间
            self._time_method("intelligent_scroll_total", scroll_phase_start)
            logger.info("✓ 滚动完成")
        except Exception as e:
            logger.warning(f"滚动失败: {e}")

        # 初始化提取变量
        content = ""
        likes = 0
        collects = 0
        comments = 0
        author_name = "Unknown"
        publish_time = 0
        date_desc = ""
        image_urls = []
        
        # 2. 获取 UI层级 (核心优化)
        # 增加一次重试逻辑，如果第一次没抓到日期
        text_nodes = []
        limit_y = 2500
        
        for attempt in range(2):
            xml_dump_start = time.time()
            xml_content = self.device.dump_hierarchy()
            self._time_method("dump_hierarchy", xml_dump_start)
            
            # 检测白屏状态 - 检查文本节点数量
            current_text_nodes = []
            root = ET.fromstring(xml_content)
            
            def parse_nodes(node):
                text = node.attrib.get('text', '') or node.attrib.get('content-desc', '')
                bounds_str = node.attrib.get('bounds', '[0,0][0,0]')
                try:
                    coords = bounds_str.replace('][', ',').replace('[', '').replace(']', '').split(',')
                    x1, y1, x2, y2 = map(int, coords)
                    if text:
                        current_text_nodes.append({
                            'text': text,
                            'l': x1, 't': y1, 'r': x2, 'b': y2,
                            'cx': (x1 + x2) / 2, 'cy': (y1 + y2) / 2
                        })
                except: pass
                for child in node: parse_nodes(child)
            
            parse_nodes(root)
            
            # 白屏检测：如果文本节点太少，可能是白屏
            print(f'当前文本节点数量: {len(current_text_nodes)}')
            if len(current_text_nodes) < 11:
                logger.error(f"✗ 检测到白屏状态 - 文本节点数量异常少 ({len(current_text_nodes)}个节点)")
                logger.info("--- 调试: 捕获的文本节点 ---")
                for i, n in enumerate(current_text_nodes):
                    logger.info(f"[{i}] {n['text']} (t={n['t']}, b={n['b']}, l={n['l']}, r={n['r']})")
                logger.info("--- 调试结束 ---")
                
                # 如果是第一次尝试，重新加载页面
                if attempt == 0:
                    logger.info("🔄 尝试重新加载页面...")
                    # 重新发送跳转指令
                    self.device.open_url(jump_url)
                    time.sleep(2)  # 等待页面重新加载
                    continue
                else:
                    # 第二次尝试仍白屏，直接返回None
                    logger.error("✗ 页面加载失败 - 白屏状态")
                    return None
            
            # 检查是否存在加载指示器
            loading_found = False
            for node in current_text_nodes:
                if re.search(r'(加载|loading|等待|waiting|\.\.\.|\\u231a|\\u25ba)', node['text'], re.IGNORECASE):
                    loading_found = True
                    break
            
            if loading_found:
                logger.warning("⚠ 检测到页面正在加载中")
                if attempt == 0:
                    logger.info("🔄 等待页面加载完成...")
                    time.sleep(2)
                    continue
            
            text_nodes = current_text_nodes # 保留最新的节点供后续提取使用
            
            # 4. 分析节点数据 (简化版日期快速检查)
            found_date_in_this_xml = False
            follow_node = None
            for n in text_nodes:
                if n['text'] in ["关注", "已关注"]:
                    follow_node = n
                    break
            
            if follow_node:
                # 寻找作者名
                best_dist = 999
                for n in text_nodes:
                    if n == follow_node: continue
                    if abs(n['cy'] - follow_node['cy']) < 100 and n['r'] <= follow_node['l'] + 50:
                        dist = follow_node['l'] - n['r']
                        if dist < best_dist:
                            best_dist = dist
                            author_name = n['text']
            
            # 寻找日期
            min_y = follow_node['b'] if follow_node else 150
            # 提前寻找 limit_y
            current_limit_y = 2500
            for n in text_nodes:
                if re.match(r"^共\s*\d+\s*条评论$", n['text']) or n['text'] in ["说点什么", "写评论", "写点什么", "这里是评论区"]:
                    current_limit_y = min(current_limit_y, n['t'])
            limit_y = current_limit_y

            for n in text_nodes:
                if n['t'] > min_y - 200 and n['b'] < limit_y + 150:
                    txt = n['text'].strip()
                    if 2 <= len(txt) <= 50 and txt not in ["点赞", "收藏", "评论", "关注", "分享", "回复", "不喜欢"]:
                        try:
                            ts = parse_time_to_timestamp_ms(txt)
                            publish_time = ts
                            date_desc = txt
                            found_date_in_this_xml = True
                            # 不要 break，因为日期通常在最后
                        except: continue
            
            if found_date_in_this_xml:
                break
            
            if attempt == 0:
                logger.warning("⚠ 未识别到发布时间，尝试额外滚动并重试...")
                self.device.swipe(540, 1500, 540, 1000, 0.2)
                time.sleep(0.5)

        if not date_desc:
            logger.warning("未识别到发布时间")
            # 埋点调试: 打印出识别到的所有节点及其坐标
            logger.info("--- 调试: 所有捕获的文本节点 ---")
            for i, n in enumerate(text_nodes):
                logger.info(f"[{i}] {n['text']} (t={n['t']}, b={n['b']}, l={n['l']}, r={n['r']})")
            logger.info("--- 调试结束 ---")
        else:
            logger.info(f"✓ 识别到发布时间: {date_desc} -> {publish_time}")
        
        logger.info(f"text_nodes: {text_nodes}")

        
        # B. 互动数据提取 (底部区域)
        # 使用 limit_y 作为分割线大概率更准确
        bottom_nodes = [n for n in text_nodes if n['t'] >= limit_y - 300] # 互动栏通常在 limit_y 上方一点点 或者 就在 mask 区域
        bottom_nodes.sort(key=lambda x: x['l']) # 从左到右
        
        for n in bottom_nodes:
            txt = n['text']
            # 保留数字、小数点、w/W 和 "万" 字
            num_txt = ''.join(c for c in txt if c.isdigit() or c in ['.', 'w', 'W', '万'])
            if not num_txt: continue
            
            cx = n['cx']
            if 500 < cx < 750:
                likes = parse_count_to_int(num_txt)
            elif 750 < cx < 900:
                collects = parse_count_to_int(num_txt)
            elif cx >= 900:
                comments = parse_count_to_int(num_txt)

        # C. 正文提取
        # 过滤掉非正文内容
        content_lines = []
        # exclude_keywords = ['收藏', '点赞', '评论', '分享', '发布于', '说点什么', '条评论', '关注', author_name]
        # if date_desc:
        #     exclude_keywords.append(date_desc)
        
        # 按照垂直位置排序 (使用 min_y 和 limit_y 约束)
        content_nodes = [n for n in text_nodes if min_y < n['t'] < limit_y]
        content_nodes.sort(key=lambda x: x['t'])
        
        for n in content_nodes:
            t = n['text']
            if len(t) < 2: continue
            # if any(k in t for k in exclude_keywords): continue
            
            # 简单的去重策略
            if content_lines and t in content_lines[-1]: continue
            content_lines.append(t)
            
        content = "\n".join(content_lines)
        logger.info(f"提取正文: {content}")
        # 5. 图片提取 (保持原有逻辑但优化等待)
        try:
             # 这里还是需要交互，无法纯靠XML
            share_btn = self.device(description="分享")
            if share_btn.exists:
                share_btn.click()
                # 显式等待 "复制链接"
                copy_link = self.device(text="复制链接")
                if copy_link.wait(timeout=2.0):
                    copy_link.click()
                    # 等待剪贴板更新? 稍微缓一下
                    time.sleep(0.5)
                    share_link = self.device.clipboard
                    if "http" in str(share_link):
                        image_urls = self._fetch_web_images(share_link)
                else:
                    logger.warning("未找到复制链接按钮")
                    self.device.press("back")
        except Exception as e:
            logger.warning(f"⚠ 图片提取异常: {e}")

        self._time_method("_get_detail_data", start_time)
        return {
            "content": content,
            "image_urls": image_urls,
            "likes": likes,
            "collects": collects,
            "comments": comments,
            "author_name": author_name,
            "publish_time": publish_time,
            "date_desc": date_desc
        }
    
    def _fetch_web_images(self, url: str) -> List[str]:
        """
        从分享链接中解析图片地址
        
        Args:
            url (str): 分享链接URL
            
        Returns:
            List[str]: 图片URL列表
        """
        start_time = time.time()
        try:
            headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"}
            res = requests.get(url, headers=headers, timeout=10)
            html = res.text
            img_patterns = [
                r'property="og:image" content="(https://[^"]+)"',
                r'"url":"(https://sns-img-[^"]+)"',
                r'"url":"(https://sns-img-qc\.xhscdn\.com/[^"]+)"'
            ]
            found = []
            for pattern in img_patterns:
                matches = re.findall(pattern, html)
                for m in matches:
                    clean_url = m.replace('\\u002F', '/')
                    if clean_url not in found: found.append(clean_url)
            self._time_method("_fetch_web_images", start_time)
            return found
        except:
            self._time_method("_fetch_web_images", start_time)
            return []
    
    def save_note_data(self, data: Dict[str, Union[str, List[str]]], 
                      filename: str = "last_extracted_note.txt", 
                      note_url: str = "") -> None:
        """
        保存笔记数据到文件
        
        Args:
            data (Dict[str, Union[str, List[str]]]): 笔记数据
            filename (str): 保存文件名
            note_url (str): 笔记URL
        """
        start_time = time.time()
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 50 + "\n")
                f.write("【小红书笔记提取结果】\n")
                f.write("=" * 50 + "\n")
                if note_url:
                    f.write(f"笔记URL: {note_url}\n")
                    f.write("=" * 50 + "\n")
                f.write(f"作者: {data.get('author_name', 'Unknown')}\n")
                f.write(f"点赞数: {data.get('likes', '0')}\n")
                f.write(f"收藏数: {data.get('collects', '0')}\n")
                f.write(f"评论数: {data.get('comments', '0')}\n")
                f.write(f"图片数: {len(data.get('image_urls', []))}\n")
                f.write(f"发布时间: {data.get('date_desc', '')} ({data.get('publish_time', 0)})\n")
                f.write("=" * 50 + "\n")
                f.write("【正文内容】\n")
                f.write(data['content'])
                f.write("\n" + "=" * 50 + "\n")
                if data['image_urls']:
                    f.write("【图片URL】\n")
                    for i, url in enumerate(data['image_urls'], 1):
                        f.write(f"{i}. {url}\n")
                    f.write("=" * 50 + "\n")
            
            logger.info(f"✓ 笔记数据已保存到: {filename}")
            self._time_method("save_note_data", start_time)
        except Exception as e:
            logger.error(f"✗ 保存笔记数据失败: {e}")
            self._time_method("save_note_data", start_time)
            raise


def extract_note_from_url(url: str, device_serial: Optional[str] = None, enable_time_logging: bool = True) -> Optional[Dict[str, Union[str, List[str]]]]:
    """
    便捷函数：直接从URL提取笔记数据，支持设备重试机制
    
    Args:
        url (str): 小红书笔记URL
        device_serial (str, optional): 设备序列号
        enable_time_logging (bool, optional): 是否启用耗时打印，默认为True
        
    Returns:
        Optional[Dict[str, Union[str, List[str]]]]: 笔记数据，如果没有成功则返回None
    """
    start_time = time.time()
    logger.info(f"[extract_note_from_url] 开始处理URL: {url}")
    try:
        extractor = XHSNoteExtractor(device_serial=device_serial, enable_time_logging=enable_time_logging)
        result = extractor.extract_note_data(url=url)
        elapsed_time = time.time() - start_time
        logger.info(f"[extract_note_from_url] 总耗时: {elapsed_time:.3f}秒")
        return result
    except Exception as e:
        logger.error(f"[extract_note_from_url] 提取失败: {e}")
        elapsed_time = time.time() - start_time
        logger.info(f"[extract_note_from_url] 总耗时: {elapsed_time:.3f}秒")
        return None


def convert_url_format(url: str) -> str:
    """
    便捷函数：转换URL格式
    
    Args:
        url (str): 输入URL
        
    Returns:
        str: 转换后的xhsdiscover协议格式URL
    """
    start_time = time.time()
    logger.info(f"[convert_url_format] 开始转换URL: {url}")
    parsed_data = XHSNoteExtractor.parse_xhs_url(url)
    result = XHSNoteExtractor.convert_to_xhsdiscover_format(
        parsed_data["note_id"], 
        parsed_data["xsec_token"]
    )
    elapsed_time = time.time() - start_time
    logger.info(f"[convert_url_format] 耗时: {elapsed_time:.3f}秒，结果: {result}")
    return result