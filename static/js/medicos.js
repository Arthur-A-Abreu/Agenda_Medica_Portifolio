// Abre o modal de edição preenchendo os campos com os dados do médico
function abrirEdicao(id, nome, crm, numero, email) {
    document.getElementById('edit_nome').value   = nome;
    document.getElementById('edit_crm').value    = crm;
    document.getElementById('edit_numero').value = numero;
    document.getElementById('edit_email').value  = email;
    document.getElementById('formEdicao').action = '/medicos/' + id + '/editar/';
    document.getElementById('modalEdicao').classList.add('active');
}

// Lê os data-attributes do botão e chama abrirEdicao (evita conflito de aspas no HTML)
function abrirEdicaoBtn(btn) {
    abrirEdicao(
        btn.dataset.id,
        btn.dataset.nome,
        btn.dataset.crm,
        btn.dataset.numero,
        btn.dataset.email
    );
}

// Fecha o modal de edição
function fecharModal() {
    document.getElementById('modalEdicao').classList.remove('active');
}

function abrirModalUsuario(id, nome) {
    document.getElementById('user_medico_nome').innerText = nome;
    document.getElementById('formUsuario').action = '/medicos/' + id + '/usuario/';
    document.getElementById('modalUsuario').classList.add('active');
}

function fecharModalUsuario() {
    document.getElementById('modalUsuario').classList.remove('active');
}

// Fecha o modal ao clicar fora dele
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('modalEdicao').addEventListener('click', function (e) {
        if (e.target === this) fecharModal();
    });
    document.getElementById('modalUsuario').addEventListener('click', function (e) {
        if (e.target === this) fecharModalUsuario();
    });
});
