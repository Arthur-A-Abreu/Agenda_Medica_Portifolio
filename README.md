# 🏥 Agenda Medica - Gestão e Calendário de Plantões

Um sistema web completo desenvolvido em **Django** para o gerenciamento de escalas médicas e plantões. A plataforma permite a organização visual dos horários, controle de equipe e exportação de dados consolidados de forma automatizada.

## 🚀 Funcionalidades Principais

* **🔒 Controle de Acesso e Autenticação:** O sistema é totalmente privado. Apenas usuários cadastrados e autenticados podem acessar a plataforma.
* **👥 Níveis de Permissão (Roles):** Divisão clara entre `Administradores` (que gerenciam a plataforma, cadastram médicos e usuários) e `Usuários Comuns/Médicos` (que visualizam as escalas).
* **📅 Escala Médica Interativa:** Calendário dinâmico para visualização de plantões diurnos e noturnos, organizados por mês e profissional.
* **📊 Geração de Relatórios (Exportação para Excel):** Funcionalidade que permite baixar uma planilha automatizada com o formulário do mês detalhando os plantões realizados por cada médico.
* **🌗 Modo Claro/Escuro:** Interface responsiva e com opção de personalização de tema para maior conforto visual.
* **⚙️ Gestão de Cadastros:** Módulo de administração de médicos (com CRM, contatos) e painel de controle de anúncios e trocas pendentes.

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python, Django
* **Front-end:** HTML5, CSS3, JavaScript
* **Banco de Dados:** SQLite (Padrão do Django) / [Altere caso esteja usando PostgreSQL, MySQL, etc.]
* **Outras Bibliotecas:** `openpyxl`.

## 📁 Estrutura do Projeto

A arquitetura do projeto foi dividida em "Apps" do Django para separar as responsabilidades:
* `agenda/` e `plantoes/`: Lógica central de alocação de horários e exibição do calendário.
* `user/` e `medicos/`: Gestão de perfis, autenticação e dados cadastrais dos profissionais.
* `anuncios/` e `deashboard/`: Lógica para comunicados internos e painel de indicadores.
