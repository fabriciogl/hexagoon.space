/*
 * Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
 */

function showResposta(id){
    form = document.getElementById('form'+id);
    selecionado = form['alternativaRadio'].value;
    resposta = document.getElementById('resposta'+id).getAttribute('value')
    if (resposta === selecionado){
        document.getElementById('resultado'+id).textContent = 'Você acertou!';
    } else {
        document.getElementById('resultado'+id).textContent = 'Você errou! A resposta correta é ' + resposta;
    }
    return false
}