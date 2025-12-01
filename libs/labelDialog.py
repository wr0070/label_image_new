try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import new_icon, label_validator, trimmed
import os
from PyQt5.QtGui import QFont

BB = QDialogButtonBox


class LabelDialog(QDialog):
    """
    三标签输入弹窗
    最终返回拼接后的字符串: '标签1, 标签2, 标签3'
    """

    def __init__(self, texts=None, parent=None, list_item=None):
        """
        texts: list[str] 初始值，可小于3
        list_item: 历史标签列表，用于补全（此版本不显示历史框）
        """
        super().__init__(parent)

        if texts is None:
            texts = ["", "", ""]

        self.labels = ["施工场景", "风险隐患类型", "可能导致的事故类型"]

        # 从 txt 文件中读取 options
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        file_names = ["scene.txt", "risk.txt", "accident.txt"]
        self.options = []
        for f in file_names:
            file_path = os.path.join(base_path, f)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = [line.strip() for line in file.readlines() if line.strip()]
                    self.options.append(lines)
            else:
                self.options.append([])

        self.edits = []

        font = QFont("微软雅黑", 12)  # 设置全局字体
        self.setFont(font)

        layout = QVBoxLayout()

        # 三个下拉框
        for i in range(3):
            label = QLabel(self.labels[i] + ":")
            label.setFont(font)

            combo = QComboBox()
            combo.setEditable(True)
            combo.addItems(self.options[i])
            combo.setCurrentText(texts[i] if i < len(texts) else "")

            # ----- 自适应宽度 + 最小尺寸 -----
            combo.setMinimumWidth(250)         # 最小宽度
            combo.setMinimumHeight(35)         # 更大的输入区域
            combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            combo.setFont(font)

            self.edits.append(combo)

            layout.addWidget(label)
            layout.addWidget(combo)

        # --------- OK / Cancel 按钮 -------
        self.button_box = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(new_icon('done'))
        bb.button(BB.Cancel).setIcon(new_icon('undo'))
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)

        bb.setMinimumHeight(40)
        bb.setFont(font)

        layout.addWidget(bb)

        self.setLayout(layout)

        # 默认窗口大小（可调）
        self.resize(420, 260)


    def post_process_edit(self, edit):
        """去除空格"""
        edit.setText(trimmed(edit.text()))

    def validate(self):
        """至少有一个标签非空才接受"""
        if any(trimmed(e.text()) for e in self.edits):
            self.accept()

    def pop_up(self, texts=None, move=True):
        """
        显示弹窗，返回拼接后的字符串
        texts: list[str] 初始值，可少于3个
        """
        if texts is None:
            texts = ["", "", ""]

        # 清空旧值并设置初始文本
        for i, edit in enumerate(self.edits):
            edit.clearEditText()
            edit.setCurrentText(texts[i] if i < len(texts) else "")
            edit.setFocus(Qt.PopupFocusReason)

        # 位置调整逻辑
        if move:
            cursor_pos = QCursor.pos()
            btn = self.button_box.buttons()[0]
            self.adjustSize()
            btn.adjustSize()
            offset = btn.mapToGlobal(btn.pos()) - self.pos()
            offset += QPoint(btn.size().width() // 4, btn.size().height() // 2)
            cursor_pos.setX(max(0, cursor_pos.x() - offset.x()))
            cursor_pos.setY(max(0, cursor_pos.y() - offset.y()))
            parent_bottom_right = self.parentWidget().geometry()
            max_x = parent_bottom_right.x() + parent_bottom_right.width() - self.sizeHint().width()
            max_y = parent_bottom_right.y() + parent_bottom_right.height() - self.sizeHint().height()
            max_global = self.parentWidget().mapToGlobal(QPoint(max_x, max_y))
            if cursor_pos.x() > max_global.x():
                cursor_pos.setX(max_global.x())
            if cursor_pos.y() > max_global.y():
                cursor_pos.setY(max_global.y())
            self.move(cursor_pos)

        if self.exec_():
            # 返回所有下拉框当前选中的文本，用分号拼接
            return ';'.join([edit.currentText() for edit in self.edits])
        else:
            return None


    def list_item_click(self, t_qlist_widget_item):
        """单击历史标签补全"""
        text = trimmed(t_qlist_widget_item.text())
        # 按顺序填入第一个空框
        for edit in self.edits:
            if not edit.text().strip():
                edit.setText(text)
                break

    def list_item_double_click(self, t_qlist_widget_item):
        """双击直接确定"""
        self.list_item_click(t_qlist_widget_item)
        self.validate()