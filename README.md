[![CircleCI](https://circleci.com/gh/mrsbelo/message_scheduler/tree/master.svg?style=svg)](https://circleci.com/gh/mrsbelo/message_scheduler/tree/master)

# Agendador de Mensagens

## Projeto - Plataforma de comunicação
---

Objetivo: criar um serviço de agendamento de mensagens. Inicialmente o serviço irá permitir agendar mensagens de email, sms, push e whatsapp.

---

### Database Schema

Esquema pensado para iniciar o projeto contém duas tabelas: Message e User. 

**User** 
- **email**: para as mensagens dos tipos email e push
- **phone**: para as mensagens dos tipos sms e whatsapp

**Message** 

- **created**: gerado automaticamente, registra o momento da criação do agendamento
- **scheduled**: data e horário do agendamento para que a mensagem seja enviada
- **message**: a mensagem a ser enviada ao user
- **kind**: plataforma de envio da mensagem: 0 para email, 1 para sms, 2 para push e 3 para whatsapp
- **status**: registra se o envio já foi efetuado: 0 para agendada e 1 para enviada
- **user_id**: chave estrangeira do alvo da mensagem

![](docs/db_schema.png)


 ## Ferramentas utilizadas

 - [DB Designer](https://www.dbdesigner.net/) - utilizado no design do database schema