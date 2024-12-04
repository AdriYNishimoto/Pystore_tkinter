import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import csv
from datetime import datetime

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "sistema_vendas"
}

# Conexão com o banco de dados
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Classe principal do sistema
class SistemaVendas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas")
        self.root.geometry("800x600")
        self.create_login_screen()

    def create_login_screen(self):
        # Tela de Login
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Usuário:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Senha:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Entrar", command=self.login).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, role FROM usuarios WHERE username=%s AND senha=%s",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()

            if user:
                user_id, role = user
                if role == "admin":
                    self.admin_dashboard()
                elif role == "vendedor":
                    self.vendedor_dashboard(user_id)
                else:
                    messagebox.showerror("Erro", "Usuário não autorizado.")
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def admin_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Dashboard - Administrador", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Cadastrar Produto", command=self.cadastrar_produto).pack(pady=10)
        tk.Button(self.root, text="Editar Produto", command=self.editar_produto).pack(pady=10)
        tk.Button(self.root, text="Cadastrar Vendedor", command=self.cadastrar_vendedor).pack(pady=10)
        tk.Button(self.root, text="Cadastrar Cliente", command=self.cadastrar_cliente).pack(pady=10)
        tk.Button(self.root, text="Buscar Produto", command=self.buscar_produto).pack(pady=10)
        tk.Button(self.root, text="Buscar Cliente", command=self.buscar_cliente).pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.create_login_screen).pack(pady=10)

    def vendedor_dashboard(self, user_id):
        self.clear_screen()
        tk.Label(self.root, text="Dashboard - Vendedor", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Realizar Venda", command=lambda: self.realizar_venda(user_id)).pack(pady=10)
        tk.Button(self.root, text="Relatórios de Vendas", command=self.gerar_relatorio).pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.create_login_screen).pack(pady=10)

    def cadastrar_produto(self):
        self.clear_screen()
        tk.Label(self.root, text="Cadastrar Produto", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Nome:").pack()
        nome_entry = tk.Entry(self.root)
        nome_entry.pack()
        tk.Label(self.root, text="Descrição:").pack()
        descricao_entry = tk.Entry(self.root)
        descricao_entry.pack()
        tk.Label(self.root, text="Quantidade em Estoque:").pack()
        quantidade_entry = tk.Entry(self.root)
        quantidade_entry.pack()
        tk.Label(self.root, text="Valor Unitário:").pack()
        valor_entry = tk.Entry(self.root)
        valor_entry.pack()

        def salvar_produto():
            nome = nome_entry.get()
            descricao = descricao_entry.get()
            quantidade = quantidade_entry.get()
            valor = valor_entry.get()

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO produtos (nome, descricao, quantidade, valor) VALUES (%s, %s, %s, %s)",
                    (nome, descricao, int(quantidade), float(valor))
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                self.admin_dashboard()

        tk.Button(self.root, text="Salvar", command=salvar_produto).pack(pady=10)

    def editar_produto(self):
        self.clear_screen()
        tk.Label(self.root, text="Editar Produto", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="ID do Produto:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack()

        def carregar_dados():
            produto_id = id_entry.get()
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome, descricao, quantidade, valor FROM produtos WHERE id = %s", (produto_id,))
                produto = cursor.fetchone()
                conn.close()

                if produto:
                    nome_var.set(produto[0])
                    descricao_var.set(produto[1])
                    quantidade_var.set(produto[2])
                    valor_var.set(produto[3])
                else:
                    messagebox.showerror("Erro", "Produto não encontrado.")

        nome_var = tk.StringVar()
        descricao_var = tk.StringVar()
        quantidade_var = tk.IntVar()
        valor_var = tk.DoubleVar()

        tk.Button(self.root, text="Carregar Dados", command=carregar_dados).pack(pady=10)
        tk.Label(self.root, text="Nome:").pack()
        tk.Entry(self.root, textvariable=nome_var).pack()
        tk.Label(self.root, text="Descrição:").pack()
        tk.Entry(self.root, textvariable=descricao_var).pack()
        tk.Label(self.root, text="Quantidade:").pack()
        tk.Entry(self.root, textvariable=quantidade_var).pack()
        tk.Label(self.root, text="Valor:").pack()
        tk.Entry(self.root, textvariable=valor_var).pack()

        def salvar_edicao():
            produto_id = id_entry.get()
            nome = nome_var.get()
            descricao = descricao_var.get()
            quantidade = quantidade_var.get()
            valor = valor_var.get()

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "UPDATE produtos SET nome=%s, descricao=%s, quantidade=%s, valor=%s WHERE id=%s",
                        (nome, descricao, quantidade, valor, produto_id)
                    )
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                    self.admin_dashboard()
                except mysql.connector.Error as e:
                    messagebox.showerror("Erro", f"Erro ao editar produto: {e}")
                conn.close()

        tk.Button(self.root, text="Salvar", command=salvar_edicao).pack(pady=10)

    def cadastrar_vendedor(self):
        self.clear_screen()
        tk.Label(self.root, text="Cadastrar Vendedor", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Usuário:").pack()
        usuario_entry = tk.Entry(self.root)
        usuario_entry.pack()
        tk.Label(self.root, text="Senha:").pack()
        senha_entry = tk.Entry(self.root)
        senha_entry.pack()

        def salvar_vendedor():
            usuario = usuario_entry.get()
            senha = senha_entry.get()

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (username, senha, role) VALUES (%s, %s, %s)",
                    (usuario, senha, "vendedor")
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Vendedor cadastrado com sucesso!")
                self.admin_dashboard()

        tk.Button(self.root, text="Salvar", command=salvar_vendedor).pack(pady=10)

    def cadastrar_cliente(self):
        self.clear_screen()
        tk.Label(self.root, text="Cadastrar Cliente", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Nome Completo:").pack()
        nome_entry = tk.Entry(self.root)
        nome_entry.pack()
        tk.Label(self.root, text="Email:").pack()
        email_entry = tk.Entry(self.root)
        email_entry.pack()
        tk.Label(self.root, text="Telefone:").pack()
        telefone_entry = tk.Entry(self.root)
        telefone_entry.pack()

        def salvar_cliente():
            nome = nome_entry.get()
            email = email_entry.get()
            telefone = telefone_entry.get()

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)",
                        (nome, email, telefone)
                    )
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                    self.admin_dashboard()
                except mysql.connector.Error as e:
                    messagebox.showerror("Erro", f"Erro ao salvar cliente: {e}")
                conn.close()

        tk.Button(self.root, text="Salvar", command=salvar_cliente).pack(pady=10)

    def buscar_produto(self):
        self.clear_screen()
        tk.Label(self.root, text="Buscar Produto", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Nome do Produto:").pack()
        busca_entry = tk.Entry(self.root)
        busca_entry.pack()

        def buscar():
            busca = busca_entry.get()
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome FROM produtos WHERE nome LIKE %s", (f"%{busca}%",))
                resultados = cursor.fetchall()
                conn.close()

                result_text.delete("1.0", tk.END)
                for resultado in resultados:
                    result_text.insert(tk.END, f"ID: {resultado[0]} | Nome: {resultado[1]}\n")

        tk.Button(self.root, text="Buscar", command=buscar).pack(pady=10)
        result_text = tk.Text(self.root, height=10)
        result_text.pack()

        tk.Button(self.root, text="Voltar", command=self.admin_dashboard).pack(pady=10)


    def buscar_cliente(self):
        self.clear_screen()
        tk.Label(self.root, text="Buscar Cliente", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="Nome do Cliente:").pack()
        busca_entry = tk.Entry(self.root)
        busca_entry.pack()

        def buscar():
            busca = busca_entry.get()
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome FROM clientes WHERE nome LIKE %s", (f"%{busca}%",))
                resultados = cursor.fetchall()
                conn.close()

                result_text.delete("1.0", tk.END)
                for resultado in resultados:
                    result_text.insert(tk.END, f"ID: {resultado[0]} | Nome: {resultado[1]}\n")

        tk.Button(self.root, text="Buscar", command=buscar).pack(pady=10)
        result_text = tk.Text(self.root, height=10)
        result_text.pack()

        tk.Button(self.root, text="Voltar", command=self.admin_dashboard).pack(pady=10)


    def realizar_venda(self, user_id):
        self.clear_screen()
        tk.Label(self.root, text="Realizar Venda", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text="ID do Cliente:").pack()
        cliente_entry = tk.Entry(self.root)
        cliente_entry.pack()
        tk.Label(self.root, text="ID do Produto:").pack()
        produto_entry = tk.Entry(self.root)
        produto_entry.pack()
        tk.Label(self.root, text="Quantidade:").pack()
        quantidade_entry = tk.Entry(self.root)
        quantidade_entry.pack()

        def finalizar_venda():
            cliente_id = cliente_entry.get()
            produto_id = produto_entry.get()
            quantidade = quantidade_entry.get()

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT quantidade FROM produtos WHERE id = %s", (produto_id,))
                produto = cursor.fetchone()

                if produto and produto[0] >= int(quantidade):
                    cursor.execute(
                        "INSERT INTO vendas (vendedor_id, cliente_id, produto_id, quantidade, data_venda) VALUES (%s, %s, %s, %s, %s)",
                        (user_id, cliente_id, produto_id, quantidade, datetime.now())
                    )
                    cursor.execute(
                        "UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s",
                        (quantidade, produto_id)
                    )
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")
                    self.vendedor_dashboard(user_id)
                else:
                    messagebox.showerror("Erro", "Quantidade insuficiente em estoque.")
                conn.close()

        tk.Button(self.root, text="Finalizar Venda", command=finalizar_venda).pack(pady=10)

    def gerar_relatorio(self):
        self.clear_screen()
        tk.Label(self.root, text="Relatório de Vendas", font=("Arial", 20)).pack(pady=20)

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT vendas.id, usuarios.username, clientes.nome, produtos.nome, vendas.quantidade, vendas.data_venda "
                "FROM vendas "
                "JOIN usuarios ON vendas.vendedor_id = usuarios.id "
                "JOIN clientes ON vendas.cliente_id = clientes.id "
                "JOIN produtos ON vendas.produto_id = produtos.id"
            )
            vendas = cursor.fetchall()
            conn.close()

            tree = ttk.Treeview(self.root, columns=("ID", "Vendedor", "Cliente", "Produto", "Quantidade", "Data"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Vendedor", text="Vendedor")
            tree.heading("Cliente", text="Cliente")
            tree.heading("Produto", text="Produto")
            tree.heading("Quantidade", text="Quantidade")
            tree.heading("Data", text="Data")
            tree.pack()

            for venda in vendas:
                tree.insert("", tk.END, values=venda)

            def exportar_csv():
                with open("relatorio_vendas.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Vendedor", "Cliente", "Produto", "Quantidade", "Data"])
                    writer.writerows(vendas)
                messagebox.showinfo("Sucesso", "Relatório exportado para relatorio_vendas.csv")

            tk.Button(self.root, text="Exportar CSV", command=exportar_csv).pack(pady=10)

# Inicialização do sistema
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVendas(root)
    root.mainloop()
