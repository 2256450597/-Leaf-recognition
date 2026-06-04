"""PyQt5 主界面：农作物病害检测分析平台"""
import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
    QSplitter, QMessageBox, QHeaderView, QFrame,
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models import CropDiseasePipeline
from src.export import export_csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基于YOLO的农作物病害检测分析平台")
        self.setMinimumSize(1200, 800)

        self.pipeline = CropDiseasePipeline()
        self.history = []

        self._init_ui()
        self._load_models()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_splitter = QSplitter(Qt.Horizontal, central)

        # ===== 左侧：图片预览区 =====
        left_panel = QVBoxLayout()
        self.image_label = QLabel("图片预览区")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(500, 400)
        self.image_label.setStyleSheet(
            "border: 2px dashed #ccc; background: #fafafa; font-size: 16px; color: #999;"
        )

        btn_layout = QHBoxLayout()
        btn_upload = QPushButton("上传图片")
        btn_upload.clicked.connect(self._on_upload)
        btn_batch = QPushButton("批量导入")
        btn_batch.clicked.connect(self._on_batch)
        btn_layout.addWidget(btn_upload)
        btn_layout.addWidget(btn_batch)

        left_panel.addWidget(self.image_label)
        left_panel.addLayout(btn_layout)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        main_splitter.addWidget(left_widget)

        # ===== 右侧：结果 + 历史 =====
        right_panel = QVBoxLayout()

        # 结果区
        result_frame = QFrame()
        result_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        result_layout = QVBoxLayout(result_frame)
        result_title = QLabel("检测结果")
        result_title.setFont(QFont("Arial", 14, QFont.Bold))
        self.crop_result_label = QLabel("🌿 作物类型: --")
        self.crop_result_label.setFont(QFont("Arial", 12))
        self.disease_result_label = QLabel("🦠 病害类型: --")
        self.disease_result_label.setFont(QFont("Arial", 12))
        self.conf_label = QLabel("")
        self.conf_label.setFont(QFont("Arial", 10))
        self.conf_label.setStyleSheet("color: #666;")

        result_layout.addWidget(result_title)
        result_layout.addWidget(self.crop_result_label)
        result_layout.addWidget(self.disease_result_label)
        result_layout.addWidget(self.conf_label)
        right_panel.addWidget(result_frame)

        # 历史记录区
        history_label = QLabel("───── 历史记录 ─────")
        history_label.setFont(QFont("Arial", 11, QFont.Bold))
        right_panel.addWidget(history_label)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["文件名", "检测结果", "时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        right_panel.addWidget(self.table)

        # 导出按钮
        btn_export = QPushButton("导出 CSV")
        btn_export.clicked.connect(self._on_export)
        right_panel.addWidget(btn_export)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([600, 500])

    def _load_models(self):
        try:
            self.pipeline.load_models()
            QMessageBox.information(self, "就绪", "4 个模型已加载（支持 23 种病害识别），可以开始检测。")
        except FileNotFoundError as e:
            QMessageBox.warning(self, "警告", f"模型文件未找到:\n{e}\n请先完成训练。")

    def _on_upload(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "Images (*.jpg *.jpeg *.png *.bmp)"
        )
        if not path:
            return

        pixmap = QPixmap(path)
        scaled = pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)
        self.image_label.setStyleSheet("border: none; background: transparent;")

        try:
            result = self.pipeline.predict(path)
            self._show_result(result)
            result["file"] = os.path.basename(path)
            result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.insert(0, result)
            self._add_history_row(result)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def _on_batch(self):
        folder = QFileDialog.getExistingDirectory(self, "选择图片文件夹")
        if not folder:
            return

        exts = {'.jpg', '.jpeg', '.png', '.bmp'}
        paths = [
            os.path.join(folder, f)
            for f in sorted(os.listdir(folder))
            if os.path.splitext(f)[1].lower() in exts
        ]
        if not paths:
            QMessageBox.information(self, "提示", "文件夹中没有图片。")
            return

        try:
            results = self.pipeline.predict_batch(paths)
            for r in results:
                r["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history = results + self.history
            self._refresh_table()
            QMessageBox.information(self, "完成", f"已处理 {len(results)} 张图片。")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def _show_result(self, result: dict):
        self.crop_result_label.setText(
            f"🌿 作物类型: {result['crop']}  ({result['crop_conf']:.1%})"
        )
        self.disease_result_label.setText(
            f"🦠 病害类型: {result['disease']}  ({result['disease_conf']:.1%})"
        )

        if result["disease"] == "健康":
            color = "#2ecc71"
        elif result["disease_conf"] < 0.5:
            color = "#f39c12"
        else:
            color = "#e74c3c"
        self.disease_result_label.setStyleSheet(f"color: {color};")
        self.conf_label.setText(
            f"作物置信度: {result['crop_conf']:.2%}  |  病害置信度: {result['disease_conf']:.2%}"
        )

    def _add_history_row(self, result: dict):
        row = self.table.rowCount()
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(result.get("file", "")))
        combined = f"{result.get('crop', '?')}_{result.get('disease', '?')}"
        item = QTableWidgetItem(combined)
        if result.get("disease") == "健康":
            item.setForeground(QColor("#2ecc71"))
        else:
            item.setForeground(QColor("#e74c3c"))
        self.table.setItem(0, 1, item)
        self.table.setItem(0, 2, QTableWidgetItem(result.get("time", "")))

    def _refresh_table(self):
        self.table.setRowCount(0)
        for r in self.history[:50]:
            self._add_history_row(r)

    def _on_export(self):
        if not self.history:
            QMessageBox.information(self, "提示", "没有可导出的记录。")
            return
        path, _ = QFileDialog.getSaveFileName(self, "导出 CSV", "", "CSV Files (*.csv)")
        if path:
            export_csv(self.history, path)
            QMessageBox.information(self, "完成", f"已导出到 {path}")
