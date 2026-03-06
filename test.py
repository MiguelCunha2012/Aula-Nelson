import pytest
from sistema_cadastro import AlunoService

@pytest.fixture
def service():
    # Usa banco em memória para isolar os testes
    return AlunoService(":memory:")

# --- Testes de Validação de Nome ---
def test_nome_vazio(service):
    with pytest.raises(ValueError, match="Nome deve ter pelo menos 3 caracteres."):
        service.cadastrar_aluno("", 20, "teste@email.com", 8.0)

def test_nome_curto(service):
    with pytest.raises(ValueError, match="Nome deve ter pelo menos 3 caracteres."):
        service.cadastrar_aluno("Jo", 20, "teste@email.com", 8.0)

# --- Testes de Validação de Idade ---
def test_idade_menor_que_16(service):
    with pytest.raises(ValueError, match="Idade deve estar entre 16 e 100 anos."):
        service.cadastrar_aluno("João Silva", 15, "teste@email.com", 8.0)

def test_idade_maior_que_100(service):
    with pytest.raises(ValueError, match="Idade deve estar entre 16 e 100 anos."):
        service.cadastrar_aluno("João Silva", 101, "teste@email.com", 8.0)

# --- Testes de Validação de Email ---
def test_email_sem_arroba(service):
    with pytest.raises(ValueError, match="Email inválido."):
        service.cadastrar_aluno("João Silva", 20, "email.com", 8.0)

def test_email_sem_ponto(service):
    with pytest.raises(ValueError, match="Email inválido."):
        service.cadastrar_aluno("João Silva", 20, "email@com", 8.0)

# --- Testes de Validação de Nota e Status ---
@pytest.mark.parametrize("nota,status_esperado", [
    (7.0, "Aprovado"),   # Limite aprovação
    (10.0, "Aprovado"),  # Nota máxima
    (6.9, "Reprovado"),  # Quase aprovado
    (0.0, "Reprovado"),  # Nota mínima
])
def test_calculo_status(service, nota, status_esperado):
    aluno = service.cadastrar_aluno("João Silva", 20, f"teste{nota}@email.com", nota)
    assert aluno["status"] == status_esperado

# --- Teste de Sucesso Completo ---
def test_cadastro_sucesso(service):
    resultado = service.cadastrar_aluno("João Silva", 20, "joao@email.com", 8.5)
    assert resultado["nome"] == "João Silva"
    assert resultado["status"] == "Aprovado"

# --- Teste Desafio Extra (Email Duplicado) ---
def test_email_duplicado(service):
    service.cadastrar_aluno("Aluno 1", 20, "repetido@email.com", 8.0)
    with pytest.raises(ValueError, match="Email já cadastrado."):
        service.cadastrar_aluno("Aluno 2", 22, "repetido@email.com", 9.0)