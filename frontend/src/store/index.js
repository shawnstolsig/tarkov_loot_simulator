import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		marketApiKey: 'm07rRZrjmjRMHtsP',
		marketEndpoints: {
			all: 'https://tarkov-market.com/api/v1/items/all',
			item: 'https://tarkov-market.com/api/v1/item',
		},
		backendEndpoints: {
			api: 'http://localhost:8000/api/v1',
		}
	},
	getters: {
		marketApiKey(state){return state.marketApiKey},
		marketEndpoints(state){return state.marketEndpoints},
		backendEndpoints(state){return state.backendEndpoints},
	},
	mutations: {
	},
	actions: {
	},
	modules: {
	}
})
