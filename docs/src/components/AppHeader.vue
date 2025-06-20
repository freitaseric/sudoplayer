<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import routes from '../routes'

const router = useRouter()

const namedRoutes = computed(() => routes.filter((route) => route.name))

function goToBotInvite() {
  window.open(
    'https://discord.com/oauth2/authorize?client_id=1381308570389315654',
    '_blank',
    'width=500;height=800;'
  )
}
</script>

<template>
  <header>
    <div id="logo">
      <img src="/logo.png" alt="Sudo Player" />
      <span>SudoPlayer</span>
    </div>
    <div id="menu">
      <nav>
        <RouterLink
          v-for="route in namedRoutes"
          :key="route.name"
          :to="route.path"
          >{{ route.name }}</RouterLink
        >
      </nav>
      <span id="separator" />
      <div id="actions">
        <button @click="goToBotInvite">Adicione-me</button>
        <button @click="router.push('/sudoplayer/login')">Fazer Login</button>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0.2rem 3rem;
  margin-bottom: 8rem;
  background-color: var(--color-foreground);

  #logo {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.5s ease-in-out;

    &:hover {
      cursor: pointer;
      transform: scale(1.2);
    }

    img {
      height: 4rem;
    }

    span {
      background: linear-gradient(
        to right,
        var(--color-accent-primary),
        var(--color-accent-secondary)
      );
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      color: transparent;
      font-size: 2rem;
      font-weight: bold;
    }
  }

  #menu {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 2.5rem;

    nav {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      gap: 1rem;

      a {
        text-transform: uppercase;
        font-weight: 600;
        transition: all 0.5s ease-in-out;
        color: var(--color-text-muted);

        &:hover {
          opacity: 60%;
        }

        &.router-link-exact-active {
          color: var(--color-accent-secondary);
        }

        &.router-link-exact-active:hover {
          opacity: 100%;
          color: var(--color-accent-primary);
        }
      }
    }

    span#separator {
      height: 1.5rem;
      width: 2px;
      background-color: var(--color-text);
    }

    #actions {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      gap: 1rem;

      button {
        border: none;
        border-radius: 8px;
        color: var(--color-text);
        text-transform: uppercase;
        padding: 0.5rem 1rem;
        font-weight: 700;
        transition: transform 0.2s ease-in-out;

        &:nth-child(1) {
          border: 1px solid white;
          background-color: transparent;
        }
        &:nth-child(2) {
          background-color: var(--color-accent-primary);
        }

        &:hover {
          cursor: pointer;
          transform: scale(1.05);
        }
      }
    }
  }
}
</style>
