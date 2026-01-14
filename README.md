# 🚗 Sistema de Gerenciamento de Estacionamento
API REST desenvolvida com FastAPI para gerenciamento completo de estacionamento, incluindo cadastro de veículos, controle de vagas e sistema de cobrança automatizado.

# 📋 Sobre o Projeto

## Sistema backend para controle de estacionamento que permite:

* Cadastro de veículos (carros e motos)
* Gerenciamento de vagas por tipo de veículo
* Registro automático de entrada e saída
* Cálculo de permanência e cobrança
* Consulta de status em tempo real

  
## 🧠 Tecnologias Utilizadas

* [FastAPI](https://fastapi.tiangolo.com/) — Framework web moderno e rápido

* [SQLAlchemy](https://www.sqlalchemy.org/) — para trabalhar com banco de dados

* [Pydantic](https://docs.pydantic.dev/latest/) - Validação de dados e schemas

* SQLite - Banco de dados (desenvolvimento)


## 📦 Funcionalidades
### Gestão de Veículos

* Cadastro de veículos com validação de placa única
* Diferenciação entre carros e motos
* Armazenamento de dados de contato

### Controle de Vagas

* Gerenciamento de vagas por tipo (carro/moto)
* Ocupação e liberação automática de vagas
* Verificação de disponibilidade em tempo real

### Sistema de Cobrança

* Registro automático de horário de entrada
* Cálculo de permanência em horas
* Cobrança baseada no tempo e tipo de vaga
* Controle de pagamentos

## 🗃️ Estrutura do Banco de Dados
### Tabela: vehicles

* id - Identificador único
* plate - Placa do veículo (única)
* type - Tipo (carro/moto)
* phone_number - Telefone de contato
* email - Email de contato

### Tabela: parking_spots

* id - Identificador único
* type - Tipo da vaga (carro/moto)
* price - Valor por hora
* is_occupied - Status de ocupação
* vehicle_id - Veículo ocupando a vaga

### Tabela: parking_records

* id - Identificador único
* parking_spot_id - Vaga utilizada
* vehicle_id - Veículo estacionado
* entry_time - Horário de entrada
* exit_time - Horário de saída
* price - Valor total cobrado
* paid - Status de pagamento

## 🔐 Autenticação
### O sistema utiliza JWT (JSON Web Tokens) para autenticação. Para acessar endpoints protegidos:

Faça login para obter o token
Inclua o token no header: Authorization: Bearer {seu_token}


## 📌 Contribuições

Contribuições são bem-vindas!
Sinta-se à vontade para enviar issues, melhorar rotas ou adicionar novos recursos.


[Linkedin](https://www.linkedin.com/in/guilherme-v-848a1013a/)
