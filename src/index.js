// Native DSH Cordis plugin for model allowlist management.
import { readFileSync } from 'node:fs'
export const name = 'dsh-model-manager'
export const description = 'Manage enabled model allowlists in DeepSeek Harness'
export const inject = ['settings', 'credentials']

function listModels(providers, providerFilter) {
  const rows = []
  for (const [provider, profile] of Object.entries(providers)) {
    if (providerFilter && provider !== providerFilter) continue
    if (!profile || typeof profile !== 'object') continue
    if (!Array.isArray(profile.models)) continue
    for (const model of profile.models) {
      if (model && typeof model === 'object' && model.id) {
        rows.push({ provider, id: model.id, name: model.name || '' })
      }
    }
  }
  return rows
}

export async function apply(ctx) {
  const args = ctx.get('cmdlineArgs')?.get() ?? []
  if ((args[0] === 'models' || args[0] === 'model-manager') && (args.includes('--version') || args.includes('-v'))) {
    const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'))
    console.log(pkg.version)
    const exit = ctx.get('appExit')
    if (exit) exit(0)
    return
  }
  if (args[0] !== 'models' && args[0] !== 'model-manager') return

  const appExit = ctx.get('appExit')
  const finish = (code) => { if (appExit) appExit(code) }

  try {
    const settings = ctx.get('settings')
    if (!settings) {
      console.error('dsh-model-manager requires settings service.')
      finish(1); return
    }

    const command = args[1]
    if (!command) {
      console.error('Usage: dsh --profile tools models <list|enable|disable|search> ...')
      finish(2); return
    }

    const current = settings.get('llm-pi-ai') ?? {}
    const providers = (current.providers && typeof current.providers === 'object') ? { ...current.providers } : {}

    if (command === 'list') {
      const filter = args.find((a, i) => a === '--provider' && args[i+1]) ? args[args.indexOf('--provider')+1] : undefined
      const rows = listModels(providers, filter)
      if (args.includes('--json')) {
        console.log(JSON.stringify(rows, null, 2))
      } else {
        for (const row of rows) {
          console.log(`${row.provider}/${row.id}${row.name ? ` (${row.name})` : ''}`)
        }
      }
      finish(0); return
    }

    if (command === 'search') {
      const q = (args[2] || '').toLowerCase()
      for (const row of listModels(providers)) {
        const hay = `${row.provider}/${row.id} ${row.name}`.toLowerCase()
        if (hay.includes(q)) console.log(`${row.provider}/${row.id}${row.name ? ` (${row.name})` : ''}`)
      }
      finish(0); return
    }

    if (command === 'enable' || command === 'disable') {
      const target = args[2]
      if (!target || !target.includes('/')) {
        console.error('expected provider/model')
        finish(2); return
      }
      const idx = target.indexOf('/')
      const provider = target.slice(0, idx)
      const modelId = target.slice(idx + 1)
      const profile = providers[provider] && typeof providers[provider] === 'object' ? providers[provider] : {}
      const models = Array.isArray(profile.models) ? profile.models : []

      if (command === 'enable') {
        if (models.some(m => m && typeof m === 'object' && m.id === modelId)) {
          console.log(`${provider}/${modelId} already enabled`)
          finish(0); return
        }
        const newModels = [...models, { id: modelId }]
        providers[provider] = { ...profile, models: newModels }
        await settings.update('llm-pi-ai', { providers })
        console.log(`enabled ${provider}/${modelId}`)
        finish(0); return
      }

      const next = models.filter(m => !(m && typeof m === 'object' && m.id === modelId))
      if (next.length === models.length) {
        console.log(`${provider}/${modelId} not enabled`)
        finish(0); return
      }
      providers[provider] = { ...profile, models: next }
      await settings.update('llm-pi-ai', { providers })
      console.log(`disabled ${provider}/${modelId}`)
      finish(0); return
    }

    console.error(`Unknown command: ${command}`)
    finish(2)
  } catch (error) {
    console.error('dsh-model-manager failed:', error)
    finish(1)
  }
}
