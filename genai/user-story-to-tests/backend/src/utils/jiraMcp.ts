export function formatTestCaseDescription(testCase: {
  testCaseId: string
  testCaseTitle: string
  testCaseSteps: string[]
  testData?: string
  expectedResult: string
  category: string
}): string {
  const stepsText = testCase.testCaseSteps
    .map((step, i) => `${i + 1}. ${step}`)
    .join('\n')

  let description = `*Test Case ID:* ${testCase.testCaseId}\n`
  description += `*Title:* ${testCase.testCaseTitle}\n`
  description += `*Category:* ${testCase.category}\n\n`
  description += `h3. Test Steps\n${stepsText}\n\n`

  if (testCase.testData) {
    description += `h3. Test Data\n{code}\n${testCase.testData}\n{code}\n\n`
  }

  description += `h3. Expected Result\n${testCase.expectedResult}`

  return description
}
