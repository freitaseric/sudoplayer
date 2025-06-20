import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import eslint from "vite-plugin-eslint";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    eslint(),
    vue(),
    VitePWA({
      manifest: {
        name: "SudoPlayer",
        short_name: "SudoPlayer | Discord Bot",
        icons: [
          {
            src: "/android-chrome-192x192.png",
            sizes: "192x192",
            type: "image/png",
          },
          {
            src: "/android-chrome-512x512.png",
            sizes: "512x512",
            type: "image/png",
          },
        ],
        theme_color: "#42b883",
        background_color: "#ffffff",
        display: "standalone",
      },
    }),
  ],
  base: "/sudoplayer/",
});
