# Health Establishments Finder API


Este é o repositório do **backend** de um sistema de busca de estabelecimentos de saúde, desenvolvido utilizando **FastAPI** e **Prisma** para acesso ao banco de dados **PostgreSQL**. O sistema visa facilitar a busca por estabelecimentos de saúde, utilizando dados da API pública do governo federal (CNES) e futuramente integrando dados adicionais através de técnicas de **web scraping** em sites privados de saúde confiáveis.

## Funcionalidades

- **Busca por estabelecimentos de saúde**: Baseando-se na API pública do governo (CNES).
- **Integração com PostgreSQL**: Gerenciamento eficiente de dados utilizando Prisma como ORM.
- **Futuras implementações**: Cadastro de dados adicionais de fontes privadas confiáveis por meio de scraping, agregando mais informações aos usuários.

## Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno, rápido e eficiente.
- **[Prisma](https://www.prisma.io/)**: ORM para trabalhar com o banco de dados PostgreSQL de forma simplificada e eficiente.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar os dados dos estabelecimentos de saúde.
- **Web Scraping**: Ferramentas futuras para integrar dados além da API pública.

## Estrutura do Projeto

A estrutura do projeto, os passos detalhados para instalação e a documentação completa serão disponibilizados ao término do desenvolvimento.

## Contribuições

Este projeto será **open source**, e qualquer contribuição será bem-vinda. Se você tiver sugestões, encontrar problemas ou desejar colaborar com o desenvolvimento, sinta-se à vontade para abrir uma *issue* ou submeter um *pull request*.

## Frontend

O backend deste projeto será integrado com um frontend dedicado. Para mais detalhes, acesse o repositório do frontend [aqui](https://github.com/gabrielsldz/front)

## Roadmap
- [x] Crud inicial todo implementado e esboço do projeto iniciado
- [x] Scrapping de todos os dados disponíveis na API aberta do governo brasileiro.
- [ ] Implementação de scraping de dados em sites privados confiáveis.
- [ ] Integração com outros serviços de saúde para oferecer informações mais detalhadas.
- [ ] Melhorias no desempenho e na segurança.

