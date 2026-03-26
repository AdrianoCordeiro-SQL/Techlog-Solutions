from app.banco_de_dados.local import BancoDeDadosLocal
from app.modelos.cliente import Cliente, ClienteCriarAtualizar


class ClienteRepositorio:
    def __init__(self, database: BancoDeDadosLocal):
        self.db = database

    async def listar_clientes(self) -> list[Cliente]:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            linhas = cursor.fetchall()
            clientes = [
                Cliente(
                    id_=linha[0],
                    nome=linha[1],
                    email=linha[2],
                    telefone=linha[3],
                )
                for linha in linhas
            ]
            return clientes

    async def buscar_cliente(self, cliente_id: int) -> Cliente | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, telefone FROM clientes WHERE id = ?",
                (cliente_id,),
            )
            linha = cursor.fetchone()
            if linha:
                return Cliente(
                    id_=linha[0],
                    nome=linha[1],
                    email=linha[2],
                    telefone=linha[3],
                )
            return None

    async def criar_cliente(self, cliente: ClienteCriarAtualizar) -> Cliente:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (cliente.nome, cliente.email, cliente.telefone),
            )

            cliente_id = cursor.lastrowid
            if cliente_id is None:
                raise RuntimeError("Falha ao criar cliente: ID nao retornado pelo banco.")

            return Cliente(
                id_=cliente_id,
                nome=cliente.nome,
                email=cliente.email,
                telefone=cliente.telefone,
            )

    async def atualizar_cliente(
        self, cliente_id: int, cliente: ClienteCriarAtualizar
    ) -> Cliente | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                (cliente.nome, cliente.email, cliente.telefone, cliente_id),
            )
            if cursor.rowcount == 0:
                return None
            return Cliente(
                id_=cliente_id,
                nome=cliente.nome,
                email=cliente.email,
                telefone=cliente.telefone,
            )

    async def deletar_cliente(self, cliente_id: int) -> bool:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            return cursor.rowcount > 0
    