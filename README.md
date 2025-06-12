# SudoPlayer

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/freitaseric/sudoplayer/deploy.yml?label=deploy)
![GitHub License](https://img.shields.io/github/license/freitaseric/sudoplayer)
![Static Badge](https://img.shields.io/badge/version-v1.0--SNAPSHOT-0d1117?labelColor=306593)

## 📖 Sobre o Projeto

**SudoPlayer** é um bot para discord perfeito para gamers de Linux. Com ele você terá alertas sobre os melhores jogos do
mundo e com suporte para o sistema operacional, com o ou sem a necessidade do Proton, além de ajuda para configurar e
arrumar ocasionais erros em sua gameplay.

Para mais informações verifique a [#tabela de funcionalidades](#-funcionalidades)

## 📃 Sumário

<!-- TOC -->
* [SudoPlayer](#sudoplayer)
  * [📖 Sobre o Projeto](#-sobre-o-projeto)
  * [📃 Sumário](#-sumário)
  * [✨ Funcionalidades](#-funcionalidades)
  * [🚀 Como adicionar o SudoPlayer](#-como-adicionar-o-sudoplayer)
  * [🤖 Principais comandos](#-principais-comandos)
  * [🤝 Como Contribuir](#-como-contribuir)
  * [📜 Licença](#-licença)
<!-- TOC -->

## ✨ Funcionalidades

| Nome                | Descrição                                                                                                                               | Status |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------|--------|
| Busca estática      | Busca e exibe informações detalhadas sobre um jogo, incluindo dados da Steam e um resumo do status e dicas do ProtonDB.                 | 👷     |
| Notificador Diário  | Uma tarefa agendada que envia, em um canal específico, as informações dos jogos com maior avaliação no ProtonDB.                        | ⚪      |
| Alertas de ProtonDB | Monitora o ProtonDB e envia alertas automáticos em um canal quando um jogo importante muda de classificação (ex: de Ouro para Platina). | ⚪      |

* ✅ -> `Concluído`
* 👷 -> `Em progresso`
* 🚧 -> `Cancelado`
* ⚪ -> `Não iniciado`

## 🚀 Como adicionar o SudoPlayer

É fácil ter o **SudoPlayer** em seu servidor ou lista de aplicativos de usuário:

**[>> Clique aqui para instalar o bot <<](https://discord.com/oauth2/authorize?client_id=1381308570389315654)**

## 🤖 Principais comandos

* `/ajuda` - Exibe todos os comandos disponíveis.

## 🛠️ Auto-Hospedagem (Self-Hosting)

### Pré-requisitos

1. Java Development Kit (JDK): Versão 17 ou superior. (recomendado: JDK 17 Temurin)
2. Gradle: Versão 8.13 ou superior.

### Instalação e Compilação

#### 1. Clone o repositório
```shell
# Utilize este comando caso tenha o Git instalado em sua máquina.
git clone https://github.com/freitaseric/sudoplayer.git --depth=1 --branch=main # ou baixe o zip no site
cd sudoplayer
```

#### 2. Compile o projeto
```shell
# Se estiver no Linux ou macOS
./gradlew shadowJar

# Se estiver no Windows
.\gradlew.bat shadowJar
```

O arquivo jar executável estará em `build/libs/SudoPlayer-1.0-SNAPSHOT-all.jar`

#### 3. Configuração do ambiente

```dotenv
BOT_TOKEN="o token do seu bot"
```

#### 4. Execução
```shell
java -Xms128M -Xmx1G -jar ./build/libs/SudoPlayer-1.0-SNAPSHOT-all.jar
```

> [!TIP]
> Se estiver num servidor, você pode querer deixar o bot rodando como um serviço.
> Siga este passo a passo caso esteja a rodar um servidor linux, neste caso mostrarei como fazer com o Ubuntu Server 24.04 LTS:
> ```shell
> SUDOPLAYER_HOME="/opt/sudoplayer"
> SUDOPLAYER_JAR_PATH="build/libs/SudoPlayer-1.0-SNAPSHOT-all.jar"
> 
> sudo tee /etc/systemd/system/sudo-player.service > /dev/null <<EOL
> [Unit]
> Description=Meu SudoPlayer bot personalizado
> After=network.target
>
> [Service]
> Type=simple
> WorkingDirectory=${SUDOPLAYER_HOME}
> ExecStart=java -Xms128M -Xmx1G -jar ${SUDOPLAYER_HOME}/${SUDOPLAYER_JAR_PATH}
> Restart=on-failure
> RestartSec=5s
> 
> [Install]
> WantedBy=multi-user.target
> EOL
> ```
> Após isso um serviço chamado `sudo-player.service` estará disponível para você iniciar via systemd.
> ```shell
> sudo systemctl enable --now sudo-player.service
> ```

## 🤝 Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer
contribuição que você fizer será **muito apreciada**.

Por favor, leia o nosso [CONTRIBUTING.md](./CONTRIBUTING.md) para detalhes sobre o nosso código de conduta e o processo para submeter pull
requests.

## 📜 Licença

Distribuído sob a Licença MIT. Veja [LICENSE](./LICENSE) para mais informações.
