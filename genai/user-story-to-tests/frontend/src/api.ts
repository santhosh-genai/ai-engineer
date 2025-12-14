import { GenerateRequest, GenerateResponse } from './types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081/api'

export async function generateTests(request: GenerateRequest): Promise<GenerateResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/generate-tests`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
    }

    const data: GenerateResponse = await response.json()
    return data
  } catch (error) {
    console.error('Error generating tests:', error)
    throw error instanceof Error ? error : new Error('Unknown error occurred')
  }
}

export async function connectJira(body: { baseUrl: string; email: string; apiToken: string }) {
  const resp = await fetch(`${API_BASE_URL}/jira/connect`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!resp.ok) {
    const errorData = await resp.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(errorData.error || `HTTP error! status: ${resp.status}`)
  }
  return resp.json()
}

export async function fetchJiraStories(body: { baseUrl: string; email: string; apiToken: string; project: string }) {
  const resp = await fetch(`${API_BASE_URL}/jira/stories`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!resp.ok) {
    const errorData = await resp.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(errorData.error || `HTTP error! status: ${resp.status}`)
  }
  return resp.json()
}

export async function fetchJiraStory(body: { baseUrl: string; email: string; apiToken: string; issueIdOrKey: string }) {
  const resp = await fetch(`${API_BASE_URL}/jira/story`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!resp.ok) {
    const errorData = await resp.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(errorData.error || `HTTP error! status: ${resp.status}`)
  }
  return resp.json()
}

export async function pushTestCaseToJira(body: {
  baseUrl: string
  email: string
  apiToken: string
  projectKey: string
  parentIssueKey: string
  testCaseId: string
  testCaseTitle: string
  testCaseSteps: string[]
  testData?: string
  expectedResult: string
  category: string
}) {
  const resp = await fetch(`${API_BASE_URL}/jira/push-test-case`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!resp.ok) {
    const errorData = await resp.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(errorData.error || `HTTP error! status: ${resp.status}`)
  }
  return resp.json()
}

export async function pushTestCaseToJiraViaMCP(body: {
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
}) {
  const resp = await fetch(`${API_BASE_URL}/jira/push-test-case-mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!resp.ok) {
    const errorData = await resp.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(errorData.error || `HTTP error! status: ${resp.status}`)
  }
  return resp.json()
}