import unittest
import json
from app import create_app
from app.database import db

class TestAtividadesCasa(unittest.TestCase):
    def setUp(self):
        # Configurar o aplicativo para teste
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Criar um contexto de aplicativo
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        # Limpar o contexto do aplicativo
        self.app_context.pop()
    
    def test_get_atividade_casa_sem_parametros(self):
        # Testar a rota sem parâmetros
        response = self.client.get('/atividades/casa')
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a resposta é um JSON válido
        data = json.loads(response.data)
        self.assertIn('atividade', data)
        self.assertIn('tempo_estimado', data)
    
    def test_get_atividade_casa_com_tempo(self):
        # Testar a rota com parâmetro de tempo
        response = self.client.get('/atividades/casa?tempo=30')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('atividade', data)
        self.assertTrue(isinstance(data['tempo_estimado'], int))
    
    def test_get_atividade_casa_reset(self):
        # Testar o reset do histórico
        response = self.client.get('/atividades/casa?reset=true')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Histórico de atividades resetado')

if __name__ == '__main__':
    unittest.main()
