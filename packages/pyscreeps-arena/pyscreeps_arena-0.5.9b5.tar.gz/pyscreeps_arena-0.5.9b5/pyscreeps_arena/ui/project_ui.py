# -*- coding: utf-8 -*-
"""
项目创建UI界面
"""
import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QMessageBox, QComboBox, QStackedWidget)
from pyscreeps_arena.ui.qprefabs.qprefabs import QPrefabsManager
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QIcon
from pyscreeps_arena.core import const
from pyscreeps_arena.ui.rs_icon import get_pixmap
from pyscreeps_arena.afters import ToConfigAfter, ToEmptyAfter, ToPrefabAfter, ToCustomAfter
from PyQt6.QtWidgets import QRadioButton, QGroupBox

# Language mapping
LANG = {
    'cn': {
        'window_title': 'PyScreeps Arena - 项目创建器',
        'title': 'PyScreeps Arena',
        'version': '版本: {0}',
        'author': '作者: {0}',
        'github': 'GitHub: {0}',
        'project_name': '项目名称:',
        'name_placeholder': '输入项目名称...',
        'save_location': '保存位置:',
        'path_placeholder': '选择项目保存位置...',
        'browse': '浏览...',
        'language': '语 言:',
        'arena': '竞技场:',
        'difficulty': '难 度:',
        'empty': '空白 (Empty)',
        'basic': '基础 (Basic)',
        'prefab': '预设 (Prefab)',
        'pi': '预设继承 (P&&I)',
        'create_project': '创建项目',
        'cancel': '取消',
        'path_exists': '路径已存在',
        'path_exists_message': "路径 '{0}' 已存在。\n是否继续？",
        'success': '成功',
        'success_message': "项目 '{0}' 创建成功！\n路径: {1}",
        'error': '错误',
        'error_message': '项目创建失败:\n{0}',
        'select_location': '选择项目保存位置',
        'next_page': '下一页',
        'previous_page': '上一页',
    },
    'en': {
        'window_title': 'PyScreeps Arena - Project Creator',
        'title': 'PyScreeps Arena',
        'version': 'Version: {0}',
        'author': 'Author: {0}',
        'github': 'GitHub: {0}',
        'project_name': 'Project Name:',
        'name_placeholder': 'Enter project name...',
        'save_location': 'Save Location:',
        'path_placeholder': 'Select project save location...',
        'browse': 'Browse...',
        'language': 'Language:',
        'arena': 'Arena:',
        'difficulty': 'Difficulty:',
        'empty': 'Empty',
        'basic': 'Basic',
        'prefab': 'Prefab',
        'pi': 'Prefab & Inherit',
        'create_project': 'Create Project',
        'cancel': 'Cancel',
        'path_exists': 'Path Exists',
        'path_exists_message': "Path '{0}' already exists.\nContinue anyway?",
        'success': 'Success',
        'success_message': "Project '{0}' created successfully!\nPath: {1}",
        'error': 'Error',
        'error_message': 'Failed to create project:\n{0}',
        'select_location': 'Select Project Save Location',
        'next_page': 'Next Page',
        'previous_page': 'Previous',
    }
}



