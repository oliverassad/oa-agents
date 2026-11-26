import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Rtk } from '../../types'

// caveman's own selectable modes (caveman-config.js VALID_MODES, minus the one-shot ones).
const MODES = ['off', 'caveman', 'ultracave', 'megacave']

const mode = atom({ plugin: 'team', key: 'mode' } as const, 'off')
const rtk = atom({ plugin: 'team', key: 'rtk' } as const, null)

const claudeDir = async ($: EngineInterface) =>
  (await $.env.get('CLAUDE_CONFIG_DIR')) ?? `${(await $.env.get('HOME')) ?? (await $.env.get('USERPROFILE'))}/.claude`

// caveman writes its mode here; no file means off.
async function readMode($: EngineInterface): Promise<string> {
  const text = await $.fs.read(`${await claudeDir($)}/.caveman-active`).catch(() => '')
  const m = text.trim()
  return MODES.includes(m) ? m : 'off'
}

// rtk's own totals; null when rtk is missing or its output changes shape.
async function readRtk($: EngineInterface): Promise<Rtk | null> {
  const ran = await $.process.run(['rtk', 'gain', '-f', 'json']).catch(() => undefined)
  if (ran?.exitCode !== 0) return null
  try {
    const s = JSON.parse(ran.stdout).summary
    return typeof s?.total_saved === 'number' ? { saved: s.total_saved, pct: s.avg_savings_pct ?? 0 } : null
  } catch {
    return null
  }
}

export const fmt = (n: number) =>
  n >= 1e9 ? `${(n / 1e9).toFixed(1)}B` : n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : `${n}`

const refresh = async ($: EngineInterface) => {
  const [m, r] = await Promise.all([readMode($), readRtk($)])
  await update($, mode, () => m)
  await update($, rtk, () => r)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await refresh($)
    return next(e)
  }).catch(($, e, next) => next(e))

  // caveman's tracker changes the flag on a prompt; rtk counts every command of the turn.
  on('turn.complete', async ($, e, next) => {
    if (e.agentId === undefined) await refresh($)
    return next(e)
  }).catch(($, e, next) => next(e))

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    // Other bands (ponytail) share the slot: keep theirs, draw ours below.
    const above = await next(e).catch(() => undefined)
    if (e.props.hasSurvey) return above ?? next(e)

    const m = await read($, mode)
    const r = await read($, rtk)
    const { Box, Text, Button } = $.ui.resolve(e)
    // One click steps to the next mode; caveman's own command does the switch, so its tracker stays the only logic.
    const step = async () => {
      const to = MODES[(MODES.indexOf(m) + 1) % MODES.length]
      await update($, mode, () => to)
      await $.command.run({ command: 'caveman:caveman', args: to })
    }

    const row = (
      <Box flexDirection="row" alignItems="center" gap={2}>
        <Button key="mode" plain onPress={step}>
          <Text color={m === 'off' ? 'inactive' : 'suggestion'}>●</Text> {m}
        </Button>
        {r !== null && (
          <Text dimColor>
            rtk {fmt(r.saved)} saved · {Math.round(r.pct)}%
          </Text>
        )}
      </Box>
    )
    return above ? <Box flexDirection="column">{above}{row}</Box> : row
  }).catch(($, e, next) => next(e))
}
