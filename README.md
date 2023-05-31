# Elementum Rajada

Uma rajada de provedores.

---

### Funcionalidade

- Rápido
- Provedores brasileiros e estrangeiros
- Fácil configuração de provedores e filtros
- Compatível com Elementum
- Utilizável em outros addons através do [menu de contexto](https://github.com/addon-rajada/context.elementum) do Elementum

---

### Instalação

**Importante: Caso já tenha alguma versão do Rajada instalada, recomendado desinstalar a mesma e reiniciar o Kodi antes de prosseguir**

Adicionar o repositório https://addon-rajada.github.io e instalar o addon.

Mais detalhes [aqui](https://github.com/addon-rajada/addon-rajada.github.io).

---

### Compatibilidade

Abaixo os casos de teste realizados pelo desenvolvedor. Outras versões necessário o usuário verificar por si.

| **Kodi** | **Elementum** | **Status Repo** | **Status Rajada** |
|-|-|-|-|
| 17.3 | 0.1.87 x86 | ? | ? |
| 18.6 | 0.1.87 x86 | Ok | Ok |
| 18.9 | 0.1.87 arm | Ok | Ok |
| 19.5 | 0.1.87 arm | Ok | Ok |
| 20.1 | 0.1.87 x86 | Ok | Ok |
| 21.0 ALPHA 1 | 0.1.87 x86 | Fail | Fail |

---

### Documentação

- [Guia para adição de provedores](https://elementumorg.github.io/burst/create/)
- [Documentação do Burst](https://readthedocs.org/projects/scriptelementumburst/downloads/pdf/latest/)

---

### Changelog

**0.2**

- adicionado provedores
- obtendo nome e hash a partir do link magnético
- melhorado filtro de termos bloqueados para evitar carregamento inútil da subpage
- adicionado filtro de similaridade de strings
- tamanho do addon reduzido

**0.1**

- provedores brasileiros
- parsing de todos os links magnéticos da subpage

---

### Créditos

- @scakemyer pelo módulo inicial do Quasar Burst
- @mancuniancol por seu trabalho no Magnetic
- @elgatito pelo módulo [Elementum Burst](https://github.com/elgatito/script.elementum.burst)
