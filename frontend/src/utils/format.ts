export function formatEUR(value: number): string {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(value)
}

export function formatHeures(value: number): string {
  return `${new Intl.NumberFormat('fr-FR').format(value)} h`
}


