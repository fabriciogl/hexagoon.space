/*
 * Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
 */
const baseUrl = window.location.origin;

window.onload = async function(e){

    if (localStorage.getItem("jwt")){
        document.querySelector('input[type=email]').style.display = 'none';
        document.querySelector('input[type=password]').style.display = 'none';
        document.querySelector('input[value=Logar]').style.display = 'none';
        document.querySelector('#aa').style.display = 'block';
        document.querySelector('#ca').style.display = 'block';
        document.querySelector('#pa').style.display = 'block';
    }

    let data = document.querySelector('#dataLoad').innerText;
    data = JSON.parse(data);
    // inicializacao do editor é assincrona, então temos que aguardar a inicialização.
    await editor.isReady;
    editor.render(data);

};

async function showLogin(){
    document.querySelector('input[type=email]').style.display = 'block';
    document.querySelector('input[type=password]').style.display = 'block';
    document.querySelector('input[value=Logar]').style.display = 'block';
};

async function fazerLogin(){
    const email = document.querySelector('input[type=email]');
    const senha = document.querySelector('input[type=password]');

    const login_response = await fetch(`${baseUrl}/autenticacao`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": email.value,
            "senha": senha.value
        })
    });

    if (!login_response.ok) {
        const resposta = await login_response.json();
        const p = document.createElement("p");
        const alerta = document.createTextNode(`Falha na autenticação! ${resposta['detail']}`);
        p.appendChild(alerta); //adiciona o nó de texto à nova div criada
        document.querySelector('#navigation').appendChild(p);

        // torna visível os campos de login
        email.style.display = 'block';
        senha.style.display = 'block';
        document.querySelector('input[value=Logar]').style.display = 'block';
    }

    if (login_response.ok){

        const resposta = await login_response.json();

        // setar o jwt no localstorage
        localStorage.setItem("jwt", resposta['token']);

        // seta display none para os elementos de input
        senha.style.display = 'none';
        email.style.display = 'none';
        document.querySelector('input[value=Logar]').style.display = 'none';

        document.querySelector('#ca').style.display = 'block';
        document.querySelector('#aa').style.display = 'block';
        document.querySelector('#pa').style.display = 'block';
    }
}

const editor = new EditorJS({
    /**
     * Wrapper of Editor
     */
    holder: 'editorjs',

    readOnly: true,
    /**
     * Tools list
     */
    tools: {
        /**
         * Each Tool is a Plugin. Pass them via 'class' option with necessary settings {@link docs/tools.md}
         */
        header: {
            class: Header,
            inlineToolbar: ['link'],
            config: {
                placeholder: 'Header'
            },
            shortcut: 'CMD+SHIFT+H'
        },
        /**
         * Or pass class directly without any configuration
         */
        image: {
            class: SimpleImage,
            inlineToolbar: ['link'],
            shortcut: 'CMD+SHIFT+.'
        },
        list: {
            class: List,
            inlineToolbar: true,
            shortcut: 'CMD+SHIFT+L'
        },
        checklist: {
            class: Checklist,
            inlineToolbar: true,
        },
        quote: {
            class: Quote,
            inlineToolbar: true,
            config: {
                quotePlaceholder: 'Enter a quote',
                captionPlaceholder: 'Quote\'s author',
            },
            shortcut: 'CMD+SHIFT+O'
        },
        warning: Warning,
        marker: {
            class:  Marker,
            shortcut: 'CMD+SHIFT+M'
        },
        code: {
            class:  CodeTool,
            shortcut: 'CMD+SHIFT+C'
        },
        delimiter: Delimiter,
        inlineCode: {
            class: InlineCode,
            shortcut: 'CMD+SHIFT+C'
        },
        linkTool: LinkTool,
        embed: Embed,
        table: {
            class: Table,
            inlineToolbar: true,
            shortcut: 'CMD+ALT+T'
        },
    },
    /**
     * This Tool will be used as default
     */
    // initialBlock: 'paragraph',
    /**
     * Initial Editor data
     */
    data: {
        blocks: [
        ]
    },
    onChange: function() {
        console.log('something changed');
    }
});


async function readOnlyArtigo(){

    let proteger = document.querySelector('#pa');

    if (proteger.getAttribute('data-protected') === 'false'){
        proteger.setAttribute('value', 'Proteger Artigo');
        proteger.setAttribute('data-protected', 'true');
    } else {
        proteger.setAttribute('value', 'Desproteger Artigo');
        proteger.setAttribute('data-protected', 'false');
    }

    editor.readOnly.toggle();

}

async function respostaPushArtigo(response){

    if (response.status === 401) {
        const resposta = await response.json();
        document.querySelector('#alert').textContent = `Falha na atualização do artigo! ${resposta['detail']}`;

        // torna visível os campos de login
        document.querySelector('input[type=email]').style.display = 'block';
        document.querySelector('input[type=password]').style.display = 'block';
        document.querySelector('input[value=Logar]').style.display = 'block';
    }

    if (!response.ok){
        const resposta = await response.json();
        document.querySelector('#alert').textContent = `Falha na atualização do artigo! ${resposta['detail']}`;

    }

    if (response.status === 200){
        document.querySelector('#alert').textContent = `Artigo atualizado com sucesso!!`;
    }

    if (response.status === 201){
        document.querySelector('#alert').textContent = `Artigo criado com sucesso!!`;
        const resposta = await response.json();
        const li_original = document.querySelector('.list-group-item');
        const li_clone = li_original.cloneNode(true);
        li_clone.querySelector('a').innerText = resposta.titulo;
        li_clone.querySelector('a').setAttribute('href', `/${resposta.id}`);
        document.querySelector('ul').appendChild(li_clone);
    }


}


async function updateArtigo(){

    const token = localStorage.getItem("jwt");
    const id = document.querySelector('#aid').textContent;

    let savedData;
    try{
        savedData = await editor.save();
    } catch {
        alert('Desproteja o artigo para salvá-lo.')
        return
    }

    const artigo_response = await fetch(`${baseUrl}/artigo/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
        "corpo": JSON.stringify(savedData)
        })
    });

    respostaPushArtigo(artigo_response);

}

async function enviarArtigo(){

    const modalidade_artigo = document.querySelector('#maid').textContent;
    let savedData;

    try{
        savedData = await editor.save();
    } catch {
        alert('Desproteja o artigo para salvá-lo.')
        return
    }
    const token = localStorage.getItem("jwt");

    const artigo_response = await fetch(`${baseUrl}/artigo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            "corpo": JSON.stringify(savedData),
            "modalidade_artigo_id": modalidade_artigo
        })
    });

    respostaPushArtigo(artigo_response);

}

async function createArtigo(){

    // alterar o conteúdo do editor
    const newContent = {"blocks": [{"data": {"level": 2, "text": "Novo Artigo"}, "type": "header"}]}
    editor.render(newContent);

    document.querySelector('#ca').value = "Enviar Artigo"
    document.querySelector('#ca').onclick = enviarArtigo;
}

async function selecionaGrupo(){
    const grupo_id = window.event.target.selectedOptions[0].value;
    window.open(`${baseUrl}/grupos/${grupo_id}`, '_self');
}