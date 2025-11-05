export interface GenerateRequest {
  storyTitle: string
  acceptanceCriteria: string
  description?: string
  additionalInfo?: string
}

export interface TestCase {
  id: string
  title: string
  steps: string[]
  testData?: string
  expectedResult: string
  category: string
}

export interface GenerateResponse {
  cases: TestCase[]
  model?: string
  promptTokens: number
  completionTokens: number
}

export interface JiraIssueSummary {
  id: string
  key: string
  title: string
}

export interface JiraStoryDetail {
  key: string
  id: string
  title: string
  description?: string
  acceptanceCriteria?: string
}