import service, { requestWithRetry } from './index'

export const generateArticle = (data) => {
  return requestWithRetry(() => service.post('/api/article/generate', data), 2, 800)
}

export const getArticle = (articleId) => {
  return service.get(`/api/article/${articleId}`)
}

export const getArticleProgress = (articleId) => {
  return service.get(`/api/article/${articleId}/progress`)
}

export const getArticleAgentLog = (articleId, fromLine = 0) => {
  return service.get(`/api/article/${articleId}/agent-log`, { params: { from_line: fromLine } })
}

export const chatWithArticle = (data) => {
  return requestWithRetry(() => service.post('/api/article/chat', data), 2, 800)
}
