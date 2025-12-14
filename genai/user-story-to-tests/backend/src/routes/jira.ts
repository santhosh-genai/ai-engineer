import express from 'express'
import fetch from 'node-fetch'
import { formatTestCaseDescription } from '../utils/jiraMcp'

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

type PushTestCaseBody = JiraConnectBody & {
  projectKey: string
  parentIssueKey: string
  testCaseId: string
  testCaseTitle: string
  testCaseSteps: string[]
  testData?: string
  expectedResult: string
  category: string
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

// Push test case as a subtask to a parent story
jiraRouter.post('/push-test-case', async (req, res) => {
  try {
    const body = req.body as PushTestCaseBody
    if (!body?.baseUrl || !body?.email || !body?.apiToken || !body?.projectKey || !body?.parentIssueKey || !body?.testCaseTitle) {
      console.error('Missing required fields:', {
        baseUrl: !!body?.baseUrl,
        email: !!body?.email,
        apiToken: !!body?.apiToken,
        projectKey: !!body?.projectKey,
        parentIssueKey: !!body?.parentIssueKey,
        testCaseTitle: !!body?.testCaseTitle
      })
      res.status(400).json({ error: 'Missing required fields' })
      return
    }

    const auth = buildAuthHeader(body.email, body.apiToken)
    // Try v3 first, fall back to v2 if needed
    const url = `${body.baseUrl.replace(/\/$/, '')}/rest/api/3/issues`
    const urlV2 = `${body.baseUrl.replace(/\/$/, '')}/rest/api/2/issue`

    console.log('Push test case request:', {
      url,
      urlV2,
      projectKey: body.projectKey,
      parentIssueKey: body.parentIssueKey,
      testCaseId: body.testCaseId,
      testCaseTitle: body.testCaseTitle
    })

    // Format steps for the description
    const stepsDescription = body.testCaseSteps
      .map((step, index) => `Step ${index + 1}: ${step}`)
      .join('\n')

    // Create description in Atlassian Document Format (ADF) for v3
    const description = {
      version: 1,
      type: 'doc',
      content: [
        {
          type: 'heading',
          attrs: { level: 2 },
          content: [{ type: 'text', text: 'Test Steps' }]
        },
        {
          type: 'paragraph',
          content: [{ type: 'text', text: stepsDescription }]
        },
        ...(body.testData ? [{
          type: 'heading',
          attrs: { level: 2 },
          content: [{ type: 'text', text: 'Test Data' }]
        },
        {
          type: 'paragraph',
          content: [{ type: 'text', text: body.testData }]
        }] : []),
        {
          type: 'heading',
          attrs: { level: 2 },
          content: [{ type: 'text', text: 'Expected Result' }]
        },
        {
          type: 'paragraph',
          content: [{ type: 'text', text: body.expectedResult }]
        }
      ]
    }

    // Plain text description for v2 and for reference
    const plainDescription = body.testCaseSteps
      .map((step, index) => `Step ${index + 1}: ${step}`)
      .join('\n')
      + (body.testData ? `\n\nTest Data:\n${body.testData}` : '')
      + `\n\nExpected Result:\n${body.expectedResult}`

    const issuePayload = {
      fields: {
        project: { key: body.projectKey },
        issuetype: { name: 'Task' },
        summary: `[${body.category}] ${body.testCaseTitle}`,
        description: description,
        labels: [body.category.toLowerCase(), `test-case-${body.testCaseId}`, `parent-${body.parentIssueKey}`]
      }
    }

    console.log('Jira issue payload:', JSON.stringify(issuePayload, null, 2))

    let resp: any
    let responseText = ''
    let apiVersion = 'v3'

    try {
      resp = await fetch(url, {
        method: 'POST',
        headers: {
          Authorization: auth,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(issuePayload)
      })

      responseText = await resp.text()
      console.log('Jira v3 response status:', resp.status, resp.statusText)
      console.log('Jira v3 response body:', responseText)

      // If v3 fails with 404 or 400, try v2
      if (!resp.ok && (resp.status === 404 || resp.status === 400)) {
        console.log('V3 API failed, trying V2 API...')
        apiVersion = 'v2'
        
        const v2Payload = {
          fields: {
            project: { key: body.projectKey },
            issuetype: { name: 'Task' },
            summary: `[${body.category}] ${body.testCaseTitle}`,
            description: plainDescription,
            labels: issuePayload.fields.labels
          }
        }

        console.log('V2 Payload:', JSON.stringify(v2Payload, null, 2))

        resp = await fetch(urlV2, {
          method: 'POST',
          headers: {
            Authorization: auth,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(v2Payload)
        })

        responseText = await resp.text()
        console.log('Jira v2 response status:', resp.status, resp.statusText)
        console.log('Jira v2 response body:', responseText)
      }
    } catch (fetchErr: any) {
      console.error('Fetch error:', fetchErr)
      res.status(502).json({ error: 'Failed to reach Jira API', details: fetchErr.message })
      return
    }

    if (resp.status === 401 || resp.status === 403) {
      res.status(401).json({ error: 'Authentication failed. Check email and API token.' })
      return
    }

    if (!resp.ok) {
      res.status(502).json({ 
        error: `Failed to create Jira issue (${apiVersion}): ${resp.status} ${resp.statusText}`, 
        details: responseText 
      })
      return
    }

    try {
      const data: any = JSON.parse(responseText)
      res.json({ ok: true, issueKey: data.key, issueId: data.id, apiUsed: apiVersion })
    } catch (parseErr) {
      console.error('Failed to parse successful Jira response:', parseErr)
      res.status(502).json({ error: 'Failed to parse Jira response', details: responseText })
    }
  } catch (err: any) {
    console.error('Error in /jira/push-test-case', err)
    res.status(500).json({ error: err?.message || 'Internal server error' })
  }
})

// MCP-based push test case endpoint (uses Jira REST API with credentials from frontend)
jiraRouter.post('/push-test-case-mcp', async (req, res) => {
  try {
    const body = req.body as {
      baseUrl: string
      email: string
      apiToken: string
      projectKey: string
      parentIssueKey?: string
      testCaseId: string
      testCaseTitle: string
      testCaseSteps: string[]
      testData?: string
      expectedResult: string
      category?: string
    }

    if (!body?.baseUrl || !body?.email || !body?.apiToken || !body?.projectKey || !body?.testCaseId || !body?.testCaseTitle) {
      res.status(400).json({ error: 'Missing required fields' })
      return
    }

    const auth = buildAuthHeader(body.email, body.apiToken)
    const url = `${body.baseUrl.replace(/\/$/, '')}/rest/api/3/issues`
    const urlV2 = `${body.baseUrl.replace(/\/$/, '')}/rest/api/2/issue`

    const description = formatTestCaseDescription({
      testCaseId: body.testCaseId,
      testCaseTitle: body.testCaseTitle,
      testCaseSteps: body.testCaseSteps || [],
      testData: body.testData,
      expectedResult: body.expectedResult || '',
      category: body.category || 'Functional'
    })

    // Create description in Atlassian Document Format (ADF) for v3
    const adfDescription = {
      version: 1,
      type: 'doc',
      content: [
        {
          type: 'paragraph',
          content: [{ type: 'text', text: description }]
        }
      ]
    }

    const issuePayload = {
      fields: {
        project: { key: body.projectKey },
        issuetype: { name: 'Task' },
        summary: `[${body.testCaseId}] ${body.testCaseTitle}`,
        description: adfDescription,
        labels: [body.category?.toLowerCase() || 'test', `test-case-${body.testCaseId}`]
      }
    }

    let resp: any
    let responseText = ''
    let apiVersion = 'v3'

    try {
      resp = await fetch(url, {
        method: 'POST',
        headers: {
          Authorization: auth,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(issuePayload)
      })

      responseText = await resp.text()

      // If v3 fails with 404 or 400, try v2
      if (!resp.ok && (resp.status === 404 || resp.status === 400)) {
        console.log('V3 API failed, trying V2 API...')
        apiVersion = 'v2'
        
        const v2Payload = {
          fields: {
            project: { key: body.projectKey },
            issuetype: { name: 'Task' },
            summary: `[${body.testCaseId}] ${body.testCaseTitle}`,
            description: description,
            labels: issuePayload.fields.labels
          }
        }

        resp = await fetch(urlV2, {
          method: 'POST',
          headers: {
            Authorization: auth,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(v2Payload)
        })

        responseText = await resp.text()
      }
    } catch (fetchErr: any) {
      console.error('Fetch error:', fetchErr)
      res.status(502).json({ error: 'Failed to reach Jira API', details: fetchErr.message })
      return
    }

    if (resp.status === 401 || resp.status === 403) {
      res.status(401).json({ error: 'Authentication failed. Check email and API token.' })
      return
    }

    if (!resp.ok) {
      res.status(502).json({ 
        error: `Failed to create Jira issue (${apiVersion}): ${resp.status} ${resp.statusText}`, 
        details: responseText 
      })
      return
    }

    try {
      const data: any = JSON.parse(responseText)
      res.json({ 
        success: true, 
        jiraKey: data.key, 
        jiraId: data.id, 
        apiUsed: apiVersion,
        message: `Test case ${body.testCaseId} pushed to Jira successfully`
      })
    } catch (parseErr) {
      console.error('Failed to parse successful Jira response:', parseErr)
      res.status(502).json({ error: 'Failed to parse Jira response', details: responseText })
    }
  } catch (error: any) {
    console.error('Push test case MCP error:', error)
    const errorMessage = error instanceof Error ? error.message : 'Failed to push test case'
    res.status(500).json({ error: errorMessage })
  }
})

export default jiraRouter
