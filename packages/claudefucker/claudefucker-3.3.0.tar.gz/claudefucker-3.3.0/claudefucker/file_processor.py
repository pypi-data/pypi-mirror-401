"""
文件处理工具模块
支持文件上传、解析、OCR等功能
"""
import os
import base64
from typing import Optional, Dict, Any
from werkzeug.utils import secure_filename
import mimetypes


class FileProcessor:
    """文件处理器"""
    
    def __init__(self, upload_dir: str = "uploads"):
        """
        初始化文件处理器
        
        Args:
            upload_dir: 上传文件保存目录
        """
        self.upload_dir = upload_dir
        self._ensure_upload_dir()
        
        # 支持的文件类型
        self.supported_image_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
        self.supported_document_types = {
            'application/pdf',
            'text/plain',
            'text/markdown',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/csv'
        }
    
    def _ensure_upload_dir(self):
        """确保上传目录存在"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
    
    def is_allowed_file(self, filename: str, file_type: str = 'document') -> bool:
        """
        检查文件类型是否允许
        
        Args:
            filename: 文件名
            file_type: 文件类型 ('image' 或 'document')
            
        Returns:
            是否允许
        """
        # 检查文件扩展名
        allowed_extensions = {
            'image': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
            'document': {'pdf', 'txt', 'md', 'doc', 'docx', 'csv'}
        }
        
        if '.' not in filename:
            return False
        
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in allowed_extensions.get(file_type, set())
    
    def save_uploaded_file(self, file) -> Optional[str]:
        """
        保存上传的文件
        
        Args:
            file: 上传的文件对象
            
        Returns:
            保存的文件路径
        """
        if not file or not file.filename:
            return None
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_dir, filename)
        
        # 确保文件名唯一
        counter = 1
        while os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            filepath = os.path.join(self.upload_dir, f"{name}_{counter}{ext}")
            counter += 1
        
        file.save(filepath)
        return filepath
    
    def file_to_base64(self, filepath: str) -> str:
        """
        将文件转换为base64编码
        
        Args:
            filepath: 文件路径
            
        Returns:
            base64编码的字符串
        """
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        base64_data = base64.b64encode(file_data).decode('utf-8')
        
        # 获取MIME类型
        mime_type, _ = mimetypes.guess_type(filepath)
        
        return f"data:{mime_type};base64,{base64_data}"
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            filepath: 文件路径
            
        Returns:
            文件信息字典
        """
        if not os.path.exists(filepath):
            return {}
        
        file_stat = os.stat(filepath)
        mime_type, _ = mimetypes.guess_type(filepath)
        
        return {
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "size": file_stat.st_size,
            "mime_type": mime_type,
            "is_image": mime_type in self.supported_image_types,
            "is_document": mime_type in self.supported_document_types
        }
    
    def read_text_file(self, filepath: str) -> str:
        """
        读取文本文件内容
        
        Args:
            filepath: 文件路径
            
        Returns:
            文件内容
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(filepath, 'r', encoding='gbk') as f:
                    return f.read()
            except:
                return ""
    
    def prepare_image_for_vision(self, filepath: str, detail: str = 'high') -> Dict[str, Any]:
        """
        准备图像用于视觉模型
        
        Args:
            filepath: 图像文件路径
            detail: 图像细节等级 ('high' 或 'low')
            
        Returns:
            格式化后的图像数据
        """
        base64_data = self.file_to_base64(filepath)
        
        return {
            "type": "image_url",
            "image_url": {
                "url": base64_data,
                "detail": detail
            }
        }
    
    def prepare_document_for_chat(self, filepath: str) -> str:
        """
        准备文档内容用于聊天
        
        Args:
            filepath: 文档文件路径
            
        Returns:
            文档内容
        """
        file_info = self.get_file_info(filepath)
        
        if file_info.get('is_image'):
            # 对于图像，返回base64编码
            return self.file_to_base64(filepath)
        elif file_info.get('is_document'):
            # 对于文档，读取文本内容
            content = self.read_text_file(filepath)
            return f"""
文件名: {file_info['filename']}
文件大小: {file_info['size']} bytes
文件类型: {file_info['mime_type']}

内容:
{content}
"""
        else:
            # 其他类型文件
            return f"文件: {file_info['filename']}, 类型: {file_info.get('mime_type', 'unknown')}"
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """
        清理旧文件
        
        Args:
            max_age_hours: 文件最大保存时间（小时）
        """
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(self.upload_dir):
            filepath = os.path.join(self.upload_dir, filename)
            
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > max_age_seconds:
                    try:
                        os.remove(filepath)
                        print(f"Cleaned up old file: {filepath}")
                    except Exception as e:
                        print(f"Failed to remove file {filepath}: {e}")
