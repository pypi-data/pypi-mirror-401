import sys
from dataclasses import dataclass
from PySide6.QtWidgets import *
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtCore import Qt, QTimer

@dataclass
class Product:
    id: int
    n: str
    c: str
    d: str
    p: float

@dataclass
class CartItem:
    pr: Product
    q: int

def main():
    app = QApplication(sys.argv)
    
    w = QWidget()
    w.setWindowTitle("Chill Coffee — Касса")
    w.resize(1300, 750)
    
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")
    db.open()
    
    q = QSqlQuery()
    q.exec("CREATE TABLE p(id INT,n TEXT,c TEXT,d TEXT,p REAL)")
    q.exec("""
    INSERT INTO p VALUES
    (1,'Капучино','Напитки','Кофе с молочной пенкой',180),
    (2,'Латте','Напитки','Мягкий кофе с молоком',190),
    (3,'Американо','Напитки','Классический кофе',150),
    (4,'Сэндвич','Еда','С курицей и сыром',250),
    (5,'Круассан','Десерты','Сливочный круассан',120),
    (6,'Эспрессо','Напитки','Крепкий черный кофе',140),
    (7,'Чай черный','Напитки','Листовой черный чай',130),
    (8,'Чизкейк','Десерты','Классический чизкейк',220),
    (9,'Салат Цезарь','Еда','С курицей и сухариками',280),
    (10,'Мокачино','Напитки','Кофе с шоколадом',200)
    """)
    
    products: list[Product] = []
    q.exec("SELECT * FROM p")
    while q.next():
        products.append(Product(
            q.value(0),
            q.value(1),
            q.value(2),
            q.value(3),
            q.value(4)
        ))
    
    cart: dict[int, CartItem] = {}
    sort_mode = 0
    
    stack = QStackedWidget()
    
    products_page = QWidget()
    products_layout = QVBoxLayout()
    
    search = QLineEdit()
    search.setPlaceholderText("Поиск")
    
    cat = QComboBox()
    cat.addItem("Любая категория")
    for p in products:
        if cat.findText(p.c) < 0:
            cat.addItem(p.c)
    
    asc = QPushButton("Цена ↑")
    desc = QPushButton("Цена ↓")
    
    table = QTableWidget(0, 3)
    table.setHorizontalHeaderLabels(["Название", "Категория", "Цена"])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    add_btn = QPushButton("Добавить в корзину")
    add_btn.setStyleSheet("height: 40px;")
    
    to_cart_btn = QPushButton("Перейти к оформлению")
    to_cart_btn.setStyleSheet("background:#4CAF50;color:white;height:40px;")
    
    products_layout.addWidget(search)
    products_layout.addWidget(cat)
    
    sort_layout = QHBoxLayout()
    sort_layout.addWidget(asc)
    sort_layout.addWidget(desc)
    products_layout.addLayout(sort_layout)
    
    products_layout.addWidget(table)
    
    btn_layout = QHBoxLayout()
    btn_layout.addWidget(add_btn)
    btn_layout.addWidget(to_cart_btn)
    products_layout.addLayout(btn_layout)
    
    products_page.setLayout(products_layout)
    
    cart_page = QWidget()
    main_h_layout = QHBoxLayout()
    
    left_column = QVBoxLayout()
    
    cart_section = QGroupBox("Корзина заказа")
    cart_section_layout = QVBoxLayout()
    
    cart_table = QTableWidget(0, 5)
    cart_table.setHorizontalHeaderLabels(["Название", "Цена", "Кол-во", "-", "+"])
    cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    cart_table.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    total = QLabel("Стоимость корзины: 0 ₽")
    total.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
    
    cart_section_layout.addWidget(cart_table)
    cart_section_layout.addWidget(total)
    cart_section.setLayout(cart_section_layout)
    
    back_to_products_btn = QPushButton("← Вернуться к товарам")
    
    left_column.addWidget(cart_section)
    left_column.addWidget(back_to_products_btn)
    
    right_column = QVBoxLayout()
    
    order_section = QGroupBox("Оформление заказа")
    order_layout = QVBoxLayout()
    
    client_layout = QVBoxLayout()
    client_label = QLabel("Информация о клиенте:")
    client_layout.addWidget(client_label)
    
    client_edit = QLineEdit()
    client_edit.setPlaceholderText("Номер телефона или имя")
    client_layout.addWidget(client_edit)
    
    no_client = QCheckBox("Без клиента")
    client_layout.addWidget(no_client)
    order_layout.addLayout(client_layout)
    
    order_layout.addSpacing(20)
    
    payment_layout = QVBoxLayout()
    payment_label = QLabel("Способ оплаты:")
    payment_layout.addWidget(payment_label)
    
    pay_type = QComboBox()
    pay_type.addItems(["Наличные", "Банковская карта", "QR-код"])
    payment_layout.addWidget(pay_type)
    order_layout.addLayout(payment_layout)
    
    order_layout.addSpacing(20)
    
    delivery_layout = QVBoxLayout()
    delivery_label = QLabel("Способ получения:")
    delivery_layout.addWidget(delivery_label)
    
    delivery_buttons = QVBoxLayout()
    in_cafe = QRadioButton("В заведении")
    takeaway = QRadioButton("На вынос")
    courier = QRadioButton("Курьером")
    in_cafe.setChecked(True)
    delivery_buttons.addWidget(in_cafe)
    delivery_buttons.addWidget(takeaway)
    delivery_buttons.addWidget(courier)
    delivery_layout.addLayout(delivery_buttons)
    order_layout.addLayout(delivery_layout)
    
    order_layout.addStretch()
    
    confirm_order_btn = QPushButton("Оформить заказ")
    confirm_order_btn.setStyleSheet("background:#ff6b6b;color:white;height:50px;font-size:16px;font-weight:bold;")
    order_layout.addWidget(confirm_order_btn)
    
    order_section.setLayout(order_layout)
    right_column.addWidget(order_section)
    
    main_h_layout.addLayout(left_column, 2)
    main_h_layout.addLayout(right_column, 1)
    cart_page.setLayout(main_h_layout)
    
    stack.addWidget(products_page)
    stack.addWidget(cart_page)
    
    main_layout = QVBoxLayout(w)
    main_layout.addWidget(stack)
    
    notification_overlay = QWidget(w)
    notification_overlay.setFixedHeight(41)
    notification_overlay.setStyleSheet("""
        background-color: rgba(0, 0, 0, 0.3);
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    """)
    notification_overlay.hide()
    
    notification_label = QLabel(notification_overlay)
    notification_label.setAlignment(Qt.AlignCenter)
    notification_label.setGeometry(0, 0, w.width(), 45)
    notification_label.setStyleSheet("""
        color: white;
        font-size: 14px;
        font-weight: normal;
    """)
    
    def show_notification(message, color="white"):
        """Показывает уведомление сверху экрана"""
        notification_label.setText(message)
    
        notification_label.setGeometry(0, 0, w.width(), 45)
    
        notification_overlay.resize(w.width(), 45)
        notification_overlay.move(0, 0)
    
        notification_overlay.raise_()
        notification_overlay.show()
    
        QTimer.singleShot(1500, notification_overlay.hide)
    
    def refresh_products():
        table.setRowCount(0)
        filtered = []
    
        for p in products:
            if ((search.text().lower() in p.n.lower() or
                 search.text().lower() in p.c.lower()) and
                (cat.currentText() == "Любая категория" or p.c == cat.currentText())):
                filtered.append(p)
    
        if sort_mode:
            filtered.sort(key=lambda x: x.p, reverse=(sort_mode == 2))
    
        for p in filtered:
            r = table.rowCount()
            table.insertRow(r)
            i = QTableWidgetItem(p.n)
            i.setData(Qt.UserRole, p.id)
            table.setItem(r, 0, i)
            table.setItem(r, 1, QTableWidgetItem(p.c))
            table.setItem(r, 2, QTableWidgetItem(str(p.p) + " ₽"))
    
    def refresh_cart():
        cart_table.setRowCount(0)
        s = 0
        for item in cart.values():
            r = cart_table.rowCount()
            cart_table.insertRow(r)
            cart_table.setItem(r, 0, QTableWidgetItem(item.pr.n))
            cart_table.setItem(r, 1, QTableWidgetItem(str(item.pr.p) + " ₽"))
            cart_table.setItem(r, 2, QTableWidgetItem(str(item.q)))
            cart_table.setItem(r, 3, QTableWidgetItem("-"))
            cart_table.setItem(r, 4, QTableWidgetItem("+"))
            cart_table.item(r, 0).setData(Qt.UserRole, item.pr.id)
            s += item.pr.p * item.q
    
        total.setText(f"Стоимость корзины: {s} ₽")
    
    refresh_products()
    
    search.textChanged.connect(refresh_products)
    cat.currentTextChanged.connect(refresh_products)
    
    asc.clicked.connect(lambda: (globals().__setitem__("sort_mode", 1), refresh_products()))
    desc.clicked.connect(lambda: (globals().__setitem__("sort_mode", 2), refresh_products()))
    
    def add_to_cart():
        r = table.currentRow()
        if r < 0:
            QMessageBox.warning(w, "Ошибка", "Выберите товар для добавления в корзину")
            return
        pid = table.item(r, 0).data(Qt.UserRole)
        product_name = ""
        for p in products:
            if p.id == pid:
                product_name = p.n
                if pid in cart:
                    cart[pid].q += 1
                    show_notification(f"✓ Товар '{product_name}' уже в корзине. Количество увеличено до {cart[pid].q} шт.")
                else:
                    cart[pid] = CartItem(p, 1)
                    show_notification(f"✓ Товар '{product_name}' добавлен в корзину")
                break
    
        refresh_cart()
    
    add_btn.clicked.connect(add_to_cart)
    
    def cart_click(r, c):
        pid = cart_table.item(r, 0).data(Qt.UserRole)
        if pid not in cart:
            return
    
        product_name = cart[pid].pr.n
    
        if c == 3:  # Кнопка "-"
            cart[pid].q -= 1
            if cart[pid].q <= 0:
                del cart[pid]
        elif c == 4:  # Кнопка "+"
            cart[pid].q += 1
    
        refresh_cart()
    
    cart_table.cellClicked.connect(cart_click)
    
    def go_to_cart():
        if stack.currentIndex() != 1:
            stack.setCurrentIndex(1)
    
    def go_to_products():
        if stack.currentIndex() != 0:
            stack.setCurrentIndex(0)
    
    to_cart_btn.clicked.connect(go_to_cart)
    back_to_products_btn.clicked.connect(go_to_products)
    
    def make_order():
        if not cart:
            QMessageBox.warning(w, "Корзина пуста", "Добавьте товары в корзину перед оформлением заказа")
            return
    
        client_info = ""
        if not no_client.isChecked() and client_edit.text().strip():
            client_info = client_edit.text().strip()
    
        payment_method = pay_type.currentText()
    
        delivery_method = "В заведении"
        if takeaway.isChecked():
            delivery_method = "На вынос"
        elif courier.isChecked():
            delivery_method = "Курьером"
    
        confirm_msg = QMessageBox(w)
        confirm_msg.setWindowTitle("Подтверждение заказа")
        confirm_msg.setText("Вы уверены, что хотите оформить заказ?")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setDefaultButton(QMessageBox.No)
    
        if confirm_msg.exec() != QMessageBox.Yes:
            return
    
        receipt = "=" * 40 + "\n"
        receipt += "CHILL COFFEE — КАССОВЫЙ ЧЕК\n"
        receipt += "=" * 40 + "\n"
        receipt += f"Клиент: {client_info if client_info else 'Без клиента'}\n"
        receipt += f"Оплата: {payment_method}\n"
        receipt += f"Получение: {delivery_method}\n"
        receipt += "=" * 40 + "\n"
        receipt += "ТОВАРЫ:\n"
    
        total_sum = 0
        for item in cart.values():
            item_total = item.pr.p * item.q
            receipt += f"{item.pr.n} x{item.q} = {item_total} ₽\n"
            total_sum += item_total
    
        receipt += "-" * 40 + "\n"
        receipt += f"ИТОГО: {total_sum} ₽\n"
        receipt += "=" * 40 + "\n"
        receipt += "Спасибо за заказ! Ждем вас снова!\n"
        receipt += "=" * 40
    
        msg = QMessageBox(w)
        msg.setWindowTitle("Заказ оформлен")
        msg.setText("Заказ успешно оформлен!")
        msg.setDetailedText(receipt)
        msg.setIcon(QMessageBox.Information)
    
        msg.exec()
    
        cart.clear()
        refresh_cart()
        client_edit.clear()
        no_client.setChecked(False)
        go_to_products()
    
    confirm_order_btn.clicked.connect(make_order)
    
    no_client.toggled.connect(
        lambda b: (client_edit.setEnabled(not b), client_edit.clear() if b else None)
    )
    
    def resizeEvent(event):
        notification_overlay.resize(w.width(), 45)
        notification_overlay.move(0, 0)
        notification_label.setGeometry(0, 0, w.width(), 45)
        QWidget.resizeEvent(w, event)
    
    w.resizeEvent = resizeEvent
    
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()