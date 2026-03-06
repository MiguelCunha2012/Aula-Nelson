import sqlite3

class AlunoService:
    def __init__(self, db_name="sistema_escola.db"):
        # Conecta ao banco de dados persistente [cite: 23]
        self.conn = sqlite3.connect(db_name)
        self._criar_tabela()

    def _criar_tabela(self):
        # Garante que a tabela existe antes de operar [cite: 68, 70]
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE,
                nota REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def cadastrar_aluno(self, nome, idade, email, nota):
        # Regra 1 - Nome obrigatório e tamanho mínimo
        if not nome or len(nome.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres.")

        # Regra 2 - Idade válida (16 a 100 anos)
        if not (16 <= idade <= 100):
            raise ValueError("Idade deve estar entre 16 e 100 anos.")

        # Regra 3 - Email válido (deve conter @ e .)
        if "@" not in email or "." not in email:
            raise ValueError("Email inválido.")

        # Regra 4 - Nota válida (0 a 10)
        if not (0 <= nota <= 10):
            raise ValueError("Nota deve estar entre 0 e 10.")

        # Desafio Extra - Email único
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM alunos WHERE email = ?", (email,))
        if cursor.fetchone():
            raise ValueError("Email já cadastrado.")

        # Regra 5 - Cálculo de status
        status = "Aprovado" if nota >= 7 else "Reprovado"

        # Persistência no SQLite
        cursor.execute(
            "INSERT INTO alunos (nome, idade, email, nota, status) VALUES (?, ?, ?, ?, ?)",
            (nome, idade, email, nota, status)
        )
        self.conn.commit()

        # Retorno esperado
        return {
            "nome": nome,
            "idade": idade,
            "email": email,
            "nota": nota,
            "status": status
        }