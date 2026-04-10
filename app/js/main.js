document.addEventListener('DOMContentLoaded', function() {
    const botao = document.getElementById('gerarAtividade');
    const resultado = document.getElementById('resultado');

    botao.addEventListener('click', async function() {
        try {
            const response = await fetch('/api/atividades/casa?tempo=60');
            const data = await response.json();
            resultado.textContent = data.atividade;
        } catch (error) {
            console.error('Erro ao buscar atividade:', error);
            resultado.textContent = 'Erro ao buscar atividade. Tente novamente.';
        }
    });
});