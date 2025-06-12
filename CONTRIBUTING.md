# Contribuindo para SudoPlayer Bot

Neste arquivo encontra-se o passo a passo de como contribuir com este projeto de código aberto de todas as maneiras
disponíveis para o mesmo.

Siga os passos descritos aqui e lembre-se e manter uma conduta adequada para com a suas contribuições visando o melhor
para a comunidade e projeto.

## Sumário

<!-- TOC -->

* [Contribuindo para SudoPlayer Bot](#contribuindo-para-sudoplayer-bot)
    * [Sumário](#sumário)

<!-- TOC -->

## Faça sugestões

Caso tenha uma ideia de melhoria, funcionalidade, dentre outros e queria compartilhar com nosco, saiba que exite uma
maneira muito simples de fazer isso.

Para enviar uma sugestão, basta [clicar neste link](https://discord.gg/vjTq9hNhjq) e entrar na comunidade oficial do bot
no discord.
Uma vez nela, você poderá acessar o canal `#sugestões` e postar suas ideias incríveis no nosso fórum.

## Faça contribuições de código

### Pré-requisitos

1. Java Development Kit (JDK): Versão 17 ou superior. (recomendado: JDK 17 Temurin)
2. Gradle: Versão 8.13 ou superior.
3. Um editor de código ou IDE. Recomendamos o uso do `IntelliJ IDEA` ou `Visual Studio Code`

### Instalação e Compilação

#### 1. Clone o repositório

```shell
# Utilize este comando caso tenha o Git instalado em sua máquina.
git clone https://github.com/freitaseric/sudoplayer.git --depth=1 --branch=main # ou baixe o zip no site
cd sudoplayer
```

#### 2. Baixe as dependências

> [!WARNING]
> Pule este passo caso esteja numa IDE como `IntelliJ IDEA`!

```shell
# Se estiver no Linux ou macOS
./gradlew build

# Se estiver no Windows
.\gradlew.bat build
```

#### 3. Configuração do ambiente

```dotenv
BOT_TOKEN="o token do seu bot"
```

#### 4. Sua primeira contribuição de código

Acesse a pasta `src/main/java/io/github/freitaseric/sudoplayer` e começe a criar seus códigos nos arquivos contidos
nela.

#### 5. Enviando sua contribuição

Crie seu fork do repositório, faça um push do seu projeto local para o mesmo e por fim abra um pull request para o
repositório original.

Após disso basta aguardar a análise do seu código e possível aprovação.