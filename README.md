# Projeto Base - Vita

<p align="center">
  <img src="https://github.com/yurivfernandes/projeto-base-vita/blob/main/frontend/src/assets/logo_login.svg" alt="Logo Vita" width="200"/>
</p>

## Sobre o Projeto
Projeto base desenvolvido para servir como template inicial para todas as aplicações Vita. Este template inclui as funcionalidades essenciais de autenticação e estrutura básica do frontend.

## Funcionalidades Base
- Sistema completo de autenticação
- Tela de login personalizada com logo Vita
- Welcome page
- Header com logo Vita e navegação básica
- Estrutura de rotas protegidas
- Perfil de usuário e alteração de senha

## Tecnologias Utilizadas

### Backend
- Django 4.2
- Django REST Framework
- JWT Authentication
- PostgreSQL
- Python Dotenv

### Frontend
- React 18
- TypeScript
- Vite
- React Router DOM
- Axios
- Styled Components

### Segurança e Utilitários
- Django CORS Headers
- DRF Swagger/OpenAPI
- Django REST Knox
- Django Filter

## Como Utilizar
1. Clone este repositório
2. Configure as variáveis de ambiente necessárias
3. Instale as dependências do backend e frontend
4. Inicie o servidor de desenvolvimento
5. Comece a desenvolver seu projeto a partir desta base

## Estrutura do Projeto
O projeto está organizado com uma clara separação entre backend e frontend, com todas as configurações necessárias para início imediato do desenvolvimento.

### Estrutura Principal do Frontend
```
frontend/
  ├── src/
  │   ├── assets/
  │   │   └── images/
  │   │       └── _login.svg
  │   ├── components/
  │   │   └── Header/
  │   ├── pages/
  │   │   ├── Login/
  │   │   └── Welcome/
  │   └── services/
  │       └── auth/
