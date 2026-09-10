import { FormEvent, useState } from 'react'
import axios from 'axios'
import { ArrowRight, Building2, Loader2, Lock, Mail, UserRound } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { api } from '@/lib/api'

type Mode = 'login' | 'signup'

export default function Login() {
  const [mode, setMode] = useState<Mode>('login')
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('admin@buildsure.ai')
  const [password, setPassword] = useState('password')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const isSignup = mode === 'signup'

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const endpoint = isSignup ? '/auth/register' : '/auth/login'
      const payload = isSignup ? { email, password, full_name: fullName, role: 'site_manager' } : { email, password }
      const response = await api.post(endpoint, payload)
      localStorage.setItem('buildsure_access_token', response.data.data.access_token)
      navigate('/')
    } catch (requestError: unknown) {
      setError(axios.isAxiosError(requestError) ? requestError.response?.data?.detail || 'Unable to complete authentication.' : 'Unable to complete authentication.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-primary-navy px-4 py-10">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-2xl bg-white shadow-2xl md:grid-cols-[1.05fr_0.95fr]">
        <section className="hidden bg-primary-slate p-10 text-white md:flex md:flex-col md:justify-between">
          <div>
            <div className="mb-14 flex items-center gap-3"><Building2 className="h-10 w-10 text-accent-orange" /><div><h1 className="text-2xl font-bold">BuildSure AI</h1><p className="text-sm text-slate-300">Construction Risk Intelligence</p></div></div>
            <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-accent-orange">One view. Safer sites.</p>
            <h2 className="max-w-md text-4xl font-bold leading-tight">Turn site signals into confident decisions.</h2>
            <p className="mt-6 max-w-md text-slate-300">Coordinate safety, compliance, insurance, and risk intelligence from one operating workspace.</p>
          </div>
          <p className="text-sm text-slate-400">Live intelligence for every project phase.</p>
        </section>
        <section className="p-8 sm:p-12">
          <div className="mb-8 md:hidden"><div className="flex items-center gap-3"><Building2 className="h-9 w-9 text-accent-orange" /><div><h1 className="text-xl font-bold text-slate-800">BuildSure AI</h1><p className="text-xs text-slate-500">Risk Intelligence</p></div></div></div>
          <p className="text-sm font-semibold text-accent-orange">{isSignup ? 'Create workspace access' : 'Welcome back'}</p>
          <h2 className="mt-2 text-3xl font-bold text-slate-800">{isSignup ? 'Create your account' : 'Sign in to your workspace'}</h2>
          <p className="mt-2 text-sm text-slate-500">{isSignup ? 'Start monitoring your construction projects.' : 'Continue to your project intelligence dashboard.'}</p>
          <div className="my-6 grid grid-cols-2 rounded-lg bg-slate-100 p-1">{(['login', 'signup'] as Mode[]).map((item) => <button key={item} type="button" onClick={() => { setMode(item); setError('') }} className={`rounded-md py-2 text-sm font-semibold transition ${mode === item ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500'}`}>{item === 'login' ? 'Sign in' : 'Sign up'}</button>)}</div>
          <form onSubmit={submit} className="space-y-4">
            {isSignup && <label className="block text-sm font-medium text-slate-700">Full name<div className="relative mt-1"><UserRound className="absolute left-3 top-3 h-5 w-5 text-slate-400" /><input required value={fullName} onChange={(event) => setFullName(event.target.value)} className="w-full rounded-lg border border-slate-200 py-2.5 pl-10 pr-4 outline-none focus:border-accent-orange focus:ring-2 focus:ring-orange-100" placeholder="Your name" /></div></label>}
            <label className="block text-sm font-medium text-slate-700">Work email<div className="relative mt-1"><Mail className="absolute left-3 top-3 h-5 w-5 text-slate-400" /><input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="w-full rounded-lg border border-slate-200 py-2.5 pl-10 pr-4 outline-none focus:border-accent-orange focus:ring-2 focus:ring-orange-100" placeholder="you@company.com" /></div></label>
            <label className="block text-sm font-medium text-slate-700">Password<div className="relative mt-1"><Lock className="absolute left-3 top-3 h-5 w-5 text-slate-400" /><input required minLength={8} type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="w-full rounded-lg border border-slate-200 py-2.5 pl-10 pr-4 outline-none focus:border-accent-orange focus:ring-2 focus:ring-orange-100" placeholder="At least 8 characters" /></div></label>
            {error && <p role="alert" className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
            <button disabled={loading} type="submit" className="flex w-full items-center justify-center gap-2 rounded-lg bg-accent-orange py-3 font-semibold text-white transition hover:bg-orange-600 disabled:opacity-60">{loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <>{isSignup ? 'Create account' : 'Sign in'}<ArrowRight className="h-4 w-4" /></>}</button>
          </form>
        </section>
      </div>
    </div>
  )
}