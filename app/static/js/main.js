document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formAtividade');
    const resultadoDiv = document.getElementById('resultado');
    const atividadeDiv = document.getElementById('atividade');
    const tempoDiv = document.getElementById('tempo');
    const detalhesDiv = document.getElementById('detalhes');
    const erroDiv = document.getElementById('erro');
    const tipoAtividadeSelect = document.getElementById('tipoAtividade');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Limpar resultados anteriores
        resultadoDiv.style.display = 'none';
        erroDiv.style.display = 'none';
        
        // Obter os valores do formulário
        const tempoInput = document.getElementById('tempoDisponivel');
        const tempo = parseInt(tempoInput.value, 10) || 60; // Valor padrão 60 se não informado
        const tipoAtividade = tipoAtividadeSelect.value;
        const filtrarMusica = document.getElementById('filtrarMusica').checked;
        
        // Montar a URL da requisição
        const url = `/${tipoAtividade}?tempo=${tempo}&filtrar_musica=${filtrarMusica}`;
        
        // Fazer a requisição para a API
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.erro || 'Erro ao buscar atividade');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Exibir a atividade
                atividadeDiv.textContent = data.atividade;
                tempoDiv.textContent = data.tempo_estimado 
                    ? `Tempo estimado: ${data.tempo_estimado} minutos`
                    : '';
                
                // Limpar detalhes anteriores
                detalhesDiv.innerHTML = '';
                
                // Adicionar detalhes se existirem
                if (data.detalhes) {
                    const detalhes = document.createElement('div');
                    detalhes.className = 'detalhes';
                    
                    // Tratar detalhes de música
                    if (data.detalhes.musica) {
                        const musica = document.createElement('p');
                        musica.innerHTML = `<strong>Música:</strong> ${data.detalhes.musica}`;
                        detalhes.appendChild(musica);
                    }
                    
                    // Tratar detalhes de redes sociais
                    if (data.detalhes.rede_social) {
                        const redeSocial = document.createElement('p');
                        redeSocial.innerHTML = `<strong>Rede Social:</strong> ${data.detalhes.rede_social}`;
                        detalhes.appendChild(redeSocial);
                    }

                    // Tratar detalhes de TV
                    if (data.detalhes.programa || data.detalhes.serie_ou_filme) {
                        if (data.detalhes.programa) {
                            const programa = document.createElement('p');
                            programa.innerHTML = `<strong>Programa:</strong> ${data.detalhes.programa}`;
                            detalhes.appendChild(programa);
                        }
                        if (data.detalhes.serie_ou_filme) {
                            const serieFilme = document.createElement('p');
                            serieFilme.innerHTML = `<strong>Série/Filme:</strong> ${data.detalhes.serie_ou_filme}`;
                            detalhes.appendChild(serieFilme);
                        }
                    }
                    
                    // Tratar detalhes de jogos (para a rota /casa)
                    if (data.detalhes.jogo) {
                        const jogo = document.createElement('p');
                        jogo.innerHTML = `<strong>Jogo:</strong> ${data.detalhes.jogo}`;
                        if (data.detalhes.tempo_jogo) {
                            jogo.innerHTML += ` (${data.detalhes.tempo_jogo} min)`;
                        }
                        detalhes.appendChild(jogo);
                    }
                    
                    detalhesDiv.appendChild(detalhes);
                }
                
                // Exibir o resultado
                resultadoDiv.style.display = 'block';
                
                // Rolar até o resultado
                resultadoDiv.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Erro:', error);
                erroDiv.textContent = error.message || 'Ocorreu um erro ao buscar a atividade. Tente novamente.';
                erroDiv.style.display = 'block';
            });
    });
});
