import { expect, test } from 'claude-code/testing'

const BAND = { plugin: 'team', component: 'AbovePrompt', props: { hasSurvey: false, isCollapsed: false, isWorking: false, maxRows: 4, bodyColumns: 80, scroll: { offset: 0, bodyRows: 4 }, view: {} } } as const
const GAIN = JSON.stringify({ summary: { total_saved: 8461762, avg_savings_pct: 26.65 } })

test('the band shows the caveman mode and rtk savings, and a click steps the mode', async ($, on) => {
  const ran: string[] = []
  on('env.get', () => ({ value: '/h' }))
  on('fs.read', () => ({ value: 'ultracave\n' }))
  on('process.run', () => ({ value: { exitCode: 0, stdout: GAIN, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }))
  on('command.run', (_, e) => {
    ran.push(`${e.command} ${e.args}`)
    return {}
  })
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ ...BAND, surface })
    expect((await ui.find({ type: 'Text', text: /rtk/ }))?.text).toBe('rtk 8.5M saved · 27%')
    await ui.unmount()
  }

  const ui = await $.ui.mount({ ...BAND, surface: 'desktop' })
  await ui.press({ key: 'mode' })
  expect(ran).toEqual(['caveman:caveman megacave'])
  await ui.unmount()
})

test('no rtk, no badge', async ($, on) => {
  on('env.get', () => ({ value: '/h' }))
  on('fs.read', () => ({ value: 'caveman' }))
  on('process.run', () => ({ value: { exitCode: 127, stdout: '', stderr: 'not found', isStdoutTruncated: false, isStderrTruncated: false } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  const ui = await $.ui.mount({ ...BAND, surface: 'desktop' })
  expect(await ui.find({ type: 'Text', text: /rtk/ })).toBe(undefined)
  await ui.unmount()
})
