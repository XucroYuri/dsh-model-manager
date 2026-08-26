// Minimal DSH Cordis command wrapper around the Python CLI.
import { spawnSync } from 'node:child_process'

export const name = 'dsh-model-manager'
export const description = 'Manage enabled model allowlists in DeepSeek Harness'

export function apply(ctx) {
  const args = ctx.get('cmdlineArgs')?.get() ?? []
  if (args[0] !== 'models' && args[0] !== 'model-manager') return

  const result = spawnSync('dsh-model-manager', args.slice(1), {
    stdio: 'inherit',
    shell: false,
  })

  const exit = ctx.get('appExit')
  if (exit) exit(result.status ?? 1)
}
