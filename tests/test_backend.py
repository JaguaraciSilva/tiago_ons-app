from fastapi.testclient import TestClient
import sys
import os

# Adiciona o diretório do backend ao path do Python para conseguir importar a app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from main import app, listar_datasets_ons, consultar_dados_ons

client = TestClient(app)

def test_health_or_root():
    """Valida se a aplicação FastAPI está online e responde."""
    # Como não temos uma rota GET na raiz no exemplo anterior, 
    # podemos testar enviar um pedido POST com dados inválidos para verificar o comportamento esperado (validação do Pydantic).
    response = client.post("/chat", json={})
    assert response.status_code == 422 # Erro de validaçãounprocessable entity por falta do campo 'pregunta'

def test_ferramenta_listar_datasets():
    """Testa diretamente a ferramenta LangChain mapeada para listar os datasets do ONS."""
    resultado = listar_datasets_ons.invoke({})
    assert isinstance(resultado, str)
    assert "Datasets disponíveis" in resultado

def test_ferramenta_consultar_dados():
    """Testa diretamente a ferramenta LangChain de consulta detalhada de dados."""
    resultado = consultar_dados_ons.invoke({"dataset_nome": "carga_energia", "filtros": "ano=2024"})
    assert isinstance(resultado, str)
    assert "carga_energia" in resultado