class QProjectBody(QWidget):
    """Project creation body widget"""
    
    # Signals
    projectCreated = pyqtSignal(str, str)  # (project_name, project_path)
    projectCancelled = pyqtSignal()
    languageChanged = pyqtSignal(str)  # (language_code)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._proj_name = ""
        self._proj_path = ""
        self._init_ui()
    
    def lang(self, key, *args):
        """Get translation for the current language"""
        # Get language code from combo box data
        lang = self._lang_combo.currentData() or 'cn'
        
        if lang not in LANG:
            lang = 'cn'
        return LANG[lang][key].format(*args)
    
    def _get_settings_path(self):
        """Get cross-platform settings file path"""
        # Get user's home directory
        home_dir = os.path.expanduser("~")
        
        # Create settings directory if it doesn't exist
        settings_dir = os.path.join(home_dir, ".psaui")
        os.makedirs(settings_dir, exist_ok=True)
        
        # Return settings file path
        return os.path.join(settings_dir, "psaui.json")
    
    def _save_settings(self):
        """Save settings to psaui.json"""
        settings = {
            "language": self._lang_combo.currentIndex(),
            "path": self._path_input.text()
        }
        
        try:
            settings_path = self._get_settings_path()
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _load_settings(self):
        """Load settings from psaui.json if it exists"""
        try:
            settings_path = self._get_settings_path()
            if os.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Load language setting
                if "language" in settings:
                    language_index = settings["language"]
                    if 0 <= language_index < self._lang_combo.count():
                        self._lang_combo.setCurrentIndex(language_index)
                
                # Load path setting
                if "path" in settings and settings["path"]:
                    self._path_input.setText(settings["path"])
                    self._proj_path = settings["path"]
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def _update_language_options(self):
        """Update language combo box options based on current language"""
        # Get current language
        lang_text = self._lang_combo.currentText()
        current_lang = lang_text.split('(')[1].strip(')') if '(' in lang_text else 'cn'
        
        # Save current index
        current_index = self._lang_combo.currentIndex()
        
        # Disconnect signal to avoid recursion
        self._lang_combo.currentTextChanged.disconnect(self._update_language)
        
        # Clear existing items
        self._lang_combo.clear()
        
        # Add items based on current language
        if current_lang == 'en':
            # In English mode, show only language codes
            self._lang_combo.addItems(["cn", "en"])
        else:
            # In Chinese mode, show full language names
            self._lang_combo.addItems(["中文 (cn)", "英文 (en)"])
        
        # Restore current index
        if current_index < self._lang_combo.count():
            self._lang_combo.setCurrentIndex(current_index)
        
        # Reconnect signal
        self._lang_combo.currentTextChanged.connect(self._update_language)
    
    def _update_language(self):
        """Update all UI elements to use the current language"""
        # Get current language code
        current_lang = self._lang_combo.currentData() or 'cn'
        
        # Update window title
        self.setWindowTitle(self.lang('window_title'))
        
        # Update title
        self._title_label.setText(self.lang('title'))
        
        # Update info labels
        self._version_label.setText(self.lang('version', const.VERSION))
        self._author_label.setText(self.lang('author', const.AUTHOR))
        self._github_label.setText(self.lang('github', const.GITHUB_NAME))
        
        # Update input labels and placeholders
        current_lang = self._lang_combo.currentData() or 'cn'
        if current_lang == 'en':
            self._name_label.setText('Name:')
        else:
            self._name_label.setText(self.lang('project_name'))
        self._name_input.setPlaceholderText(self.lang('name_placeholder'))
        self._path_label.setText(self.lang('save_location'))
        self._path_input.setPlaceholderText(self.lang('path_placeholder'))
        
        # Update buttons
        self._browse_btn.setText(self.lang('browse'))
        if hasattr(self, '_create_btn'):
            self._create_btn.setText(self.lang('create_project'))
        if hasattr(self, '_cancel_btn'):
            self._cancel_btn.setText(self.lang('cancel'))
        
        # Update config labels
        self._lang_label.setText(self.lang('language'))
        self._arena_label.setText(self.lang('arena'))
        self._level_label.setText(self.lang('difficulty'))
        
        # Update radio buttons
        self._empty_radio.setText(self.lang('empty'))
        self._basic_radio.setText(self.lang('basic'))
        self._prefab_radio.setText(self.lang('prefab'))
        self._pi_radio.setText(self.lang('pi'))
        
        # Update language combo box items based on current language
        if current_lang == 'en':
            # In English mode, show only language codes
            self._lang_combo.blockSignals(True)
            current_index = self._lang_combo.currentIndex()
            self._lang_combo.clear()
            self._lang_combo.addItem("cn", "cn")
            self._lang_combo.addItem("en", "en")
            self._lang_combo.setCurrentIndex(current_index)
            self._lang_combo.blockSignals(False)
            
            # Update arena combo box items
            self._arena_combo.blockSignals(True)
            current_arena_index = self._arena_combo.currentIndex()
            self._arena_combo.clear()
            self._arena_combo.addItem("gray", "gray")
            self._arena_combo.addItem("green", "green")
            self._arena_combo.addItem("blue", "blue")
            self._arena_combo.addItem("red", "red")
            self._arena_combo.setCurrentIndex(current_arena_index)
            self._arena_combo.blockSignals(False)
            
            # Update level combo box items
            self._level_combo.blockSignals(True)
            current_level_index = self._level_combo.currentIndex()
            self._level_combo.clear()
            self._level_combo.addItem("basic", "basic")
            self._level_combo.addItem("advanced", "advanced")
            self._level_combo.setCurrentIndex(current_level_index)
            self._level_combo.blockSignals(False)
        else:
            # In Chinese mode, show full language names
            self._lang_combo.blockSignals(True)
            current_index = self._lang_combo.currentIndex()
            self._lang_combo.clear()
            self._lang_combo.addItem("中文 (cn)", "cn")
            self._lang_combo.addItem("英文 (en)", "en")
            self._lang_combo.setCurrentIndex(current_index)
            self._lang_combo.blockSignals(False)
            
            # Update arena combo box items
            self._arena_combo.blockSignals(True)
            current_arena_index = self._arena_combo.currentIndex()
            self._arena_combo.clear()
            self._arena_combo.addItem("灰色 (gray)", "gray")
            self._arena_combo.addItem("绿色 (green)", "green")
            self._arena_combo.addItem("蓝色 (blue)", "blue")
            self._arena_combo.addItem("红色 (red)", "red")
            self._arena_combo.setCurrentIndex(current_arena_index)
            self._arena_combo.blockSignals(False)
            
            # Update level combo box items
            self._level_combo.blockSignals(True)
            current_level_index = self._level_combo.currentIndex()
            self._level_combo.clear()
            self._level_combo.addItem("基础 (basic)", "basic")
            self._level_combo.addItem("高级 (advanced)", "advanced")
            self._level_combo.setCurrentIndex(current_level_index)
            self._level_combo.blockSignals(False)
        
        # Save settings after language change
        self._save_settings()
        
    def _init_ui(self):
        """初始化UI界面"""
        self.setFixedSize(500, 580)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        # 减小左右边距，保持上下边距
        layout.setContentsMargins(15, 15, 15, 30)
        
        # 创建项目创建页面
        self._project_page = QWidget()
        self._project_layout = QVBoxLayout(self._project_page)
        self._project_layout.setSpacing(15)
        self._project_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建堆叠容器
        self._stacked_widget = QStackedWidget()
        layout.addWidget(self._stacked_widget)
        
        # 标题
        self._title_label = QLabel("PyScreeps Arena")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self._title_label.setFont(title_font)
        self._project_layout.addWidget(self._title_label)
        
        # 项目信息
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(8)
        
        # 版本信息
        self._version_label = QLabel(f"版本: {const.VERSION}")
        self._version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self._version_label)
        
        # 作者信息
        self._author_label = QLabel(f"作者: {const.AUTHOR}")
        self._author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self._author_label)
        
        # GitHub信息
        self._github_label = QLabel(f"GitHub: {const.GITHUB_NAME}")
        self._github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self._github_label)
        
        self._project_layout.addWidget(info_widget)
        
        # 分隔线
        separator = QLabel("─" * 50)
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator.setStyleSheet("color: #ccc;")
        self._project_layout.addWidget(separator)
        
        # 项目输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setSpacing(12)
        
        # 项目名称输入
        name_layout = QHBoxLayout()
        self._name_label = QLabel("项目名称:")
        self._name_label.setFixedWidth(80)
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("输入项目名称...")
        self._name_input.textChanged.connect(self._on_name_changed)
        self._name_input.returnPressed.connect(self._create_project)
        name_layout.addWidget(self._name_label)
        name_layout.addWidget(self._name_input)
        input_layout.addLayout(name_layout)
        
        # 项目路径输入
        path_layout = QHBoxLayout()
        self._path_label = QLabel("保存位置:")
        self._path_label.setFixedWidth(80)
        self._path_input = QLineEdit()
        self._path_input.setPlaceholderText("选择项目保存位置...")
        self._path_input.setReadOnly(True)
        # 默认桌面路径
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(desktop_path):
            self._path_input.setText(desktop_path)
            self._proj_path = desktop_path
        path_layout.addWidget(self._path_label)
        path_layout.addWidget(self._path_input)
        
        # 浏览按钮
        self._browse_btn = QPushButton("浏览...")
        self._browse_btn.setFixedWidth(80)
        self._browse_btn.clicked.connect(self._browse_path)
        path_layout.addWidget(self._browse_btn)
        
        input_layout.addLayout(path_layout)
        self._project_layout.addWidget(input_widget)
        
        # 分隔线
        separator2 = QLabel("─" * 50)
        separator2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator2.setStyleSheet("color: #ccc;")
        self._project_layout.addWidget(separator2)
        
        # 配置选项区域（左右布局）
        config_container = QWidget()
        config_container_layout = QHBoxLayout(config_container)
        config_container_layout.setSpacing(20)
        
        # 左侧：语言、竞技场、难度配置
        left_config_widget = QWidget()
        left_config_layout = QVBoxLayout(left_config_widget)
        left_config_layout.setSpacing(10)
        
        # 语言选择
        lang_layout = QHBoxLayout()
        self._lang_label = QLabel("语 言:")
        self._lang_label.setFixedWidth(80)
        self._lang_combo = QComboBox()
        # 语言选项
        self._lang_combo.addItem("中文 (cn)", "cn")
        self._lang_combo.addItem("英文 (en)", "en")
        self._lang_combo.setCurrentIndex(0)
        self._lang_combo.currentIndexChanged.connect(self._update_language)
        lang_layout.addWidget(self._lang_label)
        lang_layout.addWidget(self._lang_combo)
        left_config_layout.addLayout(lang_layout)
        
        # 竞技场选择
        arena_layout = QHBoxLayout()
        self._arena_label = QLabel("竞技场:")
        self._arena_label.setFixedWidth(80)
        self._arena_combo = QComboBox()
        # 竞技场选项
        self._arena_combo.addItem("灰色 (gray)", "gray")
        self._arena_combo.addItem("绿色 (green)", "green")
        self._arena_combo.addItem("蓝色 (blue)", "blue")
        self._arena_combo.addItem("红色 (red)", "red")
        self._arena_combo.setCurrentIndex(0)
        arena_layout.addWidget(self._arena_label)
        arena_layout.addWidget(self._arena_combo)
        left_config_layout.addLayout(arena_layout)
        
        # 难度级别选择
        level_layout = QHBoxLayout()
        self._level_label = QLabel("难 度:")
        self._level_label.setFixedWidth(80)
        self._level_combo = QComboBox()
        # 难度选项
        self._level_combo.addItem("基础 (basic)", "basic")
        self._level_combo.addItem("高级 (advanced)", "advanced")
        self._level_combo.setCurrentIndex(0)
        level_layout.addWidget(self._level_label)
        level_layout.addWidget(self._level_combo)
        left_config_layout.addLayout(level_layout)
        
        config_container_layout.addWidget(left_config_widget)
        
        # 右侧：模式选择（单选框）
        right_config_widget = QWidget()
        right_config_layout = QVBoxLayout(right_config_widget)
        right_config_layout.setSpacing(8)
        
        # 模式选择标题
        # mode_title = QLabel("模式选择")
        # mode_title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        # right_config_layout.addWidget(mode_title)
        
        # 单选按钮
        self._empty_radio = QRadioButton("空白 (Empty)")
        self._basic_radio = QRadioButton("基础 (Basic)")
        self._prefab_radio = QRadioButton("预设 (Prefab)")
        self._pi_radio = QRadioButton("预设继承 (P&&I)")
        
        # 默认选择基础模式
        self._basic_radio.setChecked(True)
        
        # 添加到布局
        right_config_layout.addWidget(self._empty_radio)
        right_config_layout.addWidget(self._basic_radio)
        right_config_layout.addWidget(self._prefab_radio)
        right_config_layout.addWidget(self._pi_radio)
        
        config_container_layout.addWidget(right_config_widget)
        
        self._project_layout.addWidget(config_container)
        
        self._project_layout.addStretch()
        
        # 加载设置
        self._load_settings()
        
        # 创建预制件管理器页面
        self._prefabs_page = QPrefabsManager()
        
        # 添加页面到堆叠容器
        self._stacked_widget.addWidget(self._project_page)
        self._stacked_widget.addWidget(self._prefabs_page)
        
        # 连接堆叠容器的页面变化信号
        self._stacked_widget.currentChanged.connect(self._on_page_changed)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 创建按钮
        self._create_btn = QPushButton("创建项目")
        self._create_btn.setFixedSize(120, 35)
        self._create_btn.clicked.connect(self._on_next_or_create)
        self._create_btn.setEnabled(False)
        self._create_btn.setDefault(True)
        button_layout.addWidget(self._create_btn)
        
        # 取消按钮
        self._cancel_btn = QPushButton("取消")
        self._cancel_btn.setFixedSize(80, 35)
        self._cancel_btn.clicked.connect(self._on_previous_or_cancel)
        button_layout.addWidget(self._cancel_btn)
        
        # 添加按钮区域到主布局
        layout.addLayout(button_layout)
        
        # 初始更新语言
        # 延迟调用，确保所有UI元素都已创建
        self._update_language()
        
        # 初始更新按钮文本
        self._update_button_texts()
        
    def _on_name_changed(self, text):
        """项目名称改变时的处理"""
        self._proj_name = text.strip()
        self._create_btn.setEnabled(bool(self._proj_name and self._proj_path))
    
    def _on_cancel(self):
        """Handle cancel button click"""
        self.projectCancelled.emit()
        # Exit the application when cancel is clicked
        QApplication.quit()
    
    def _on_next_or_create(self):
        """Handle next or create button click"""
        current_index = self._stacked_widget.currentIndex()
        max_index = self._stacked_widget.count() - 1
        
        if current_index < max_index:
            # Go to next page
            self._stacked_widget.setCurrentIndex(current_index + 1)
        else:
            # Create project
            self._create_project()
    
    def _on_previous_or_cancel(self):
        """Handle previous or cancel button click"""
        current_index = self._stacked_widget.currentIndex()
        
        if current_index > 0:
            # Go to previous page
            self._stacked_widget.setCurrentIndex(current_index - 1)
        else:
            # Cancel
            self._on_cancel()
    
    def _on_page_changed(self, index):
        """Handle page changed signal"""
        self._update_button_texts()
    
    def _update_button_texts(self):
        """Update button texts based on current page index"""
        current_index = self._stacked_widget.currentIndex()
        max_index = self._stacked_widget.count() - 1
        
        # Update create/next button
        if current_index < max_index:
            self._create_btn.setText(self.lang('next_page'))
        else:
            self._create_btn.setText(self.lang('create_project'))
        
        # Update cancel/previous button
        if current_index == 0:
            self._cancel_btn.setText(self.lang('cancel'))
        else:
            self._cancel_btn.setText(self.lang('previous_page'))
        
    def _browse_path(self):
        """浏览选择路径"""
        current_path = self._path_input.text() or os.path.expanduser("~")
        path = QFileDialog.getExistingDirectory(
            self, self.lang('select_location'), current_path
        )
        if path:
            self._path_input.setText(path)
            self._proj_path = path
            self._create_btn.setEnabled(bool(self._proj_name and self._proj_path))
            # Save settings after path change
            self._save_settings()
            
    def _create_project(self):
        """创建项目"""
        if not self._proj_name or not self._proj_path:
            return
            
        # 构建完整路径
        full_path = os.path.join(self._proj_path, self._proj_name)
        
        # 检查路径是否已存在
        if os.path.exists(full_path):
            reply = QMessageBox.question(
                self, self.lang('path_exists'),
                self.lang('path_exists_message', full_path),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        try:
            # 创建项目
            self._extract_project_template(full_path)
            
            QMessageBox.information(
                self, self.lang('success'),
                self.lang('success_message', self._proj_name, full_path)
            )
            
            # 处理预制件
            self._process_prefabs(full_path)
            
            self.projectCreated.emit(self._proj_name, full_path)
            
            # 成功创建项目后关闭程序
            QApplication.quit()
            
        except Exception as e:
            QMessageBox.critical(
                self, self.lang('error'),
                self.lang('error_message', str(e))
            )
            
    def _extract_project_template(self, target_path):
        """提取项目模板"""
        # 获取当前包路径
        this_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_7z_path = os.path.join(this_path, 'project.7z')
        
        if not os.path.exists(project_7z_path):
            raise FileNotFoundError(f"项目模板文件不存在: {project_7z_path}")
            
        # 创建目标目录
        os.makedirs(target_path, exist_ok=True)
        
        # 解压项目模板
        import py7zr
        with py7zr.SevenZipFile(project_7z_path, mode='r') as archive:
            archive.extractall(path=target_path)
            
        print(f"[DEBUG] 项目模板已解压到: {target_path}")  # 调试输出
        
        # 获取用户选择的配置
        lang = self._lang_combo.currentData() or 'cn'
        arena = self._arena_combo.currentData() or 'gray'
        level = self._level_combo.currentData() or 'basic'
        
        # 调用配置方法
        ToConfigAfter(path=target_path, language=lang, arena=arena, level=level)
        print(f"[DEBUG] 项目配置已更新: language={lang}, arena={arena}, level={level}")  # 调试输出
        
        # 根据选择的模式执行相应的操作
        if self._empty_radio.isChecked():
            print(f"[DEBUG] 执行空白模式配置")
            ToEmptyAfter(path=target_path)
        elif self._basic_radio.isChecked():
            print(f"[DEBUG] 执行基础模式配置（不操作）")
            # 基础模式不执行任何操作
        elif self._prefab_radio.isChecked():
            print(f"[DEBUG] 执行预设模式配置")
            ToPrefabAfter(path=target_path)
        elif self._pi_radio.isChecked():
            print(f"[DEBUG] 执行预设继承模式配置")
            ToPrefabAfter(path=target_path)
            ToCustomAfter(path=target_path)
    
    # Properties
    @pyqtProperty(str, constant=False)
    def projectName(self) -> str:
        """Get project name"""
        return self._proj_name
    
    @projectName.setter
    def projectName(self, value: str):
        """Set project name"""
        self._proj_name = value.strip()
        self._name_input.setText(self._proj_name)
        self._create_btn.setEnabled(bool(self._proj_name and self._proj_path))
    
    @pyqtProperty(str, constant=False)
    def projectPath(self) -> str:
        """Get project path"""
        return self._proj_path
    
    @projectPath.setter
    def projectPath(self, value: str):
        """Set project path"""
        self._proj_path = value
        self._path_input.setText(self._proj_path)
        self._create_btn.setEnabled(bool(self._proj_name and self._proj_path))
    
    @pyqtProperty(str, constant=False)
    def language(self) -> str:
        """Get current language code"""
        return self._lang_combo.currentData() or 'cn'
    
    @language.setter
    def language(self, value: str):
        """Set language code"""
        if value == 'cn':
            self._lang_combo.setCurrentIndex(0)
        elif value == 'en':
            self._lang_combo.setCurrentIndex(1)
    
    def _process_prefabs(self, project_path: str):
        """
        Process selected prefabs: copy them to src directory, handle naming conflicts,
        and add import statements to main.py
        
        Args:
            project_path: Path to the newly created project
        """
        print(f"Processing prefabs for project: {project_path}")
        
        # Check if QPrefabsManager exists and has selected prefabs
        if hasattr(self, '_prefabs_page'):
            # Get selected prefabs as list
            selected_prefabs = self._prefabs_page.selectedPrefabs
            print(f"Selected prefabs: {selected_prefabs}")
            
            if selected_prefabs:
                # Convert to dict format using list_to_dict method
                prefabs_dict = self._prefabs_page.list_to_dict(selected_prefabs)
                print(f"Prefabs dict: {prefabs_dict}")
                
                # Create src directory if it doesn't exist
                src_dir = os.path.join(project_path, 'src')
                os.makedirs(src_dir, exist_ok=True)
                print(f"Src directory: {src_dir}")
                
                # Get existing directory names in src
                existing_dirs = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]
                print(f"Existing dirs in src: {existing_dirs}")
                
                # Process each prefab
                imported_modules = []
                
                for name, path in prefabs_dict.items():
                    # Clean directory name: replace non-alphanumeric and non-underscore characters with underscore
                    clean_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)
                    
                    # Handle naming conflicts
                    final_name = clean_name
                    i = 2
                    while final_name in existing_dirs:
                        final_name = f"{clean_name}_{i}"
                        i += 1
                    
                    # Add to existing_dirs to avoid conflicts with subsequent prefabs
                    existing_dirs.append(final_name)
                    
                    # Target directory path
                    target_dir = os.path.join(src_dir, final_name)
                    
                    # Copy directory from path to target_dir
                    import shutil
                    try:
                        shutil.copytree(path, target_dir)
                        imported_modules.append(final_name)
                        print(f"Copied prefab {name} to {target_dir}")
                    except Exception as e:
                        print(f"Error copying prefab {name}: {e}")
                
                # Add import statements to main.py
                if imported_modules:
                    main_py_path = os.path.join(project_path, 'src', 'main.py')
                    print(f"Main.py path: {main_py_path}")
                    if os.path.exists(main_py_path):
                        # Read main.py content
                        with open(main_py_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        print(f"Main.py content:\n{content}")
                        
                        # Find the end of import statements
                        import_end = 0
                        lines = content.split('\n')
                        # Iterate through all lines to find the last import statement
                        for i, line in enumerate(lines):
                            if line.strip().startswith('from ') or line.strip().startswith('import '):
                                import_end = i + 1
                            elif import_end > 0 and line.strip() == '':
                                # Keep moving past empty lines after imports
                                import_end = i + 1
                            elif import_end > 0 and line.strip() != '':
                                # Stop when we reach non-empty, non-import line
                                break
                        # If no imports found, add at the beginning
                        print(f"Import end position: {import_end}")
                        
                        # Add import statements
                        import_lines = []
                        for module in imported_modules:
                            import_lines.append(f"from {module} import *")
                        print(f"Import lines to add: {import_lines}")
                        
                        # Process the content to properly format imports
                        # First, separate the content into import section and code section
                        import_section = []
                        code_section = []
                        in_imports = True
                        
                        for line in lines:
                            if in_imports:
                                if line.strip().startswith('from ') or line.strip().startswith('import '):
                                    import_section.append(line.strip())
                                elif line.strip() == '':
                                    # Skip empty lines in import section
                                    pass
                                else:
                                    # Reached end of imports
                                    in_imports = False
                                    code_section.append(line)
                            else:
                                # Add all other lines to code section
                                code_section.append(line)
                        
                        # Add new imports to import section
                        import_section.extend(import_lines)
                        
                        # Create properly formatted content
                        # Join imports without empty lines between them
                        import_text = '\n'.join(import_section)
                        # Join code section as is
                        code_text = '\n'.join(code_section)
                        # Combine with exactly two empty lines between imports and code
                        new_content = import_text + '\n\n\n' + code_text
                        print(f"New main.py content:\n{new_content}")
                        
                        # Write back to main.py
                        with open(main_py_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"Added import statements for {len(imported_modules)} modules to main.py")
                        
                        # Verify the changes
                        with open(main_py_path, 'r', encoding='utf-8') as f:
                            verify_content = f.read()
                        print(f"Verified main.py content:\n{verify_content}")
                    else:
                        print(f"Main.py not found at {main_py_path}")
                else:
                    print("No modules to import")
            else:
                print("No selected prefabs")
        else:
            print("No QPrefabsManager found")


class ProjectCreatorUI(QMainWindow):
    """Project creator main window"""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """Initialize main window"""
        self.setWindowTitle("PyScreeps Arena - 项目创建器")
        self.setWindowIcon(QIcon(get_pixmap()))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create project body widget
        self._project_body = QProjectBody()
        
        # Connect signals
        self._project_body.projectCreated.connect(self._on_project_created)
        self._project_body.projectCancelled.connect(self._on_project_cancelled)
        self._project_body.languageChanged.connect(self._on_language_changed)
        
        # Add project body to layout
        layout.addWidget(self._project_body)
        
        # Set window size
        self.setFixedSize(550, 650)
    
    def _on_project_created(self, project_name: str, project_path: str):
        """Handle project created signal"""
        print(f"Project created: {project_name} at {project_path}")
        # You can add additional handling here if needed
    
    def _on_project_cancelled(self):
        """Handle project cancelled signal"""
        print("Project creation cancelled")
        # You can add additional handling here if needed
    
    def _on_language_changed(self, language_code: str):
        """Handle language changed signal"""
        print(f"Language changed to: {language_code}")
        # You can add additional handling here if needed
    
    # Properties to expose project body properties
    @pyqtProperty(str, constant=False)
    def projectName(self) -> str:
        """Get project name"""
        return self._project_body.projectName
    
    @projectName.setter
    def projectName(self, value: str):
        """Set project name"""
        self._project_body.projectName = value
    
    @pyqtProperty(str, constant=False)
    def projectPath(self) -> str:
        """Get project path"""
        return self._project_body.projectPath
    
    @projectPath.setter
    def projectPath(self, value: str):
        """Set project path"""
        self._project_body.projectPath = value
    
    @pyqtProperty(str, constant=False)
    def language(self) -> str:
        """Get current language code"""
        return self._project_body.language
    
    @language.setter
    def language(self, value: str):
        """Set language code"""
        self._project_body.language = value


def run_project_creator():
    """运行项目创建器UI"""
    app = QApplication(sys.argv)
    window = ProjectCreatorUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_project_creator()
