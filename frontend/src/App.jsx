import { useState, useCallback, useRef } from 'react'

const API = '/api'

/* ── SVG Icons ── */
const Icons = {
  Logo: () => (
    <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none">
      <rect width="32" height="32" rx="8" fill="#22C55E" fillOpacity="0.15"/>
      <path d="M16 4c-1 0-2 .5-3 1.5L7 12c-1.5 2-1 4.5 1 5.5l2 .5v5c0 1.5 1.5 3 3 3h6c1.5 0 3-1.5 3-3v-5l2-.5c2-1 2.5-3.5 1-5.5l-6-6.5C18 4.5 17 4 16 4z" stroke="#22C55E" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M16 22c1.5 0 3-1 3-2.5s-1.5-2.5-3-2.5-3 1-3 2.5 1.5 2.5 3 2.5z" stroke="#22C55E" strokeWidth="1.5"/>
    </svg>
  ),
  Upload: () => (
    <svg className="w-10 h-10" viewBox="0 0 24 24" fill="none" stroke="#22C55E" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
    </svg>
  ),
  Image: () => (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>
    </svg>
  ),
  Check: () => (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><path d="M22 4L12 14.01l-3-3"/></svg>
  ),
  AlertTriangle: () => (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
  ),
  Leaf: () => (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M17 8c-3-2-7-1-10 3-3 4-2.5 9 .5 11 3 2 7 1 10-3 2-3 2-7-.5-11z"/><path d="M14 4c2-1.5 6-.5 8 2s2 6 .5 8"/></svg>
  ),
  Bug: () => (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M8 2l1.88 1.88M16 2l-1.88 1.88M3 8h18M5 12h14M6 16h12"/><circle cx="12" cy="12" r="2"/><path d="M20 8v6a8 8 0 01-16 0V8"/></svg>
  ),
  BarChart: () => (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
  ),
  Download: () => (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
  ),
  Folder: () => (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>
  ),
  Clock: () => (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
  ),
  Spinner: () => (
    <svg className="w-8 h-8 animate-spin" viewBox="0 0 24 24" fill="none">
      <circle className="opacity-20" cx="12" cy="12" r="10" stroke="#22C55E" strokeWidth="3"/>
      <path className="opacity-80" fill="#22C55E" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
  ),
}

