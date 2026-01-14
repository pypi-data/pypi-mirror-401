from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QSlider, QWidget, QMenu, QGraphicsScene, QGridLayout, QGraphicsItem, QGraphicsTextItem, QHBoxLayout, QGraphicsRectItem, QGraphicsView, QGraphicsSceneMouseEvent, QGraphicsDropShadowEffect
from PyQt6.QtCore import pyqtSignal, QPoint, Qt, QTimer, QRectF
from PyQt6.QtGui import QResizeEvent, QPainter, QColor, QPen, QBrush, QPolygon, QLinearGradient
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton

class PopupDialog (QDialog):
    def __init__(self, parent=None,entry_id=None,action_type=None):      
        super().__init__(parent)   
  

        self.ouder = parent
        self._viewmodel = parent._viewmodel

        self.setWindowTitle("Actions")
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

        self.entry_id = entry_id
        self.action_type = action_type
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #adb5bd;
                border-radius: 5px;
            }
            QPushButton {
                padding: 8px 25px;
                border: none;
                border-radius: 3px;
                text-align: left;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e2e6ea;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

     
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(lambda: self._handle_edit_action(self.entry_id, self.action_type)) 
        layout.addWidget(edit_btn)

        # Copy button
        copy_btn = QPushButton("Copy")
        copy_btn.clicked.connect(lambda: self._handle_copy_action(self.entry_id))
        layout.addWidget(copy_btn)

        # Separator (can use a line or just spacing)
        layout.addSpacing(5)

        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self._handle_delete_action(self.entry_id))
        layout.addWidget(delete_btn)

        layout.addSpacing(5)

        # Conditional buttons
        if self._viewmodel.has_clipboard():
            layout.addSpacing(5)
            
            insert_copied_above_btn = QPushButton("Insert Copied Above")
            insert_copied_above_btn.clicked.connect(lambda: self._handle_insert_copied_above(entry_id))
            layout.addWidget(insert_copied_above_btn)
            
            insert_copied_below_btn = QPushButton("Insert Copied Below")
            insert_copied_below_btn.clicked.connect(lambda: self._handle_insert_copied_below(entry_id))
            layout.addWidget(insert_copied_below_btn)
        else:
            insert_above_btn = QPushButton("Insert Above")
            insert_above_btn.clicked.connect(lambda: self._handle_insert_above(entry_id))
            layout.addWidget(insert_above_btn)
            
            insert_below_btn = QPushButton("Insert Below")
            insert_below_btn.clicked.connect(lambda: self._handle_insert_below(entry_id))
            layout.addWidget(insert_below_btn)

        # Position the dialog
        self.adjustSize()


    # Handler methods
    def _handle_edit_action(self, entry_id: str, action_type: str):
            """Handle edit action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_edit(viewmodel, entry_id, action_type))

    def _deferred_edit(self, viewmodel, entry_id, action_type):
            try:
                viewmodel.handle_edit(entry_id, action_type)
            except Exception as e:
                print(f"ERROR in handle_edit: {e}")
                import traceback
                traceback.print_exc()
            self.accept()

    def _handle_copy_action(self, entry_id: str):
            """Handle copy action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_copy(viewmodel, entry_id))

    def _deferred_copy(self, viewmodel, entry_id):
            try:
                viewmodel.handle_copy(entry_id)
            except Exception as e:
                print(f"ERROR in handle_copy: {e}")
            self.accept()

    def _handle_delete_action(self, entry_id: str):
            """Handle delete action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_delete(viewmodel, entry_id))

    def _deferred_delete(self, viewmodel, entry_id):
            try:
                viewmodel.handle_delete(entry_id)
            except Exception as e:
                print(f"ERROR in handle_delete: {e}")
            self.accept()

    def _handle_insert_copied_above(self, entry_id: str):
            """Handle insert copied above action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_insert_copied_above(viewmodel, entry_id))

    def _deferred_insert_copied_above(self, viewmodel, entry_id):
            try:
                viewmodel.handle_insert_copied_above(entry_id)
            except Exception as e:
                print(f"ERROR in handle_insert_copied_above: {e}")
            self.accept()

    def _handle_insert_copied_below(self, entry_id: str):
            """Handle insert copied below action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_insert_copied_below(viewmodel, entry_id))

    def _deferred_insert_copied_below(self, viewmodel, entry_id):
            try:
                viewmodel.handle_insert_copied_below(entry_id)
            except Exception as e:
                print(f"ERROR in handle_insert_copied_below: {e}")
            self.accept()

    def _handle_insert_above(self, entry_id: str):
            """Handle insert above action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_insert_above(viewmodel, entry_id))

    def _deferred_insert_above(self, viewmodel, entry_id):
            try:
                viewmodel.handle_insert_above(entry_id)
            except Exception as e:
                print(f"ERROR in handle_insert_above: {e}")
            self.accept()

    def _handle_insert_below(self, entry_id: str):
            """Handle insert below action."""
            viewmodel = self._viewmodel
            QTimer.singleShot(150, lambda: self._deferred_insert_below(viewmodel, entry_id))

    def _deferred_insert_below(self, viewmodel, entry_id):
            try:
                viewmodel.handle_insert_below(entry_id)
            except Exception as e:
                print(f"ERROR in handle_insert_below: {e}")
            self.accept()
       