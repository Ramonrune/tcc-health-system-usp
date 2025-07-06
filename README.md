# Sistema de Apoio à Decisão para Diagnóstico na Atenção Primária à Saúde

Este projeto tem como objetivo o desenvolvimento de um sistema para apoiar médicos da Atenção Primária à Saúde (APS) no processo de diagnóstico, reduzindo a ocorrência de erros e melhorando a qualidade dos atendimentos.

## 🩺 Contexto

Erros de diagnóstico são uma das principais causas de danos a pacientes, afetando de 5% a 20% dos atendimentos médicos. Na APS, esse cenário é agravado por fatores como:

- Sobrecarga de trabalho e tempo limitado;
- Falta de conhecimento especializado;
- Registros clínicos desorganizados;
- Dificuldade de acesso a especialistas.

## 🎯 Objetivos

### Objetivo Geral
Desenvolver um sistema de apoio à decisão clínica para médicos da APS.

### Objetivos Específicos
- Criar uma interface gráfica com boa usabilidade e baixo custo cognitivo;
- Utilizar serviços de NLP em nuvem para extrair dados de históricos clínicos;
- Utilizar metodologia SCRUM no desenvolvimento;
- Garantir escalabilidade e segurança com AWS.

## ⚙️ Tecnologias Utilizadas

- **Frontend**: Quasar Framework, Vue.js  
- **Backend**: Python (FastAPI), REST APIs protegidas
- **Infraestrutura**: Amazon Web Services (AWS)
- **NLP**: Serviços de linguagem natural da Azure
- **Metodologia**: SCRUM com sprints iterativas

## 🖥️ Funcionalidades

- **Gestão de Identidade**: Login, criação e ativação de contas
- **Módulo Médico**: Gestão de atendimentos e pacientes
- **Módulo Paciente**: Histórico, exames, medicamentos e doenças
- **Resumo Inteligente**: Análise automática com dados-chave e grau de confiança

## 🔐 Segurança

- APIs protegidas com autenticação
- Redirecionamento para login em tentativas de acesso não autenticadas
- Código HTTP 401 para acessos não autorizados

## 📊 Desempenho

- Tempo médio de resposta das APIs: **101ms**
- Erros durante testes de carga: **0%**
- Lighthouse Score da aplicação: **97/100**

## 🧪 Avaliação

O sistema foi avaliado por 12 médicos da APS com experiência prática. Todos consideraram:

- Interface clara e objetiva
- Útil para a prática clínica diária
- Potencial para reduzir a sobrecarga cognitiva

### Sugestões Futuras:
- Gráficos de evolução clínica
- Alertas de exames atrasados
- Mecanismos de busca inteligente

## 📌 Conclusão

A aplicação demonstrou alto potencial para apoiar decisões clínicas na APS, sendo bem avaliada em critérios de:

- Clareza
- Simplicidade
- Completude
- Utilidade
- Desempenho
