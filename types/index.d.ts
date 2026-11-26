export type Rtk = { saved: number; pct: number }

declare module 'claude-code' {
  interface PluginState {
    team: { mode: string; rtk: Rtk | null }
  }
}
