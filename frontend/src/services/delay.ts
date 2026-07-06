/** Simule la latence réseau (<1s comme demandé) pour les services mockés. */
export const delay = (ms = 250 + Math.random() * 400) =>
  new Promise<void>((resolve) => setTimeout(resolve, ms))