export default function App() {
  const [image, setImage] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const [batchLoading, setBatchLoading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const fileRef = useRef(null)

  const handleFile = useCallback(async (file) => {
    setImage(URL.createObjectURL(file))
    setResult(null)
    setLoading(true)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${API}/predict`, { method: 'POST', body: form })
      const data = await res.json()
      setResult(data)
      setHistory(prev => [data, ...prev].slice(0, 50))
    } catch { setResult({ error: '推理失败，请检查后端服务是否已启动' }) }
    finally { setLoading(false) }
  }, [])

  const handleBatch = useCallback(async () => {
    const input = document.createElement('input')
    input.type = 'file'; input.accept = 'image/*'; input.multiple = true
    input.style.display = 'none'
    document.body.appendChild(input)
    input.onchange = async (e) => {
      const files = [...e.target.files]
      document.body.removeChild(input)
      if (!files.length) return
      setBatchLoading(true)
      const form = new FormData()
      files.forEach(f => form.append('files', f))
      try {
        const res = await fetch(`${API}/batch`, { method: 'POST', body: form })
        const data = await res.json()
        setHistory(prev => [...data.results, ...prev].slice(0, 100))
      } catch { alert('批量推理失败') }
      finally { setBatchLoading(false) }
    }
    input.click()
  }, [])

  const handleExport = useCallback(async () => {
    const res = await fetch(`${API}/export`)
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `results_${new Date().toISOString().slice(0, 10)}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault(); setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f?.type.startsWith('image/')) handleFile(f)
  }, [handleFile])

  const healthyCount = history.filter(h => h.disease === '健康').length
  const diseasedCount = history.filter(h => h.disease && h.disease !== '健康').length

  return (
    <div className="min-h-screen bg-bg">
      {/* ── Header ── */}
      <header className="border-b border-gray-800 bg-primary/80 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Icons.Logo />
            <div>
              <h1 className="text-lg font-semibold text-text tracking-tight" style={{ fontFamily: 'var(--font-heading)' }}>CropGuard</h1>
              <p className="text-xs text-text-muted -mt-0.5">农作物病害检测分析平台</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={handleBatch} disabled={batchLoading}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-text-secondary bg-surface border border-gray-700 rounded-lg hover:bg-surface-hover hover:text-text hover:border-gray-600 transition-all duration-200 disabled:opacity-40">
              {batchLoading ? <Icons.Spinner /> : <Icons.Folder />}
              <span className="hidden sm:inline">批量导入</span>
            </button>
            {history.length > 0 && (
              <button onClick={handleExport}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-accent bg-accent-bg border border-accent-border rounded-lg hover:bg-accent hover:text-black transition-all duration-200">
                <Icons.Download />
                <span className="hidden sm:inline">导出 CSV</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* ── Main Content ── */}
      <main className="max-w-7xl mx-auto px-6 py-6">
        {/* Stats Row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard icon={<Icons.BarChart />} label="累计检测" value={history.length} unit="次" accent="blue" />
          <StatCard icon={<Icons.Check />} label="健康样本" value={healthyCount} unit="张" accent="green" />
          <StatCard icon={<Icons.AlertTriangle />} label="病害样本" value={diseasedCount} unit="张" accent="red" />
          <StatCard icon={<Icons.Leaf />} label="病害种类" value="17" unit="种" accent="green" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* ── Left: Upload + Result (2 cols) ── */}
          <div className="lg:col-span-2 space-y-6">
            {/* Upload Zone */}
            <div
              onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileRef.current?.click()}
              className={`group relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 ${
                dragOver
                  ? 'border-accent bg-accent-bg scale-[1.005] shadow-lg shadow-accent/10'
                  : 'border-gray-700 bg-surface/50 hover:border-gray-500 hover:bg-surface'
              } ${image && !loading ? 'p-4' : ''}`}
            >
              <input ref={fileRef} type="file" accept="image/*" className="hidden"
                onChange={e => e.target.files[0] && handleFile(e.target.files[0])} />
              {image ? (
                <img src={image} alt="Preview" className="max-h-[400px] mx-auto rounded-xl shadow-2xl" />
              ) : (
                <div className="space-y-4">
                  <div className="w-16 h-16 mx-auto rounded-2xl bg-accent-bg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Icons.Upload />
                  </div>
                  <div>
                    <p className="text-lg font-medium text-text" style={{ fontFamily: 'var(--font-heading)' }}>
                      拖拽图片到此处或 <span className="text-accent">点击上传</span>
                    </p>
                    <p className="text-sm text-text-muted mt-2">支持 JPG / PNG 格式农作物叶片图片，两阶段级联推理</p>
                  </div>
                </div>
              )}
            </div>

            {/* Loading State */}
            {loading && (
              <div className="bg-surface border border-gray-700 rounded-2xl p-8 flex items-center gap-5 animate-pulse">
                <Icons.Spinner />
                <div>
                  <p className="font-medium text-text" style={{ fontFamily: 'var(--font-heading)' }}>正在分析叶片图像...</p>
                  <p className="text-sm text-text-muted mt-1">Stage 1 作物识别 → Stage 2 病害分类</p>
                </div>
              </div>
            )}

            {/* Result */}
            {result && !loading && (
              <div className="bg-surface border border-gray-700 rounded-2xl overflow-hidden">
                {result.error ? (
                  <div className="p-6 flex items-center gap-3 text-danger bg-danger-bg">
                    <Icons.AlertTriangle /><span className="text-sm">{result.error}</span>
                  </div>
                ) : (
                  <div>
                    {/* Result Header */}
                    <div className="px-6 py-4 border-b border-gray-700 flex items-center justify-between">
                      <h2 className="font-semibold text-text flex items-center gap-2" style={{ fontFamily: 'var(--font-heading)' }}>
                        <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                        检测结果
                      </h2>
                      <span className="text-xs text-text-muted font-mono">{result.file}</span>
                    </div>
                    {/* Result Body */}
                    <div className="p-6 grid grid-cols-2 gap-4">
                      {/* Crop */}
                      <div className="bg-bg rounded-xl p-5 border border-gray-800">
                        <div className="flex items-center gap-2 text-text-muted text-xs uppercase tracking-wider mb-3">
                          <Icons.Leaf /> Stage 1 · 作物类型
                        </div>
                        <p className="text-2xl font-semibold text-text mb-3" style={{ fontFamily: 'var(--font-heading)' }}>{result.crop}</p>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
                            <div className="h-full bg-gradient-to-r from-accent to-accent-light rounded-full transition-all duration-700"
                              style={{ width: `${(result.crop_conf * 100).toFixed(0)}%` }} />
                          </div>
                          <span className="text-sm font-mono text-accent font-medium">{(result.crop_conf * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      {/* Disease */}
                      <div className={`rounded-xl p-5 border ${result.disease === '健康' ? 'bg-accent/5 border-accent-border' : 'bg-danger/5 border-danger-border'}`}>
                        <div className="flex items-center gap-2 text-xs uppercase tracking-wider mb-3"
                          style={{ color: result.disease === '健康' ? '#4ADE80' : '#F87171' }}>
                          <Icons.Bug /> Stage 2 · 病害类型
                        </div>
                        <p className="text-2xl font-semibold mb-3" style={{
                          fontFamily: 'var(--font-heading)',
                          color: result.disease === '健康' ? '#4ADE80' : '#F87171',
                        }}>{result.disease}</p>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
                            <div className="h-full rounded-full transition-all duration-700"
                              style={{
                                width: `${(result.disease_conf * 100).toFixed(0)}%`,
                                background: result.disease === '健康'
                                  ? 'linear-gradient(90deg, #22C55E, #4ADE80)'
                                  : 'linear-gradient(90deg, #F87171, #EF4444)',
                              }} />
                          </div>
                          <span className="text-sm font-mono font-medium"
                            style={{ color: result.disease === '健康' ? '#4ADE80' : '#F87171' }}>
                            {(result.disease_conf * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* ── Right: History Panel (1 col) ── */}
          <div className="bg-surface border border-gray-700 rounded-2xl flex flex-col h-fit lg:sticky lg:top-24 max-h-[calc(100vh-120px)]">
            <div className="px-5 py-4 border-b border-gray-700 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Icons.Clock />
                <h2 className="font-semibold text-text text-sm" style={{ fontFamily: 'var(--font-heading)' }}>检测记录</h2>
              </div>
              <span className="text-xs text-text-muted bg-bg px-2 py-0.5 rounded-full font-mono">{history.length}</span>
            </div>
            {history.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center py-16 px-4">
                <div className="w-16 h-16 rounded-2xl bg-bg flex items-center justify-center mb-4">
                  <Icons.Image />
                </div>
                <p className="text-sm text-text-muted text-center">暂无检测记录</p>
                <p className="text-xs text-text-muted/60 mt-1 text-center">上传农作物叶片图片即可开始检测</p>
              </div>
            ) : (
              <div className="flex-1 overflow-y-auto divide-y divide-gray-800">
                {history.map((item, i) => {
                  const isHealthy = item.disease === '健康'
                  return (
                    <div key={i}
                      onClick={() => { setResult(item); setImage(null) }}
                      className="flex items-center gap-3 px-5 py-3 hover:bg-surface-hover cursor-pointer transition-colors group"
                    >
                      {/* Status dot */}
                      <div className="relative flex-shrink-0">
                        <div className={`w-2.5 h-2.5 rounded-full ${isHealthy ? 'bg-accent' : 'bg-danger'}`} />
                        {isHealthy && <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-accent animate-ping opacity-30" />}
                      </div>
                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-text truncate font-medium">{item.file}</p>
                        <p className="text-xs text-text-muted mt-0.5">
                          <span>{item.crop}</span>
                          <span className="mx-1.5 text-gray-700">·</span>
                          <span className={isHealthy ? 'text-accent' : 'text-danger'}>{item.disease}</span>
                        </p>
                      </div>
                      {/* Confidence + Time */}
                      <div className="text-right flex-shrink-0">
                        <p className={`text-xs font-mono font-medium ${isHealthy ? 'text-accent' : 'text-danger'}`}>
                          {item.crop_conf != null ? `${(item.crop_conf * 100).toFixed(0)}%` : ''}
                        </p>
                        <p className="text-xs text-text-muted/50 mt-0.5">{item.time?.slice(11, 16) || ''}</p>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

function StatCard({ icon, label, value, unit, accent }) {
  const colors = {
    green: { bg: 'bg-accent/10', text: 'text-accent', glow: 'shadow-accent/10' },
    red: { bg: 'bg-danger/10', text: 'text-danger', glow: 'shadow-danger/10' },
    blue: { bg: 'bg-blue-500/10', text: 'text-blue-400', glow: 'shadow-blue-500/10' },
  }
  const c = colors[accent] || colors.blue
  return (
    <div className={`bg-surface border border-gray-700 rounded-xl p-4 hover:border-gray-600 transition-all duration-200 ${c.glow}`}>
      <div className="flex items-center justify-between mb-3">
        <span className={`w-8 h-8 rounded-lg ${c.bg} flex items-center justify-center ${c.text}`}>{icon}</span>
      </div>
      <div className="flex items-baseline gap-1.5">
        <span className="text-2xl font-semibold text-text font-mono">{value}</span>
        <span className="text-sm text-text-muted">{unit}</span>
      </div>
      <p className="text-xs text-text-muted mt-1">{label}</p>
    </div>
  )
}
