# Sistema de Vendas - PYSTORE

O Sistema de Vendas é uma aplicação desenvolvida em Python com a biblioteca Tkinter para a interface gráfica e MySQL para o gerenciamento do banco de dados. Este sistema oferece funcionalidades para gestão de vendas, controle de estoque e cadastro de usuários, clientes e produtos, permitindo que administradores e vendedores realizem suas tarefas de forma eficiente.

- Type some Markdown on the left
- See HTML in the right
- ✨Magic ✨

## Funcionalidades
### Para Administradores:
- Dashboard Administrativo: Controle completo sobre os dados do sistema.
- Cadastro de Produtos: Adicione novos produtos ao estoque com informações detalhadas.
- Edição de Produtos: Atualize informações de produtos existentes.
- Cadastro de Vendedores: Registre novos vendedores no sistema.
- Cadastro de Clientes: Insira informações de clientes, incluindo nome, e-mail e telefone.
- Busca Avançada: Localize produtos ou clientes rapidamente.
- Relatórios de Vendas: Geração de relatórios detalhados com opção de exportação para CSV.

### Para Vendedores:
- Dashboard de Vendedor: Acesso às funcionalidades específicas para vendas.
- Realização de Vendas: Registre vendas com controle automático do estoque.
- Relatórios de Vendas: Consulte informações detalhadas sobre vendas realizadas.

## Tecnologias Utilizadas
- Python: Linguagem principal para desenvolvimento do sistema.
- Tkinter: Interface gráfica.
- MySQL: Banco de dados para armazenamento de informações.
- CSV: Exportação de relatórios.

## Pré-requisitos
Antes de executar o projeto, certifique-se de ter:
- Python 3.11 ou superior instalado em sua máquina.
- MySQL instalado e configurado.
- Biblioteca mysql-connector-python instalada:

```sh    
pip install mysql-connector-python
```

## Configuração do Banco de Dados
- Crie o banco de dados `sistema_vendas` no MySQL.
- Execute as seguintes tabelas (exemplo):
```sh
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    role ENUM('admin', 'vendedor') NOT NULL
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade INT NOT NULL,
    valor DECIMAL(10, 2) NOT NULL
);

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendedor_id INT NOT NULL,
    cliente_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    data_venda DATETIME NOT NULL,
    FOREIGN KEY (vendedor_id) REFERENCES usuarios(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
```
- Atualize as configurações de banco no arquivo `db_config` para se adequar ao seu ambiente.

## Como Executar
- Clone este repositório:
```sh
git clone https://github.com/seu-usuario/sistema-vendas.git
cd sistema-vendas
```
- Execute o programa:
```sh
python sistema_vendas.py
```
