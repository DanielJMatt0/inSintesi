import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'


const md = new MarkdownIt({
  breaks: true,
  linkify: true,
})

/**
 * Format a date or ISO string into a European-style string.
 * Example output: "01 Nov 2025, 10:45"
 */
export function formatDate(val) {
  if (!val) return '—'
  try {
    const d = typeof val === 'string' ? new Date(val) : val
    return new Intl.DateTimeFormat('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(d)
  } catch {
    return String(val)
  }
}

export function useMarkdown() {
  const renderMarkdown = (text) => {
    if (!text) return ''
    const html = md.render(text)
    return DOMPurify.sanitize(html)
  }

  return { renderMarkdown }
}
