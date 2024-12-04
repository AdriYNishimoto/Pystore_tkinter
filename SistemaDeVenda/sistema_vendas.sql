CREATE DATABASE sistema_vendas;

USE sistema_vendas;

-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,  
    role ENUM('admin', 'vendedor') NOT NULL
);

-- Tabela de Produtos
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade INT NOT NULL CHECK (quantidade >= 0), 
    valor DECIMAL(10, 2) NOT NULL
);

-- Tabela de Clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  -- Evitar emails duplicados
    telefone VARCHAR(20) NOT NULL UNIQUE  -- Evitar telefones duplicados
);

-- Tabela de Vendas
CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    vendedor_id INT,
    produto_id INT,
    quantidade INT NOT NULL,
    valor_total DECIMAL(10, 2),
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (vendedor_id) REFERENCES usuarios(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Inserção de Usuário Administrador
INSERT INTO usuarios (username, senha, role) VALUES ('admin', 'admin', 'admin');

-- Consultas para verificar os dados
SELECT * FROM usuarios;
SELECT * FROM clientes;
SELECT * FROM produtos;
SELECT * FROM vendas;
