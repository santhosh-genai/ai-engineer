import express from 'express'
import fetch from 'node-fetch'

export const jiraRouter = express.Router()

type JiraConnectBody = {
  baseUrl: string
  email: string
  apiToken: string
}

type JiraStoriesBody = JiraConnectBody & {
  project: string
}

type JiraStoryBody = JiraConnectBody & {
  issueIdOrKey: string
}

function buildAuthHeader(email: string, apiToken: string) {
  const token = Buffer.from(`${email}:${apiToken}`).toString('base64')
  return `Basic ${token}`
}

async function handleJiraFetch(url: string, authHeader: string) {
  const resp = await fetch(url, {
    method: 'GET',
    headers: {
      Authorization: authHeader,
      'Accept': 'application/json'
    }
  })
  return resp
}

// Test connection to Jira using the /myself endpoint
jiraRouter.post('/connect', async (req, res) => {
  try {
    const body = req.body as JiraConnectBody
    if (!body?.baseUrl || !body?.email || !body?.apiToken) {
      res.status(400).json({ error: 'Missing baseUrl, email or apiToken' })
      return
    }

    const auth = buildAuthHeader(body.email, body.apiToken)
    const url = `${body.baseUrl.replace(/\/$/, '')}/rest/api/3/myself`

    const resp = await handleJiraFetch(url, auth)
    if (resp.status === 401 || resp.status === 403) {
      res.status(401).json({ error: 'Authentication failed. Check email and API token.' })
      return
    }

    if (!resp.ok) {
      const text = await resp.text().catch(() => '')
      res.status(502).json({ error: `Failed to reach Jira: ${resp.status} ${resp.statusText}`, details: text })
      return
    }

  const data: any = await resp.json()
  res.json({ ok: true, accountId: data.accountId, displayName: data.displayName })
  } catch (err: any) {
    console.error('Error in /jira/connect', err)
    res.status(500).json({ error: err?.message || 'Internal server error' })
  }
})

// Fetch stories list for a project (issue type = Story)
jiraRouter.post('/stories', async (req, res) => {
  try {
    const body = req.body as JiraStoriesBody
    if (!body?.baseUrl || !body?.email || !body?.apiToken || !body?.project) {
      res.status(400).json({ error: 'Missing baseUrl, email, apiToken or project' })
      return
    }

    const auth = buildAuthHeader(body.email, body.apiToken)
    const url = `${body.baseUrl.replace(/\/$/, '')}/rest/api/3/search/jql`

    // Use the newer search/jql POST API as the older query-string search endpoint may be removed
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: auth,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        jql: `project = ${body.project} AND issuetype = Story ORDER BY updated DESC`,
        fields: ['summary', 'issuetype'],
        maxResults: 100
      })
    })
    if (resp.status === 401 || resp.status === 403) {
      res.status(401).json({ error: 'Authentication failed. Check email and API token.' })
      return
    }

    if (!resp.ok) {
      const text = await resp.text().catch(() => '')
      res.status(502).json({ error: `Failed to fetch stories: ${resp.status} ${resp.statusText}`, details: text })
      return
    }

  const data: any = await resp.json()
  const issues = (data.issues || []).map((it: any) => ({
      id: it.id,
      key: it.key,
      title: it.fields?.summary || ''
    }))

    res.json({ issues })
  } catch (err: any) {
    console.error('Error in /jira/stories', err)
    res.status(500).json({ error: err?.message || 'Internal server error' })
  }
})

// Fetch story details by issue id or key
jiraRouter.post('/story', async (req, res) => {
  try {
    const body = req.body as JiraStoryBody
    if (!body?.baseUrl || !body?.email || !body?.apiToken || !body?.issueIdOrKey) {
      res.status(400).json({ error: 'Missing baseUrl, email, apiToken or issueIdOrKey' })
      return
    }

    const auth = buildAuthHeader(body.email, body.apiToken)
    const url = `${body.baseUrl.replace(/\/$/, '')}/rest/api/3/issue/${encodeURIComponent(body.issueIdOrKey)}?fields=summary,description`

    const resp = await handleJiraFetch(url, auth)
    if (resp.status === 401 || resp.status === 403) {
      res.status(401).json({ error: 'Authentication failed. Check email and API token.' })
      return
    }

    if (resp.status === 404) {
      res.status(404).json({ error: 'Issue not found' })
      return
    }

    if (!resp.ok) {
      const text = await resp.text().catch(() => '')
      res.status(502).json({ error: `Failed to fetch story: ${resp.status} ${resp.statusText}`, details: text })
      return
    }

  const data: any = await resp.json()
  const summary = data.fields?.summary || ''
  const description = extractDescriptionAsText(data.fields?.description)
    const acceptanceCriteria = extractAcceptanceCriteria(description)

    res.json({ key: data.key, id: data.id, title: summary, description, acceptanceCriteria })
  } catch (err: any) {
    console.error('Error in /jira/story', err)
    res.status(500).json({ error: err?.message || 'Internal server error' })
  }
})

// Helper: Jira description can be in Atlassian Document Format - convert basic structure to plain text
function extractDescriptionAsText(descriptionField: any): string {
  if (!descriptionField) return ''
  try {
    if (typeof descriptionField === 'string') return descriptionField
    if (descriptionField.type === 'doc' && Array.isArray(descriptionField.content)) {
      return descriptionField.content.map((node: any) => renderNodeText(node)).join('\n\n')
    }
    return JSON.stringify(descriptionField)
  } catch (e) {
    return ''
  }
}

function renderNodeText(node: any): string {
  if (!node) return ''
  if (node.type === 'paragraph' && Array.isArray(node.content)) {
    return node.content.map((c: any) => c.text || '').join('')
  }
  if (node.type === 'heading' && Array.isArray(node.content)) {
    return node.content.map((c: any) => c.text || '').join('')
  }
  if (node.text) return node.text
  if (Array.isArray(node.content)) return node.content.map((c: any) => renderNodeText(c)).join('')
  return ''
}

// Very simple extractor for acceptance criteria blocks inside description
function extractAcceptanceCriteria(description: string): string {
  if (!description) return ''
  // Look for headings or labels
  const regex = /Acceptance Criteria[:\-]?\s*\n([\s\S]{0,2000})/i
  const match = description.match(regex)
  if (match && match[1]) {
    // Stop at next blank line followed by capitalized word or end
    return match[1].trim()
  }

  // Try to find bullet lists that look like acceptance criteria
  const lines = description.split('\n')
  const acLines = lines.filter(l => l.trim().startsWith('-') || l.trim().startsWith('*'))
  if (acLines.length > 0) return acLines.join('\n')

  return ''
}

export default jiraRouter
