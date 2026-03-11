import { reactive } from 'vue'

const state = reactive({ form: null })

export const setArticleForm = (form) => { state.form = { ...form } }
export const getArticleForm = () => state.form
export const clearArticleForm = () => { state.form = null }
